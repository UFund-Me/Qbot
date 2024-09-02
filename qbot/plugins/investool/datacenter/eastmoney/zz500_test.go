package eastmoney

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestZZ500(t *testing.T) {
	results, err := _em.ZZ500(_ctx)
	fmt.Println(err)
	require.Nil(t, err)
	t.Log(results)
}
