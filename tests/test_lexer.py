"""
Lexer test cases for TyC compiler
TODO: Implement 100 test cases for lexer
"""

import pytest
from tests.utils import Tokenizer


# ==========================================
# 1. OPERATORS & MAXIMAL MUNCTIONS (15)
# ==========================================
def test_lexer_001():
    """Operators: a---b"""
    tokenizer = Tokenizer("a---b")
    assert tokenizer.get_tokens_as_string() == "a,--,-,b,<EOF>"

def test_lexer_002():
    """Operators: a++++b"""
    tokenizer = Tokenizer("a++++b")
    assert tokenizer.get_tokens_as_string() == "a,++,++,b,<EOF>"

def test_lexer_003():
    """Operators: x<=<y"""
    tokenizer = Tokenizer("x<=<y")
    assert tokenizer.get_tokens_as_string() == "x,<=,<,y,<EOF>"

def test_lexer_004():
    """Operators: x>>>=y"""
    tokenizer = Tokenizer("x>>>=y")
    assert tokenizer.get_tokens_as_string() == "x,>,>,>=,y,<EOF>"

def test_lexer_005():
    """Operators: !!x"""
    tokenizer = Tokenizer("!!x")
    assert tokenizer.get_tokens_as_string() == "!,!,x,<EOF>"

def test_lexer_006():
    """Operators: !===x"""
    tokenizer = Tokenizer("!===x")
    assert tokenizer.get_tokens_as_string() == "!=,==,x,<EOF>"

def test_lexer_007():
    """Operators: a=b==c"""
    tokenizer = Tokenizer("a=b==c")
    assert tokenizer.get_tokens_as_string() == "a,=,b,==,c,<EOF>"

def test_lexer_008():
    """Operators: a=b!=c"""
    tokenizer = Tokenizer("a=b!=c")
    assert tokenizer.get_tokens_as_string() == "a,=,b,!=,c,<EOF>"

def test_lexer_009():
    """Error: a&&&b"""
    tokenizer = Tokenizer("a&&&b")
    assert tokenizer.get_tokens_as_string() == "a,&&,Error Token &"

def test_lexer_010():
    """Error: a|||b"""
    tokenizer = Tokenizer("a|||b")
    assert tokenizer.get_tokens_as_string() == "a,||,Error Token |"

def test_lexer_011():
    """Operators: ++--x"""
    tokenizer = Tokenizer("++--x")
    assert tokenizer.get_tokens_as_string() == "++,--,x,<EOF>"

def test_lexer_012():
    """Operators: x--++"""
    tokenizer = Tokenizer("x--++")
    assert tokenizer.get_tokens_as_string() == "x,--,++,<EOF>"

def test_lexer_013():
    """Operators: +-+-x"""
    tokenizer = Tokenizer("+-+-x")
    assert tokenizer.get_tokens_as_string() == "+,-,+,-,x,<EOF>"

def test_lexer_014():
    """Operators: x=--+y"""
    tokenizer = Tokenizer("x=--+y")
    assert tokenizer.get_tokens_as_string() == "x,=,--,+,y,<EOF>"

def test_lexer_015():
    """Operators: x=+++y"""
    tokenizer = Tokenizer("x=+++y")
    assert tokenizer.get_tokens_as_string() == "x,=,++,+,y,<EOF>"



# ==========================================
# 2. NUMBERS & NUMERIC EDGE CASES (15)
# ==========================================
def test_lexer_016():
    """Number: 1e+"""
    tokenizer = Tokenizer("1e+")
    assert tokenizer.get_tokens_as_string() == "1,e,+,<EOF>"

def test_lexer_017():
    """Number: 1e-"""
    tokenizer = Tokenizer("1e-")
    assert tokenizer.get_tokens_as_string() == "1,e,-,<EOF>"

def test_lexer_018():
    """Number: .e1"""
    tokenizer = Tokenizer(".e1")
    assert tokenizer.get_tokens_as_string() == ".,e1,<EOF>"

