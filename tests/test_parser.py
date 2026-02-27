"""
Parser test cases for TyC compiler
TODO: Implement 100 test cases for parser
"""

import pytest
from tests.utils import Parser

# ==========================================
# 1. BASIC PROGRAMS (6)
# ==========================================
def test_parser_001():
    """Empty main"""
    source = "void main() {}"
    assert Parser(source).parse() == "success"

def test_parser_002():
    """Main returns int"""
    source = "int main() { return 0; }"
    assert Parser(source).parse() == "success"

def test_parser_003():
    """Implicit return type"""
    source = "main() { }"
    assert Parser(source).parse() == "success"

def test_parser_004():
    """Empty statement (invalid)"""
    source = "void main() { ; }"
    assert Parser(source).parse() == "Error on line 1 col 14: ;"

def test_parser_005():
    """Nested empty block"""
    source = "void main() { {} }"
    assert Parser(source).parse() == "success"

def test_parser_006():
    """Deep nested block"""
    source = "void main() { {{}} }"
    assert Parser(source).parse() == "success"


# ==========================================
# 2. DECLARATIONS (5)
# ==========================================
def test_parser_007():
    """Auto declaration"""
    source = "void main() { auto x; }"
    assert Parser(source).parse() == "success"

def test_parser_008():
    """Int declaration"""
    source = "void main() { int x; }"
    assert Parser(source).parse() == "success"

def test_parser_009():
    """String declaration"""
    source = "void main() { string s; }"
    assert Parser(source).parse() == "success"

def test_parser_010():
    """Float declaration"""
    source = "void main() { float f; }"
    assert Parser(source).parse() == "success"

def test_parser_011():
    """Void variable (invalid)"""
    source = "void main() { void x; }"
    assert Parser(source).parse() == "Error on line 1 col 14: void"


# ==========================================
# 3. UNARY EXPRESSIONS (5)
# ==========================================
def test_parser_012():
    """Unary minus"""
    source = "void main() { auto x = -1; }"
    assert Parser(source).parse() == "success"

def test_parser_013():
    """Unary plus"""
    source = "void main() { auto x = +1; }"
    assert Parser(source).parse() == "success"

def test_parser_014():
    """Logical not"""
    source = "void main() { auto x = !1; }"
    assert Parser(source).parse() == "success"

def test_parser_015():
    """Double logical not"""
    source = "void main() { auto x = !!1; }"
    assert Parser(source).parse() == "success"

def test_parser_016():
    """Invalid unary chain"""
    source = "void main() { auto x = !; }"
    assert Parser(source).parse() == "Error on line 1 col 24: ;"


# ==========================================
# 4. ARITHMETIC (4)
# ==========================================
def test_parser_017():
    """Operator precedence"""
    source = "void main() { auto x = 1 + 2 * 3; }"
    assert Parser(source).parse() == "success"

def test_parser_018():
    """Parentheses override"""
    source = "void main() { auto x = (1 + 2) * 3; }"
    assert Parser(source).parse() == "success"

def test_parser_019():
    """Chained comparison"""
    source = "void main() { auto x = 1 < 2 == 1; }"
    assert Parser(source).parse() == "success"

def test_parser_020():
    """Invalid comparison"""
    source = "void main() { auto x = < 2; }"
    assert Parser(source).parse() == "Error on line 1 col 23: <"


# ==========================================
# 5. LOGICAL (3)
# ==========================================
def test_parser_021():
    """Logical precedence"""
    source = "void main() { auto x = 1 && 0 || 1; }"
    assert Parser(source).parse() == "success"

def test_parser_022():
    """Logical with parentheses"""
    source = "void main() { auto x = (1 && 0) || 1; }"
    assert Parser(source).parse() == "success"

def test_parser_023():
    """Invalid logical"""
    source = "void main() { auto x = && 1; }"
    assert Parser(source).parse() == "Error on line 1 col 23: &&"


# ==========================================
# 6. INC / DEC (3)
# ==========================================
def test_parser_024():
    """Prefix increment"""
    source = "void main() { auto x = 0; ++x; }"
    assert Parser(source).parse() == "success"

def test_parser_025():
    """Postfix increment"""
    source = "void main() { auto x = 0; x++; }"
    assert Parser(source).parse() == "success"

