"""
Lexer test cases for TyC compiler
TODO: Implement 100 test cases for lexer
"""

import pytest
from tests.utils import Tokenizer
from build.lexererr import ErrorToken, IllegalEscape, UncloseString

def assert_tokens(src: str, expected: str) -> None:
    result = Tokenizer(src).get_tokens_as_string()
    assert result == expected

def assert_lexer_error(src: str, error_cls, expected: str) -> None:
    msg = Tokenizer(src).get_tokens_as_string()
    msg = msg.split(",")[-1] if "," in msg else msg

    if error_cls.__name__ == "ErrorToken":
        msg = msg.replace("Error Token ", "", 1)
    elif error_cls.__name__ == "UncloseString":
        msg = msg.replace("Unclosed String: ", "", 1)
    elif error_cls.__name__ == "IllegalEscape":
        msg = msg.replace("Illegal Escape In String: ", "", 1)

    assert msg == expected


# ==========================================
# 1. OPERATORS & MAXIMAL MUNCTIONS (15)
# ==========================================
def test_lexer_001():
    source = "a---b"
    expected = "a,--,-,b,<EOF>"
    assert_tokens(source, expected)

def test_lexer_002():
    source = "a++++b"
    expected = "a,++,++,b,<EOF>"
    assert_tokens(source, expected)

def test_lexer_003():
    source = "x<=<y"
    expected = "x,<=,<,y,<EOF>"
    assert_tokens(source, expected)

def test_lexer_004():
    source = "x>>>=y"
    expected = "x,>,>,>=,y,<EOF>"
    assert_tokens(source, expected)

def test_lexer_005():
    source = "!!x"
    expected = "!,!,x,<EOF>"
    assert_tokens(source, expected)

def test_lexer_006():
    source = "!===x"
    expected = "!=,==,x,<EOF>"
    assert_tokens(source, expected)

def test_lexer_007():
    source = "a=b==c"
    expected = "a,=,b,==,c,<EOF>"
    assert_tokens(source, expected)

def test_lexer_008():
    source = "a=b!=c"
    expected = "a,=,b,!=,c,<EOF>"
    assert_tokens(source, expected)

def test_lexer_009():
    source = "a&&&b"
    assert_lexer_error(source, ErrorToken, "&")

def test_lexer_010():
    source = "a|||b"
    assert_lexer_error(source, ErrorToken, "|")

def test_lexer_011():
    source = "++--x"
    expected = "++,--,x,<EOF>"
    assert_tokens(source, expected)

def test_lexer_012():
    source = "x--++"
    expected = "x,--,++,<EOF>"
    assert_tokens(source, expected)

def test_lexer_013():
    source = "+-+-x"
    expected = "+,-,+,-,x,<EOF>"
    assert_tokens(source, expected)

def test_lexer_014():
    source = "x=--+y"
    expected = "x,=,--,+,y,<EOF>"
    assert_tokens(source, expected)

def test_lexer_015():
    source = "x=+++y"
    expected = "x,=,++,+,y,<EOF>"
    assert_tokens(source, expected)


# ==========================================
# 2. NUMBERS & NUMERIC EDGE CASES (15)
# ==========================================
def test_lexer_016():
    source = "1e+"
    expected = "1,e,+,<EOF>"
    assert_tokens(source, expected)

def test_lexer_017():
    source = "1e-"
    expected = "1,e,-,<EOF>"
    assert_tokens(source, expected)

def test_lexer_018():
    source = ".e1"
    expected = ".,e1,<EOF>"
    assert_tokens(source, expected)

def test_lexer_019():
    source = "0..1"
    expected = "0.,.1,<EOF>"
    assert_tokens(source, expected)

def test_lexer_020():
    source = "1.2.3"
    expected = "1.2,.3,<EOF>"
    assert_tokens(source, expected)

def test_lexer_021():
    source = "9e--2"
    expected = "9,e,--,2,<EOF>"
    assert_tokens(source, expected)

def test_lexer_022():
    source = "9e++2"
    expected = "9,e,++,2,<EOF>"
    assert_tokens(source, expected)