def test_lexer_019():
    """Number: 0..1"""
    tokenizer = Tokenizer("0..1")
    assert tokenizer.get_tokens_as_string() == "0.,.1,<EOF>"

def test_lexer_020():
    """Number: 1.2.3"""
    tokenizer = Tokenizer("1.2.3")
    assert tokenizer.get_tokens_as_string() == "1.2,.3,<EOF>"

def test_lexer_021():
    """Number: 9e--2"""
    tokenizer = Tokenizer("9e--2")
    assert tokenizer.get_tokens_as_string() == "9,e,--,2,<EOF>"

def test_lexer_022():
    """Number: 9e++2"""
    tokenizer = Tokenizer("9e++2")
    assert tokenizer.get_tokens_as_string() == "9,e,++,2,<EOF>"

def test_lexer_023():
    """Number: leading zeros"""
    tokenizer = Tokenizer("007.08")
    assert tokenizer.get_tokens_as_string() == "007.08,<EOF>"

def test_lexer_024():
    """Number: .5.6"""
    tokenizer = Tokenizer(".5.6")
    assert tokenizer.get_tokens_as_string() == ".5,.6,<EOF>"

def test_lexer_025():
    """Number: 10e2.5"""
    tokenizer = Tokenizer("10e2.5")
    assert tokenizer.get_tokens_as_string() == "10e2,.5,<EOF>"

def test_lexer_026():
    """Number: 1e2e3"""
    tokenizer = Tokenizer("1e2e3")
    assert tokenizer.get_tokens_as_string() == "1e2,e3,<EOF>"

def test_lexer_027():
    """Number: 0e"""
    tokenizer = Tokenizer("0e")
    assert tokenizer.get_tokens_as_string() == "0,e,<EOF>"

def test_lexer_028():
    """Number: 0e+1"""
    tokenizer = Tokenizer("0e+1")
    assert tokenizer.get_tokens_as_string() == "0e+1,<EOF>"

def test_lexer_029():
    """Number: single dot"""
    tokenizer = Tokenizer(".")
    assert tokenizer.get_tokens_as_string() == ".,<EOF>"

def test_lexer_030():
    """Number: trailing dot"""
    tokenizer = Tokenizer("1.")
    assert tokenizer.get_tokens_as_string() == "1.,<EOF>"



# ==========================================
# 3. STRINGS & ESCAPE HANDLING (20)
# ==========================================
def test_lexer_031():
    """String: \\\\"""
    tokenizer = Tokenizer("\"\\\\\"")
    assert tokenizer.get_tokens_as_string() == "\\\\,<EOF>"

def test_lexer_032():
    """String: \\n \\t"""
    tokenizer = Tokenizer("\"\\n\\t\"")
    assert tokenizer.get_tokens_as_string() == "\\n\\t,<EOF>"

def test_lexer_033():
    """String: escaped quote"""
    tokenizer = Tokenizer("\"\\\"\"")
    assert tokenizer.get_tokens_as_string() == "\\\",<EOF>"

def test_lexer_034():
    """String: a\\\\b"""
    tokenizer = Tokenizer("\"a\\\\b\"")
    assert tokenizer.get_tokens_as_string() == "a\\\\b,<EOF>"

def test_lexer_035():
    """Illegal escape: \\x"""
    tokenizer = Tokenizer("\"bad\\x\"")
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: bad\\x"

def test_lexer_036():
    """Illegal escape: \\q"""
    tokenizer = Tokenizer("\"bad\\q\"")
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: bad\\q"

def test_lexer_037():
    """Unclosed string with escaped newline"""
    tokenizer = Tokenizer("\"bad\\\n\"")
    assert tokenizer.get_tokens_as_string() == "Unclosed String: bad\\\n"

def test_lexer_038():
    """Unclosed string: EOF"""
    tokenizer = Tokenizer("\"unclosed")
    assert tokenizer.get_tokens_as_string() == "Unclosed String: unclosed"