def test_parser_026():
    """Invalid increment"""
    source = "void main() { ++; }"
    assert Parser(source).parse() == "Error on line 1 col 16: ;"


# ==========================================
# 7. WHILE (3)
# ==========================================
def test_parser_027():
    """While empty body"""
    source = "void main() { while (1) {} }"
    assert Parser(source).parse() == "success"

def test_parser_028():
    """While empty stmt"""
    source = "void main() { while (0) ; }"
    assert Parser(source).parse() == "Error on line 1 col 24: ;"

def test_parser_029():
    """Malformed while"""
    source = "void main() { while 1 {} }"
    assert Parser(source).parse() == "Error on line 1 col 20: 1"


# ==========================================
# 8. FOR (3)
# ==========================================
def test_parser_030():
    """Classic for"""
    source = "void main() { for (auto i=0; i<10; i++) {} }"
    assert Parser(source).parse() == "success"

def test_parser_031():
    """For missing semicolon"""
    source = "void main() { for (auto i=0 i<10; i++) {} }"
    assert Parser(source).parse() == "Error on line 1 col 28: i"

def test_parser_032():
    """For infinite"""
    source = "void main() { for (;;) {} }"
    assert Parser(source).parse() == "success"


# ==========================================
# 9. IF (4)
# ==========================================
def test_parser_033():
    """Simple if"""
    source = "void main() { if (1) {} }"
    assert Parser(source).parse() == "success"

def test_parser_034():
    """If else"""
    source = "void main() { if (1) {} else {} }"
    assert Parser(source).parse() == "success"

def test_parser_035():
    """Dangling else"""
    source = "void main() { if (1) if (0) {} else {} }"
    assert Parser(source).parse() == "success"

def test_parser_036():
    """Malformed if"""
    source = "void main() { if 1 {} }"
    assert Parser(source).parse() == "Error on line 1 col 17: 1"


# ==========================================
# 10. JUMP (3)
# ==========================================
def test_parser_037():
    """Break"""
    source = "void main() { while (1) break; }"
    assert Parser(source).parse() == "success"

def test_parser_038():
    """Continue"""
    source = "void main() { for (;;) continue; }"
    assert Parser(source).parse() == "success"

def test_parser_039():
    """Break outside loop"""
    source = "void main() { break; }"
    # Parser is syntactically permissive; semantic check (break outside loop) should be handled later
    assert Parser(source).parse() == "success"


# ==========================================
# 11. FUNCTIONS (3)
# ==========================================
def test_parser_040():
    """Void function"""
    source = "void foo() {} void main() {}"
    assert Parser(source).parse() == "success"

def test_parser_041():
    """Function call"""
    source = "void foo() {} void main() { foo(); }"
    assert Parser(source).parse() == "success"

def test_parser_042():
    """Invalid function call"""
    source = "void main() { foo(,); }"
    assert Parser(source).parse() == "Error on line 1 col 18: ,"


# ==========================================
# 12. STRUCT (3)
# ==========================================
def test_parser_043():
    """Struct decl"""
    source = "struct S { int x; }; void main() {}"
    assert Parser(source).parse() == "success"

def test_parser_044():
    """Struct usage"""
    source = "struct S { int x; }; void main() { S s; }"
    assert Parser(source).parse() == "success"

def test_parser_045():
    """Struct missing semicolon"""
    source = "struct S { int x; } void main() {}"
    assert Parser(source).parse() == "Error on line 1 col 20: void"


# ==========================================
# 13. ASSIGN (2)
# ==========================================
def test_parser_046():
    """Assignment"""
    source = "void main() { auto x = 1; x = x + 1; }"
    assert Parser(source).parse() == "success"

def test_parser_047():
    """Assign to literal"""
    source = "void main() { 1 = x; }"
    assert Parser(source).parse() == "Error on line 1 col 16: ="


# ==========================================
# 14. IO (2)
# ==========================================
def test_parser_048():
    """Read int"""
    source = "void main() { auto x = readInt(); }"
    assert Parser(source).parse() == "success"

def test_parser_049():
    """Print int"""
    source = "void main() { printInt(1); }"
    assert Parser(source).parse() == "success"


# ==========================================
# 15. FINAL STRESS (1)
# ==========================================
def test_parser_050():
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
def test_parser_051():
    """Missing closing brace"""
    source = "void main() {"
    assert Parser(source).parse() == "Error on line 1 col 13: <EOF>"

