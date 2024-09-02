package cmds

import (
	"testing"

	"github.com/axiaoxin-com/investool/models"
	"github.com/stretchr/testify/require"
)

func TestExportExcel(t *testing.T) {
	e := Exportor{
		Stocks: []models.ExportorData{
			{
				Name: "中文名称",
				Code: "1234code",
			}, {
				Name: "中文名称1",
				Code: "code12345",
			},
		},
	}

	_, err := e.ExportExcel(_ctx, "/tmp/test.xlsx")
	require.Nil(t, err)
}
