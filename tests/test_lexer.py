"""
Lexer test cases for TyC compiler
TODO: Implement 100 test cases for lexer
"""

import pytest
from tests.utils import Tokenizer

# =========================
# 1. KEYWORDS (10)
# =========================
def test_kw_auto():             assert Tokenizer("auto").get_tokens_as_string() == "auto,<EOF>"
def test_kw_int():              assert Tokenizer("int").get_tokens_as_string() == "int,<EOF>"
def test_kw_float():            assert Tokenizer("float").get_tokens_as_string() == "float,<EOF>"
def test_kw_string():           assert Tokenizer("string").get_tokens_as_string() == "string,<EOF>"
def test_kw_void():             assert Tokenizer("void").get_tokens_as_string() == "void,<EOF>"
def test_kw_if():               assert Tokenizer("if").get_tokens_as_string() == "if,<EOF>"
def test_kw_else():             assert Tokenizer("else").get_tokens_as_string() == "else,<EOF>"
def test_kw_for():              assert Tokenizer("for").get_tokens_as_string() == "for,<EOF>"
def test_kw_while():            assert Tokenizer("while").get_tokens_as_string() == "while,<EOF>"
def test_kw_return():           assert Tokenizer("return").get_tokens_as_string() == "return,<EOF>"


# =========================
# 2. OPERATORS (15)
# =========================
def test_op_add():              assert Tokenizer("+").get_tokens_as_string() == "+,<EOF>"
def test_op_sub():              assert Tokenizer("-").get_tokens_as_string() == "-,<EOF>"
def test_op_mul():              assert Tokenizer("*").get_tokens_as_string() == "*,<EOF>"
def test_op_div():              assert Tokenizer("/").get_tokens_as_string() == "/,<EOF>"
def test_op_mod():              assert Tokenizer("%").get_tokens_as_string() == "%,<EOF>"
def test_op_assign():           assert Tokenizer("=").get_tokens_as_string() == "=,<EOF>"
def test_op_eq():               assert Tokenizer("==").get_tokens_as_string() == "==,<EOF>"
def test_op_neq():              assert Tokenizer("!=").get_tokens_as_string() == "!=,<EOF>"
def test_op_lt():               assert Tokenizer("<").get_tokens_as_string() == "<,<EOF>"
def test_op_le():               assert Tokenizer("<=").get_tokens_as_string() == "<=,<EOF>"
def test_op_gt():               assert Tokenizer(">").get_tokens_as_string() == ">,<EOF>"
def test_op_ge():               assert Tokenizer(">=").get_tokens_as_string() == ">=,<EOF>"
def test_op_and():              assert Tokenizer("&&").get_tokens_as_string() == "&&,<EOF>"
def test_op_or():               assert Tokenizer("||").get_tokens_as_string() == "||,<EOF>"
def test_op_not():              assert Tokenizer("!").get_tokens_as_string() == "!,<EOF>"


# =========================
# 3. SEPARATORS (10)
# =========================
def test_sep_lp():              assert Tokenizer("(").get_tokens_as_string() == "(,<EOF>"
def test_sep_rp():              assert Tokenizer(")").get_tokens_as_string() == "),<EOF>"
def test_sep_lsb():             assert Tokenizer("[").get_tokens_as_string() == "[,<EOF>"
def test_sep_rsb():             assert Tokenizer("]").get_tokens_as_string() == "],<EOF>"
def test_sep_lb():              assert Tokenizer("{").get_tokens_as_string() == "{,<EOF>"
def test_sep_rb():              assert Tokenizer("}").get_tokens_as_string() == "},<EOF>"
def test_sep_semi():            assert Tokenizer(";").get_tokens_as_string() == ";,<EOF>"
def test_sep_comma():           assert Tokenizer(",").get_tokens_as_string() == ",,<EOF>"
def test_sep_colon():           assert Tokenizer(":").get_tokens_as_string() == ":,<EOF>"
def test_sep_dot():             assert Tokenizer(".").get_tokens_as_string() == ".,<EOF>"


