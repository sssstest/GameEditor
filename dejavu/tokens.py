#!/usr/bin/env python

eof="eof"
unexpected="unexpected"

name="name"
real="real"
string="string"

l_brace="l_brace"#"{"
r_brace="r_brace"#"}"
l_paren="l_paren"#"("
r_paren="r_paren"#")"
l_square="l_square"#"["
r_square="r_square"#"]"

equals="equals"#"="

less="less"#"<"
less_equals="less_equals"#"<="
is_equals="is_equals"#"=="
not_equals="not_equals"#"!="
greater_equals="greater_equals"#">="
greater="greater"#">"

plus_equals="plus_equals"#"+="
minus_equals="minus_equals"#"-="
times_equals="times_equals"#"*="
div_equals="div_equals"#"/="
and_equals="and_equals"#"&="
or_equals="or_equals"#"|="
xor_equals="xor_equals"#"^="

comma="comma"#","
dot="dot"#"."
colon="colon"#":"
semicolon="semicolon"#";"
question="question"#"?"

dollar="dollar"#"$"

plusplus="plusplus"#"++"
minusminus="minusminus"#"--"

plus="plus"#"+"
minus="minus"#"-"
times="times"#"*"
divide="divide"#"/"

exclaim="exclaim"#"!"
tilde="tilde"#"~"

ampamp="ampamp"#"&&"
pipepipe="pipepipe"#"||"
caretcaret="caretcaret"#"^^"

bit_and="bit_and"#"&"
bit_or="bit_or"#"|"
bit_xor="bit_xor"#"^"
shift_left="shift_left"#"<<"
shift_right="shift_right"#">>"

kw_div="kw_div"
kw_mod="kw_mod"

kw_true="kw_true"
kw_false="kw_false"

kw_self="kw_self"
kw_other="kw_other"
kw_all="kw_all"
kw_noone="kw_noone"
kw_global="kw_global"
kw_local="kw_local"

kw_globalvar="kw_globalvar"
kw_var="kw_var"

kw_unsigned="kw_unsigned"

kw_if="kw_if"
kw_then="kw_then"
kw_else="kw_else"
kw_repeat="kw_repeat"
kw_while="kw_while"
kw_do="kw_do"
kw_until="kw_until"
kw_for="kw_for"
kw_switch="kw_switch"
kw_with="kw_with"
kw_case="kw_case"
kw_default="kw_default"
kw_break="kw_break"
kw_continue="kw_continue"
kw_exit="kw_exit"
kw_return="kw_return"

OPERATORS={}

OPERATORS[l_brace] = "{"
OPERATORS[r_brace] = "}"
OPERATORS[l_paren] = "("
OPERATORS[r_paren] = ")"
OPERATORS[l_square] = "["
OPERATORS[r_square] = "]"

OPERATORS[equals] = "="

OPERATORS[less] = "<"
OPERATORS[less_equals] = "<="
OPERATORS[is_equals] = "=="
OPERATORS[not_equals] = "!="
OPERATORS[greater_equals] = ">="
OPERATORS[greater] = ">"

OPERATORS[plus_equals] = "+="
OPERATORS[minus_equals] = "-="
OPERATORS[times_equals] = "*="
OPERATORS[div_equals] = "/="
OPERATORS[and_equals] = "&="
OPERATORS[or_equals] = "|="
OPERATORS[xor_equals] = "^="

OPERATORS[comma] = ","
OPERATORS[dot] = "."
OPERATORS[colon] = ":"
OPERATORS[semicolon] = ";"

OPERATORS[plus] = "+"
OPERATORS[minus] = "-"
OPERATORS[times] = "*"
OPERATORS[divide] = "/"

OPERATORS[exclaim] = "!"
OPERATORS[tilde] = "~"

OPERATORS[ampamp] = "&&"
OPERATORS[pipepipe] = "||"
OPERATORS[caretcaret] = "^^"

OPERATORS[bit_and] = "&"
OPERATORS[bit_or] = "|"
OPERATORS[bit_xor] = "^"
OPERATORS[shift_left] = "<<"
OPERATORS[shift_right] = ">>"
