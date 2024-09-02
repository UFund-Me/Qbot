package chinabond

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func _TestQueryFxsyl(t *testing.T) {
	results, err := _c.QueryFxsyl(_ctx, "5781a1ff7651967e0176978d957b7346", "2021-11-19")
	require.Nil(t, err)
	require.NotEqual(t, len(results), 0)
	require.NotZero(t, results[0][1])
}
func _TestQueryCurrentSyl(t *testing.T) {
	result, err := _c.QueryCurrentSyl(_ctx, "中债证券公司债收益率曲线(AAA)")
	require.Nil(t, err)
	require.NotZero(t, result)
	t.Log(result)
}
