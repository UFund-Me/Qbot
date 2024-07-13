// Functions from Go's strings package usable as template actions

package webserver

import (
	"html/template"
	"strings"
	"unicode"

	"github.com/axiaoxin-com/goutils"
)

// TemplFuncs is a template.FuncMap with functions that can be used as template actions.
var TemplFuncs = template.FuncMap{
	"StrContains":       func(s, substr string) bool { return strings.Contains(s, substr) },
	"StrContainsAny":    func(s, chars string) bool { return strings.ContainsAny(s, chars) },
	"StrContainsRune":   func(s string, r rune) bool { return strings.ContainsRune(s, r) },
	"StrCount":          func(s, sep string) int { return strings.Count(s, sep) },
	"StrEqualFold":      func(s, t string) bool { return strings.EqualFold(s, t) },
	"StrFields":         func(s string) []string { return strings.Fields(s) },
	"StrFieldsFunc":     func(s string, f func(rune) bool) []string { return strings.FieldsFunc(s, f) },
	"StrHasPrefix":      func(s, prefix string) bool { return strings.HasPrefix(s, prefix) },
	"StrHasSuffix":      func(s, suffix string) bool { return strings.HasSuffix(s, suffix) },
	"StrIndex":          func(s, sep string) int { return strings.Index(s, sep) },
	"StrIndexAny":       func(s, chars string) int { return strings.IndexAny(s, chars) },
	"StrIndexByte":      func(s string, c byte) int { return strings.IndexByte(s, c) },
	"StrIndexFunc":      func(s string, f func(rune) bool) int { return strings.IndexFunc(s, f) },
	"StrIndexRune":      func(s string, r rune) int { return strings.IndexRune(s, r) },
	"StrJoin":           func(a []string, sep string) string { return strings.Join(a, sep) },
	"StrLastIndex":      func(s, sep string) int { return strings.LastIndex(s, sep) },
	"StrLastIndexAny":   func(s, chars string) int { return strings.LastIndexAny(s, chars) },
	"StrLastIndexFunc":  func(s string, f func(rune) bool) int { return strings.LastIndexFunc(s, f) },
	"StrMap":            func(mapping func(rune) rune, s string) string { return strings.Map(mapping, s) },
	"StrRepeat":         func(s string, count int) string { return strings.Repeat(s, count) },
	"StrReplace":        func(s, old, new string, n int) string { return strings.Replace(s, old, new, n) },
	"StrSplit":          func(s, sep string) []string { return strings.Split(s, sep) },
	"StrSplitAfter":     func(s, sep string) []string { return strings.SplitAfter(s, sep) },
	"StrSplitAfterN":    func(s, sep string, n int) []string { return strings.SplitAfterN(s, sep, n) },
	"StrSplitN":         func(s, sep string, n int) []string { return strings.SplitN(s, sep, n) },
	"StrTitle":          func(s string) string { return strings.Title(s) },
	"StrToLower":        func(s string) string { return strings.ToLower(s) },
	"StrToLowerSpecial": func(_case unicode.SpecialCase, s string) string { return strings.ToLowerSpecial(_case, s) },
	"StrToTitle":        func(s string) string { return strings.ToTitle(s) },
	"StrToTitleSpecial": func(_case unicode.SpecialCase, s string) string { return strings.ToTitleSpecial(_case, s) },
	"StrToUpper":        func(s string) string { return strings.ToUpper(s) },
	"StrToUpperSpecial": func(_case unicode.SpecialCase, s string) string { return strings.ToUpperSpecial(_case, s) },
	"StrTrim":           func(s string, cutset string) string { return strings.Trim(s, cutset) },
	"StrTrimFunc":       func(s string, f func(rune) bool) string { return strings.TrimFunc(s, f) },
	"StrTrimLeft":       func(s string, cutset string) string { return strings.TrimLeft(s, cutset) },
	"StrTrimLeftFunc":   func(s string, f func(rune) bool) string { return strings.TrimLeftFunc(s, f) },
	"StrTrimPrefix":     func(s, prefix string) string { return strings.TrimPrefix(s, prefix) },
	"StrTrimRight":      func(s string, cutset string) string { return strings.TrimRight(s, cutset) },
	"StrTrimRightFunc":  func(s string, f func(rune) bool) string { return strings.TrimRightFunc(s, f) },
	"StrTrimSpace":      func(s string) string { return strings.TrimSpace(s) },
	"StrTrimSuffix":     func(s, suffix string) string { return strings.TrimSuffix(s, suffix) },
	"IsStrInSlice":      goutils.IsStrInSlice,
	"YiWanString":       goutils.YiWanString,
	"mod":               func(i, j int) bool { return i%j == 0 },
}
