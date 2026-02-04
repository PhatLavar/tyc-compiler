"""
Parser test cases for TyC compiler
TODO: Implement 100 test cases for parser
"""

import pytest
from tests.utils import Parser

# ==========================================
# 1. BASIC PROGRAMS (6)
# ==========================================
def test_001():
    """Empty main"""
    source = "void main() {}"
    assert Parser(source).parse() == "success"

def test_002():
    """Main returns int"""
    source = "int main() { return 0; }"
    assert Parser(source).parse() == "success"

def test_003():
    """Implicit return type"""
    source = "main() { }"
    assert Parser(source).parse() == "success"

def test_004():
    """Empty statement (invalid)"""
    source = "void main() { ; }"
    assert Parser(source).parse() == "Error on line 1 col 14: ;"

def test_005():
    """Nested empty block"""
    source = "void main() { {} }"
    assert Parser(source).parse() == "success"

def test_006():
    """Deep nested block"""
    source = "void main() { {{}} }"
    assert Parser(source).parse() == "success"


# ==========================================
# 2. DECLARATIONS (5)
# ==========================================
def test_007():
    """Auto declaration"""
    source = "void main() { auto x; }"
    assert Parser(source).parse() == "success"

def test_008():
    """Int declaration"""
    source = "void main() { int x; }"
    assert Parser(source).parse() == "success"

def test_009():
    """String declaration"""
    source = "void main() { string s; }"
    assert Parser(source).parse() == "success"

def test_010():
    """Float declaration"""
    source = "void main() { float f; }"
    assert Parser(source).parse() == "success"

def test_011():
    """Void variable (invalid)"""
    source = "void main() { void x; }"
    assert Parser(source).parse() == "Error on line 1 col 14: void"


# ==========================================
# 3. UNARY EXPRESSIONS (5)
# ==========================================
def test_012():
    """Unary minus"""
    source = "void main() { auto x = -1; }"
    assert Parser(source).parse() == "success"

def test_013():
    """Unary plus"""
    source = "void main() { auto x = +1; }"
    assert Parser(source).parse() == "success"

def test_014():
    """Logical not"""
    source = "void main() { auto x = !1; }"
    assert Parser(source).parse() == "success"

def test_015():
    """Double logical not"""
    source = "void main() { auto x = !!1; }"
    assert Parser(source).parse() == "success"

def test_016():
    """Invalid unary chain"""
    source = "void main() { auto x = !; }"
    assert Parser(source).parse() == "Error on line 1 col 24: ;"


# ==========================================
# 4. ARITHMETIC (4)
# ==========================================
def test_017():
    """Operator precedence"""
    source = "void main() { auto x = 1 + 2 * 3; }"
    assert Parser(source).parse() == "success"

def test_018():
    """Parentheses override"""
    source = "void main() { auto x = (1 + 2) * 3; }"
    assert Parser(source).parse() == "success"

def test_019():
    """Chained comparison"""
    source = "void main() { auto x = 1 < 2 == 1; }"
    assert Parser(source).parse() == "success"

def test_020():
    """Invalid comparison"""
    source = "void main() { auto x = < 2; }"
    assert Parser(source).parse() == "Error on line 1 col 23: <"


# ==========================================
# 5. LOGICAL (3)
# ==========================================
def test_021():
    """Logical precedence"""
    source = "void main() { auto x = 1 && 0 || 1; }"
    assert Parser(source).parse() == "success"

def test_022():
    """Logical with parentheses"""
    source = "void main() { auto x = (1 && 0) || 1; }"
    assert Parser(source).parse() == "success"

def test_023():
    """Invalid logical"""
    source = "void main() { auto x = && 1; }"
    assert Parser(source).parse() == "Error on line 1 col 23: &&"


# ==========================================
# 6. INC / DEC (3)
# ==========================================
def test_024():
    """Prefix increment"""
    source = "void main() { auto x = 0; ++x; }"
    assert Parser(source).parse() == "success"

def test_025():
    """Postfix increment"""
    source = "void main() { auto x = 0; x++; }"
    assert Parser(source).parse() == "success"

def test_026():
    """Invalid increment"""
    source = "void main() { ++; }"
    assert Parser(source).parse() == "Error on line 1 col 16: ;"


# ==========================================
# 7. WHILE (3)
# ==========================================
def test_027():
    """While empty body"""
    source = "void main() { while (1) {} }"
    assert Parser(source).parse() == "success"

def test_028():
    """While empty stmt"""
    source = "void main() { while (0) ; }"
    assert Parser(source).parse() == "Error on line 1 col 24: ;"

def test_029():
    """Malformed while"""
    source = "void main() { while 1 {} }"
    assert Parser(source).parse() == "Error on line 1 col 20: 1"


