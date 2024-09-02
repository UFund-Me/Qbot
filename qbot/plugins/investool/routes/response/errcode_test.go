package response

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestErrCode(t *testing.T) {
	assert.Equal(t, CodeSuccess.Code(), success)
}
