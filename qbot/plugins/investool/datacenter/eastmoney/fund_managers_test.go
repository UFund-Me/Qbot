package eastmoney

import (
	"encoding/json"
	"testing"

	"github.com/stretchr/testify/require"
)

func _TestFundManagers(t *testing.T) {
	data, err := _em.FundMangers(_ctx, "all", "penavgrowth", "desc")
	require.Nil(t, err)
	require.NotEmpty(t, data)
	// t.Logf("data:%+v\n", data)
	_, err = json.Marshal(data)
	require.Nil(t, err)
	fd := data.Filter(_ctx, ParamFundManagerFilter{
		MinWorkingYears:     8,
		MinYieldse:          15.0,
		MaxCurrentFundCount: 10,
	})
	for _, d := range fd {
		t.Logf("d:%+v\n", *d)
	}
}