# ==========================================
# 8. FOR (3)
# ==========================================
def test_030():
    """Classic for"""
    source = "void main() { for (auto i=0; i<10; i++) {} }"
    assert Parser(source).parse() == "success"

def test_031():
    """For missing semicolon"""
    source = "void main() { for (auto i=0 i<10; i++) {} }"
    assert Parser(source).parse() == "Error on line 1 col 28: i"

def test_032():
    """For infinite"""
    source = "void main() { for (;;) {} }"
    assert Parser(source).parse() == "success"


# ==========================================
# 9. IF (4)
# ==========================================
def test_033():
    """Simple if"""
    source = "void main() { if (1) {} }"
    assert Parser(source).parse() == "success"

def test_034():
    """If else"""
    source = "void main() { if (1) {} else {} }"
    assert Parser(source).parse() == "success"

def test_035():
    """Dangling else"""
    source = "void main() { if (1) if (0) {} else {} }"
    assert Parser(source).parse() == "success"

def test_036():
    """Malformed if"""
    source = "void main() { if 1 {} }"
    assert Parser(source).parse() == "Error on line 1 col 17: 1"


# ==========================================
# 10. JUMP (3)
# ==========================================
def test_037():
    """Break"""
    source = "void main() { while (1) break; }"
    assert Parser(source).parse() == "success"

def test_038():
    """Continue"""
    source = "void main() { for (;;) continue; }"
    assert Parser(source).parse() == "success"

def test_039():
    """Break outside loop"""
    source = "void main() { break; }"
    # Parser is syntactically permissive; semantic check (break outside loop) should be handled later
    assert Parser(source).parse() == "success"


# ==========================================
# 11. FUNCTIONS (3)
# ==========================================
def test_040():
    """Void function"""
    source = "void foo() {} void main() {}"
    assert Parser(source).parse() == "success"

def test_041():
    """Function call"""
    source = "void foo() {} void main() { foo(); }"
    assert Parser(source).parse() == "success"

def test_042():
    """Invalid function call"""
    source = "void main() { foo(,); }"
    assert Parser(source).parse() == "Error on line 1 col 18: ,"


# ==========================================
# 12. STRUCT (3)
# ==========================================
def test_043():
    """Struct decl"""
    source = "struct S { int x; }; void main() {}"
    assert Parser(source).parse() == "success"

def test_044():
    """Struct usage"""
    source = "struct S { int x; }; void main() { S s; }"
    assert Parser(source).parse() == "success"

def test_045():
    """Struct missing semicolon"""
    source = "struct S { int x; } void main() {}"
    assert Parser(source).parse() == "Error on line 1 col 20: void"


# ==========================================
# 13. ASSIGN (2)
# ==========================================
def test_046():
    """Assignment"""
    source = "void main() { auto x = 1; x = x + 1; }"
    assert Parser(source).parse() == "success"

def test_047():
    """Assign to literal"""
    source = "void main() { 1 = x; }"
    assert Parser(source).parse() == "Error on line 1 col 16: ="


# ==========================================
# 14. IO (2)
# ==========================================
def test_048():
    """Read int"""
    source = "void main() { auto x = readInt(); }"
    assert Parser(source).parse() == "success"

def test_049():
    """Print int"""
    source = "void main() { printInt(1); }"
    assert Parser(source).parse() == "success"


# ==========================================
# 15. FINAL STRESS (1)
# ==========================================
def test_050():
    """Complex program"""
    source = """
    int fact(int n) {
        if (n <= 1) return 1;
        else return n * fact(n - 1);
    }
    void main() {
        int r = fact(5);
    }
    """
    assert Parser(source).parse() == "success"


# ==========================================
# 16. ERROR HANDLING (30)
# ==========================================
def test_051():
    """Missing closing brace"""
    source = "void main() {"
    assert Parser(source).parse() == "Error on line 1 col 13: <EOF>"

def test_052():
    """Extra closing brace"""
    source = "void main() {}}"
    assert Parser(source).parse() == "Error on line 1 col 14: }"

def test_053():
    """Missing parentheses in main"""
    source = "void main { }"
    assert Parser(source).parse() == "Error on line 1 col 10: {"

def test_054():
    """Empty if condition"""
    source = "void main() { if () {} }"
    assert Parser(source).parse() == "Error on line 1 col 18: )"

def test_055():
    """If without parentheses"""
    source = "void main() { if 1 {} }"
    assert Parser(source).parse() == "Error on line 1 col 17: 1"

def test_056():
    """Else without if"""
    source = "void main() { else {} }"
    assert Parser(source).parse() == "Error on line 1 col 14: else"

