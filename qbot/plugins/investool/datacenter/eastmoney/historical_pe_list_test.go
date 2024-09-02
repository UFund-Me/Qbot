package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestPEGetMidValue(t *testing.T) {
	d := HistoricalPEList{
		HistoricalPE{Date: "1", Value: 6.0},
		HistoricalPE{Date: "1", Value: 1.0},
		HistoricalPE{Date: "1", Value: 5.0},
		HistoricalPE{Date: "1", Value: 2.0},
		HistoricalPE{Date: "1", Value: 4.0},
		HistoricalPE{Date: "1", Value: 3.0},
	}
	m, err := d.GetMidValue(_ctx)
	require.Nil(t, err)
	require.Equal(t, 3.5, m)
}

func TestQueryHistoricalPEList(t *testing.T) {
	d, err := _em.QueryHistoricalPEList(_ctx, "600149.sh")
	require.Nil(t, err)
	t.Log(d)
}