def test_lexer_039():
    """Unclosed string: newline"""
    tokenizer = Tokenizer("\"line\nbreak\"")
    assert tokenizer.get_tokens_as_string() == "Unclosed String: line\n"

def test_lexer_040():
    """Unclosed string: escaped quote"""
    tokenizer = Tokenizer("\"\\\"")
    assert tokenizer.get_tokens_as_string() == "Unclosed String: \\\""

def test_lexer_041():
    """String followed by unclosed string"""
    tokenizer = Tokenizer("\"ok\"\"bad")
    assert tokenizer.get_tokens_as_string() == "ok,Unclosed String: bad"

def test_lexer_042():
    """Triple quote unclosed"""
    tokenizer = Tokenizer("\"\"\"")
    assert tokenizer.get_tokens_as_string() == ",Unclosed String: "

def test_lexer_043():
    """Two valid strings"""
    tokenizer = Tokenizer("\"a\"\"b\"")
    assert tokenizer.get_tokens_as_string() == "a,b,<EOF>"

def test_lexer_044():
    """String containing //"""
    tokenizer = Tokenizer("\"//not comment\"")
    assert tokenizer.get_tokens_as_string() == "//not comment,<EOF>"

def test_lexer_045():
    """String containing /* */"""
    tokenizer = Tokenizer("\"/*not comment*/\"")
    assert tokenizer.get_tokens_as_string() == "/*not comment*/,<EOF>"

def test_lexer_046():
    """String: \\b \\f \\r"""
    tokenizer = Tokenizer("\"\\b\\f\\r\"")
    assert tokenizer.get_tokens_as_string() == "\\b\\f\\r,<EOF>"

def test_lexer_047():
    """String with tab"""
    tokenizer = Tokenizer("\"a\\tb\"")
    assert tokenizer.get_tokens_as_string() == "a\\tb,<EOF>"

def test_lexer_048():
    """Illegal escape: \\z"""
    tokenizer = Tokenizer("\"bad\\z\"")
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: bad\\z"

def test_lexer_049():
    """Unclosed string: \\n"""
    tokenizer = Tokenizer("\"a\\n")
    assert tokenizer.get_tokens_as_string() == "Unclosed String: a\\n"

def test_lexer_050():
    """String with escaped quotes"""
    tokenizer = Tokenizer("\"\\\"\\\"\"")
    assert tokenizer.get_tokens_as_string() == "\\\"\\\",<EOF>"



# ======================================================
# 4. COMMENTS, IDENTIFIERS, WHITESPACES, ERRORS (50)
# =======================================================
def test_lexer_051():
    """Nested block comment"""
    tokenizer = Tokenizer("/*/**/x")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"

def test_lexer_052():
    """Multiple line comments"""
    tokenizer = Tokenizer("//\n//\nx")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"

def test_lexer_053():
    """Comment inside block"""
    tokenizer = Tokenizer("/* // */ x")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"

def test_lexer_054():
    """Multiple block comments"""
    tokenizer = Tokenizer("a/*b*/c/*d*/e")
    assert tokenizer.get_tokens_as_string() == "a,c,e,<EOF>"

def test_lexer_055():
    """Identifier: ifelse"""
    tokenizer = Tokenizer("ifelse")
    assert tokenizer.get_tokens_as_string() == "ifelse,<EOF>"

def test_lexer_056():
    """Identifier: _if"""
    tokenizer = Tokenizer("_if")
    assert tokenizer.get_tokens_as_string() == "_if,<EOF>"

def test_lexer_057():
    """Identifier: while1"""
    tokenizer = Tokenizer("while1")
    assert tokenizer.get_tokens_as_string() == "while1,<EOF>"

def test_lexer_058():
    """Keyword vs identifier"""
    tokenizer = Tokenizer("int intx")
    assert tokenizer.get_tokens_as_string() == "int,intx,<EOF>"

