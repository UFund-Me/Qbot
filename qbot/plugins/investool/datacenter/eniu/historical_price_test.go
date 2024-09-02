package eniu

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestGetPathCode(t *testing.T) {
	code := _e.GetPathCode(_ctx, "002459.SZ")
	require.Equal(t, "sz002459", code)
}

func TestQueryHistoricalStockPrice(t *testing.T) {
	data, err := _e.QueryHistoricalStockPrice(_ctx, "002312.SZ")
	require.Nil(t, err)
	require.NotEmpty(t, data.Date)
	v, _ := data.HistoricalVolatility(_ctx, "YEAR")
	t.Log("volatility:", v)
}

func TestHistoricalVolatility(t *testing.T) {
	data := RespHistoricalStockPrice{
		Price: []float64{
			8.47,
			8.54,
			8.3,
			7.57,
			7.77,
			7.4,
			8.23,
			7.83,
			7.43,
			7.02,
			6.75,
			6.73,
			6.7,
			6.5,
			7.45,
			7.4,
			7.25,
			7.15,
			7.25,
			7.0,
		},
	}
	d, err := data.HistoricalVolatility(_ctx, "DAY")
	require.Nil(t, err)
	w, err := data.HistoricalVolatility(_ctx, "WEEK")
	require.Nil(t, err)
	m, err := data.HistoricalVolatility(_ctx, "MONTH")
	require.Nil(t, err)
	y, err := data.HistoricalVolatility(_ctx, "YEAR")
	require.Nil(t, err)
	t.Log("day volatility:", d, " week volatility:", w, " month volatility:", m, " year volatility:", y)
}
