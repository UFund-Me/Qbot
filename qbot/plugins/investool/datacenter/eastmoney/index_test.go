package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestIndex(t *testing.T) {
	data, err := _em.Index(_ctx, "000905")
	require.Nil(t, err)
	t.Log(data)
}
