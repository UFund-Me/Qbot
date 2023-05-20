package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestQueryFinaGincomeData(t *testing.T) {
	data, err := _em.QueryFinaGincomeData(_ctx, "002671.sz")
	require.Nil(t, err)
	require.NotEmpty(t, data)
	t.Log(data[0].ReportType)
}
