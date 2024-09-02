package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestQueryOrgRating(t *testing.T) {
	data, err := _em.QueryOrgRating(_ctx, "002459.sz")
	require.Nil(t, err)
	require.Len(t, data, 3)
}