def test_lexer_059():
    """Error: backspace"""
    tokenizer = Tokenizer("a\b\t\nc")
    assert tokenizer.get_tokens_as_string() == "a,Error Token \b"

def test_lexer_060():
    """Whitespace handling"""
    tokenizer = Tokenizer("x\r\f\ty")
    assert tokenizer.get_tokens_as_string() == "x,y,<EOF>"

def test_lexer_061():
    """Error: @"""
    tokenizer = Tokenizer("@")
    assert tokenizer.get_tokens_as_string() == "Error Token @"

def test_lexer_062():
    """Error: #"""
    tokenizer = Tokenizer("#")
    assert tokenizer.get_tokens_as_string() == "Error Token #"

def test_lexer_063():
    """Error: $"""
    tokenizer = Tokenizer("$")
    assert tokenizer.get_tokens_as_string() == "Error Token $"

def test_lexer_064():
    """Error in expression"""
    tokenizer = Tokenizer("x=@")
    assert tokenizer.get_tokens_as_string() == "x,=,Error Token @"

def test_lexer_065():
    """Error after number"""
    tokenizer = Tokenizer("x=1$")
    assert tokenizer.get_tokens_as_string() == "x,=,1,Error Token $"

def test_lexer_066():
    """Unclosed block comment treated as tokens"""
    tokenizer = Tokenizer("/* unclosed")
    assert tokenizer.get_tokens_as_string() == "/,*,unclosed,<EOF>"

def test_lexer_067():
    """Block comment with stars"""
    tokenizer = Tokenizer("x/***/y")
    assert tokenizer.get_tokens_as_string() == "x,y,<EOF>"

def test_lexer_068():
    """Weird block comment"""
    tokenizer = Tokenizer("a/*/b*/c")
    assert tokenizer.get_tokens_as_string() == "a,c,<EOF>"

def test_lexer_069():
    """Comment in assignment"""
    tokenizer = Tokenizer("x=/*c*/1")
    assert tokenizer.get_tokens_as_string() == "x,=,1,<EOF>"

def test_lexer_070():
    """Line comment at end"""
    tokenizer = Tokenizer("x//comment")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"

def test_lexer_071():
    """Block comment at end"""
    tokenizer = Tokenizer("x/*comment*/")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"

def test_lexer_072():
    """Empty string"""
    tokenizer = Tokenizer("\"\"")
    assert tokenizer.get_tokens_as_string() == ",<EOF>"

def test_lexer_073():
    """String with space"""
    tokenizer = Tokenizer("\" \"")
    assert tokenizer.get_tokens_as_string() == " ,<EOF>"

def test_lexer_074():
    """String with spaces"""
    tokenizer = Tokenizer("\"a b c\"")
    assert tokenizer.get_tokens_as_string() == "a b c,<EOF>"

def test_lexer_075():
    """String containing block comment"""
    tokenizer = Tokenizer("\"a/*b*/c\"")
    assert tokenizer.get_tokens_as_string() == "a/*b*/c,<EOF>"

def test_lexer_076():
    """String containing line comment"""
    tokenizer = Tokenizer("\"a//b\"")
    assert tokenizer.get_tokens_as_string() == "a//b,<EOF>"

def test_lexer_077():
    """Expression with block comment"""
    tokenizer = Tokenizer("x=1/*c*/+2")
    assert tokenizer.get_tokens_as_string() == "x,=,1,+,2,<EOF>"

def test_lexer_078():
    """Expression with line comment"""
    tokenizer = Tokenizer("x=1//c\n+2")
    assert tokenizer.get_tokens_as_string() == "x,=,1,+,2,<EOF>"

def test_lexer_079():
    """Operators: a+++b"""
    tokenizer = Tokenizer("a+++b")
    assert tokenizer.get_tokens_as_string() == "a,++,+,b,<EOF>"

def test_lexer_080():
    """Operators: a----b"""
    tokenizer = Tokenizer("a----b")
    assert tokenizer.get_tokens_as_string() == "a,--,--,b,<EOF>"

