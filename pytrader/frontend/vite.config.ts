import { UserConfigExport, ConfigEnv, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { viteMockServe } from 'vite-plugin-mock'
import viteSvgIcons from 'vite-plugin-svg-icons'

const setAlias = (alias: [string, string][]) => alias.map(v => {return { find: v[0], replacement: path.resolve(__dirname, v[1]) }})
const proxy = (list: [string, string][]) => {
    const obj:IObject<any> = {}
    list.forEach((v) => {
        obj[v[0]] = {
            target: v[1],
            changeOrigin: true,
            rewrite: (path:any) => path.replace(new RegExp(`^${v[0]}`), ''),
            ...(/^https:\/\//.test(v[1]) ? { secure: false } : {})
        }
    })
    return obj
}

export default ({ command, mode }: ConfigEnv): UserConfigExport => {
    const root = process.cwd()
    const env = loadEnv(mode, root) as unknown as ImportMetaEnv
    const prodMock = false
    return {
        resolve: {
            alias: setAlias([
                ['/@', 'src'],
                ['/mock', 'mock'],
                ['/server', 'server']
            ])
        },
        server: {
            proxy: env.VITE_PROXY ? proxy(JSON.parse(env.VITE_PROXY)) : {},
            port: env.VITE_PORT
        },
        build: {
            // sourcemap: true,
            manifest: true,
            rollupOptions: {
                outDir: '../static',
                output: {
                    manualChunks: {
                        'element-plus': ['element-plus'],
                        echarts: ['echarts'],
                        pinyin: ['pinyin']
                    }
                }
            },
            chunkSizeWarningLimit: 600
        },
        plugins: [
            vue(),
            // viteMockServe({
            //     mockPath: 'mock',
            //     localEnabled: command === 'serve',
            //     prodEnabled: command !== 'serve' && prodMock,
            //     //  这样可以控制关闭mock的时候不让mock打包到最终代码内
            //     injectCode: `
            //     import { setupProdMockServer } from '/mock/mockProdServer';
            //     setupProdMockServer();
            //     `
            // }),
            viteSvgIcons({
                // 指定需要缓存的图标文件夹
                iconDirs: [path.resolve(process.cwd(), 'src/icons')],
                // 指定symbolId格式
                symbolId: 'icon-[dir]-[name]'
            })
        ],
        css: {
            postcss: {
                plugins: [
                    require('autoprefixer'),
                    require('tailwindcss'),
                    require('postcss-nested'),
                    require('postcss-simple-vars'),
                    require('postcss-import')
                ]
            }
        }
    }
}
