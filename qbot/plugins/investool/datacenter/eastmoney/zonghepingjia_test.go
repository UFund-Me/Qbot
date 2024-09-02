package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestQueryZongHePingJia(t *testing.T) {
	data, err := _em.QueryZongHePingJia(_ctx, "600809.sh")
	require.Nil(t, err)
	t.Logf("%+v", data)
}
