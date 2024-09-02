package core

import (
	"testing"

	"github.com/axiaoxin-com/logging"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/require"
)

func TestSearchStocks(t *testing.T) {
	logging.SetLevel("info")
	s := NewSearcher(_ctx)
	k := []string{"招商银行", "贵州茅台", "600038"}
	results, err := s.SearchStocks(_ctx, k)
	require.Nil(t, err)
	require.Len(t, results, 3)
}

func TestSearchFunds(t *testing.T) {
	viper.SetDefault("app.chan_size", 500)
	s := NewSearcher(_ctx)
	data, err := s.SearchFunds(_ctx, []string{"007135", "000209"})
	require.Nil(t, err)
	require.NotEmpty(t, data)
	t.Log("data:", data["000209"])
}

func TestSearchFundByStock(t *testing.T) {
	viper.SetDefault("app.chan_size", 500)
	s := NewSearcher(_ctx)
	result, err := s.SearchFundByStock(_ctx, "金域医学")
	require.Nil(t, err)
	require.NotEmpty(t, result)
	t.Log("result:", result)
}
