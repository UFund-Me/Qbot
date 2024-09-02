package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestZSCFG(t *testing.T) {
	results, err := _em.ZSCFG(_ctx, "000905")
	require.Nil(t, err)
	t.Log(results)
}