def test_parser_052():
    """Extra closing brace"""
    source = "void main() {}}"
    assert Parser(source).parse() == "Error on line 1 col 14: }"

def test_parser_053():
    """Missing parentheses in main"""
    source = "void main { }"
    assert Parser(source).parse() == "Error on line 1 col 10: {"

def test_parser_054():
    """Empty if condition"""
    source = "void main() { if () {} }"
    assert Parser(source).parse() == "Error on line 1 col 18: )"

def test_parser_055():
    """If without parentheses"""
    source = "void main() { if 1 {} }"
    assert Parser(source).parse() == "Error on line 1 col 17: 1"

def test_parser_056():
    """Else without if"""
    source = "void main() { else {} }"
    assert Parser(source).parse() == "Error on line 1 col 14: else"

def test_parser_057():
    """While without parentheses"""
    source = "void main() { while 1 {} }"
    assert Parser(source).parse() == "Error on line 1 col 20: 1"

def test_parser_058():
    """While missing body"""
    source = "void main() { while (1) }"
    assert Parser(source).parse() == "Error on line 1 col 24: }"

def test_parser_059():
    """Dangling binary operator"""
    source = "void main() { auto x = 1 + ; }"
    assert Parser(source).parse() == "Error on line 1 col 27: ;"

def test_parser_060():
    """Double binary operator"""
    source = "void main() { auto x = 1 * * 2; }"
    assert Parser(source).parse() == "Error on line 1 col 27: *"

def test_parser_061():
    """For missing semicolons"""
    source = "void main() { for (i=0 i<10 i++) {} }"
    assert Parser(source).parse() == "Error on line 1 col 23: i"

def test_parser_062():
    """For missing condition expression"""
    source = "void main() { for (i=0;;i++) {} }"
    # Empty condition is syntactically allowed (infinite loop)
    assert Parser(source).parse() == "success"

def test_parser_063():
    """For missing increment part"""
    source = "void main() { for (i=0;i<10) {} }"
    assert Parser(source).parse() == "Error on line 1 col 27: )"

def test_parser_064():
    """Assignment without lhs"""
    source = "void main() { = 1; }"
    assert Parser(source).parse() == "Error on line 1 col 14: ="

def test_parser_065():
    """Assignment without rhs"""
    source = "void main() { x = ; }"
    assert Parser(source).parse() == "Error on line 1 col 18: ;"

def test_parser_066():
    """Unary operator without operand"""
    source = "void main() { auto x = !; }"
    assert Parser(source).parse() == "Error on line 1 col 24: ;"

def test_parser_067():
    """Increment literal"""
    source = "void main() { 1++; }"
    # Parser accepts the syntax; semantic analysis validates if it's a valid lvalue
    assert Parser(source).parse() == "success"

def test_parser_068():
    """Decrement literal"""
    source = "void main() { --1; }"
    # Parser accepts the syntax; semantic analysis validates if it's a valid lvalue
    assert Parser(source).parse() == "success"

def test_parser_069():
    """Call literal as function"""
    source = "void main() { 1(); }"
    assert Parser(source).parse() == "Error on line 1 col 15: ("

def test_parser_070():
    """Function call missing closing parenthesis"""
    source = "void main() { foo(1, 2; }"
    assert Parser(source).parse() == "Error on line 1 col 22: ;"

def test_parser_071():
    """Function call missing comma"""
    source = "void main() { foo(1 2); }"
    assert Parser(source).parse() == "Error on line 1 col 20: 2"

def test_parser_072():
    """Trailing comma in argument list"""
    source = "void main() { foo(1,); }"
    assert Parser(source).parse() == "Error on line 1 col 20: )"

def test_parser_073():
    """Return value in void function"""
    source = "void main() { return 1; }"
    # Semantic error (returning value from void) should be reported during semantic analysis
    assert Parser(source).parse() == "success"

def test_parser_074():
    """Return missing semicolon"""
    source = "void main() { return }"
    assert Parser(source).parse() == "Error on line 1 col 21: }"

def test_parser_075():
    """Break outside loop"""
    source = "void main() { break; }"
    # Syntactically allowed; semantic checks should reject break outside loop later
    assert Parser(source).parse() == "success"

def test_parser_076():
    """Continue outside loop"""
    source = "void main() { continue; }"
    # Syntactically allowed; semantic checks should reject continue outside loop later
    assert Parser(source).parse() == "success"

