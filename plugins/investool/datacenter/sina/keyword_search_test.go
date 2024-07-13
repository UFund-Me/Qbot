package sina

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestKeywordSearch(t *testing.T) {
	results, err := _s.KeywordSearch(_ctx, "比亚迪")
	require.Nil(t, err)
	t.Log(results)
}
