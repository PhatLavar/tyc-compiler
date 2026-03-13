"""
AST Generation test cases for TyC compiler.
TODO: Implement 100 test cases for AST generation

TO_DEBUG:
print(f"RESULT: {repr(result)}")
print(f"EXPECTED: {repr(expected)}")
"""

import pytest
from tests.utils import ASTGenerator


def test_ast_gen_placeholder():
    """Placeholder test - replace with actual test cases"""
    source = """void main() {
}"""
    # TODO: Add actual test assertions
    # Example:
    # expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    # assert str(ASTGenerator(source).generate()) == expected
    assert True

# ==========================================
# 1. PROGRAM AND BASIC STRUCTURE (10)
# ==========================================

def test_ast_gen_001():
    """Empty program"""
    source = """void main() {}"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_002():
    """Main with return type"""
    source = """int main() { return 0; }"""
    expected = "Program([FuncDecl(IntType(), main, [], BlockStmt([ReturnStmt(return IntLiteral(0))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_003():
    """Main with inferred return type"""
    source = """main() { return 1; }"""
    expected = "Program([FuncDecl(auto, main, [], BlockStmt([ReturnStmt(return IntLiteral(1))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_004():
    """Multiple functions"""
    source = """void foo() {} void bar() {} void main() {}"""
    expected = (
        "Program(["
        "FuncDecl(VoidType(), foo, [], BlockStmt([])), "
        "FuncDecl(VoidType(), bar, [], BlockStmt([])), "
        "FuncDecl(VoidType(), main, [], BlockStmt([]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_005():
    """Function with single parameter"""
    source = """void greet(string name) {}"""
    expected = "Program([FuncDecl(VoidType(), greet, [Param(StringType(), name)], BlockStmt([]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_006():
    """Function with multiple parameters"""
    source = """int add(int a, int b) {}"""
    expected = "Program([FuncDecl(IntType(), add, [Param(IntType(), a), Param(IntType(), b)], BlockStmt([]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected    

def test_ast_gen_007():
    """Nested empty blocks"""
    source = """void main() { {{}} }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([BlockStmt([BlockStmt([])])]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_008():
    """Function returning struct type"""
    source = """struct Point { int x; }; Point getPoint() {}"""
    expected = (
        "Program(["
        "StructDecl(Point, [MemberDecl(IntType(), x)]), "
        "FuncDecl(StructType(Point), getPoint, [], BlockStmt([]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_009():
    """Function accepting struct type"""
    source = """struct Point { int x; }; void setPoint(Point p) {}"""
    expected = (
        "Program(["
        "StructDecl(Point, [MemberDecl(IntType(), x)]), "
        "FuncDecl(VoidType(), setPoint, [Param(StructType(Point), p)], BlockStmt([]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_010():
    """Comment preservation - comments should NOT appear in AST"""
    source = """/* comment */ void main() { // inline comment\n}"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected


# ==========================================
# 2. STRUCT DECLARATIONS (10)
# ==========================================

def test_ast_gen_011():
    """Empty struct"""
    source = """struct Empty {}; void main() {}"""
    expected = "Program([StructDecl(Empty, []), FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_012():
    """Struct with single member"""
    source = """struct Point { int x; }; void main() {}"""
    expected = "Program([StructDecl(Point, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_013():
    """Struct with multiple members"""
    source = """struct Point { int x; int y; }; void main() {}"""
    expected = "Program([StructDecl(Point, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)]), FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_014():
    """Struct with different types"""
    source = """struct Data { int i; float f; string s; }; void main() {}"""
    expected = (
        "Program(["
        "StructDecl(Data, ["
        "MemberDecl(IntType(), i), "
        "MemberDecl(FloatType(), f), "
        "MemberDecl(StringType(), s)"
        "]), "
        "FuncDecl(VoidType(), main, [], BlockStmt([]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_015():
    """Struct with struct member"""
    source = """struct Point { int x; }; struct Line { Point p1; Point p2; }; void main() {}"""
    expected = (
        "Program(["
        "StructDecl(Point, [MemberDecl(IntType(), x)]), "
        "StructDecl(Line, ["
        "MemberDecl(StructType(Point), p1), "
        "MemberDecl(StructType(Point), p2)"
        "]), "
        "FuncDecl(VoidType(), main, [], BlockStmt([]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_016():
    """Struct with self-reference (syntax only)"""
    source = """struct Node { Node next; }; void main() {}"""
    expected = (
        "Program(["
        "StructDecl(Node, [MemberDecl(StructType(Node), next)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt([]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_017():
    """Multiple struct declarations"""
    source = """struct A { int x; }; struct B { float y; }; void main() {}"""
    expected = (
        "Program(["
        "StructDecl(A, [MemberDecl(IntType(), x)]), "
        "StructDecl(B, [MemberDecl(FloatType(), y)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt([]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_018():
    """Struct with float member"""
    source = """struct F { float val; }; void main() {}"""
    expected = "Program([StructDecl(F, [MemberDecl(FloatType(), val)]), FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_019():
    """Struct with string member"""
    source = """struct S { string text; }; void main() {}"""
    expected = "Program([StructDecl(S, [MemberDecl(StringType(), text)]), FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_020():
    """Struct before function using it"""
    source = """struct P { int x; }; void use(P p) {} void main() {}"""
    expected = (
        "Program(["
        "StructDecl(P, [MemberDecl(IntType(), x)]), "
        "FuncDecl(VoidType(), use, [Param(StructType(P), p)], BlockStmt([])), "
        "FuncDecl(VoidType(), main, [], BlockStmt([]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected


# ==========================================
# 3. VARIABLE DECLARATIONS (10)
# ==========================================

def test_ast_gen_021():
    """Auto variable with int"""
    source = """void main() { auto x = 5; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = IntLiteral(5))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_022():
    """Auto variable with float"""
    source = """void main() { auto f = 3.14; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, f = FloatLiteral(3.14))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_023():
    """Auto variable with string"""
    source = """void main() { auto s = \"hello\"; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, s = StringLiteral('hello'))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_024():
    """Explicit int declaration with init"""
    source = """void main() { int x = 10; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x = IntLiteral(10))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_025():
    """Explicit float declaration with init"""
    source = """void main() { float f = 2.5; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(FloatType(), f = FloatLiteral(2.5))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_026():
    """Explicit string declaration with init"""
    source = """void main() { string s = \"text\"; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StringType(), s = StringLiteral('text'))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_027():
    """Variable without initializer"""
    source = """void main() { int x; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x)]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_028():
    """Multiple variable declarations"""
    source = """void main() { int x; int y; auto z = 5; }"""
    expected = (
        "Program([FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(IntType(), x), "
        "VarDecl(IntType(), y), "
        "VarDecl(auto, z = IntLiteral(5))"
        "]))])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_029():
    """Struct variable with struct literal"""
    source = """struct P { int x; }; void main() { P p = {5}; }"""
    expected = (
        "Program(["
        "StructDecl(P, [MemberDecl(IntType(), x)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(P), p = StructLiteral({IntLiteral(5)}))"
        "]))])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_030():
    """Variable in for loop init"""
    source = """void main() { for (int i=0; i<10; i++) {} }"""
    expected = (
        "Program([FuncDecl(VoidType(), main, [], BlockStmt(["
        "ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)++) do BlockStmt([]))"
        "]))])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected


# ==========================================
# 4. SIMPLE EXPRESSIONS (10)
# ==========================================

def test_ast_gen_031():
    """Integer literal"""
    source = """void main() { auto x = 42; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = IntLiteral(42))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_032():
    """Float literal"""
    source = """void main() { auto x = 3.14; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = FloatLiteral(3.14))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_033():
    """String literal"""
    source = """void main() { auto x = \"hello\"; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = StringLiteral('hello'))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_034():
    """Identifier"""
    source = """void main() { int x; auto y = x; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x), VarDecl(auto, y = Identifier(x))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_035():
    """Negative literal"""
    source = """void main() { auto x = -5; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = PrefixOp(-IntLiteral(5)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_036():
    """Positive unary"""
    source = """void main() { auto x = +5; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = PrefixOp(+IntLiteral(5)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_037():
    """Logical not"""
    source = """void main() { auto x = !1; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = PrefixOp(!IntLiteral(1)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_038():
    """Prefix increment"""
    source = """void main() { int x; ++x; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x), ExprStmt(PrefixOp(++Identifier(x)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_039():
    """Postfix increment"""
    source = """void main() { int x; x++; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x), ExprStmt(PostfixOp(Identifier(x)++))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_040():
    """Function call"""
    source = """void foo() {} void main() { foo(); }"""
    expected = (
        "Program(["
        "FuncDecl(VoidType(), foo, [], BlockStmt([])), "
        "FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(FuncCall(foo, []))]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected


# ==========================================
# 5. BINARY OPERATIONS (10)
# ==========================================

def test_ast_gen_041():
    """Addition"""
    source = """void main() { auto x = 1 + 2; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(IntLiteral(1), +, IntLiteral(2)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_042():
    """Subtraction"""
    source = """void main() { auto x = 5 - 3; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(IntLiteral(5), -, IntLiteral(3)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_043():
    """Multiplication"""
    source = """void main() { auto x = 2 * 3; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(IntLiteral(2), *, IntLiteral(3)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_044():
    """Division"""
    source = """void main() { auto x = 10 / 2; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(IntLiteral(10), /, IntLiteral(2)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_045():
    """Modulus"""
    source = """void main() { auto x = 10 % 3; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(IntLiteral(10), %, IntLiteral(3)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_046():
    """Comparison less than"""
    source = """void main() { auto x = 1 < 2; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(IntLiteral(1), <, IntLiteral(2)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_047():
    """Equality"""
    source = """void main() { auto x = 1 == 1; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(IntLiteral(1), ==, IntLiteral(1)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_048():
    """Not equal"""
    source = """void main() { auto x = 1 != 2; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(IntLiteral(1), !=, IntLiteral(2)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_049():
    """Logical AND"""
    source = """void main() { auto x = 1 && 0; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(IntLiteral(1), &&, IntLiteral(0)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_050():
    """Logical OR"""
    source = """void main() { auto x = 1 || 0; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(IntLiteral(1), ||, IntLiteral(0)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected


# ==========================================
# 6. COMPOUND EXPRESSIONS (10)
# ==========================================

def test_ast_gen_051():
    """Parenthesized expression"""
    source = """void main() { auto x = (1 + 2); }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(IntLiteral(1), +, IntLiteral(2)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_052():
    """Add then multiply"""
    source = """void main() { auto x = 1 + 2 * 3; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3))))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_053():
    """Chained arithmetic"""
    source = """void main() { auto x = 1 + 2 + 3; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), +, IntLiteral(3)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_054():
    """Mixed arithmetic and comparison"""
    source = """void main() { auto x = 1 + 2 > 3; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), >, IntLiteral(3)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_055():
    """Logical with arithmetic"""
    source = """void main() { auto x = 1 == 2 && 3 == 4; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(BinaryOp(IntLiteral(1), ==, IntLiteral(2)), &&, BinaryOp(IntLiteral(3), ==, IntLiteral(4))))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_056():
    """Assignment in variable init"""
    source = """void main() { int x = 5; auto y = x = 10; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x = IntLiteral(5)), VarDecl(auto, y = AssignExpr(Identifier(x) = IntLiteral(10)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_057():
    """Nested parentheses"""
    source = """void main() { auto x = ((1 + 2) * (3 + 4)); }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), *, BinaryOp(IntLiteral(3), +, IntLiteral(4))))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_058():
    """Function call in expression"""
    source = """int foo() { return 5; } void main() { auto x = foo(); }"""
    expected = (
        "Program(["
        "FuncDecl(IntType(), foo, [], BlockStmt([ReturnStmt(return IntLiteral(5))])), "
        "FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = FuncCall(foo, []))]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_059():
    """Multiple function calls"""
    source = """int foo() { return 5; } void main() { foo(); foo(); }"""
    expected = (
        "Program(["
        "FuncDecl(IntType(), foo, [], BlockStmt([ReturnStmt(return IntLiteral(5))])), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "ExprStmt(FuncCall(foo, [])), "
        "ExprStmt(FuncCall(foo, []))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_060():
    """Complex expression with all operators"""
    source = """void main() { auto x = 1 + 2 * 3 - 4 / 2 == 3; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(BinaryOp(BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3))), -, BinaryOp(IntLiteral(4), /, IntLiteral(2))), ==, IntLiteral(3)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected


# ==========================================
# 7. MEMBER ACCESS (5)
# ==========================================

def test_ast_gen_061():
    """Simple member access"""
    source = """struct P { int x; }; void main() { P p; auto v = p.x; }"""
    expected = (
        "Program(["
        "StructDecl(P, [MemberDecl(IntType(), x)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(P), p), "
        "VarDecl(auto, v = MemberAccess(Identifier(p).x))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_062():
    """Member access on function return"""
    source = """struct P { int x; }; P getP() { P p = {5}; return p; } void main() { auto v = getP().x; }"""
    expected = (
        "Program(["
        "StructDecl(P, [MemberDecl(IntType(), x)]), "
        "FuncDecl(StructType(P), getP, [], BlockStmt(["
        "VarDecl(StructType(P), p = StructLiteral({IntLiteral(5)})), "
        "ReturnStmt(return Identifier(p))"
        "])), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(auto, v = MemberAccess(FuncCall(getP, []).x))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_063():
    """Chained member access"""
    source = """struct Inner { int val; }; struct Outer { Inner i; }; void main() { Outer o; auto v = o.i.val; }"""
    expected = (
        "Program(["
        "StructDecl(Inner, [MemberDecl(IntType(), val)]), "
        "StructDecl(Outer, [MemberDecl(StructType(Inner), i)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(Outer), o), "
        "VarDecl(auto, v = MemberAccess(MemberAccess(Identifier(o).i).val))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_064():
    """Member assignment"""
    source = """struct P { int x; }; void main() { P p; p.x = 5; }"""
    expected = (
        "Program(["
        "StructDecl(P, [MemberDecl(IntType(), x)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(P), p), "
        "ExprStmt(AssignExpr(MemberAccess(Identifier(p).x) = IntLiteral(5)))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_065():
    """Member in expression"""
    source = """struct P { int x; }; void main() { P p; auto v = p.x + 1; }"""
    expected = (
        "Program(["
        "StructDecl(P, [MemberDecl(IntType(), x)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(P), p), "
        "VarDecl(auto, v = BinaryOp(MemberAccess(Identifier(p).x), +, IntLiteral(1)))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected


# ==========================================
# 8. CONTROL FLOW STATEMENTS (15)
# ==========================================

def test_ast_gen_066():
    """Simple if"""
    source = """void main() { if (1) {} }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then BlockStmt([]))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_067():
    """If with else"""
    source = """void main() { if (1) {} else {} }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then BlockStmt([]), else BlockStmt([]))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_068():
    """If-else chain"""
    source = """void main() { if (1) {} else if (0) {} else {} }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then BlockStmt([]), else IfStmt(if IntLiteral(0) then BlockStmt([]), else BlockStmt([])))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_069():
    """While loop"""
    source = """void main() { while (1) {} }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while IntLiteral(1) do BlockStmt([]))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_070():
    """While with break"""
    source = """void main() { while (1) break; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while IntLiteral(1) do BreakStmt())]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_071():
    """While with continue"""
    source = """void main() { while (1) continue; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while IntLiteral(1) do ContinueStmt())]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_072():
    """For loop with all parts"""
    source = """void main() { for (int i=0; i<10; i++) {} }"""
    expected = (
        "Program([FuncDecl(VoidType(), main, [], BlockStmt(["
        "ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)++) do BlockStmt([]))"
        "]))])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_073():
    """For loop infinite"""
    source = """void main() { for (;;) {} }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; None do BlockStmt([]))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_074():
    """Switch with case"""
    source = """void main() { switch (1) { case 1: break; } }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case IntLiteral(1): [BreakStmt()])])]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_075():
    """Switch with default"""
    source = """void main() { switch (1) { default: break; } }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [], default DefaultStmt(default: [BreakStmt()]))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_076():
    """Multiple case clauses"""
    source = """void main() { switch (1) { case 1: break; case 2: break; } }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch IntLiteral(1) cases [CaseStmt(case IntLiteral(1): [BreakStmt()]), CaseStmt(case IntLiteral(2): [BreakStmt()])])]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_077():
    """Return without value"""
    source = """void main() { return; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ReturnStmt(return)]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_078():
    """Return with value"""
    source = """int main() { return 42; }"""
    expected = "Program([FuncDecl(IntType(), main, [], BlockStmt([ReturnStmt(return IntLiteral(42))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_079():
    """Nested control flow"""
    source = """void main() { if (1) { while (1) { for (;;) {} } } }"""
    expected = (
        "Program([FuncDecl(VoidType(), main, [], BlockStmt(["
        "IfStmt(if IntLiteral(1) then BlockStmt(["
        "WhileStmt(while IntLiteral(1) do BlockStmt(["
        "ForStmt(for None; None; None do BlockStmt([]))"
        "]))"
        "]))"
        "]))])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_080():
    """Expression as statement"""
    source = """void main() { 1 + 2; }"""
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), +, IntLiteral(2)))]))])"
    result = str(ASTGenerator(source).generate())
    assert result == expected


# ==========================================
# 9. STRUCT INITIALIZATION (10)
# ==========================================

def test_ast_gen_081():
    """Struct literal with single field"""
    source = """struct P { int x; }; void main() { P p = {5}; }"""
    expected = (
        "Program(["
        "StructDecl(P, [MemberDecl(IntType(), x)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(P), p = StructLiteral({IntLiteral(5)}))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_082():
    """Struct literal with multiple fields"""
    source = """struct P { int x; int y; }; void main() { P p = {1, 2}; }"""
    expected = (
        "Program(["
        "StructDecl(P, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(P), p = StructLiteral({IntLiteral(1), IntLiteral(2)}))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_083():
    """Nested struct literal"""
    source = """struct Inner { int x; }; struct Outer { Inner i; }; void main() { Outer o = {{5}}; }"""
    expected = (
        "Program(["
        "StructDecl(Inner, [MemberDecl(IntType(), x)]), "
        "StructDecl(Outer, [MemberDecl(StructType(Inner), i)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(Outer), o = StructLiteral({StructLiteral({IntLiteral(5)})}))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_084():
    """Struct literal with expressions"""
    source = """struct P { int x; int y; }; void main() { P p = {1+2, 3*4}; }"""
    expected = (
        "Program(["
        "StructDecl(P, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(P), p = StructLiteral({"
        "BinaryOp(IntLiteral(1), +, IntLiteral(2)), "
        "BinaryOp(IntLiteral(3), *, IntLiteral(4))"
        "}))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_085():
    """Struct literal as function argument"""
    source = """struct P { int x; }; void foo(P p) {} void main() { foo({5}); }"""
    expected = (
        "Program(["
        "StructDecl(P, [MemberDecl(IntType(), x)]), "
        "FuncDecl(VoidType(), foo, [Param(StructType(P), p)], BlockStmt([])), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "ExprStmt(FuncCall(foo, [StructLiteral({IntLiteral(5)})]))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_086():
    """Empty struct literal"""
    source = """struct Empty {}; void main() { Empty e = {}; }"""
    expected = (
        "Program(["
        "StructDecl(Empty, []), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(Empty), e = StructLiteral({}))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_087():
    """Struct with complex init"""
    source = """struct Data { int a; float b; string c; }; void main() { Data d = {1, 2.5, \"hi\"}; }"""
    expected = (
        "Program(["
        "StructDecl(Data, ["
        "MemberDecl(IntType(), a), "
        "MemberDecl(FloatType(), b), "
        "MemberDecl(StringType(), c)"
        "]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(Data), d = StructLiteral({"
        "IntLiteral(1), "
        "FloatLiteral(2.5), "
        "StringLiteral('hi')"
        "}))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_088():
    """Struct literal in variable assignment"""
    source = """struct P { int x; }; void main() { P p; p = {5}; }"""
    expected = (
        "Program(["
        "StructDecl(P, [MemberDecl(IntType(), x)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(P), p), "
        "ExprStmt(AssignExpr(Identifier(p) = StructLiteral({IntLiteral(5)})))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_089():
    """Multiple nested levels"""
    source = """struct A { int x; }; struct B { A a; int y; }; struct C { B b; }; void main() { C c = {{{1}, 2}}; }"""
    expected = (
        "Program(["
        "StructDecl(A, [MemberDecl(IntType(), x)]), "
        "StructDecl(B, [MemberDecl(StructType(A), a), MemberDecl(IntType(), y)]), "
        "StructDecl(C, [MemberDecl(StructType(B), b)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(C), c = StructLiteral({"
        "StructLiteral({StructLiteral({IntLiteral(1)}), IntLiteral(2)})"
        "}))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_090():
    """Struct with function call in init"""
    source = """struct P { int x; }; int getX() { return 5; } void main() { P p = {getX()}; }"""
    expected = (
        "Program(["
        "StructDecl(P, [MemberDecl(IntType(), x)]), "
        "FuncDecl(IntType(), getX, [], BlockStmt([ReturnStmt(return IntLiteral(5))])), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(P), p = StructLiteral({FuncCall(getX, [])}))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected


# ==========================================
# 10. COMPLEX PROGRAMS (10)
# ==========================================

def test_ast_gen_091():
    """Recursive factorial"""
    source = """
    int fact(int n) {
        if (n <= 1) return 1;
        else return n * fact(n - 1);
    }
    void main() {}
    """
    expected = (
        "Program(["
        "FuncDecl(IntType(), fact, [Param(IntType(), n)], BlockStmt(["
        "IfStmt(if BinaryOp(Identifier(n), <=, IntLiteral(1)) then "
        "ReturnStmt(return IntLiteral(1)), else "
        "ReturnStmt(return BinaryOp(Identifier(n), *, FuncCall(fact, [BinaryOp(Identifier(n), -, IntLiteral(1))]))))"
        "])), "
        "FuncDecl(VoidType(), main, [], BlockStmt([]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_092():
    """Point struct with functions"""
    source = """
    struct Point { int x; int y; };
    void setPoint(Point p) {}
    Point getPoint() {}
    void main() {}
    """
    expected = (
        "Program(["
        "StructDecl(Point, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)]), "
        "FuncDecl(VoidType(), setPoint, [Param(StructType(Point), p)], BlockStmt([])), "
        "FuncDecl(StructType(Point), getPoint, [], BlockStmt([])), "
        "FuncDecl(VoidType(), main, [], BlockStmt([]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_093():
    """Variable initialization with various types"""
    source = """
    void main() {
        int i = 5;
        float f = 3.14;
        string s = "hello";
        auto a = 10;
    }
    """
    expected = (
        "Program([FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(IntType(), i = IntLiteral(5)), "
        "VarDecl(FloatType(), f = FloatLiteral(3.14)), "
        "VarDecl(StringType(), s = StringLiteral('hello')), "
        "VarDecl(auto, a = IntLiteral(10))"
        "]))])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_094():
    """Nested loops with control flow"""
    source = """
    void main() {
        for (int i=0; i<10; i++) {
            for (int j=0; j<10; j++) {
                if (i == j) break;
            }
        }
    }
    """
    expected = (
        "Program([FuncDecl(VoidType(), main, [], BlockStmt(["
        "ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)++) do "
        "BlockStmt(["
        "ForStmt(for VarDecl(IntType(), j = IntLiteral(0)); BinaryOp(Identifier(j), <, IntLiteral(10)); PostfixOp(Identifier(j)++) do "
        "BlockStmt(["
        "IfStmt(if BinaryOp(Identifier(i), ==, Identifier(j)) then BreakStmt()"
        ")"
        "]))"
        "]))"
        "]))])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_095():
    """Switch with multiple cases and default"""
    source = """
    void main() {
        switch (1) {
            case 1: break;
            case 2: break;
            case 3: break;
            default: break;
        }
    }
    """
    expected = (
        "Program([FuncDecl(VoidType(), main, [], BlockStmt(["
        "SwitchStmt(switch IntLiteral(1) cases ["
        "CaseStmt(case IntLiteral(1): [BreakStmt()]), "
        "CaseStmt(case IntLiteral(2): [BreakStmt()]), "
        "CaseStmt(case IntLiteral(3): [BreakStmt()])"
        "], default DefaultStmt(default: [BreakStmt()]))"
        "]))])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_096():
    """Function with all statement types"""
    source = """
    void main() {
        int x = 5;
        if (x > 0) x++;
        while (x < 10) x = x + 1;
        return;
    }
    """
    expected = (
        "Program([FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(IntType(), x = IntLiteral(5)), "
        "IfStmt(if BinaryOp(Identifier(x), >, IntLiteral(0)) then "
        "ExprStmt(PostfixOp(Identifier(x)++))), "
        "WhileStmt(while BinaryOp(Identifier(x), <, IntLiteral(10)) do "
        "ExprStmt(AssignExpr(Identifier(x) = BinaryOp(Identifier(x), +, IntLiteral(1))))), "
        "ReturnStmt(return)"
        "]))])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_097():
    """Complex expression evaluation"""
    source = """
    void main() {
        auto result = 1 + 2 * 3 - 4 / 2 && 5 > 3 || 6 == 7;
    }
    """
    expected = (
        "Program([FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(auto, result = "
        "BinaryOp("
        "BinaryOp("
        "BinaryOp("
        "BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3))), "
        "-, BinaryOp(IntLiteral(4), /, IntLiteral(2))), "
        "&&, BinaryOp(IntLiteral(5), >, IntLiteral(3))), "
        "||, BinaryOp(IntLiteral(6), ==, IntLiteral(7))))"
        "]))])"
    )
    result = str(ASTGenerator(source).generate())
    print(f"RESULT: {repr(result)}")
    print(f"EXPECTED: {repr(expected)}")
    assert result == expected

def test_ast_gen_098():
    """Struct operations"""
    source = """
    struct Data { int value; };
    void main() {
        Data d = {42};
        auto v = d.value;
        d.value = 100;
    }
    """
    expected = (
        "Program(["
        "StructDecl(Data, [MemberDecl(IntType(), value)]), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(Data), d = StructLiteral({IntLiteral(42)})), "
        "VarDecl(auto, v = MemberAccess(Identifier(d).value)), "
        "ExprStmt(AssignExpr(MemberAccess(Identifier(d).value) = IntLiteral(100)))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_099():
    """Function calls with arguments"""
    source = """
    int add(int a, int b) { return a + b; }
    void main() {
        auto sum = add(3, 4);
        auto result = add(add(1, 2), add(3, 4));
    }
    """
    expected = (
        "Program(["
        "FuncDecl(IntType(), add, [Param(IntType(), a), Param(IntType(), b)], "
        "BlockStmt([ReturnStmt(return BinaryOp(Identifier(a), +, Identifier(b)))])), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(auto, sum = FuncCall(add, [IntLiteral(3), IntLiteral(4)])), "
        "VarDecl(auto, result = FuncCall(add, ["
        "FuncCall(add, [IntLiteral(1), IntLiteral(2)]), "
        "FuncCall(add, [IntLiteral(3), IntLiteral(4)])"
        "]))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected

def test_ast_gen_100():
    """Complete program"""
    source = """
    struct Point { int x; int y; };
    
    Point createPoint(int x, int y) {
        return {x, y};
    }
    
    void printPoint(Point p) {
        printInt(p.x);
        printInt(p.y);
    }
    
    void main() {
        Point p = createPoint(10, 20);
        printPoint(p);
        
        for (int i=0; i<5; i++) {
            if (i % 2 == 0) {
                printInt(i);
            }
        }
    }
    """
    expected = (
        "Program(["
        "StructDecl(Point, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)]), "
        "FuncDecl(StructType(Point), createPoint, [Param(IntType(), x), Param(IntType(), y)], "
        "BlockStmt([ReturnStmt(return StructLiteral({Identifier(x), Identifier(y)}))])), "
        "FuncDecl(VoidType(), printPoint, [Param(StructType(Point), p)], "
        "BlockStmt(["
        "ExprStmt(FuncCall(printInt, [MemberAccess(Identifier(p).x)])), "
        "ExprStmt(FuncCall(printInt, [MemberAccess(Identifier(p).y)]))"
        "])), "
        "FuncDecl(VoidType(), main, [], BlockStmt(["
        "VarDecl(StructType(Point), p = FuncCall(createPoint, [IntLiteral(10), IntLiteral(20)])), "
        "ExprStmt(FuncCall(printPoint, [Identifier(p)])), "
        "ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(5)); PostfixOp(Identifier(i)++) do "
        "BlockStmt(["
        "IfStmt(if BinaryOp(BinaryOp(Identifier(i), %, IntLiteral(2)), ==, IntLiteral(0)) then "
        "BlockStmt([ExprStmt(FuncCall(printInt, [Identifier(i)]))]))"
        "]))"
        "]))"
        "])"
    )
    result = str(ASTGenerator(source).generate())
    assert result == expected