def test_lexer_023():
    source = "007.08"
    expected = "007.08,<EOF>"
    assert_tokens(source, expected)

def test_lexer_024():
    source = ".5.6"
    expected = ".5,.6,<EOF>"
    assert_tokens(source, expected)

def test_lexer_025():
    source = "10e2.5"
    expected = "10e2,.5,<EOF>"
    assert_tokens(source, expected)

def test_lexer_026():
    source = "1e2e3"
    expected = "1e2,e3,<EOF>"
    assert_tokens(source, expected)

def test_lexer_027():
    source = "0e"
    expected = "0,e,<EOF>"
    assert_tokens(source, expected)

def test_lexer_028():
    source = "0e+1"
    expected = "0e+1,<EOF>"
    assert_tokens(source, expected)

def test_lexer_029():
    source = "."
    expected = ".,<EOF>"
    assert_tokens(source, expected)

def test_lexer_030():
    source = "1."
    expected = "1.,<EOF>"
    assert_tokens(source, expected)


# ==========================================
# 3. STRINGS & ESCAPE HANDLING (20)
# ==========================================
def test_lexer_031():
    source = "\"\\\\\""
    expected = "\\\\,<EOF>"
    assert_tokens(source, expected)

def test_lexer_032():
    source = "\"\\n\\t\""
    expected = "\\n\\t,<EOF>"
    assert_tokens(source, expected)

def test_lexer_033():
    source = "\"\\\"\""
    expected = "\\\",<EOF>"
    assert_tokens(source, expected)

def test_lexer_034():
    source = "\"a\\\\b\""
    expected = "a\\\\b,<EOF>"
    assert_tokens(source, expected)

def test_lexer_035():
    source = "\"bad\\x\""
    assert_lexer_error(source, IllegalEscape, "bad\\x")

def test_lexer_036():
    source = "\"bad\\q\""
    assert_lexer_error(source, IllegalEscape, "bad\\q")

def test_lexer_037():
    source = "\"bad\\\n\""
    assert_lexer_error(source, UncloseString, "bad\\\n")

def test_lexer_038():
    source = "\"unclosed"
    assert_lexer_error(source, UncloseString, "unclosed")

def test_lexer_039():
    source = "\"line\nbreak\""
    assert_lexer_error(source, UncloseString, "line\n")

def test_lexer_040():
    source = "\"\\\""
    assert_lexer_error(source, UncloseString, "\\\"")

def test_lexer_041():
    source = "\"ok\"\"bad"
    assert_lexer_error(source, UncloseString, "bad")

def test_lexer_042():
    source = "\"\"\""
    assert_lexer_error(source, UncloseString, "")

def test_lexer_043():
    source = "\"a\"\"b\""
    expected = "a,b,<EOF>"
    assert_tokens(source, expected)

def test_lexer_044():
    source = "\"//not comment\""
    expected = "//not comment,<EOF>"
    assert_tokens(source, expected)

def test_lexer_045():
    source = "\"/*not comment*/\""
    expected = "/*not comment*/,<EOF>"
    assert_tokens(source, expected)

def test_lexer_046():
    source = "\"\\b\\f\\r\""
    expected = "\\b\\f\\r,<EOF>"
    assert_tokens(source, expected)

def test_lexer_047():
    source = "\"a\\tb\""
    expected = "a\\tb,<EOF>"
    assert_tokens(source, expected)

def test_lexer_048():
    source = "\"bad\\z\""
    assert_lexer_error(source, IllegalEscape, "bad\\z")

def test_lexer_049():
    source = "\"a\\n"
    assert_lexer_error(source, UncloseString, "a\\n")

def test_lexer_050():
    source = "\"\\\"\\\"\""
    expected = "\\\"\\\",<EOF>"
    assert_tokens(source, expected)


# ======================================================
# 4. COMMENTS, IDENTIFIERS, WHITESPACES, ERRORS (50)
# =======================================================
def test_lexer_051():
    source = "/*/**/x"
    expected = "x,<EOF>"
    assert_tokens(source, expected)

def test_lexer_052():
    source = "//\n//\nx"
    expected = "x,<EOF>"
    assert_tokens(source, expected)

