package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestQueryFreeHolders(t *testing.T) {
	data, err := _em.QueryFreeHolders(_ctx, "600031.sh")
	t.Log(data)
	require.Nil(t, err)
	require.Len(t, data, 10)
}
