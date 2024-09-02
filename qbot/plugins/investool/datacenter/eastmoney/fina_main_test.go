package eastmoney

import (
	"testing"
	"time"

	"github.com/stretchr/testify/require"
)

func TestQueryHistoricalFinaMainData(t *testing.T) {
	data, err := _em.QueryHistoricalFinaMainData(_ctx, "600188.SH")
	require.Nil(t, err)
	require.NotEmpty(t, data)
	data1 := data.FilterByReportType(_ctx, FinaReportTypeYear)
	require.NotEmpty(t, data1)
	year := time.Now().Year() - 1
	data2 := data.FilterByReportYear(_ctx, year)
	require.Equal(t, 4, len(data2))
	ratio := data.GetAvgRevenueIncreasingRatioByYear(_ctx, year)
	t.Log("ratio:", ratio)
	em, err := data.MidValue(_ctx, "EPS", 10, FinaReportTypeYear)
	require.Nil(t, err)
	rm, err := data.MidValue(_ctx, "ROE", 0, FinaReportTypeYear)
	require.Nil(t, err)
	t.Log("eps mid:", em, " roe mid:", rm)
}

func TestQueryFinaPublishDateList(t *testing.T) {
	date, err := _em.QueryFinaPublishDateList(_ctx, "000026")
	require.Nil(t, err)
	t.Log("pubdate:", date)
}
