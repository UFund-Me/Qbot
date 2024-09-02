package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestQueryJiaZhiPingGu(t *testing.T) {
	data, err := _em.QueryJiaZhiPingGu(_ctx, "002291.sz")
	require.Nil(t, err)
	t.Logf("%+v", data)
}
