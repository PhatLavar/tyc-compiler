"""
Static Semantic Checker for TyC Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the TyC procedural programming language. It performs type checking,
scope management, type inference, and detects all semantic errors as
specified in the TyC language specification.
"""

from functools import reduce
from typing import (
    Dict,
    List,
    Set,
    Optional,
    Any,
    Tuple,
    NamedTuple,
    Union,
    TYPE_CHECKING,
)
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode,
    Program,
    StructDecl,
    MemberDecl,
    FuncDecl,
    Param,
    VarDecl,
    IfStmt,
    WhileStmt,
    ForStmt,
    BreakStmt,
    ContinueStmt,
    ReturnStmt,
    BlockStmt,
    SwitchStmt,
    CaseStmt,
    DefaultStmt,
    Type,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    BinaryOp,
    PrefixOp,
    PostfixOp,
    AssignExpr,
    MemberAccess,
    FuncCall,
    Identifier,
    StructLiteral,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    ExprStmt,
    Expr,
    Stmt,
    Decl,
)

# Type aliases for better type hints
TyCType = Union[IntType, FloatType, StringType, VoidType, StructType]
from .static_error import (
    StaticError,
    Redeclared,
    UndeclaredIdentifier,
    UndeclaredFunction,
    UndeclaredStruct,
    TypeCannotBeInferred,
    TypeMismatchInStatement,
    TypeMismatchInExpression,
    MustInLoop,
)


