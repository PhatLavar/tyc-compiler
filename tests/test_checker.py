"""
Test cases for TyC Static Semantic Checker

This module contains test cases for the static semantic checker.
100 test cases covering all error types and comprehensive scenarios.
"""

from tests.utils import Checker
from src.utils.nodes import (
    Program,
    FuncDecl,
    BlockStmt,
    VarDecl,
    AssignExpr,
    ExprStmt,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    Identifier,
    BinaryOp,
    MemberAccess,
    FuncCall,
    StructDecl,
    MemberDecl,
    Param,
    ReturnStmt,
)


# ============================================================================
# VALID PROGRAM (test_checker_001 - test_checker_005) ------------------------
# ============================================================================
def test_checker_001():
    """Valid basic program with explicit types"""
    source = """
void main() {
    int x = 5;
    int y = x + 1;
    printInt(y);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_002():
    """Valid program with auto type inference"""
    source = """
void main() {
    auto x = 10;
    auto y = 3.14;
    auto z = x + y;
    printFloat(z);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_003():
    """Valid function declaration and call"""
    source = """
int add(int a, int b) {
    return a + b;
}
void main() {
    int sum = add(5, 7);
    printInt(sum);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_004():
    """Valid struct declaration and usage"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p = {10, 20};
    p.x = 30;
    printInt(p.x);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_005():
    """Valid nested blocks with auto and built-in functions"""
    source = """
void main() {
    auto n = readInt();
    {
        auto sum = 0;
        for (int i = 0; i < n; i++) {
            sum = sum + i;
        }
        printInt(sum);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


# ============================================================================
# REDECLARED ERRORS (test_checker_006 - test_checker_015) --------------------
# ============================================================================
def test_checker_006():
    """Redeclared variable in the same block"""
    source = """
void main() {
    int x = 10;
    int x = 20;
}
"""
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected


def test_checker_007():
    """Redeclared parameter in function"""
    source = """
int sum(int a, int a) {
    return a + a;
}
"""
    expected = "Redeclared(Parameter, a)"
    assert Checker(source).check_from_source() == expected


def test_checker_008():
    """Redeclared function"""
    source = """
int foo() { return 1; }
int foo() { return 2; }
"""
    expected = "Redeclared(Function, foo)"
    assert Checker(source).check_from_source() == expected


def test_checker_009():
    """Redeclared struct"""
    source = """
struct Point { int x; };
struct Point { int y; };
void main() {}
"""
    expected = "Redeclared(Struct, Point)"
    assert Checker(source).check_from_source() == expected


def test_checker_010():
    """Redeclared member inside struct"""
    source = """
struct Point {
    int x;
    int x;
};
"""
    expected = "Redeclared(Member, x)"
    assert Checker(source).check_from_source() == expected


def test_checker_011():
    """Local variable reuses parameter name (not allowed)"""
    source = """
void func(int x) {
    int x = 100;
}
"""
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected


def test_checker_012():
    """Redeclared variable in nested block (same name as outer)"""
    source = """
void main() {
    int x = 5;
    {
        int x = 10;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_013():
    """Redeclared variable in different blocks (should be allowed)"""
    source = """
void main() {
    {
        int x = 1;
    }
    {
        int x = 2;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_014():
    """Redeclared global function and struct with same name (allowed)"""
    source = """
struct foo { int x; };
int foo(int x) { return x; }
void main() {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_015():
    """Multiple redeclared variables"""
    source = """
void main() {
    int a = 1;
    int b = 2;
    int a = 3;
}
"""
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected


# ============================================================================
# UNDECLARED IDENTIFIER (test_checker_016 - test_checker_025) ----------------
# ============================================================================
def test_checker_016():
    """Undeclared variable in assignment"""
    source = """
void main() {
    x = 10;
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected


def test_checker_017():
    """Undeclared variable in expression"""
    source = """
void main() {
    int y = x + 1;
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected


def test_checker_018():
    """Undeclared variable in function call argument"""
    source = """
void main() {
    printInt(x);
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected


def test_checker_019():
    """Undeclared variable in if condition"""
    source = """
void main() {
    if (x) {}
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected


def test_checker_020():
    """Undeclared variable in while condition"""
    source = """
void main() {
    while (x) {}
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected


def test_checker_021():
    """Undeclared variable in for loop"""
    source = """
void main() {
    for (int i = 0; i < x; i++) {}
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected


def test_checker_022():
    """Undeclared variable in return statement"""
    source = """
int func() {
    return x;
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected


def test_checker_023():
    """Undeclared variable in member access"""
    source = """
void main() {
    x.y = 10;
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected


def test_checker_024():
    """Undeclared variable in binary operation"""
    source = """
void main() {
    int z = y + 5;
}
"""
    expected = "UndeclaredIdentifier(y)"
    assert Checker(source).check_from_source() == expected


def test_checker_025():
    """Undeclared variable in prefix operation"""
    source = """
void main() {
    ++x;
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected


# ============================================================================
# UNDECLARED FUNCTION (test_checker_026 - test_checker_035) ------------------
# ============================================================================
def test_checker_026():
    """Undeclared function call"""
    source = """
void main() {
    foo();
}
"""
    expected = "UndeclaredFunction(foo)"
    assert Checker(source).check_from_source() == expected


def test_checker_027():
    """Undeclared function in assignment"""
    source = """
void main() {
    int x = bar();
}
"""
    expected = "UndeclaredFunction(bar)"
    assert Checker(source).check_from_source() == expected


def test_checker_028():
    """Undeclared function with arguments"""
    source = """
void main() {
    baz(1, 2);
}
"""
    expected = "UndeclaredFunction(baz)"
    assert Checker(source).check_from_source() == expected


def test_checker_029():
    """Undeclared function in expression"""
    source = """
void main() {
    int y = qux() + 5;
}
"""
    expected = "UndeclaredFunction(qux)"
    assert Checker(source).check_from_source() == expected


def test_checker_030():
    """Undeclared function in if condition"""
    source = """
void main() {
    if (test()) {}
}
"""
    expected = "UndeclaredFunction(test)"
    assert Checker(source).check_from_source() == expected


def test_checker_031():
    """Undeclared function in while loop"""
    source = """
void main() {
    while (check()) {}
}
"""
    expected = "UndeclaredFunction(check)"
    assert Checker(source).check_from_source() == expected


def test_checker_032():
    """Undeclared function in for loop"""
    source = """
void main() {
    for (int i = 0; i < count(); i++) {}
}
"""
    expected = "UndeclaredFunction(count)"
    assert Checker(source).check_from_source() == expected


def test_checker_033():
    """Undeclared function in return"""
    source = """
int func() {
    return getValue();
}
"""
    expected = "UndeclaredFunction(getValue)"
    assert Checker(source).check_from_source() == expected


def test_checker_034():
    """Undeclared function in member access"""
    source = """
void main() {
    obj.method;
}
"""
    expected = "UndeclaredIdentifier(obj)"
    assert Checker(source).check_from_source() == expected


def test_checker_035():
    """Undeclared function with wrong arguments"""
    source = """
void main() {
    nonexistent(1);
}
"""
    expected = "UndeclaredFunction(nonexistent)"
    assert Checker(source).check_from_source() == expected


# ============================================================================
# UNDECLARED STRUCT (test_checker_036 - test_checker_045) --------------------
# ============================================================================
def test_checker_036():
    """Undeclared struct in variable declaration"""
    source = """
void main() {
    Point p;
}
"""
    expected = "UndeclaredStruct(Point)"
    assert Checker(source).check_from_source() == expected


def test_checker_037():
    """Undeclared struct in function parameter"""
    source = """
void func(Point p) {}
"""
    expected = "UndeclaredStruct(Point)"
    assert Checker(source).check_from_source() == expected


def test_checker_038():
    """Undeclared struct in return type"""
    source = """
Point func() { return; }
"""
    expected = "UndeclaredStruct(Point)"
    assert Checker(source).check_from_source() == expected


def test_checker_039():
    """Undeclared struct in member access"""
    source = """
void main() {
    Point p;
    p.x = 10;
}
"""
    expected = "UndeclaredStruct(Point)"
    assert Checker(source).check_from_source() == expected


def test_checker_040():
    """Undeclared struct in struct literal"""
    source = """
void main() {
    Point p = {1, 2};
}
"""
    expected = "UndeclaredStruct(Point)"
    assert Checker(source).check_from_source() == expected


def test_checker_041():
    """Undeclared struct in nested struct"""
    source = """
struct Outer {
    Inner i;
};
"""
    expected = "UndeclaredStruct(Inner)"
    assert Checker(source).check_from_source() == expected


def test_checker_042():
    """Undeclared struct in assignment"""
    source = """
void main() {
    Point p1;
    Point p2;
    p1 = p2;
}
"""
    expected = "UndeclaredStruct(Point)"
    assert Checker(source).check_from_source() == expected


def test_checker_043():
    """Undeclared struct in binary operation"""
    source = """
void main() {
    Point p;
    int x = p + 1;
}
"""
    expected = "UndeclaredStruct(Point)"
    assert Checker(source).check_from_source() == expected


def test_checker_044():
    """Undeclared struct in function call"""
    source = """
void func(Point p) {}
void main() {
    func(p);
}
"""
    expected = "UndeclaredStruct(Point)"
    assert Checker(source).check_from_source() == expected


def test_checker_045():
    """Undeclared struct in switch expression"""
    source = """
void main() {
    Point p;
    switch (p) {}
}
"""
    expected = "UndeclaredStruct(Point)"
    assert Checker(source).check_from_source() == expected


# ============================================================================
# TYPE CANNOT BE INFERRED (test_checker_046 - test_checker_055) --------------
# ============================================================================
def test_checker_046():
    """Auto variable without initialization"""
    source = """
void main() {
    auto x;
}
"""
    # §5: unused `auto` at end of function body — ctx is the block (tyc-semantic).
    expected = "TypeCannotBeInferred(BlockStmt([VarDecl(auto, x)]))"
    assert Checker(source).check_from_source() == expected


def test_checker_047():
    """Auto variable in function parameter (not allowed)"""
    source = """
void func(auto x) {}
"""
    expected = "AST Generation Error: Error on line 2 col 10: auto"
    assert Checker(source).check_from_source() == expected


def test_checker_048():
    """Auto in struct member"""
    source = """
struct S {
    auto x;
};
"""
    expected = "AST Generation Error: Error on line 3 col 4: auto"
    assert Checker(source).check_from_source() == expected


def test_checker_049():
    """Auto in global scope"""
    source = """
auto global_var;
void main() {}
"""
    expected = "AST Generation Error: Error on line 2 col 0: auto"
    assert Checker(source).check_from_source() == expected


def test_checker_050():
    """Auto in nested block without init"""
    source = """
void main() {
    {
        auto y;
    }
}
"""
    expected = "TypeCannotBeInferred(BlockStmt([VarDecl(auto, y)]))"
    assert Checker(source).check_from_source() == expected

def test_checker_051():
    """Auto in for loop init without init"""
    source = """
void main() {
    for (auto i;;) {}
}
"""
    expected = (
        "TypeCannotBeInferred(BlockStmt([ForStmt(for VarDecl(auto, i); None; "
        "None do BlockStmt([]))]))"
    )
    assert Checker(source).check_from_source() == expected

def test_checker_052():
    """Auto in if statement (valid if init)"""
    source = """
void main() {
    if (int cond = 1) {}
}
"""
    expected = "AST Generation Error: Error on line 3 col 8: int"
    assert Checker(source).check_from_source() == expected


def test_checker_053():
    """Auto in while condition"""
    source = """
void main() {
    while (auto flag = 1) {}
}
"""
    expected = "AST Generation Error: Error on line 3 col 11: auto"
    assert Checker(source).check_from_source() == expected


def test_checker_054():
    """Auto in switch expression"""
    source = """
void main() {
    switch (auto val = 1) {}
}
"""
    expected = "AST Generation Error: Error on line 3 col 12: auto"
    assert Checker(source).check_from_source() == expected


def test_checker_055():
    """Auto in assignment without prior declaration"""
    source = """
void main() {
    x = 10;
    auto y = x;
}
"""
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected


# ============================================================================
# TYPE MISMATCH IN STATEMENT (test_checker_056 - test_checker_065) -----------
# ============================================================================
def test_checker_056():
    """If condition not int"""
    source = """
void main() {
    if (3.14) {}
}
"""
    expected = "TypeMismatchInStatement(IfStmt(if FloatLiteral(3.14) then BlockStmt([])))"
    assert Checker(source).check_from_source() == expected


def test_checker_057():
    """While condition not int"""
    source = """
void main() {
    while ("hello") {}
}
"""
    expected = "TypeMismatchInStatement(WhileStmt(while StringLiteral('hello') do BlockStmt([])))"
    assert Checker(source).check_from_source() == expected


def test_checker_058():
    """For condition not int"""
    source = """
void main() {
    for (int i = 0; 3.14; i++) {}
}
"""
    expected = "TypeMismatchInStatement(ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); FloatLiteral(3.14); PostfixOp(Identifier(i)++) do BlockStmt([])))"
    assert Checker(source).check_from_source() == expected


def test_checker_059():
    """Return type mismatch in function"""
    source = """
int func() {
    return 3.14;
}
"""
    expected = "TypeMismatchInStatement(ReturnStmt(return FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected


def test_checker_060():
    """Return void in int function"""
    source = """
int func() {
    return;
}
"""
    expected = "TypeMismatchInStatement(ReturnStmt(return))"
    assert Checker(source).check_from_source() == expected


def test_checker_061():
    """Variable declaration type mismatch"""
    source = """
void main() {
    int x = "string";
}
"""
    expected = "TypeMismatchInStatement(VarDecl(IntType(), x = StringLiteral('string')))"
    assert Checker(source).check_from_source() == expected


def test_checker_062():
    """Switch expression not int"""
    source = """
void main() {
    switch (3.14) {}
}
"""
    expected = "TypeMismatchInStatement(SwitchStmt(switch FloatLiteral(3.14) cases []))"
    assert Checker(source).check_from_source() == expected


def test_checker_063():
    """Case expression not int"""
    source = """
void main() {
    switch (1) {
        case 3.14: break;
    }
}
"""
    expected = "TypeMismatchInExpression(FloatLiteral(3.14))"
    assert Checker(source).check_from_source() == expected


def test_checker_064():
    """Default case with expression not int"""
    source = """
void main() {
    switch (1) {
        default: break;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_065():
    """Assignment in declaration mismatch"""
    source = """
void main() {
    float f = 10;
}
"""
    expected = "TypeMismatchInStatement(VarDecl(FloatType(), f = IntLiteral(10)))"
    assert Checker(source).check_from_source() == expected


# ============================================================================
# TYPE MISMATCH IN EXPRESSION (test_checker_066 - test_checker_075) ----------
# ============================================================================
def test_checker_066():
    """Binary op int + string"""
    source = """
void main() {
    int x = 1 + "hello";
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), +, StringLiteral('hello')))"
    assert Checker(source).check_from_source() == expected


def test_checker_067():
    """Binary op float - int (valid)"""
    source = """
void main() {
    float f = 3.14 - 1;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_068():
    """Binary op % with float"""
    source = """
void main() {
    int x = 10 % 3.5;
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(10), %, FloatLiteral(3.5)))"
    assert Checker(source).check_from_source() == expected


def test_checker_069():
    """Comparison between int and string"""
    source = """
void main() {
    int x = 1 == "1";
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), ==, StringLiteral('1')))"
    assert Checker(source).check_from_source() == expected


def test_checker_070():
    """Logical op with non-int"""
    source = """
void main() {
    int x = 1 && 3.14;
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), &&, FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected


def test_checker_071():
    """Prefix ++ on float (invalid)"""
    source = """
void main() {
    float f = 3.14;
    ++f;
}
"""
    expected = "TypeMismatchInExpression(PrefixOp(++Identifier(f)))"
    assert Checker(source).check_from_source() == expected


def test_checker_072():
    """Postfix -- on non-int"""
    source = """
void main() {
    float f = 3.14;
    f--;
}
"""
    expected = "TypeMismatchInExpression(PostfixOp(Identifier(f)--))"
    assert Checker(source).check_from_source() == expected


def test_checker_073():
    """Assignment int = string"""
    source = """
void main() {
    int x;
    x = "hello";
}
"""
    expected = (
        "TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(x) = "
        "StringLiteral('hello'))))"
    )
    assert Checker(source).check_from_source() == expected


def test_checker_074():
    """Function call with wrong arg type"""
    source = """
void main() {
    printInt(3.14);
}
"""
    expected = "TypeMismatchInExpression(FuncCall(printInt, [FloatLiteral(3.14)]))"
    assert Checker(source).check_from_source() == expected


def test_checker_075():
    """Member access on non-struct"""
    source = """
void main() {
    int x = 10;
    x.y = 5;
}
"""
    expected = (
        "TypeMismatchInStatement(ExprStmt(AssignExpr(MemberAccess(Identifier(x).y) = "
        "IntLiteral(5))))"
    )
    assert Checker(source).check_from_source() == expected


# ============================================================================
# MUST IN LOOP (test_checker_076 - test_checker_085) -------------------------
# ============================================================================
def test_checker_076():
    """Break outside loop"""
    source = """
void main() {
    break;
}
"""
    expected = "MustInLoop(BreakStmt())"
    assert Checker(source).check_from_source() == expected


def test_checker_077():
    """Continue outside loop"""
    source = """
void main() {
    continue;
}
"""
    expected = "MustInLoop(ContinueStmt())"
    assert Checker(source).check_from_source() == expected


def test_checker_078():
    """Break in if statement outside loop"""
    source = """
void main() {
    if (1) break;
}
"""
    expected = "MustInLoop(BreakStmt())"
    assert Checker(source).check_from_source() == expected


def test_checker_079():
    """Continue in function outside loop"""
    source = """
void func() {
    continue;
}
"""
    expected = "MustInLoop(ContinueStmt())"
    assert Checker(source).check_from_source() == expected


def test_checker_080():
    """Break in nested block outside loop"""
    source = """
void main() {
    {
        break;
    }
}
"""
    expected = "MustInLoop(BreakStmt())"
    assert Checker(source).check_from_source() == expected


def test_checker_081():
    """Continue in switch outside loop"""
    source = """
void main() {
    switch (1) {
        case 1: continue;
    }
}
"""
    expected = "MustInLoop(ContinueStmt())"
    assert Checker(source).check_from_source() == expected


def test_checker_082():
    """Break in while loop (valid)"""
    source = """
void main() {
    while (1) break;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_083():
    """Continue in for loop (valid)"""
    source = """
void main() {
    for (;;) continue;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_084():
    """Break in nested loop"""
    source = """
void main() {
    while (1) {
        for (;;) break;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_085():
    """Continue in nested loop"""
    source = """
void main() {
    for (;;) {
        while (1) continue;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

# ============================================================================
# ADVANCED PROGRAM CASED (test_checker_086 - test_checker_100) ---------------
# ============================================================================
def test_checker_086():
    """Complex nested scopes with auto inference"""
    source = """
void main() {
    auto a = 10;
    {
        auto b = a + 5;
        {
            auto c = b * 2;
            printInt(c);
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_087():
    """Struct with nested struct usage"""
    source = """
struct Inner {
    int val;
};
struct Outer {
    Inner i;
    int num;
};
void main() {
    Outer o;
    o.i.val = 42;
    o.num = 10;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_088():
    """Switch with multiple cases and default"""
    source = """
void main() {
    int x = 1;
    switch (x) {
        case 1: printInt(1); break;
        case 2: printInt(2); break;
        default: printInt(0);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_089():
    """For loop with complex init and update"""
    source = """
void main() {
    int j = 10;
    for (int i = 0; i < j; i++) {
        printInt(i + j);
        j--;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_090():
    """Function with multiple parameters and return"""
    source = """
int sum(int a, int b, int c) {
    return a + b + c;
}
void main() {
    int result = sum(1, 2, 3);
    printInt(result);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_091():
    """Recursive function call (assuming allowed)"""
    source = """
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
void main() {
    printInt(factorial(5));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_092():
    """Array-like struct operations"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p1 = {1, 2};
    Point p2 = {3, 4};
    int sum = p1.x + p1.y + p2.x + p2.y;
    printInt(sum);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_093():
    """Complex expression with multiple operators"""
    source = """
void main() {
    int a = 5;
    int b = 10;
    int c = 15;
    float result = (a + b) * c / 2.0 + 3.14;
    printFloat(result);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_094():
    """Nested if-else with auto"""
    source = """
void main() {
    auto x = readInt();
    if (x > 0) {
        auto y = x * 2;
        printInt(y);
    } else {
        auto z = x - 1;
        printInt(z);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_095():
    """While loop with break and continue"""
    source = """
void main() {
    int i = 0;
    while (i < 10) {
        i++;
        if (i == 5) continue;
        if (i == 8) break;
        printInt(i);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_096():
    """Function overloading simulation with different names"""
    source = """
int add(int a, int b) { return a + b; }
float add(float a, float b) { return a + b; }
void main() {
    int sum = add(1, 2);
    float fsum = add(1.0, 2.0);
}
"""
    expected = "Redeclared(Function, add)"
    assert Checker(source).check_from_source() == expected


def test_checker_097():
    """Complex struct with functions"""
    source = """
struct Data {
    int id;
    string name;
};
Data createData(int id, string name) {
    Data d;
    d.id = id;
    d.name = name;
    return d;
}
void main() {
    Data d = createData(1, "test");
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_098():
    """Mixed types in expressions"""
    source = """
void main() {
    int i = 5;
    float f = 3.14;
    auto result = i + f;
    printFloat(result);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_099():
    """Switch with fallthrough"""
    source = """
void main() {
    int x = 1;
    switch (x) {
        case 1:
        case 2: printInt(12); break;
        default: printInt(0);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_checker_100():
    """Comprehensive program with all features"""
    source = """
struct Point {
    int x;
    int y;
};
int distance(Point p1, Point p2) {
    int dx = p1.x - p2.x;
    int dy = p1.y - p2.y;
    return dx * dx + dy * dy;
}
void main() {
    Point a = {0, 0};
    Point b = {3, 4};
    int dist = distance(a, b);
    printInt(dist);
    for (int i = 0; i < 5; i++) {
        if (i % 2 == 0) printInt(i);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected



'''
# ============================================================================
# Valid Programs (test_001 - test_010)
# ============================================================================
def test_001():
    """Test a valid program that should pass all checks"""
    source = """
void main() {
    int x = 5;
    int y = x + 1;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_002():
    """Test valid program with auto type inference"""
    source = """
void main() {
    auto x = 10;
    auto y = 3.14;
    auto z = x + y;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_003():
    """Test valid program with functions"""
    source = """
int add(int x, int y) {
    return x + y;
}
void main() {
    int sum = add(5, 3);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_004():
    """Test valid program with struct"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p;
    p.x = 10;
    p.y = 20;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_005():
    """Test valid program with nested blocks"""
    source = """
void main() {
    int x = 10;
    {
        int y = 20;
        int z = x + y;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
'''