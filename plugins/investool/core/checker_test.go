package core

import (
	"encoding/json"
	"fmt"
	"testing"

	"github.com/axiaoxin-com/investool/models"
	"github.com/axiaoxin-com/logging"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/require"
)

func TestCheckFundamentals(t *testing.T) {
	stock := models.Stock{}
	logging.SetLevel("error")
	c := NewChecker(_ctx, DefaultCheckerOptions)
	result, ok := c.CheckFundamentals(_ctx, stock)
	t.Log(ok, result)
}

func _TestGetFundStocksSimilarity(t *testing.T) {
	viper.SetDefault("app.chan_size", 500)
	c := NewChecker(_ctx, DefaultCheckerOptions)
	codes := []string{
		// 4433
		"270028",
		"377530",
		"550009",
		"210003",
		"002160",
		"519644",
		"166301",
		"001365",
		"519133",
		"519642",
		"000073",
		"001808",
		"001279",
		"001397",
		"000592",
		"001975",
		"163807",
		"001869",
		// manager
		"001938",
		"008314",
		"001679",
		"163406",
		"162605",
	}

	sims, err := c.GetFundStocksSimilarity(_ctx, codes)
	require.Nil(t, err)

	for _, s := range sims {
		if len(s.SameStocks) < 4 {
			continue
		}
		sim, _ := json.MarshalIndent(s, "", "  ")
		fmt.Println(string(sim))
		fmt.Println("---------------")
	}
}
