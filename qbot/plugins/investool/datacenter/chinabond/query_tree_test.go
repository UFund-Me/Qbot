package chinabond

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestQueryTree(t *testing.T) {
	results, err := _c.QueryTree(_ctx)
	require.Nil(t, err)
	require.NotEqual(t, len(results), 0)
	id := results["中债证券公司债收益率曲线(AAA)"]
	require.Equal(t, "5781a1ff7651967e0176978d957b7346", id)
}
