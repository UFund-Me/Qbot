package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestIndustryList(t *testing.T) {
	data, err := _em.QueryIndustryList(_ctx)
	require.Nil(t, err)
	require.Len(t, data, 105)
}