def test_lexer_053():
    source = "/* // */ x"
    expected = "x,<EOF>"
    assert_tokens(source, expected)

def test_lexer_054():
    source = "a/*b*/c/*d*/e"
    expected = "a,c,e,<EOF>"
    assert_tokens(source, expected)

def test_lexer_055():
    source = "ifelse"
    expected = "ifelse,<EOF>"
    assert_tokens(source, expected)

def test_lexer_056():
    source = "_if"
    expected = "_if,<EOF>"
    assert_tokens(source, expected)

def test_lexer_057():
    source = "while1"
    expected = "while1,<EOF>"
    assert_tokens(source, expected)

def test_lexer_058():
    source = "int intx"
    expected = "int,intx,<EOF>"
    assert_tokens(source, expected)

def test_lexer_059():
    source = "a\b\t\nc"
    assert_lexer_error(source, ErrorToken, "\b")

def test_lexer_060():
    source = "x\r\f\ty"
    expected = "x,y,<EOF>"
    assert_tokens(source, expected)

def test_lexer_061():
    source = "@"
    assert_lexer_error(source, ErrorToken, "@")

def test_lexer_062():
    source = "#"
    assert_lexer_error(source, ErrorToken, "#")

def test_lexer_063():
    source = "$"
    assert_lexer_error(source, ErrorToken, "$")

def test_lexer_064():
    source = "x=@"
    assert_lexer_error(source, ErrorToken, "@")

def test_lexer_065():
    source = "x=1$"
    assert_lexer_error(source, ErrorToken, "$")

def test_lexer_066():
    source = "/* unclosed"
    expected = "/,*,unclosed,<EOF>"
    assert_tokens(source, expected)

def test_lexer_067():
    source = "x/***/y"
    expected = "x,y,<EOF>"
    assert_tokens(source, expected)

def test_lexer_068():
    source = "a/*/b*/c"
    expected = "a,c,<EOF>"
    assert_tokens(source, expected)

def test_lexer_069():
    source = "x=/*c*/1"
    expected = "x,=,1,<EOF>"
    assert_tokens(source, expected)

def test_lexer_070():
    source = "x//comment"
    expected = "x,<EOF>"
    assert_tokens(source, expected)

def test_lexer_071():
    source = "x/*comment*/"
    expected = "x,<EOF>"
    assert_tokens(source, expected)

def test_lexer_072():
    source = "\"\""
    expected = ",<EOF>"
    assert_tokens(source, expected)

def test_lexer_073():
    source = "\" \""
    expected = " ,<EOF>"
    assert_tokens(source, expected)

def test_lexer_074():
    source = "\"a b c\""
    expected = "a b c,<EOF>"
    assert_tokens(source, expected)

def test_lexer_075():
    source = "\"a/*b*/c\""
    expected = "a/*b*/c,<EOF>"
    assert_tokens(source, expected)

def test_lexer_076():
    source = "\"a//b\""
    expected = "a//b,<EOF>"
    assert_tokens(source, expected)

def test_lexer_077():
    source = "x=1/*c*/+2"
    expected = "x,=,1,+,2,<EOF>"
    assert_tokens(source, expected)

def test_lexer_078():
    source = "x=1//c\n+2"
    expected = "x,=,1,+,2,<EOF>"
    assert_tokens(source, expected)

def test_lexer_079():
    source = "a+++b"
    expected = "a,++,+,b,<EOF>"
    assert_tokens(source, expected)

def test_lexer_080():
    source = "a----b"
    expected = "a,--,--,b,<EOF>"
    assert_tokens(source, expected)

def test_lexer_081():
    source = "x=--y"
    expected = "x,=,--,y,<EOF>"
    assert_tokens(source, expected)

def test_lexer_082():
    source = "x=- -y"
    expected = "x,=,-,-,y,<EOF>"
    assert_tokens(source, expected)

def test_lexer_083():
    source = "x=+ +y"
    expected = "x,=,+,+,y,<EOF>"
    assert_tokens(source, expected)

def test_lexer_084():
    source = "x=+-y"
    expected = "x,=,+,-,y,<EOF>"
    assert_tokens(source, expected)

