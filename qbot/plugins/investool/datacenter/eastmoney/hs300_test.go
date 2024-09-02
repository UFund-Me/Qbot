package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestHS300(t *testing.T) {
	results, err := _em.HS300(_ctx)
	require.Nil(t, err)
	t.Log(results)
}
