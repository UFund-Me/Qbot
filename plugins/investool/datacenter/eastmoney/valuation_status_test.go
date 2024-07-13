package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestQueryValuationStatus(t *testing.T) {
	data, err := _em.QueryValuationStatus(_ctx, "603043.SH")
	require.Nil(t, err)
	require.Len(t, data, 4)
	t.Log("data:", data)
}