# =========================
# 4. IDENTIFIERS (10)
# =========================
def test_id_single():           assert Tokenizer("x").get_tokens_as_string() == "x,<EOF>"
def test_id_long():             assert Tokenizer("variable").get_tokens_as_string() == "variable,<EOF>"
def test_id_underscore():       assert Tokenizer("_x").get_tokens_as_string() == "_x,<EOF>"
def test_id_mix():              assert Tokenizer("a1b2").get_tokens_as_string() == "a1b2,<EOF>"
def test_id_upper():            assert Tokenizer("ABC").get_tokens_as_string() == "ABC,<EOF>"
def test_id_keyword_like():     assert Tokenizer("auto1").get_tokens_as_string() == "auto1,<EOF>"
def test_id_snake():            assert Tokenizer("my_var").get_tokens_as_string() == "my_var,<EOF>"
def test_id_camel():            assert Tokenizer("myVar").get_tokens_as_string() == "myVar,<EOF>"
def test_id_digits():           assert Tokenizer("x123").get_tokens_as_string() == "x123,<EOF>"
def test_id_long_mix():         assert Tokenizer("_aB9_").get_tokens_as_string() == "_aB9_,<EOF>"


# =========================
# 5. INTEGER LITERALS (10)
# =========================
def test_int_zero():            assert Tokenizer("0").get_tokens_as_string() == "0,<EOF>"
def test_int_pos():             assert Tokenizer("123").get_tokens_as_string() == "123,<EOF>"
def test_int_neg():             assert Tokenizer("-5").get_tokens_as_string() == "-5,<EOF>"
def test_int_large():           assert Tokenizer("99999").get_tokens_as_string() == "99999,<EOF>"
def test_int_expr():            assert Tokenizer("1+2").get_tokens_as_string() == "1,+,2,<EOF>"
def test_int_assign():          assert Tokenizer("x=10").get_tokens_as_string() == "x,=,10,<EOF>"
def test_int_multi():           assert Tokenizer("1 2").get_tokens_as_string() == "1,2,<EOF>"
def test_int_semi():            assert Tokenizer("7;").get_tokens_as_string() == "7,;,<EOF>"
def test_int_paren():           assert Tokenizer("(8)").get_tokens_as_string() == "(,8,),<EOF>"
def test_int_array():           assert Tokenizer("a[3]").get_tokens_as_string() == "a,[,3,],<EOF>"


# =========================
# 6. FLOAT LITERALS (10)
# =========================
def test_float_simple():        assert Tokenizer("3.14").get_tokens_as_string() == "3.14,<EOF>"
def test_float_dot():           assert Tokenizer(".5").get_tokens_as_string() == ".5,<EOF>"
def test_float_tail():          assert Tokenizer("5.").get_tokens_as_string() == "5.,<EOF>"
def test_float_exp():           assert Tokenizer("1e3").get_tokens_as_string() == "1e3,<EOF>"
def test_float_exp2():          assert Tokenizer("1.2e-3").get_tokens_as_string() == "1.2e-3,<EOF>"
def test_float_neg():           assert Tokenizer("-2.5").get_tokens_as_string() == "-2.5,<EOF>"
def test_float_expr():          assert Tokenizer("1.5+2").get_tokens_as_string() == "1.5,+,2,<EOF>"
def test_float_assign():        assert Tokenizer("x=1.0").get_tokens_as_string() == "x,=,1.0,<EOF>"
def test_float_multi():         assert Tokenizer("1.1 2.2").get_tokens_as_string() == "1.1,2.2,<EOF>"
def test_float_cmp():           assert Tokenizer("1.0<=2.0").get_tokens_as_string() == "1.0,<=,2.0,<EOF>"


# =========================
# 7. STRING LITERALS (10)
# =========================
def test_str_simple():          assert Tokenizer('"hi"').get_tokens_as_string() == "hi,<EOF>"
def test_str_space():           assert Tokenizer('"hello world"').get_tokens_as_string() == "hello world,<EOF>"
def test_str_empty():           assert Tokenizer('""').get_tokens_as_string() == ",<EOF>"
def test_str_escape_n():        assert Tokenizer('"a\\n"').get_tokens_as_string() == "a\\n,<EOF>"
def test_str_escape_t():        assert Tokenizer('"\\t"').get_tokens_as_string() == "\\t,<EOF>"
def test_str_quote():           assert Tokenizer('"a\\"b"').get_tokens_as_string() == 'a\\"b,<EOF>'
def test_str_assign():          assert Tokenizer('x="hi"').get_tokens_as_string() == "x,=,hi,<EOF>"
def test_str_call():            assert Tokenizer('f("a")').get_tokens_as_string() == "f,(,a,),<EOF>"
def test_str_concat():          assert Tokenizer('"a"+"b"').get_tokens_as_string() == "a,+,b,<EOF>"
def test_str_array():           assert Tokenizer('s[0]="x"').get_tokens_as_string() == "s,[,0,],=,x,<EOF>"


