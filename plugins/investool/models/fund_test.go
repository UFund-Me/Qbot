package models

import (
	"context"
	"encoding/json"
	"testing"

	"github.com/axiaoxin-com/investool/datacenter/eastmoney"
	"github.com/stretchr/testify/require"
)

func TestNewFund(t *testing.T) {
	ctx := context.TODO()
	efund, err := eastmoney.NewEastMoney().QueryFundInfo(ctx, "260104")
	require.Nil(t, err)
	fund := NewFund(ctx, efund)
	b, err := json.Marshal(fund)
	require.Nil(t, err)
	t.Log(string(b))
}
