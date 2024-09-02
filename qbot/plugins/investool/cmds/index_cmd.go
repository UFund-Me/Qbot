// 指数数据

package cmds

import (
	"context"
	"fmt"

	"github.com/axiaoxin-com/investool/datacenter"
	"github.com/urfave/cli/v2"
)

const (
	// ProcessorIndex 指数数据处理
	ProcessorIndex = "index"
)

// FlagsIndex cli flags
func FlagsIndex() []cli.Flag {
	return []cli.Flag{
		&cli.StringFlag{
			Name:     "code",
			Aliases:  []string{"c"},
			Value:    "",
			Usage:    "指定指数代码",
			Required: true,
		},
		&cli.BoolFlag{
			Name:     "desc",
			Aliases:  []string{"d"},
			Value:    false,
			Usage:    "返回指数信息",
			Required: false,
		},
		&cli.BoolFlag{
			Name:     "stocks",
			Aliases:  []string{"s"},
			Value:    false,
			Usage:    "返回指数成分股",
			Required: false,
		},
		&cli.StringFlag{
			Name:     "intersec",
			Aliases:  []string{"i"},
			Value:    "",
			Usage:    "返回成分股交集",
			Required: false,
		},
	}
}

// ActionIndex cli action
func ActionIndex() func(c *cli.Context) error {
	return func(c *cli.Context) error {
		ctx := context.Background()
		indexCode := c.String("code")

		showDesc := c.Bool("desc")
		if showDesc {
			indexData, err := datacenter.EastMoney.Index(ctx, indexCode)
			if err != nil {
				fmt.Println(err)
			}
			showIndexData(indexData)
		}

		showStocks := c.Bool("stocks")
		if showStocks {
			stocks, err := datacenter.EastMoney.ZSCFG(ctx, indexCode)
			if err != nil {
				return err
			}
			showIndexStocks(stocks)
		}

		intersecIndexCode := c.String("intersec")
		if intersecIndexCode != "" {
			stocks1, err := datacenter.EastMoney.ZSCFG(ctx, indexCode)
			if err != nil {
				return err
			}
			stocks2, err := datacenter.EastMoney.ZSCFG(ctx, intersecIndexCode)
			if err != nil {
				return err
			}
			showIntersecStocks(stocks1, stocks2)
		}
		return nil
	}
}

// CommandIndex 指数成分股 cli command
func CommandIndex() *cli.Command {
	flags := FlagsIndex()
	cmd := &cli.Command{
		Name:   ProcessorIndex,
		Usage:  "指数数据",
		Flags:  flags,
		Action: ActionIndex(),
	}
	return cmd
}