def test_057():
    """While without parentheses"""
    source = "void main() { while 1 {} }"
    assert Parser(source).parse() == "Error on line 1 col 20: 1"

def test_058():
    """While missing body"""
    source = "void main() { while (1) }"
    assert Parser(source).parse() == "Error on line 1 col 24: }"

def test_059():
    """Dangling binary operator"""
    source = "void main() { auto x = 1 + ; }"
    assert Parser(source).parse() == "Error on line 1 col 27: ;"

def test_060():
    """Double binary operator"""
    source = "void main() { auto x = 1 * * 2; }"
    assert Parser(source).parse() == "Error on line 1 col 27: *"

def test_061():
    """For missing semicolons"""
    source = "void main() { for (i=0 i<10 i++) {} }"
    assert Parser(source).parse() == "Error on line 1 col 23: i"

def test_062():
    """For missing condition expression"""
    source = "void main() { for (i=0;;i++) {} }"
    # Empty condition is syntactically allowed (infinite loop)
    assert Parser(source).parse() == "success"

def test_063():
    """For missing increment part"""
    source = "void main() { for (i=0;i<10) {} }"
    assert Parser(source).parse() == "Error on line 1 col 27: )"

def test_064():
    """Assignment without lhs"""
    source = "void main() { = 1; }"
    assert Parser(source).parse() == "Error on line 1 col 14: ="

def test_065():
    """Assignment without rhs"""
    source = "void main() { x = ; }"
    assert Parser(source).parse() == "Error on line 1 col 18: ;"

def test_066():
    """Unary operator without operand"""
    source = "void main() { auto x = !; }"
    assert Parser(source).parse() == "Error on line 1 col 24: ;"

def test_067():
    """Increment literal"""
    source = "void main() { 1++; }"
    # Parser should report the unexpected '++' token at its position
    assert Parser(source).parse() == "Error on line 1 col 15: ++"

def test_068():
    """Decrement literal"""
    source = "void main() { --1; }"
    # Parser currently reports the unexpected token at the following position
    assert Parser(source).parse() == "Error on line 1 col 17: ;"

def test_069():
    """Call literal as function"""
    source = "void main() { 1(); }"
    assert Parser(source).parse() == "Error on line 1 col 15: ("

def test_070():
    """Function call missing closing parenthesis"""
    source = "void main() { foo(1, 2; }"
    assert Parser(source).parse() == "Error on line 1 col 22: ;"

def test_071():
    """Function call missing comma"""
    source = "void main() { foo(1 2); }"
    assert Parser(source).parse() == "Error on line 1 col 20: 2"

def test_072():
    """Trailing comma in argument list"""
    source = "void main() { foo(1,); }"
    assert Parser(source).parse() == "Error on line 1 col 20: )"

def test_073():
    """Return value in void function"""
    source = "void main() { return 1; }"
    # Semantic error (returning value from void) should be reported during semantic analysis
    assert Parser(source).parse() == "success"

def test_074():
    """Return missing semicolon"""
    source = "void main() { return }"
    assert Parser(source).parse() == "Error on line 1 col 21: }"

def test_075():
    """Break outside loop"""
    source = "void main() { break; }"
    # Syntactically allowed; semantic checks should reject break outside loop later
    assert Parser(source).parse() == "success"

def test_076():
    """Continue outside loop"""
    source = "void main() { continue; }"
    # Syntactically allowed; semantic checks should reject continue outside loop later
    assert Parser(source).parse() == "success"

def test_077():
    """Struct missing semicolon"""
    source = "struct S { int x; } void main() {}"
    assert Parser(source).parse() == "Error on line 1 col 20: void"

def test_078():
    """Struct declared inside function"""
    source = "void main() { struct S { int x; }; }"
    assert Parser(source).parse() == "Error on line 1 col 14: struct"

def test_079():
    """Parameter missing type"""
    source = "void foo(x) {}"
    # Parser reports missing parameter name/type at the closing parenthesis
    assert Parser(source).parse() == "Error on line 1 col 10: )"

def test_080():
    """Parameter missing name"""
    source = "void foo(int) {}"
    assert Parser(source).parse() == "Error on line 1 col 12: )"


# ==========================================
# 17. MULTI-LINE PARSER TESTS (20)
# ==========================================
def test_081():
    """Valid nested blocks"""
    source = """
void main() {
    {
        {
            auto x = 1;
        }
    }
}
"""
    assert Parser(source).parse() == "success"

def test_082():
    """Valid if-else chain"""
    source = """
void main() {
    if (1) {
        auto x = 1;
    } else {
        auto y = 2;
    }
}
"""
    assert Parser(source).parse() == "success"