def test_parser_077():
    """Struct missing semicolon"""
    source = "struct S { int x; } void main() {}"
    assert Parser(source).parse() == "Error on line 1 col 20: void"

def test_parser_078():
    """Struct declared inside function"""
    source = "void main() { struct S { int x; }; }"
    assert Parser(source).parse() == "Error on line 1 col 14: struct"

def test_parser_079():
    """Parameter missing type"""
    source = "void foo(x) {}"
    # Parser reports missing parameter name/type at the closing parenthesis
    assert Parser(source).parse() == "Error on line 1 col 10: )"

def test_parser_080():
    """Parameter missing name"""
    source = "void foo(int) {}"
    assert Parser(source).parse() == "Error on line 1 col 12: )"


# ==========================================
# 17. MULTI-LINE PARSER TESTS (20)
# ==========================================
def test_parser_081():
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

def test_parser_082():
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

def test_parser_083():
    """Missing closing brace (EOF)"""
    source = """
void main() {
    auto x = 1;
    if (x) {
        x = x + 1;
}
"""
    assert Parser(source).parse() == "Error on line 7 col 0: <EOF>"

def test_parser_084():
    """If with empty condition"""
    source = """
void main() {
    if () {
        return;
    }
}
"""
    assert Parser(source).parse() == "Error on line 3 col 8: )"

def test_parser_085():
    """While without body"""
    source = """
void main() {
    while (1)
}
"""
    assert Parser(source).parse() == "Error on line 4 col 0: }"

def test_parser_086():
    """Broken expression across lines"""
    source = """
void main() {
    auto x = 1 +
    ;
}
"""
    assert Parser(source).parse() == "Error on line 4 col 4: ;"

def test_parser_087():
    """Valid for-loop with block"""
    source = """
void main() {
    for (auto i = 0; i < 10; i++) {
        printInt(i);
    }
}
"""
    assert Parser(source).parse() == "success"

def test_parser_088():
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

def test_parser_089():
    """Return value in void function"""
    source = """
void main() {
    return
        1;
}
"""
    # Syntactically allowed; semantic check should detect returning a value in void
    assert Parser(source).parse() == "success"

def test_parser_090():
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

def test_parser_091():
    """Nested function declaration"""
    source = """
void main() {
    void foo() {
    }
}
"""
    assert Parser(source).parse() == "Error on line 3 col 4: void"

def test_parser_092():
    """Struct declared inside function"""
    source = """
void main() {
    struct S {
        int x;
    };
}
"""
    assert Parser(source).parse() == "Error on line 3 col 4: struct"

def test_parser_093():
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

def test_parser_094():
    """Unclosed parenthesis"""
    source = """
void main() {
    auto x = (1 + 2;
}
"""
    assert Parser(source).parse() == "Error on line 3 col 19: ;"


def test_parser_095():
    """Else without matching if"""
    source = """
void main() {
    else {
        auto x = 1;
    }
}
"""
    assert Parser(source).parse() == "Error on line 3 col 4: else"

def test_parser_096():
    """Break outside loop"""
    source = """
void main() {
    break;
}
"""
    # Syntactically allowed; should be caught by semantic checks
    assert Parser(source).parse() == "success"

def test_parser_097():
    """Valid while with continue"""
    source = """
void main() {
    while (1) {
        continue;
    }
}
"""
    assert Parser(source).parse() == "success"

def test_parser_098():
    """Dangling binary operator"""
    source = """
void main() {
    auto x = 1 +
}
"""
    assert Parser(source).parse() == "Error on line 4 col 0: }"

def test_parser_099():
    """Invalid assignment target"""
    source = """
void main() {
    1 = 2;
}
"""
    assert Parser(source).parse() == "Error on line 3 col 6: ="

def test_parser_100():
    """Garbage token inside block"""
    source = """
void main() {
    @@@
}
"""
    # Lexer raises ErrorToken for invalid character
    assert Parser(source).parse() == "Error Token @"

# Additional tests covering missing scenarios

def test_parser_101():
    """Empty struct declaration"""
    source = "struct Empty {}; void main() {}"
    assert Parser(source).parse() == "success"


def test_parser_102():
    """Struct containing another struct type"""
    source = "struct B { int x; }; struct A { B b; }; void main() {}"
    assert Parser(source).parse() == "success"