# =========================
# 8. COMMENTS (5)
# =========================
def test_line_comment():        assert Tokenizer("// hi").get_tokens_as_string() == "<EOF>"
def test_block_comment():       assert Tokenizer("/* hi */").get_tokens_as_string() == "<EOF>"
def test_comment_code():        assert Tokenizer("x//c").get_tokens_as_string() == "x,<EOF>"
def test_block_mid():           assert Tokenizer("x/*c*/y").get_tokens_as_string() == "x,y,<EOF>"
def test_comment_only():        assert Tokenizer("//").get_tokens_as_string() == "<EOF>"


# =========================
# 9. INVALID TOKENS (10)
# =========================
def test_err_char():            assert Tokenizer("@").get_tokens_as_string() == "Error Token @"
def test_err_unclose_string():  assert Tokenizer('"abc').get_tokens_as_string() == "Unclosed String: abc"
def test_err_illegal_escape():  assert Tokenizer('"a\\q"').get_tokens_as_string() == "Illegal Escape In String: a\\q"
def test_err_char_mix():        assert Tokenizer("x$y").get_tokens_as_string() == "x,Error Token $"
def test_err_symbol():          assert Tokenizer("#").get_tokens_as_string() == "Error Token #"
def test_err_unclose_line():    assert Tokenizer('"a\n').get_tokens_as_string() == "Unclosed String: a\n"
def test_err_illegal_escape2(): assert Tokenizer('"\\z"').get_tokens_as_string() == "Illegal Escape In String: \\z"
def test_err_only_symbol():     assert Tokenizer("^").get_tokens_as_string() == "Error Token ^"
def test_err_mid():             assert Tokenizer("1 @ 2").get_tokens_as_string() == "1,Error Token @"
def test_err_mix_string():      assert Tokenizer('"a\\k"').get_tokens_as_string() == "Illegal Escape In String: a\\k"


# =========================
# 10. MIXED & EDGE CASES (10)
# =========================

def test_mixed_decl():
    tokenizer = Tokenizer("int a=10;")
    assert tokenizer.get_tokens_as_string() == "int,a,=,10,;,<EOF>"

def test_nested_expr():
    tokenizer = Tokenizer("(1+2)*3")
    assert tokenizer.get_tokens_as_string() == "(,1,+,2,),*,3,<EOF>"

def test_array_access():
    tokenizer = Tokenizer("arr[10]")
    assert tokenizer.get_tokens_as_string() == "arr,[,10,],<EOF>"

def test_struct_access():
    tokenizer = Tokenizer("a.b")
    assert tokenizer.get_tokens_as_string() == "a,.,b,<EOF>"

def test_logical_expr():
    tokenizer = Tokenizer("a&&b||c")
    assert tokenizer.get_tokens_as_string() == "a,&&,b,||,c,<EOF>"

def test_relational_chain():
    tokenizer = Tokenizer("a< b >=c")
    assert tokenizer.get_tokens_as_string() == "a,<,b,>=,c,<EOF>"

def test_increment():
    tokenizer = Tokenizer("i++")
    assert tokenizer.get_tokens_as_string() == "i,++,<EOF>"

def test_decrement():
    tokenizer = Tokenizer("--i")
    assert tokenizer.get_tokens_as_string() == "--,i,<EOF>"

def test_complex_statement():
    tokenizer = Tokenizer("return x+1;")
    assert tokenizer.get_tokens_as_string() == "return,x,+,1,;,<EOF>"

def test_comment_between_tokens():
    tokenizer = Tokenizer("x/*comment*/+y")
    assert tokenizer.get_tokens_as_string() == "x,+,y,<EOF>"





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