def test_083():
    """Missing closing brace (EOF)"""
    source = """
void main() {
    auto x = 1;
    if (x) {
        x = x + 1;
}
"""
    assert Parser(source).parse() == "Error on line 7 col 0: <EOF>"

def test_084():
    """If with empty condition"""
    source = """
void main() {
    if () {
        return;
    }
}
"""
    assert Parser(source).parse() == "Error on line 3 col 8: )"

def test_085():
    """While without body"""
    source = """
void main() {
    while (1)
}
"""
    assert Parser(source).parse() == "Error on line 4 col 0: }"

def test_086():
    """Broken expression across lines"""
    source = """
void main() {
    auto x = 1 +
    ;
}
"""
    assert Parser(source).parse() == "Error on line 4 col 4: ;"

def test_087():
    """Valid for-loop with block"""
    source = """
void main() {
    for (auto i = 0; i < 10; i++) {
        printInt(i);
    }
}
"""
    assert Parser(source).parse() == "success"

def test_088():
    """For loop missing condition"""
    source = """
void main() {
    for (auto i = 0; ; i++) {
        i++;
    }
}
"""
    # Empty condition is syntactically allowed (infinite loop)
    assert Parser(source).parse() == "success"

def test_089():
    """Return value in void function"""
    source = """
void main() {
    return
        1;
}
"""
    # Syntactically allowed; semantic check should detect returning a value in void
    assert Parser(source).parse() == "success"

def test_090():
    """Valid early return in int function"""
    source = """
int main() {
    if (1) {
        return 1;
    }
    return 0;
}
"""
    assert Parser(source).parse() == "success"

def test_091():
    """Nested function declaration"""
    source = """
void main() {
    void foo() {
    }
}
"""
    assert Parser(source).parse() == "Error on line 3 col 4: void"

def test_092():
    """Struct declared inside function"""
    source = """
void main() {
    struct S {
        int x;
    };
}
"""
    assert Parser(source).parse() == "Error on line 3 col 4: struct"

def test_093():
    """Valid struct and usage"""
    source = """
struct S {
    int x;
};
void main() {
    S s;
}
"""
    assert Parser(source).parse() == "success"

def test_094():
    """Unclosed parenthesis"""
    source = """
void main() {
    auto x = (1 + 2;
}
"""
    assert Parser(source).parse() == "Error on line 3 col 19: ;"


def test_095():
    """Else without matching if"""
    source = """
void main() {
    else {
        auto x = 1;
    }
}
"""
    assert Parser(source).parse() == "Error on line 3 col 4: else"

def test_096():
    """Break outside loop"""
    source = """
void main() {
    break;
}
"""
    # Syntactically allowed; should be caught by semantic checks
    assert Parser(source).parse() == "success"

def test_097():
    """Valid while with continue"""
    source = """
void main() {
    while (1) {
        continue;
    }
}
"""
    assert Parser(source).parse() == "success"

def test_098():
    """Dangling binary operator"""
    source = """
void main() {
    auto x = 1 +
}
"""
    assert Parser(source).parse() == "Error on line 4 col 0: }"

def test_099():
    """Invalid assignment target"""
    source = """
void main() {
    1 = 2;
}
"""
    assert Parser(source).parse() == "Error on line 3 col 6: ="

def test_100():
    """Garbage token inside block"""
    source = """
void main() {
    @@@
}
"""
    # Lexer raises ErrorToken for invalid character
    assert Parser(source).parse() == "Error Token @"





'''
# ========== Simple Test Cases (10 types) ==========
def test_empty_program():
    """1. Empty program"""
    assert Parser("").parse() == "success"


def test_program_with_only_main():
    """2. Program with only main function"""
    assert Parser("void main() {}").parse() == "success"


def test_struct_simple():
    """3. Struct declaration"""
    source = "struct Point { int x; int y; };"
    assert Parser(source).parse() == "success"


def test_function_no_params():
    """4. Function with no parameters"""
    source = "void greet() { printString(\"Hello\"); }"
    assert Parser(source).parse() == "success"


def test_var_decl_auto_with_init():
    """5. Variable declaration"""
    source = "void main() { auto x = 5; }"
    assert Parser(source).parse() == "success"


def test_if_simple():
    """6. If statement"""
    source = "void main() { if (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_while_simple():
    """7. While statement"""
    source = "void main() { while (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_for_simple():
    """8. For statement"""
    source = "void main() { for (auto i = 0; i < 10; ++i) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_switch_simple():
    """9. Switch statement"""
    source = "void main() { switch (1) { case 1: printInt(1); break; } }"
    assert Parser(source).parse() == "success"


def test_assignment_simple():
    """10. Assignment statement"""
    source = "void main() { int x; x = 5; }"
    assert Parser(source).parse() == "success"
'''