def test_parser_103():
    """Self-referencing struct (syntax only)"""
    source = "struct Node { Node next; }; void main() {}"
    assert Parser(source).parse() == "success"


def test_parser_104():
    """Struct member with auto (invalid)"""
    source = "struct S { auto x; };"
    assert Parser(source).parse() == "Error on line 1 col 11: auto"


def test_parser_105():
    """Struct member with initializer (invalid)"""
    source = "struct S { int x = 0; };"
    assert Parser(source).parse() == "Error on line 1 col 17: ="


def test_parser_106():
    """Function with parameters and explicit types"""
    source = "int add(int a, float b) {}"
    assert Parser(source).parse() == "success"


def test_parser_107():
    """Function with inferred return type"""
    source = "foo() { return 1; }"
    assert Parser(source).parse() == "success"


def test_parser_108():
    """Function returning and accepting struct types"""
    source = "struct S { int x; }; S f(S s) {} void main() {}"
    assert Parser(source).parse() == "success"


def test_parser_109():
    """Auto as return type (invalid)"""
    source = "auto foo() {}"
    assert Parser(source).parse() == "Error on line 1 col 0: auto"


def test_parser_110():
    """Auto as parameter type (invalid)"""
    source = "void f(auto x) {}"
    assert Parser(source).parse() == "Error on line 1 col 7: auto"


def test_parser_111():
    """Trailing comma in parameter list (invalid)"""
    source = "void foo(int x, ) {}"
    assert Parser(source).parse() == "Error on line 1 col 16: )"


def test_parser_112():
    """Prototype only (no body)"""
    source = "void foo();"
    assert Parser(source).parse() == "Error on line 1 col 10: ;"


def test_parser_113():
    """Global variable declaration is not allowed"""
    source = "int x;"
    assert Parser(source).parse() == "Error on line 1 col 5: ;"


def test_parser_114():
    """Struct variable with literal initializer"""
    source = "struct P { int x; }; void main(){ P p = {1,2}; }"
    assert Parser(source).parse() == "success"


def test_parser_115():
    """Nested struct literal initialization"""
    source = "struct P { int x; }; struct Q { P p; int y; }; void main(){ Q q = {{1},2}; }"
    assert Parser(source).parse() == "success"


def test_parser_116():
    """Auto variable initialized with struct literal"""
    source = "struct P { int x; }; void main(){ auto q = {1}; }"
    assert Parser(source).parse() == "success"


def test_parser_117():
    """Struct initialization with expressions"""
    source = "struct P { int x; int y; }; void main(){ P p = {1+2, 3*4}; }"
    assert Parser(source).parse() == "success"


def test_parser_118():
    """String operands allowed in arithmetic (syntax)"""
    source = "void main(){ auto x = \"a\" + \"b\"; }"
    assert Parser(source).parse() == "success"


def test_parser_119():
    """For loop with literal init (grammar allows but semantic later?)"""
    source = "void main(){ for (3;1;) {} }"
    # parser accepts it; semantic analyzer should reject later
    assert Parser(source).parse() == "success"


def test_parser_120():
    """Empty switch"""
    source = "void main(){ switch (1) {} }"
    assert Parser(source).parse() == "success"


def test_parser_121():
    """Single case with break"""
    source = "void main(){ switch (1){ case 1: break; } }"
    assert Parser(source).parse() == "success"


def test_parser_122():
    """Multiple cases with default"""
    source = "void main(){ switch (1){ case 1: break; case 2: break; default: break; } }"
    assert Parser(source).parse() == "success"


def test_parser_123():
    """Case with constant expression negative, positive"""
    source = "void main(){ switch (1){ case -1: break; case +5: break; } }"
    assert Parser(source).parse() == "success"


def test_parser_124():
    """Default only switch"""
    source = "void main(){ switch (1){ default: break; } }"
    assert Parser(source).parse() == "success"


def test_parser_125():
    """Error: case missing colon"""
    source = "void main(){ switch (1){ case 1 break; } }"
    assert Parser(source).parse() == "Error on line 1 col 32: break"


def test_parser_126():
    """Error: multiple default clauses"""
    source = "void main(){ switch (1){ default: break; default: break; } }"
    assert Parser(source).parse() == "Error on line 1 col 41: default"





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