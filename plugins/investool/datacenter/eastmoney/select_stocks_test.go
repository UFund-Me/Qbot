package eastmoney

import (
	"encoding/json"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestQuerySelectedStocks(t *testing.T) {
	data, err := _em.QuerySelectedStocks(_ctx)
	require.Nil(t, err)
	require.NotEmpty(t, data)
}

func TestQuerySelectedStocksWithFilter(t *testing.T) {
	filter := DefaultFilter
	filter.SpecialSecurityCodeList = []string{"002312"}
	data, err := _em.QuerySelectedStocksWithFilter(_ctx, filter)
	require.Nil(t, err)
	b, _ := json.Marshal(data)
	t.Log(string(b))
}
