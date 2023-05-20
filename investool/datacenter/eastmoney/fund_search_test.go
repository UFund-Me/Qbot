package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestSearchFund(t *testing.T) {
	results, err := _em.SearchFund(_ctx, "半导体")
	require.Nil(t, err)
	t.Log(results)
}
