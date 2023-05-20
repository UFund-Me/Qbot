package zszx

import (
	"testing"
	"time"

	"github.com/stretchr/testify/require"
)

func TestQueryMainMoneyNetInflows(t *testing.T) {
	now := time.Now()
	end := now.Format("2006-01-02")
	d, _ := time.ParseDuration("-720h")
	start := now.Add(d).Format("2006-01-02")
	results, err := _z.QueryMainMoneyNetInflows(_ctx, "002028.sz", start, end)
	require.Nil(t, err)
	require.NotEqual(t, len(results), 0)
	last3days := results[:3]
	t.Logf("last3days:%#v, sum:%f", last3days, last3days.SumMainNetIn(_ctx))
	last5days := results[:5]
	t.Logf("last5days:%#v, sum:%f", last5days, last5days.SumMainNetIn(_ctx))
	last10days := results[:10]
	t.Logf("last10days:%#v, sum:%f", last10days, last10days.SumMainNetIn(_ctx))
}