def test_lexer_081():
    """Prefix operator"""
    tokenizer = Tokenizer("x=--y")
    assert tokenizer.get_tokens_as_string() == "x,=,--,y,<EOF>"

def test_lexer_082():
    """Separated minus"""
    tokenizer = Tokenizer("x=- -y")
    assert tokenizer.get_tokens_as_string() == "x,=,-,-,y,<EOF>"

def test_lexer_083():
    """Separated plus"""
    tokenizer = Tokenizer("x=+ +y")
    assert tokenizer.get_tokens_as_string() == "x,=,+,+,y,<EOF>"

def test_lexer_084():
    """Mixed +-"""
    tokenizer = Tokenizer("x=+-y")
    assert tokenizer.get_tokens_as_string() == "x,=,+,-,y,<EOF>"

def test_lexer_085():
    """Mixed -+"""
    tokenizer = Tokenizer("x=-+y")
    assert tokenizer.get_tokens_as_string() == "x,=,-,+,y,<EOF>"

def test_lexer_086():
    """Scientific with identifier"""
    tokenizer = Tokenizer("x=1e+2y")
    assert tokenizer.get_tokens_as_string() == "x,=,1e+2,y,<EOF>"

def test_lexer_087():
    """Scientific with addition"""
    tokenizer = Tokenizer("x=1e2+3")
    assert tokenizer.get_tokens_as_string() == "x,=,1e2,+,3,<EOF>"

def test_lexer_088():
    """Float starting with dot"""
    tokenizer = Tokenizer("x=.5+1")
    assert tokenizer.get_tokens_as_string() == "x,=,.5,+,1,<EOF>"

def test_lexer_089():
    """Float ending with dot"""
    tokenizer = Tokenizer("x=1.+.2")
    assert tokenizer.get_tokens_as_string() == "x,=,1.,+,.2,<EOF>"

def test_lexer_090():
    """Double dot"""
    tokenizer = Tokenizer("x=1..2")
    assert tokenizer.get_tokens_as_string() == "x,=,1.,.2,<EOF>"

def test_lexer_091():
    """Illegal escape: \\u"""
    tokenizer = Tokenizer("\"bad\\u\"")
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: bad\\u"

def test_lexer_092():
    """Illegal escape: \\9"""
    tokenizer = Tokenizer("\"bad\\9\"")
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: bad\\9"

def test_lexer_093():
    """Illegal escape with tab"""
    tokenizer = Tokenizer("\"bad\\\t\"")
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: bad\\\t"

def test_lexer_094():
    """Error after string"""
    tokenizer = Tokenizer("\"ok\" @")
    assert tokenizer.get_tokens_as_string() == "ok,Error Token @"

def test_lexer_095():
    """Error after string"""
    tokenizer = Tokenizer("\"ok\"$")
    assert tokenizer.get_tokens_as_string() == "ok,Error Token $"

def test_lexer_096():
    """Braces"""
    tokenizer = Tokenizer("a={{{}}}")
    assert tokenizer.get_tokens_as_string() == "a,=,{,{,{,},},},<EOF>"

def test_lexer_097():
    """Parentheses"""
    tokenizer = Tokenizer("(((x)))")
    assert tokenizer.get_tokens_as_string() == "(,(,(,x,),),),<EOF>"

def test_lexer_098():
    """Mixed braces"""
    tokenizer = Tokenizer("{(x)}")
    assert tokenizer.get_tokens_as_string() == "{,(,x,),},<EOF>"

def test_lexer_099():
    """Dot and parentheses"""
    tokenizer = Tokenizer("x.(y)")
    assert tokenizer.get_tokens_as_string() == "x,.,(,y,),<EOF>"

def test_lexer_100():
    """Full expression"""
    tokenizer = Tokenizer("/*hdr*/x=1+2*(3-4);")
    assert tokenizer.get_tokens_as_string() == "x,=,1,+,2,*,(,3,-,4,),;,<EOF>"





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