class StaticChecker(ASTVisitor):
    # ======================================================================
    # INITIALIZATION -------------------------------------------------------
    # ======================================================================
    def __init__(self):
        self.global_structs: Dict[str, StructDecl] = {}
        self.global_functions: Dict[str, FuncDecl] = {}
        self.scope_stack: List[Dict[str, Any]] = [{}]
        self.unresolved_autos: Dict[str, VarDecl] = {}

        self.loop_depth: int = 0
        self.switch_depth: int = 0
        self.current_function_return_type: Optional[Any] = None
        self.inferred_return_type: Optional[Any] = None

        self.builtin_functions = {
            "readInt": (IntType(), []),
            "readFloat": (FloatType(), []),
            "readString": (StringType(), []),
            "printInt": (VoidType(), [IntType()]),
            "printFloat": (VoidType(), [FloatType()]),
            "printString": (VoidType(), [StringType()]),
        }

    def _reset(self):
        """Reset all checker state before checking a new program"""
        self.global_structs.clear()
        self.global_functions.clear()
        self.scope_stack.clear()
        self.unresolved_autos.clear()

        self.loop_depth = 0
        self.current_function_return_type = None
        self.inferred_return_type = None

    def check_program(self, node: Program):
        """Entry point for semantic checking from the test harness."""
        return self.visit_program(node)


    # ======================================================================
    # HELPERS --------------------------------------------------------------
    # ======================================================================
    def _enter_scope(self):
        self.scope_stack.append({})

    def _exit_scope(self):
        current_scope = self.scope_stack.pop()
        for var_name, var_decl in list(self.unresolved_autos.items()):
            if var_name in current_scope and current_scope[var_name] is None:
                del self.unresolved_autos[var_name]
                raise TypeCannotBeInferred(var_decl)
            
    def _lookup(self, name: str) -> Tuple[bool, Optional[Any]]:
        for scope in reversed(self.scope_stack):
            if name in scope:
                return True, scope[name]
        return False, None

    def _is_int(self, typ):
        return isinstance(typ, IntType)
    
    def _is_numeric(self, typ):
        return isinstance(typ, (IntType, FloatType))

    def _is_compatible(self, typ1, typ2):
        if type(typ1) != type(typ2): return False
        if isinstance(typ1, StructType): return typ1.struct_name == typ2.struct_name
        return True


    # ======================================================================
    # TOP-LEVEL VISITOR ----------------------------------------------------
    # ======================================================================
    # PROGRAM VISITOR
    def visit_program(self, node: "Program", o: Any = None):
        """Main semantic checking entry point"""
        self._reset()

        # Pass 1: Collect global declarations
        for decl in node.decls:
            if isinstance(decl, StructDecl):
                if decl.name in self.global_structs:
                    raise Redeclared("Struct", decl.name)
                self.global_structs[decl.name] = decl
            
            elif isinstance(decl, FuncDecl):
                if decl.name in self.global_functions:
                    raise Redeclared("Function", decl.name)
                self.global_functions[decl.name] = decl
        
        # Pass 2: Check each declaration
        for decl in node.decls:
            self.visit(decl)

        return None

    # STRUCT VISITOR
    def visit_struct_decl(self, node: "StructDecl", o: Any = None):
        seen_members = set()
        for member in node.members:
            if member.name in seen_members:
                raise Redeclared("Member", member.name)
            seen_members.add(member.name)
            self.visit(member)
        return None

    def visit_member_decl(self, node: "MemberDecl", o: Any = None):
        self.visit(node.member_type)
        return None

    # FUNCTION VISITOR
    def visit_func_decl(self, node: "FuncDecl", o: Any = None):
        self._enter_scope()
        self.loop_depth = 0
        self.inferred_return_type = None
        
        # Parameters
        for param in node.params:
            if param.name in self.scope_stack[-1]:
                raise Redeclared("Parameter", param.name)
            param_type = self.visit(param.param_type)
            self.scope_stack[-1][param.name] = param_type

        self.current_function_return_type = self.visit(node.return_type) if node.return_type else None
        
        for stmt in node.body.statements:
            self.visit(stmt)

        if self.current_function_return_type is None and self.inferred_return_type is None:
            self.inferred_return_type = VoidType()
        
        self._exit_scope()
        return None


    def visit_param(self, node: "Param", o: Any = None):
        return self.visit(node.param_type)


    # ======================================================================
    # TYPE SYSTEM VISITOR --------------------------------------------------
    # ======================================================================
    def visit_int_type(self, node: "IntType", o: Any = None):
        return IntType()

    def visit_float_type(self, node: "FloatType", o: Any = None):
        return FloatType()

    def visit_string_type(self, node: "StringType", o: Any = None):
        return StringType()

    def visit_void_type(self, node: "VoidType", o: Any = None):
        return VoidType()

    def visit_struct_type(self, node: "StructType", o: Any = None):
        if node.struct_name not in self.global_structs:
            raise UndeclaredStruct(node.struct_name)
        return node


    # ======================================================================
    # STATEMENTS VISITOR ---------------------------------------------------
    # ======================================================================
    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        self._enter_scope()
        for stmt in node.statements:
            self.visit(stmt)
        self._exit_scope()
        return None

    def visit_var_decl(self, node: "VarDecl", o: Any = None):
        current_scope = self.scope_stack[-1]

        if node.name in current_scope:
            raise Redeclared("Variable", node.name)
            
        if node.var_type is None:   # auto
            current_scope[node.name] = None
            self.unresolved_autos[node.name] = node

            if node.init_value:
                inferred_type = self.visit(node.init_value)
                current_scope[node.name] = inferred_type
                if inferred_type is not None:
                    self.unresolved_autos.pop(node.name, None)
        
        else:
            declared_type = self.visit(node.var_type)
            current_scope[node.name] = declared_type
            if node.init_value:
                if isinstance(node.init_value, StructLiteral):
                    self.visit(node.init_value)
                else:
                    init_type = self.visit(node.init_value)
                    if not self._is_compatible(init_type, declared_type):
                        raise TypeMismatchInStatement(node)
        return None
    
    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        condition_type = self.visit(node.condition)
        if not self._is_int(condition_type):
            raise TypeMismatchInStatement(node)
        self.visit(node.then_stmt)
        if node.else_stmt:
            self.visit(node.else_stmt)
        return None

    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        condition_type = self.visit(node.condition)
        if not self._is_int(condition_type):
            raise TypeMismatchInStatement(node)
        self.loop_depth += 1
        self.visit(node.body)
        self.loop_depth -= 1
        return None

    def visit_for_stmt(self, node: "ForStmt", o: Any = None):
        if node.init:
            self.visit(node.init)
        if node.condition:
            condition_type = self.visit(node.condition)
            if not self._is_int(condition_type):
                raise TypeMismatchInStatement(node)
        if node.update:
            self.visit(node.update)

        self.loop_depth += 1
        self._enter_scope()
        self.visit(node.body)
        self._exit_scope()
        self.loop_depth -= 1
        return None

    def visit_switch_stmt(self, node: "SwitchStmt", o: Any = None):
        expr_type = self.visit(node.expr)
        if not self._is_int(expr_type):
            raise TypeMismatchInStatement(node)

        self.switch_depth += 1
        for case in node.cases:
            self.visit(case)
        if node.default_case:
            self.visit(node.default_case)
        self.switch_depth -= 1
        return None

    def visit_case_stmt(self, node: "CaseStmt", o: Any = None):
        expr_type = self.visit(node.expr)
        if not self._is_int(expr_type):
            raise TypeMismatchInStatement(node)
        for stmt in node.statements:
            self.visit(stmt)
        return None

    def visit_default_stmt(self, node: "DefaultStmt", o: Any = None):
        for stmt in node.statements:
            self.visit(stmt)
        return None

    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        if self.loop_depth == 0 and self.switch_depth == 0:
            raise MustInLoop(node)
        return None

    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        if self.loop_depth == 0:
            raise MustInLoop(node)
        return None

    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        if node.expr:
            return_type = self.visit(node.expr)
            if self.current_function_return_type is None:
                if self.inferred_return_type is None:
                    self.inferred_return_type = return_type
                elif not self._is_compatible(return_type, self.inferred_return_type):
                    raise TypeMismatchInStatement(node)
                
            else:
                if not self._is_compatible(return_type, self.current_function_return_type):
                    raise TypeMismatchInStatement(node)
        
        elif self.current_function_return_type and not isinstance(self.current_function_return_type, VoidType):
            raise TypeMismatchInStatement(node)
        return None

    def visit_expr_stmt(self, node: "ExprStmt", o: Any = None):
        self.visit(node.expr)
        return None


    # ======================================================================
    # EXPRESSIONS VISITOR --------------------------------------------------
    # ======================================================================
    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        operator = node.operator

        if left_type is None and right_type is None:
            raise TypeCannotBeInferred(node)

        if operator in ("+", "-", "*", "/"):
            if not self._is_numeric(left_type) or not self._is_numeric(right_type):
                raise TypeMismatchInExpression(node)
            if isinstance(left_type, FloatType) or isinstance(right_type, FloatType):
                return FloatType()
            return IntType()
        
        if operator == "%":
            if not self._is_int(left_type) or not self._is_int(right_type):
                raise TypeMismatchInExpression(node)
            return IntType()
        
        if operator in ("==", "!=", "<", "<=", ">", ">="):
            if not self._is_numeric(left_type) or not self._is_numeric(right_type):
                raise TypeMismatchInExpression(node)
            return IntType()
        
        if operator in ("&&", "||"):
            if not self._is_int(left_type) or not self._is_int(right_type):
                raise TypeMismatchInExpression(node)
            return IntType()
        
        raise TypeMismatchInExpression(node)

    def visit_prefix_op(self, node: "PrefixOp", o: Any = None):
        operand_type = self.visit(node.operand)
        operator = node.operator

        if operator in ("++", "--"):
            if not self._is_int(operand_type) or not isinstance(node.operand, (Identifier, MemberAccess)):
                raise TypeMismatchInExpression(node)
            return IntType()
        
        if node.operator == "!":
            if not self._is_int(operand_type):
                raise TypeMismatchInExpression(node)
            return IntType()
        
        if node.operator in ("+", "-"):
            if not self._is_numeric(operand_type):
                raise TypeMismatchInExpression(node)
            return operand_type

        return None

    def visit_postfix_op(self, node: "PostfixOp", o: Any = None):
        operand_type = self.visit(node.operand)
        if not self._is_int(operand_type) or not isinstance(node.operand, (Identifier, MemberAccess)):
            raise TypeMismatchInExpression(node)
        return IntType()

    def visit_assign_expr(self, node: "AssignExpr", o: Any = None):
        if not isinstance(node.lhs, (Identifier, MemberAccess)):
            raise TypeMismatchInExpression(node)
        
        if isinstance(node.lhs, Identifier):
            exists, current_type = self._lookup(node.lhs.name)
            right_type = self.visit(node.rhs)
            
            if exists and current_type is None:
                for scope in reversed(self.scope_stack):
                    if node.lhs.name in scope:
                        scope[node.lhs.name] = right_type
                        break
                self.unresolved_autos.pop(node.lhs.name, None)
                return right_type
        
        left_type = self.visit(node.lhs)
        right_type = self.visit(node.rhs)

        if not self._is_compatible(left_type, right_type):
            raise TypeMismatchInExpression(node)
        return left_type


    def visit_member_access(self, node: "MemberAccess", o: Any = None):
        base_type = self.visit(node.obj)
        if not isinstance(base_type, StructType):
            raise TypeMismatchInExpression(node)
        
        struct_decl = self.global_structs.get(base_type.struct_name)
        if not struct_decl:
            raise UndeclaredStruct(base_type.struct_name)

        for member in struct_decl.members:
            if member.name == node.member:
                return self.visit(member.member_type)

        raise TypeMismatchInExpression(node)

    def visit_func_call(self, node: "FuncCall", o: Any = None):
        if node.name in self.global_functions:
            func = self.global_functions[node.name]
            param_types = [self.visit(p.param_type) for p in func.params]
            return_type = func.return_type or VoidType() 
        elif node.name in self.builtin_functions:
            return_type, param_types = self.builtin_functions[node.name] 
        else:
            raise UndeclaredFunction(node.name)

        if len(node.args) != len(param_types):
            raise TypeMismatchInExpression(node)

        for i, arg in enumerate(node.args):
            expected_type = param_types[i]
            
            if isinstance(arg, Identifier):
                exists, current_type = self._lookup(arg.name)
                
                if not exists:
                    raise UndeclaredIdentifier(arg.name)
                
                if current_type is None:
                    for scope in reversed(self.scope_stack):
                        if arg.name in scope:
                            scope[arg.name] = expected_type
                            break
                    self.unresolved_autos.pop(arg.name, None)
            
            arg_type = self.visit(arg)
            
            if not self._is_compatible(arg_type, expected_type):
                raise TypeMismatchInExpression(node)

        return return_type

    def visit_identifier(self, node: "Identifier", o: Any = None):
        exists, var_type = self._lookup(node.name)
    
        if not exists:
            raise UndeclaredIdentifier(node.name)
        #if var_type is None:
        #    raise TypeCannotBeInferred(node)
        
        return var_type

    def visit_struct_literal(self, node: "StructLiteral", o: Any = None):
        for value in node.values:
            self.visit(value)
        return None


    # ======================================================================
    # LITERALS VISITOR -----------------------------------------------------
    # ======================================================================
    def visit_int_literal(self, node: "IntLiteral", o: Any = None):
        return IntType()

    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        return FloatType()

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        return StringType()
