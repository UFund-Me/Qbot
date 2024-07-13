package eastmoney

import (
	"encoding/json"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestQueryFundInfo(t *testing.T) {
	data, err := _em.QueryFundInfo(_ctx, "013781")
	require.Nil(t, err)
	require.NotEmpty(t, data)
	t.Logf("data:%+v", data)
	_, err = json.Marshal(data)
	require.Nil(t, err)
}