def test_lexer_085():
    source = "x=-+y"
    expected = "x,=,-,+,y,<EOF>"
    assert_tokens(source, expected)

def test_lexer_086():
    source = "x=1e+2y"
    expected = "x,=,1e+2,y,<EOF>"
    assert_tokens(source, expected)

def test_lexer_087():
    source = "x=1e2+3"
    expected = "x,=,1e2,+,3,<EOF>"
    assert_tokens(source, expected)

def test_lexer_088():
    source = "x=.5+1"
    expected = "x,=,.5,+,1,<EOF>"
    assert_tokens(source, expected)

def test_lexer_089():
    source = "x=1.+.2"
    expected = "x,=,1.,+,.2,<EOF>"
    assert_tokens(source, expected)

def test_lexer_090():
    source = "x=1..2"
    expected = "x,=,1.,.2,<EOF>"
    assert_tokens(source, expected)

def test_lexer_091():
    source = "\"bad\\u\""
    assert_lexer_error(source, IllegalEscape, "bad\\u")

def test_lexer_092():
    source = "\"bad\\9\""
    assert_lexer_error(source, IllegalEscape, "bad\\9")

def test_lexer_093():
    source = "\"bad\\\t\""
    assert_lexer_error(source, IllegalEscape, "bad\\\t")

def test_lexer_094():
    source = "\"ok\" @"
    assert_lexer_error(source, ErrorToken, "@")

def test_lexer_095():
    source = "\"ok\"$"
    assert_lexer_error(source, ErrorToken, "$")

def test_lexer_096():
    source = "a={{{}}}"
    expected = "a,=,{,{,{,},},},<EOF>"
    assert_tokens(source, expected)

def test_lexer_097():
    source = "(((x)))"
    expected = "(,(,(,x,),),),<EOF>"
    assert_tokens(source, expected)

def test_lexer_098():
    source = "{(x)}"
    expected = "{,(,x,),},<EOF>"
    assert_tokens(source, expected)

def test_lexer_099():
    source = "x.(y)"
    expected = "x,.,(,y,),<EOF>"
    assert_tokens(source, expected)

def test_lexer_100():
    source = "/*hdr*/x=1+2*(3-4);"
    expected = "x,=,1,+,2,*,(,3,-,4,),;,<EOF>"
    assert_tokens(source, expected)





'''
# ========== Simple Test Cases (10 types) ==========
def test_keyword_auto():
    """1. Keyword"""
    tokenizer = Tokenizer("auto")
    assert tokenizer.get_tokens_as_string() == "auto,<EOF>"


def test_operator_assign():
    """2. Operator"""
    tokenizer = Tokenizer("=")
    assert tokenizer.get_tokens_as_string() == "=,<EOF>"


def test_separator_semi():
    """3. Separator"""
    tokenizer = Tokenizer(";")
    assert tokenizer.get_tokens_as_string() == ";,<EOF>"


def test_integer_single_digit():
    """4. Integer literal"""
    tokenizer = Tokenizer("5")
    assert tokenizer.get_tokens_as_string() == "5,<EOF>"


def test_float_decimal():
    """5. Float literal"""
    tokenizer = Tokenizer("3.14")
    assert tokenizer.get_tokens_as_string() == "3.14,<EOF>"


def test_string_simple():
    """6. String literal"""
    tokenizer = Tokenizer('"hello"')
    assert tokenizer.get_tokens_as_string() == "hello,<EOF>"


def test_identifier_simple():
    """7. Identifier"""
    tokenizer = Tokenizer("x")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"


def test_line_comment():
    """8. Line comment"""
    tokenizer = Tokenizer("// This is a comment")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_integer_in_expression():
    """9. Mixed: integers and operator"""
    tokenizer = Tokenizer("5+10")
    assert tokenizer.get_tokens_as_string() == "5,+,10,<EOF>"


def test_complex_expression():
    """10. Complex: variable declaration"""
    tokenizer = Tokenizer("auto x = 5 + 3 * 2;")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,5,+,3,*,2,;,<EOF>"
'''

