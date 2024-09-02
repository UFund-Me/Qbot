package webserver

import (
	"context"
	"net"
	"net/http"
	"os"
	"os/signal"
	"path"
	"strings"
	"syscall"
	"time"

	"github.com/axiaoxin-com/goutils"
	"github.com/axiaoxin-com/logging"
	"github.com/fsnotify/fsnotify"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
)

// InitWithConfigFile 根据 webserver 配置文件初始化 webserver
func InitWithConfigFile(configFile string) {
	// 加载配置文件内容到 viper 中以便使用
	configPath, file := path.Split(configFile)
	if configPath == "" {
		configPath = "./"
	}
	ext := path.Ext(file)
	configType := strings.Trim(ext, ".")
	configName := strings.TrimSuffix(file, ext)
	logging.Infof(nil, "load %s type config file %s from %s", configType, configName, configPath)

	if err := goutils.InitViper(configFile, func(e fsnotify.Event) {
		logging.Warn(nil, "Config file changed:"+e.Name)
		logging.SetLevel(viper.GetString("logging.level"))
	}); err != nil {
		// 文件不存在时 1 使用默认配置，其他 err 直接 panic
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			panic(err)
		}
		logging.Error(nil, "Init viper error:"+err.Error())
	}

	// 设置 viper 中 webserver 配置项默认值
	viper.SetDefault("env", "localhost")

	viper.SetDefault("server.addr", ":4869")
	viper.SetDefault("server.mode", gin.ReleaseMode)
	viper.SetDefault("server.pprof", true)

	viper.SetDefault("apidocs.title", "pink-lady swagger apidocs")
	viper.SetDefault("apidocs.desc", "Using pink-lady to develop gin app on fly.")
	viper.SetDefault("apidocs.host", "localhost:4869")
	viper.SetDefault("apidocs.basepath", "/")
	viper.SetDefault("apidocs.schemes", []string{"http"})

	viper.SetDefault("basic_auth.username", "admin")
	viper.SetDefault("basic_auth.password", "admin")

	// 打印viper配置
	logging.Infof(nil, "viper load all settings:%v", viper.AllSettings())

	// 初始化 sentry 并创建 sentry 客户端
	sentryDSN := viper.GetString("sentry.dsn")
	if sentryDSN == "" {
		sentryDSN = os.Getenv(logging.SentryDSNEnvKey)
	}
	sentryDebug := viper.GetBool("sentry.debug")
	if viper.GetString("server.mode") == "release" {
		sentryDebug = false
	}
	logging.Debug(nil, "Sentry use dns: "+sentryDSN)
	sentry, err := logging.NewSentryClient(sentryDSN, sentryDebug)
	if err != nil {
		logging.Error(nil, "Sentry client create error:"+err.Error())
	}

	// 根据配置创建 logging 的 logger 并将 logging 的默认 logger 替换为当前创建的 logger
	outputs := viper.GetStringSlice("logging.output_paths")
	var lumberjackSink *logging.LumberjackSink
	for _, output := range outputs {
		if strings.HasPrefix(output, "logrotate://") {
			filename := strings.Split(output, "://")[1]
			maxAge := viper.GetInt("logging.logrotate.max_age")
			maxBackups := viper.GetInt("logging.logrotate.max_backups")
			maxSize := viper.GetInt("logging.logrotate.max_size")
			compress := viper.GetBool("logging.logrotate.compress")
			localtime := viper.GetBool("logging.logrotate.localtime")
			lumberjackSink = logging.NewLumberjackSink("logrotate", filename, maxAge, maxBackups, maxSize, compress, localtime)
		}
	}
	logger, err := logging.NewLogger(logging.Options{
		Level:             viper.GetString("logging.level"),
		Format:            viper.GetString("logging.format"),
		OutputPaths:       outputs,
		DisableCaller:     viper.GetBool("logging.disable_caller"),
		DisableStacktrace: viper.GetBool("logging.disable_stacktrace"),
		AtomicLevelServer: logging.AtomicLevelServerOption{
			Addr:     viper.GetString("logging.atomic_level_server.addr"),
			Path:     viper.GetString("logging.atomic_level_server.path"),
			Username: viper.GetString("basic_auth.username"),
			Password: viper.GetString("basic_auth.password"),
		},
		SentryClient:   sentry,
		LumberjackSink: lumberjackSink,
	})
	if err != nil {
		logging.Error(nil, "Logger create error:"+err.Error())
	} else {
		logging.ReplaceLogger(logger)
	}
}

// Run 以 viper 加载的 app 配置启动运行 http.Handler 的 app
// 注意：这里依赖 viper ，必须在外部先对 viper 配置进行加载
func Run(app http.Handler) {
	// 判断是否加载 viper 配置
	if !goutils.IsInitedViper() {
		panic("Running server must init viper by config file first!")
	}

	// 创建 server
	addr := viper.GetString("server.addr")
	srv := &http.Server{
		Addr:         addr,
		Handler:      app,
		ReadTimeout:  5 * time.Minute,
		WriteTimeout: 10 * time.Minute,
	}
	// Shutdown 时需要调用的方法
	srv.RegisterOnShutdown(func() {
		// TODO
	})

	// 启动 http server
	go func() {
		var ln net.Listener
		var err error
		if strings.ToLower(strings.Split(addr, ":")[0]) == "unix" {
			ln, err = net.Listen("unix", strings.Split(addr, ":")[1])
			if err != nil {
				panic(err)
			}
		} else {
			ln, err = net.Listen("tcp", addr)
			if err != nil {
				panic(err)
			}
		}
		if err := srv.Serve(ln); err != nil {
			logging.Error(nil, err.Error())
		}
	}()
	logging.Infof(nil, "Server is running on %s", srv.Addr)

	// 监听中断信号， WriteTimeout 时间后优雅关闭服务
	// syscall.SIGTERM 不带参数的 kill 命令
	// syscall.SIGINT ctrl-c kill -2
	// syscall.SIGKILL 是 kill -9 无法捕获这个信号
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	logging.Infof(nil, "Server is shutting down.")

	// 创建一个 context 用于通知 server 3 秒后结束当前正在处理的请求
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		logging.Error(nil, "Server shutdown with error: "+err.Error())
	}
	logging.Info(nil, "Server exit.")
}
