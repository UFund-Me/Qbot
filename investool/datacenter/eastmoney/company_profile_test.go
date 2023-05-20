package eastmoney

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestQueryCompanyProfile(t *testing.T) {
	data, err := _em.QueryCompanyProfile(_ctx, "002459.sz")
	require.Nil(t, err)
	require.NotEmpty(t, data.Keywords)
	require.NotEmpty(t, data.MainForms)
	require.NotEmpty(t, data.Secucode)
	require.NotEmpty(t, data.Name)
	require.NotEmpty(t, data.Industry)
	require.NotEmpty(t, data.Concept)
	require.NotEmpty(t, data.Profile)
	require.NotEmpty(t, data.MainBusiness)
}
