package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestQueryFundByStock(t *testing.T) {
	data, err := _em.QueryFundByStock(_ctx, "金域医学", "603882")
	require.Nil(t, err)
	require.NotEmpty(t, data)
	t.Log("data:", data)
}
