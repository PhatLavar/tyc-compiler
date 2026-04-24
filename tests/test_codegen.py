"""
Test cases for TyC code generation.
"""

from src.utils.nodes import *
from tests.utils import CodeGenerator


def test_001():
    """Test 1: Hello World - print string"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [ExprStmt(FuncCall("printString", [StringLiteral("Hello World")]))],
                ),
            ),
        ],
    )
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_002():
    """Test 2: Print integer"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("printInt", [IntLiteral(42)]))]),
            ),
        ],
    )
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_003():
    """Test 3: Print float"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("printFloat", [FloatLiteral(3.14)]))]),
            ),
        ],
    )
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_004():
    """Test 4: Variable declaration and assignment"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(10)),
                        ExprStmt(FuncCall("printInt", [Identifier("x")])),
                    ],
                ),
            ),
        ],
    )
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_005():
    """Test 5: Binary operation - addition"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(5), "+", IntLiteral(3))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_006():
    """Test 6: Binary operation - multiplication"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(6), "*", IntLiteral(7))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_007():
    """Test 7: If statement"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        IfStmt(
                            BinaryOp(IntLiteral(1), "<", IntLiteral(2)),
                            ExprStmt(FuncCall("printString", [StringLiteral("yes")])),
                            ExprStmt(FuncCall("printString", [StringLiteral("no")])),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = "yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_008():
    """Test 8: While loop"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "i", IntLiteral(0)),
                        WhileStmt(
                            BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                            BlockStmt(
                                [
                                    ExprStmt(FuncCall("printInt", [Identifier("i")])),
                                    ExprStmt(
                                        AssignExpr(
                                            Identifier("i"),
                                            BinaryOp(
                                                Identifier("i"),
                                                "+",
                                                IntLiteral(1),
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_009():
    """Test 9: Function call with return value"""
    ast = Program(
        [
            FuncDecl(
                IntType(),
                "add",
                [Param(IntType(), "a"), Param(IntType(), "b")],
                BlockStmt([ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))]),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [FuncCall("add", [IntLiteral(20), IntLiteral(22)])],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_010():
    """Test 10: Multiple statements - arithmetic operations"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(10)),
                        VarDecl(IntType(), "y", IntLiteral(20)),
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(Identifier("x"), "+", Identifier("y"))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_011():
    """Test 11: For loop with postfix update"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(0)),
                            BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [ExprStmt(FuncCall("printInt", [Identifier("i")]))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_012():
    """Test 12: Prefix increment returns updated value"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(4)),
                        ExprStmt(
                            FuncCall("printInt", [PrefixOp("++", Identifier("x"))]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_013():
    """Test 13: Postfix increment returns old value"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(4)),
                        ExprStmt(
                            FuncCall("printInt", [PostfixOp("++", Identifier("x"))]),
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("x")])),
                    ],
                ),
            ),
        ],
    )
    expected = "45"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_014():
    """Test 14: Logical operators"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(1), "&&", IntLiteral(1))],
                            ),
                        ),
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(1), "||", IntLiteral(0))],
                            ),
                        ),
                        ExprStmt(FuncCall("printInt", [PrefixOp("!", IntLiteral(0))])),
                    ],
                ),
            ),
        ],
    )
    expected = "111"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_015():
    """Test 15: Struct member assignment"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "p",
                            StructLiteral([IntLiteral(1), IntLiteral(2)]),
                        ),
                        ExprStmt(
                            AssignExpr(
                                MemberAccess(Identifier("p"), "x"),
                                IntLiteral(9),
                            ),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p"), "x")]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = "9"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_016():
    """Test 16: Struct assignment copies object reference"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "p1",
                            StructLiteral([IntLiteral(3), IntLiteral(4)]),
                        ),
                        VarDecl(StructType("Point"), "p2"),
                        ExprStmt(AssignExpr(Identifier("p2"), Identifier("p1"))),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p2"), "y")]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = "4"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_017():
    """Test 17: Break and continue inside for loop"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(0)),
                            BinaryOp(Identifier("i"), "<", IntLiteral(5)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [
                                    IfStmt(
                                        BinaryOp(Identifier("i"), "==", IntLiteral(1)),
                                        ContinueStmt(),
                                    ),
                                    IfStmt(
                                        BinaryOp(Identifier("i"), "==", IntLiteral(4)),
                                        BreakStmt(),
                                    ),
                                    ExprStmt(FuncCall("printInt", [Identifier("i")])),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = "023"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_018():
    """Test 18: Switch statement with default"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(2)),
                        SwitchStmt(
                            Identifier("x"),
                            [
                                CaseStmt(
                                    IntLiteral(1),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("one")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                                CaseStmt(
                                    IntLiteral(2),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("two")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                            ],
                            DefaultStmt(
                                [
                                    ExprStmt(
                                        FuncCall(
                                            "printString",
                                            [StringLiteral("other")],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = "two"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_019():
    """Generated test 19: int_subtraction"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(9), "-", IntLiteral(4))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_020():
    """Generated test 20: int_division"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(21), "/", IntLiteral(3))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '7'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_021():
    """Generated test 21: int_modulo"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(29), "%", IntLiteral(6))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_022():
    """Generated test 22: nested_mul_add"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    BinaryOp(
                                        BinaryOp(IntLiteral(2), "+", IntLiteral(3)),
                                        "*",
                                        IntLiteral(4),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '20'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_023():
    """Generated test 23: nested_div_add"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    BinaryOp(
                                        IntLiteral(20),
                                        "/",
                                        BinaryOp(IntLiteral(3), "+", IntLiteral(2)),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '4'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_024():
    """Generated test 24: chained_subtraction"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    BinaryOp(
                                        BinaryOp(IntLiteral(30), "-", IntLiteral(5)),
                                        "-",
                                        IntLiteral(10),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '15'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_025():
    """Generated test 25: mul_with_nested_sub"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    BinaryOp(
                                        IntLiteral(6),
                                        "*",
                                        BinaryOp(IntLiteral(8), "-", IntLiteral(3)),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '30'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_026():
    """Generated test 26: sum_two_groups"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    BinaryOp(
                                        BinaryOp(IntLiteral(1), "+", IntLiteral(2)),
                                        "+",
                                        BinaryOp(IntLiteral(3), "+", IntLiteral(4)),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '10'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_027():
    """Generated test 27: division_then_mod"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(20), "%", IntLiteral(5))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '0'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_028():
    """Generated test 28: simple_add_large"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(100), "+", IntLiteral(23))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '123'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_029():
    """Generated test 29: expr_mix_1"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    BinaryOp(
                                        BinaryOp(IntLiteral(8), "*", IntLiteral(2)),
                                        "/",
                                        IntLiteral(4),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '4'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_030():
    """Generated test 30: expr_mix_2"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    BinaryOp(
                                        IntLiteral(18),
                                        "/",
                                        BinaryOp(IntLiteral(2), "+", IntLiteral(1)),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '6'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_031():
    """Generated test 31: multiple_vars_expression"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "a", IntLiteral(7)),
                        VarDecl(IntType(), "b", IntLiteral(5)),
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(Identifier("a"), "*", Identifier("b"))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '35'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_032():
    """Generated test 32: assignment_expression_result"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(0)),
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [AssignExpr(Identifier("x"), IntLiteral(8))],
                            ),
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("x")])),
                    ],
                ),
            ),
        ],
    )
    expected = '88'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_033():
    """Generated test 33: local_reassignment_then_print"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(2)),
                        ExprStmt(
                            AssignExpr(
                                Identifier("x"),
                                BinaryOp(Identifier("x"), "+", IntLiteral(9)),
                            ),
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("x")])),
                    ],
                ),
            ),
        ],
    )
    expected = '11'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_034():
    """Generated test 34: binary_in_assignment_expression"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(1)),
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    AssignExpr(
                                        Identifier("x"),
                                        BinaryOp(IntLiteral(6), "*", IntLiteral(7)),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '42'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_035():
    """Generated test 35: two_prints_from_same_vars"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(9)),
                        VarDecl(IntType(), "y", IntLiteral(3)),
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(Identifier("x"), "/", Identifier("y"))],
                            ),
                        ),
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(Identifier("x"), "%", Identifier("y"))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '30'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_036():
    """Generated test 36: float_literal_half"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("printFloat", [FloatLiteral(0.5)]))]),
            ),
        ],
    )
    expected = '0.5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_037():
    """Generated test 37: float_addition"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printFloat",
                                [BinaryOp(FloatLiteral(1.5), "+", FloatLiteral(2.25))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '3.75'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_038():
    """Generated test 38: float_subtraction"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printFloat",
                                [BinaryOp(FloatLiteral(5.5), "-", FloatLiteral(2.25))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '3.25'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_039():
    """Generated test 39: float_multiplication"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printFloat",
                                [BinaryOp(FloatLiteral(1.5), "*", FloatLiteral(2.0))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '3.0'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_040():
    """Generated test 40: float_division"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printFloat",
                                [BinaryOp(FloatLiteral(7.5), "/", FloatLiteral(2.5))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '3.0'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_041():
    """Generated test 41: float_prefix_minus"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall("printFloat", [PrefixOp("-", FloatLiteral(4.5))]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '-4.5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_042():
    """Generated test 42: float_unary_plus"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall("printFloat", [PrefixOp("+", FloatLiteral(6.25))]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '6.25'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_043():
    """Generated test 43: float_variable_expression"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(FloatType(), "a", FloatLiteral(2.5)),
                        VarDecl(FloatType(), "b", FloatLiteral(4.0)),
                        ExprStmt(
                            FuncCall(
                                "printFloat",
                                [BinaryOp(Identifier("a"), "*", Identifier("b"))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '10.0'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_044():
    """Generated test 44: float_assignment_and_print"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(FloatType(), "v", FloatLiteral(1.25)),
                        ExprStmt(
                            AssignExpr(
                                Identifier("v"),
                                BinaryOp(Identifier("v"), "+", FloatLiteral(0.75)),
                            ),
                        ),
                        ExprStmt(FuncCall("printFloat", [Identifier("v")])),
                    ],
                ),
            ),
        ],
    )
    expected = '2.0'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_045():
    """Generated test 45: float_function_return"""
    ast = Program(
        [
            FuncDecl(
                FloatType(),
                "twice",
                [Param(FloatType(), "x")],
                BlockStmt([ReturnStmt(BinaryOp(Identifier("x"), "+", Identifier("x")))]),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printFloat",
                                [FuncCall("twice", [FloatLiteral(1.25)])],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '2.5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_046():
    """Generated test 46: lt_true"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(1), "<", IntLiteral(2))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_047():
    """Generated test 47: lt_false"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(5), "<", IntLiteral(2))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '0'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_048():
    """Generated test 48: le_true"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(4), "<=", IntLiteral(4))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_049():
    """Generated test 49: gt_true"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(9), ">", IntLiteral(3))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_050():
    """Generated test 50: ge_false"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(2), ">=", IntLiteral(7))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '0'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_051():
    """Generated test 51: eq_true"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(6), "==", IntLiteral(6))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_052():
    """Generated test 52: ne_true"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(6), "!=", IntLiteral(5))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_053():
    """Generated test 53: logic_and_false"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(1), "&&", IntLiteral(0))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '0'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_054():
    """Generated test 54: logic_or_true"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(1), "||", IntLiteral(0))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_055():
    """Generated test 55: logic_or_false"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [BinaryOp(IntLiteral(0), "||", IntLiteral(0))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '0'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_056():
    """Generated test 56: not_zero"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [ExprStmt(FuncCall("printInt", [PrefixOp("!", IntLiteral(0))]))],
                ),
            ),
        ],
    )
    expected = '1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_057():
    """Generated test 57: not_nonzero"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [ExprStmt(FuncCall("printInt", [PrefixOp("!", IntLiteral(2))]))],
                ),
            ),
        ],
    )
    expected = '0'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_058():
    """Generated test 58: prefix_plus_int"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [ExprStmt(FuncCall("printInt", [PrefixOp("+", IntLiteral(8))]))],
                ),
            ),
        ],
    )
    expected = '8'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_059():
    """Generated test 59: prefix_minus_int"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [ExprStmt(FuncCall("printInt", [PrefixOp("-", IntLiteral(8))]))],
                ),
            ),
        ],
    )
    expected = '-8'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_060():
    """Generated test 60: prefix_increment_variable"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(1)),
                        ExprStmt(
                            FuncCall("printInt", [PrefixOp("++", Identifier("x"))]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '2'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_061():
    """Generated test 61: prefix_decrement_variable"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(3)),
                        ExprStmt(
                            FuncCall("printInt", [PrefixOp("--", Identifier("x"))]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '2'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_062():
    """Generated test 62: postfix_increment_variable"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(7)),
                        ExprStmt(
                            FuncCall("printInt", [PostfixOp("++", Identifier("x"))]),
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("x")])),
                    ],
                ),
            ),
        ],
    )
    expected = '78'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_063():
    """Generated test 63: postfix_decrement_variable"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(7)),
                        ExprStmt(
                            FuncCall("printInt", [PostfixOp("--", Identifier("x"))]),
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("x")])),
                    ],
                ),
            ),
        ],
    )
    expected = '76'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_064():
    """Generated test 64: assignment_expr_then_math"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(0)),
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    BinaryOp(
                                        AssignExpr(Identifier("x"), IntLiteral(5)),
                                        "+",
                                        IntLiteral(3),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '8'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_065():
    """Generated test 65: assignment_expr_preserves_new_value"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(10)),
                        ExprStmt(AssignExpr(Identifier("x"), IntLiteral(12))),
                        ExprStmt(FuncCall("printInt", [Identifier("x")])),
                    ],
                ),
            ),
        ],
    )
    expected = '12'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_066():
    """Generated test 66: nested_assignment_shape"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "a", IntLiteral(0)),
                        VarDecl(IntType(), "b", IntLiteral(0)),
                        ExprStmt(
                            AssignExpr(
                                Identifier("a"),
                                AssignExpr(Identifier("b"), IntLiteral(9)),
                            ),
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("a")])),
                        ExprStmt(FuncCall("printInt", [Identifier("b")])),
                    ],
                ),
            ),
        ],
    )
    expected = '99'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_067():
    """Generated test 67: assignment_in_if_condition"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(0)),
                        IfStmt(
                            AssignExpr(Identifier("x"), IntLiteral(1)),
                            ExprStmt(FuncCall("printString", [StringLiteral("T")])),
                            ExprStmt(FuncCall("printString", [StringLiteral("F")])),
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("x")])),
                    ],
                ),
            ),
        ],
    )
    expected = 'T1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_068():
    """Generated test 68: decrement_then_assignment_expr"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(5)),
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    AssignExpr(
                                        Identifier("x"),
                                        PrefixOp("--", Identifier("x")),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '4'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_069():
    """Generated test 69: increment_sequence"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(4)),
                        ExprStmt(
                            FuncCall("printInt", [PrefixOp("++", Identifier("x"))]),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [PostfixOp("++", Identifier("x"))]),
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("x")])),
                    ],
                ),
            ),
        ],
    )
    expected = '556'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_070():
    """Generated test 70: if_false_else_branch"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        IfStmt(
                            BinaryOp(IntLiteral(5), "<", IntLiteral(3)),
                            ExprStmt(FuncCall("printString", [StringLiteral("A")])),
                            ExprStmt(FuncCall("printString", [StringLiteral("B")])),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'B'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_071():
    """Generated test 71: if_without_else_no_output"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        IfStmt(
                            BinaryOp(IntLiteral(5), "<", IntLiteral(3)),
                            ExprStmt(FuncCall("printString", [StringLiteral("A")])),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = ''
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_072():
    """Generated test 72: nested_if_true_path"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        IfStmt(
                            BinaryOp(IntLiteral(2), "==", IntLiteral(2)),
                            BlockStmt(
                                [
                                    IfStmt(
                                        BinaryOp(IntLiteral(3), ">", IntLiteral(1)),
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("ok")],
                                            ),
                                        ),
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("bad")],
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                            ExprStmt(FuncCall("printString", [StringLiteral("outer")])),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'ok'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_073():
    """Generated test 73: while_counting"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "i", IntLiteral(0)),
                        WhileStmt(
                            BinaryOp(Identifier("i"), "<", IntLiteral(4)),
                            BlockStmt(
                                [
                                    ExprStmt(FuncCall("printInt", [Identifier("i")])),
                                    ExprStmt(
                                        AssignExpr(
                                            Identifier("i"),
                                            BinaryOp(
                                                Identifier("i"),
                                                "+",
                                                IntLiteral(1),
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '0123'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_074():
    """Generated test 74: while_accumulate_sum"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "i", IntLiteral(1)),
                        VarDecl(IntType(), "sum", IntLiteral(0)),
                        WhileStmt(
                            BinaryOp(Identifier("i"), "<=", IntLiteral(4)),
                            BlockStmt(
                                [
                                    ExprStmt(
                                        AssignExpr(
                                            Identifier("sum"),
                                            BinaryOp(
                                                Identifier("sum"),
                                                "+",
                                                Identifier("i"),
                                            ),
                                        ),
                                    ),
                                    ExprStmt(
                                        AssignExpr(
                                            Identifier("i"),
                                            BinaryOp(
                                                Identifier("i"),
                                                "+",
                                                IntLiteral(1),
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("sum")])),
                    ],
                ),
            ),
        ],
    )
    expected = '10'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_075():
    """Generated test 75: for_basic_count"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(1)),
                            BinaryOp(Identifier("i"), "<=", IntLiteral(3)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [ExprStmt(FuncCall("printInt", [Identifier("i")]))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '123'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_076():
    """Generated test 76: for_zero_iterations"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(5)),
                            BinaryOp(Identifier("i"), "<", IntLiteral(5)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [ExprStmt(FuncCall("printInt", [Identifier("i")]))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = ''
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_077():
    """Generated test 77: for_sum_loop"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "sum", IntLiteral(0)),
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(1)),
                            BinaryOp(Identifier("i"), "<=", IntLiteral(4)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [
                                    ExprStmt(
                                        AssignExpr(
                                            Identifier("sum"),
                                            BinaryOp(
                                                Identifier("sum"),
                                                "+",
                                                Identifier("i"),
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("sum")])),
                    ],
                ),
            ),
        ],
    )
    expected = '10'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_078():
    """Generated test 78: for_with_prefix_update"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(0)),
                            BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                            PrefixOp("++", Identifier("i")),
                            BlockStmt(
                                [ExprStmt(FuncCall("printInt", [Identifier("i")]))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '012'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_079():
    """Generated test 79: for_with_external_init_assignment"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "i", IntLiteral(0)),
                        ForStmt(
                            ExprStmt(AssignExpr(Identifier("i"), IntLiteral(2))),
                            BinaryOp(Identifier("i"), "<=", IntLiteral(4)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [ExprStmt(FuncCall("printInt", [Identifier("i")]))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '234'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_080():
    """Generated test 80: for_continue_skip_one"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(0)),
                            BinaryOp(Identifier("i"), "<", IntLiteral(4)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [
                                    IfStmt(
                                        BinaryOp(Identifier("i"), "==", IntLiteral(1)),
                                        ContinueStmt(),
                                    ),
                                    ExprStmt(FuncCall("printInt", [Identifier("i")])),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '023'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_081():
    """Generated test 81: for_break_stop_early"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(0)),
                            BinaryOp(Identifier("i"), "<", IntLiteral(6)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [
                                    IfStmt(
                                        BinaryOp(Identifier("i"), "==", IntLiteral(3)),
                                        BreakStmt(),
                                    ),
                                    ExprStmt(FuncCall("printInt", [Identifier("i")])),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '012'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_082():
    """Generated test 82: nested_for_rectangular_output"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(0)),
                            BinaryOp(Identifier("i"), "<", IntLiteral(2)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [
                                    ForStmt(
                                        VarDecl(IntType(), "j", IntLiteral(0)),
                                        BinaryOp(Identifier("j"), "<", IntLiteral(2)),
                                        PostfixOp("++", Identifier("j")),
                                        BlockStmt(
                                            [
                                                ExprStmt(
                                                    FuncCall(
                                                        "printInt",
                                                        [Identifier("i")],
                                                    ),
                                                ),
                                                ExprStmt(
                                                    FuncCall(
                                                        "printInt",
                                                        [Identifier("j")],
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '00011011'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_083():
    """Generated test 83: for_body_if_else"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(0)),
                            BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [
                                    IfStmt(
                                        BinaryOp(Identifier("i"), "==", IntLiteral(1)),
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("M")],
                                            ),
                                        ),
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("N")],
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'NMN'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_084():
    """Generated test 84: while_with_if_filter"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "i", IntLiteral(0)),
                        WhileStmt(
                            BinaryOp(Identifier("i"), "<", IntLiteral(5)),
                            BlockStmt(
                                [
                                    IfStmt(
                                        BinaryOp(
                                            BinaryOp(
                                                Identifier("i"),
                                                "%",
                                                IntLiteral(2),
                                            ),
                                            "==",
                                            IntLiteral(0),
                                        ),
                                        ExprStmt(
                                            FuncCall("printInt", [Identifier("i")]),
                                        ),
                                    ),
                                    ExprStmt(
                                        AssignExpr(
                                            Identifier("i"),
                                            BinaryOp(
                                                Identifier("i"),
                                                "+",
                                                IntLiteral(1),
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '024'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_085():
    """Generated test 85: for_product_loop"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "s", IntLiteral(1)),
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(1)),
                            BinaryOp(Identifier("i"), "<=", IntLiteral(3)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [
                                    ExprStmt(
                                        AssignExpr(
                                            Identifier("s"),
                                            BinaryOp(
                                                Identifier("s"),
                                                "*",
                                                Identifier("i"),
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("s")])),
                    ],
                ),
            ),
        ],
    )
    expected = '6'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_086():
    """Generated test 86: function_no_param_int"""
    ast = Program(
        [
            FuncDecl(IntType(), "value", [], BlockStmt([ReturnStmt(IntLiteral(9))])),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("printInt", [FuncCall("value", [])]))]),
            ),
        ],
    )
    expected = '9'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_087():
    """Generated test 87: function_three_params"""
    ast = Program(
        [
            FuncDecl(
                IntType(),
                "add",
                [Param(IntType(), "a"), Param(IntType(), "b")],
                BlockStmt([ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))]),
            ),
            FuncDecl(
                IntType(),
                "sum3",
                [Param(IntType(), "a"), Param(IntType(), "b"), Param(IntType(), "c")],
                BlockStmt(
                    [
                        ReturnStmt(
                            BinaryOp(
                                FuncCall("add", [Identifier("a"), Identifier("b")]),
                                "+",
                                Identifier("c"),
                            ),
                        ),
                    ],
                ),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    FuncCall(
                                        "sum3",
                                        [IntLiteral(1), IntLiteral(2), IntLiteral(3)],
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '6'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_088():
    """Generated test 88: void_function_prints"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "greet",
                [],
                BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("hi")]))]),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("greet", []))]),
            ),
        ],
    )
    expected = 'hi'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_089():
    """Generated test 89: function_local_variables"""
    ast = Program(
        [
            FuncDecl(
                IntType(),
                "calc",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(4)),
                        VarDecl(IntType(), "y", IntLiteral(5)),
                        ReturnStmt(BinaryOp(Identifier("x"), "*", Identifier("y"))),
                    ],
                ),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("printInt", [FuncCall("calc", [])]))]),
            ),
        ],
    )
    expected = '20'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_090():
    """Generated test 90: function_call_in_expression"""
    ast = Program(
        [
            FuncDecl(
                IntType(),
                "inc",
                [Param(IntType(), "x")],
                BlockStmt([ReturnStmt(BinaryOp(Identifier("x"), "+", IntLiteral(1)))]),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    BinaryOp(
                                        FuncCall("inc", [IntLiteral(4)]),
                                        "+",
                                        IntLiteral(5),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '10'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_091():
    """Generated test 91: iterative_factorial_small"""
    ast = Program(
        [
            FuncDecl(
                IntType(),
                "fact",
                [Param(IntType(), "n")],
                BlockStmt(
                    [
                        VarDecl(IntType(), "acc", IntLiteral(1)),
                        WhileStmt(
                            BinaryOp(Identifier("n"), ">", IntLiteral(1)),
                            BlockStmt(
                                [
                                    ExprStmt(
                                        AssignExpr(
                                            Identifier("acc"),
                                            BinaryOp(
                                                Identifier("acc"),
                                                "*",
                                                Identifier("n"),
                                            ),
                                        ),
                                    ),
                                    ExprStmt(
                                        AssignExpr(
                                            Identifier("n"),
                                            BinaryOp(
                                                Identifier("n"),
                                                "-",
                                                IntLiteral(1),
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        ReturnStmt(Identifier("acc")),
                    ],
                ),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall("printInt", [FuncCall("fact", [IntLiteral(5)])]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '120'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_092():
    """Generated test 92: iterative_sum_to_n"""
    ast = Program(
        [
            FuncDecl(
                IntType(),
                "sumTo",
                [Param(IntType(), "n")],
                BlockStmt(
                    [
                        VarDecl(IntType(), "acc", IntLiteral(0)),
                        VarDecl(IntType(), "i", IntLiteral(1)),
                        WhileStmt(
                            BinaryOp(Identifier("i"), "<=", Identifier("n")),
                            BlockStmt(
                                [
                                    ExprStmt(
                                        AssignExpr(
                                            Identifier("acc"),
                                            BinaryOp(
                                                Identifier("acc"),
                                                "+",
                                                Identifier("i"),
                                            ),
                                        ),
                                    ),
                                    ExprStmt(
                                        AssignExpr(
                                            Identifier("i"),
                                            BinaryOp(
                                                Identifier("i"),
                                                "+",
                                                IntLiteral(1),
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        ReturnStmt(Identifier("acc")),
                    ],
                ),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall("printInt", [FuncCall("sumTo", [IntLiteral(6)])]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '21'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_093():
    """Generated test 93: function_return_string"""
    ast = Program(
        [
            FuncDecl(
                StringType(),
                "word",
                [],
                BlockStmt([ReturnStmt(StringLiteral("TyC"))]),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("printString", [FuncCall("word", [])]))]),
            ),
        ],
    )
    expected = 'TyC'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_094():
    """Generated test 94: function_taking_string_param"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "echo",
                [Param(StringType(), "s")],
                BlockStmt([ExprStmt(FuncCall("printString", [Identifier("s")]))]),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("echo", [StringLiteral("compiler")]))]),
            ),
        ],
    )
    expected = 'compiler'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_095():
    """Generated test 95: two_functions_chain"""
    ast = Program(
        [
            FuncDecl(
                IntType(),
                "square",
                [Param(IntType(), "x")],
                BlockStmt([ReturnStmt(BinaryOp(Identifier("x"), "*", Identifier("x")))]),
            ),
            FuncDecl(
                IntType(),
                "quad",
                [Param(IntType(), "x")],
                BlockStmt(
                    [
                        ReturnStmt(
                            FuncCall("square", [FuncCall("square", [Identifier("x")])]),
                        ),
                    ],
                ),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall("printInt", [FuncCall("quad", [IntLiteral(2)])]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '16'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_096():
    """Generated test 96: void_function_called_twice"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "bang",
                [],
                BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("!")]))]),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [ExprStmt(FuncCall("bang", [])), ExprStmt(FuncCall("bang", []))],
                ),
            ),
        ],
    )
    expected = '!!'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_097():
    """Generated test 97: function_with_if_assignment_then_return"""
    ast = Program(
        [
            FuncDecl(
                IntType(),
                "sign",
                [Param(IntType(), "x")],
                BlockStmt(
                    [
                        VarDecl(IntType(), "out", IntLiteral(0)),
                        IfStmt(
                            BinaryOp(Identifier("x"), ">", IntLiteral(0)),
                            ExprStmt(AssignExpr(Identifier("out"), IntLiteral(1))),
                            ExprStmt(AssignExpr(Identifier("out"), IntLiteral(0))),
                        ),
                        ReturnStmt(Identifier("out")),
                    ],
                ),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall("printInt", [FuncCall("sign", [IntLiteral(3)])]),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [FuncCall("sign", [IntLiteral(0)])]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '10'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_098():
    """Generated test 98: function_used_inside_loop"""
    ast = Program(
        [
            FuncDecl(
                IntType(),
                "inc",
                [Param(IntType(), "x")],
                BlockStmt([ReturnStmt(BinaryOp(Identifier("x"), "+", IntLiteral(1)))]),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(0)),
                            BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [
                                    ExprStmt(
                                        FuncCall(
                                            "printInt",
                                            [FuncCall("inc", [Identifier("i")])],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '123'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_099():
    """Generated test 99: function_return_assignment_expr_value"""
    ast = Program(
        [
            FuncDecl(
                IntType(),
                "setfive",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(0)),
                        ReturnStmt(AssignExpr(Identifier("x"), IntLiteral(5))),
                    ],
                ),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("printInt", [FuncCall("setfive", [])]))]),
            ),
        ],
    )
    expected = '5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_100():
    """Generated test 100: struct_init_print_x"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "p",
                            StructLiteral([IntLiteral(1), IntLiteral(2)]),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p"), "x")]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_101():
    """Generated test 101: struct_init_print_y"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "p",
                            StructLiteral([IntLiteral(1), IntLiteral(7)]),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p"), "y")]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '7'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_102():
    """Generated test 102: struct_field_update_x"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "p",
                            StructLiteral([IntLiteral(1), IntLiteral(2)]),
                        ),
                        ExprStmt(
                            AssignExpr(
                                MemberAccess(Identifier("p"), "x"),
                                IntLiteral(5),
                            ),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p"), "x")]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_103():
    """Generated test 103: struct_field_update_y"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "p",
                            StructLiteral([IntLiteral(3), IntLiteral(4)]),
                        ),
                        ExprStmt(
                            AssignExpr(
                                MemberAccess(Identifier("p"), "y"),
                                IntLiteral(8),
                            ),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p"), "y")]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '8'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_104():
    """Generated test 104: struct_assignment_then_read"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "a",
                            StructLiteral([IntLiteral(9), IntLiteral(6)]),
                        ),
                        VarDecl(StructType("Point"), "b"),
                        ExprStmt(AssignExpr(Identifier("b"), Identifier("a"))),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("b"), "x")]),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("b"), "y")]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '96'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_105():
    """Generated test 105: struct_literal_assigned_later"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(StructType("Point"), "p"),
                        ExprStmt(
                            AssignExpr(
                                Identifier("p"),
                                StructLiteral([IntLiteral(2), IntLiteral(5)]),
                            ),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p"), "x")]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '2'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_106():
    """Generated test 106: struct_member_assignment_expr_result"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "p",
                            StructLiteral([IntLiteral(0), IntLiteral(0)]),
                        ),
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    AssignExpr(
                                        MemberAccess(Identifier("p"), "x"),
                                        IntLiteral(7),
                                    ),
                                ],
                            ),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p"), "x")]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '77'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_107():
    """Generated test 107: function_takes_struct_param"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                IntType(),
                "getx",
                [Param(StructType("Point"), "p")],
                BlockStmt([ReturnStmt(MemberAccess(Identifier("p"), "x"))]),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "p",
                            StructLiteral([IntLiteral(4), IntLiteral(9)]),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [FuncCall("getx", [Identifier("p")])]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '4'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_108():
    """Generated test 108: function_returns_struct"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                StructType("Point"),
                "make",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "p",
                            StructLiteral([IntLiteral(3), IntLiteral(8)]),
                        ),
                        ReturnStmt(Identifier("p")),
                    ],
                ),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [MemberAccess(FuncCall("make", []), "y")],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '8'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_109():
    """Generated test 109: struct_field_passed_to_function"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                IntType(),
                "twice",
                [Param(IntType(), "x")],
                BlockStmt([ReturnStmt(BinaryOp(Identifier("x"), "+", Identifier("x")))]),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "p",
                            StructLiteral([IntLiteral(2), IntLiteral(6)]),
                        ),
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    FuncCall(
                                        "twice",
                                        [MemberAccess(Identifier("p"), "y")],
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '12'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_110():
    """Generated test 110: two_struct_types_in_program"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            StructDecl("Pair", [MemberDecl(IntType(), "a"), MemberDecl(IntType(), "b")]),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Pair"),
                            "p",
                            StructLiteral([IntLiteral(7), IntLiteral(1)]),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p"), "a")]),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p"), "b")]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '71'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_111():
    """Generated test 111: struct_field_used_in_arithmetic"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "p",
                            StructLiteral([IntLiteral(4), IntLiteral(5)]),
                        ),
                        ExprStmt(
                            FuncCall(
                                "printInt",
                                [
                                    BinaryOp(
                                        MemberAccess(Identifier("p"), "x"),
                                        "+",
                                        MemberAccess(Identifier("p"), "y"),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '9'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_112():
    """Generated test 112: struct_returned_then_assigned"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                StructType("Point"),
                "mk",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "tmp",
                            StructLiteral([IntLiteral(8), IntLiteral(6)]),
                        ),
                        ReturnStmt(Identifier("tmp")),
                    ],
                ),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(StructType("Point"), "p"),
                        ExprStmt(AssignExpr(Identifier("p"), FuncCall("mk", []))),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p"), "x")]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '8'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_113():
    """Generated test 113: struct_reassign_multiple_times"""
    ast = Program(
        [
            StructDecl(
                "Point",
                [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")],
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(
                            StructType("Point"),
                            "p",
                            StructLiteral([IntLiteral(1), IntLiteral(1)]),
                        ),
                        ExprStmt(
                            AssignExpr(
                                Identifier("p"),
                                StructLiteral([IntLiteral(3), IntLiteral(4)]),
                            ),
                        ),
                        ExprStmt(
                            AssignExpr(
                                MemberAccess(Identifier("p"), "x"),
                                IntLiteral(8),
                            ),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p"), "x")]),
                        ),
                        ExprStmt(
                            FuncCall("printInt", [MemberAccess(Identifier("p"), "y")]),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '84'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_114():
    """Generated test 114: switch_first_case"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(1)),
                        SwitchStmt(
                            Identifier("x"),
                            [
                                CaseStmt(
                                    IntLiteral(1),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("one")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                                CaseStmt(
                                    IntLiteral(2),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("two")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'one'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_115():
    """Generated test 115: switch_default_case"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(9)),
                        SwitchStmt(
                            Identifier("x"),
                            [
                                CaseStmt(
                                    IntLiteral(1),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("one")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                            ],
                            DefaultStmt(
                                [
                                    ExprStmt(
                                        FuncCall(
                                            "printString",
                                            [StringLiteral("other")],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'other'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_116():
    """Generated test 116: switch_no_match_no_default"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(9)),
                        SwitchStmt(
                            Identifier("x"),
                            [
                                CaseStmt(
                                    IntLiteral(1),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("one")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = ''
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_117():
    """Generated test 117: switch_last_case"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(3)),
                        SwitchStmt(
                            Identifier("x"),
                            [
                                CaseStmt(
                                    IntLiteral(1),
                                    [
                                        ExprStmt(FuncCall("printInt", [IntLiteral(1)])),
                                        BreakStmt(),
                                    ],
                                ),
                                CaseStmt(
                                    IntLiteral(2),
                                    [
                                        ExprStmt(FuncCall("printInt", [IntLiteral(2)])),
                                        BreakStmt(),
                                    ],
                                ),
                                CaseStmt(
                                    IntLiteral(3),
                                    [
                                        ExprStmt(FuncCall("printInt", [IntLiteral(3)])),
                                        BreakStmt(),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = '3'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_118():
    """Generated test 118: switch_fallthrough_two_cases"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(1)),
                        SwitchStmt(
                            Identifier("x"),
                            [
                                CaseStmt(
                                    IntLiteral(1),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("A")],
                                            ),
                                        ),
                                    ],
                                ),
                                CaseStmt(
                                    IntLiteral(2),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("B")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'AB'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_119():
    """Generated test 119: switch_case_multiple_statements"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(2)),
                        SwitchStmt(
                            Identifier("x"),
                            [
                                CaseStmt(
                                    IntLiteral(2),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("x")],
                                            ),
                                        ),
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("y")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'xy'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_120():
    """Generated test 120: switch_expression_binary"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "a", IntLiteral(1)),
                        VarDecl(IntType(), "b", IntLiteral(2)),
                        SwitchStmt(
                            BinaryOp(Identifier("a"), "+", Identifier("b")),
                            [
                                CaseStmt(
                                    IntLiteral(3),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("sum3")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                            ],
                            DefaultStmt(
                                [
                                    ExprStmt(
                                        FuncCall("printString", [StringLiteral("bad")]),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'sum3'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_121():
    """Generated test 121: switch_inside_function"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "show",
                [Param(IntType(), "x")],
                BlockStmt(
                    [
                        SwitchStmt(
                            Identifier("x"),
                            [
                                CaseStmt(
                                    IntLiteral(4),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("hit")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                            ],
                            DefaultStmt(
                                [
                                    ExprStmt(
                                        FuncCall("printString", [StringLiteral("miss")]),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("show", [IntLiteral(4)]))]),
            ),
        ],
    )
    expected = 'hit'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_122():
    """Generated test 122: switch_default_after_fallthrough"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(2)),
                        SwitchStmt(
                            Identifier("x"),
                            [
                                CaseStmt(
                                    IntLiteral(1),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("A")],
                                            ),
                                        ),
                                    ],
                                ),
                                CaseStmt(
                                    IntLiteral(2),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("B")],
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                            DefaultStmt(
                                [
                                    ExprStmt(
                                        FuncCall("printString", [StringLiteral("C")]),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'BC'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_123():
    """Generated test 123: switch_match_middle_breaks"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(IntType(), "x", IntLiteral(2)),
                        SwitchStmt(
                            Identifier("x"),
                            [
                                CaseStmt(
                                    IntLiteral(1),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("A")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                                CaseStmt(
                                    IntLiteral(2),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("B")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                                CaseStmt(
                                    IntLiteral(3),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("C")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                            ],
                            DefaultStmt(
                                [
                                    ExprStmt(
                                        FuncCall("printString", [StringLiteral("D")]),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'B'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_124():
    """Generated test 124: string_literal_empty"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("")]))]),
            ),
        ],
    )
    expected = ''
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_125():
    """Generated test 125: string_literal_basic"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("TyC")]))]),
            ),
        ],
    )
    expected = 'TyC'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_126():
    """Generated test 126: string_variable_print"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(StringType(), "s", StringLiteral("hello")),
                        ExprStmt(FuncCall("printString", [Identifier("s")])),
                    ],
                ),
            ),
        ],
    )
    expected = 'hello'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_127():
    """Generated test 127: string_assignment"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        VarDecl(StringType(), "s", StringLiteral("a")),
                        ExprStmt(AssignExpr(Identifier("s"), StringLiteral("b"))),
                        ExprStmt(FuncCall("printString", [Identifier("s")])),
                    ],
                ),
            ),
        ],
    )
    expected = 'b'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_128():
    """Generated test 128: two_string_prints"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(FuncCall("printString", [StringLiteral("A")])),
                        ExprStmt(FuncCall("printString", [StringLiteral("B")])),
                    ],
                ),
            ),
        ],
    )
    expected = 'AB'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_129():
    """Generated test 129: string_in_if_branch"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        IfStmt(
                            IntLiteral(1),
                            ExprStmt(FuncCall("printString", [StringLiteral("yes")])),
                            ExprStmt(FuncCall("printString", [StringLiteral("no")])),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'yes'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_130():
    """Generated test 130: string_function_roundtrip"""
    ast = Program(
        [
            FuncDecl(
                StringType(),
                "get",
                [],
                BlockStmt([ReturnStmt(StringLiteral("done"))]),
            ),
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("printString", [FuncCall("get", [])]))]),
            ),
        ],
    )
    expected = 'done'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_131():
    """Generated test 131: mixed_print_string_then_int"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(FuncCall("printString", [StringLiteral("n=")])),
                        ExprStmt(FuncCall("printInt", [IntLiteral(7)])),
                    ],
                ),
            ),
        ],
    )
    expected = 'n=7'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_132():
    """Generated test 132: escape_like_text_literal"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("a\\tb")]))]),
            ),
        ],
    )
    expected = 'a\\tb'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_133():
    """Generated test 133: quoted_text_literal"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [ExprStmt(FuncCall("printString", [StringLiteral("say \"hi\"")]))],
                ),
            ),
        ],
    )
    expected = 'say "hi"'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_134():
    """Generated test 134: string_then_switch"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(FuncCall("printString", [StringLiteral("mode:")])),
                        VarDecl(IntType(), "x", IntLiteral(1)),
                        SwitchStmt(
                            Identifier("x"),
                            [
                                CaseStmt(
                                    IntLiteral(1),
                                    [
                                        ExprStmt(
                                            FuncCall(
                                                "printString",
                                                [StringLiteral("on")],
                                            ),
                                        ),
                                        BreakStmt(),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'mode:on'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_135():
    """Generated test 135: string_then_loop_digits"""
    ast = Program(
        [
            FuncDecl(
                VoidType(),
                "main",
                [],
                BlockStmt(
                    [
                        ExprStmt(FuncCall("printString", [StringLiteral("v")])),
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(1)),
                            BinaryOp(Identifier("i"), "<=", IntLiteral(3)),
                            PostfixOp("++", Identifier("i")),
                            BlockStmt(
                                [ExprStmt(FuncCall("printInt", [Identifier("i")]))],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    expected = 'v123'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
