"""
Code generator for TyC.
"""

from typing import Any

from ..utils.nodes import *
from ..utils.visitor import BaseVisitor
from .emitter import *
from .frame import *
from .io import IO_SYMBOL_LIST
from .utils import *


class StringArrayType:
    """Marker type for JVM main(String[] args)."""
    pass


class CodeGenerator(BaseVisitor):
    """Minimal AST -> Jasmin code generator."""

    def __init__(self):
        self.emit = None
        self.functions = {}
        self.current_return_type = VoidType()
        self.class_name = "TyC"
        self.structs = {}
        self.auto_decl_types = {}

    def visit(self, node, o=None):
        if isinstance(node, str):
            node = self._parse_source(node)
        return super().visit(node, o)

    def _parse_source(self, source: str):
        build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "build"))
        if build_dir not in sys.path:
            sys.path.insert(0, build_dir)

        from antlr4 import CommonTokenStream, InputStream
        from build.TyCLexer import TyCLexer
        from build.TyCParser import TyCParser
        from src.astgen.ast_generation import ASTGeneration
        from src.utils.error_listener import NewErrorListener

        input_stream = InputStream(source)
        lexer = TyCLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = TyCParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(NewErrorListener.INSTANCE)
        return ASTGeneration().visit(parser.program())

    def _lookup_symbol(self, name: str, sym_list: list[Symbol]) -> Symbol:
        for sym in reversed(sym_list):
            if sym.name == name:
                return sym
        raise RuntimeError(f"Undeclared symbol: {name}")

    def _is_struct_type(self, typ) -> bool:
        return hasattr(typ, "struct_name")

    def _coerce(self, code: str, from_type, to_type, frame) -> str:
        if is_int_type(from_type) and is_float_type(to_type):
            return code + self.emit.emit_i2f(frame)
        return code

    def _member_type(self, struct_type, member_name: str):
        if not self._is_struct_type(struct_type):
            return IntType()
        struct_decl = self.structs.get(struct_type.struct_name)
        if struct_decl is None:
            return IntType()
        for member in struct_decl.members:
            if member.name == member_name:
                return member.member_type
        return IntType()

    def _default_value(self, typ, frame) -> str:
        if is_int_type(typ):
            return self.emit.emit_push_iconst(0, frame)
        if is_float_type(typ):
            return self.emit.emit_push_fconst("0.0", frame)
        if is_string_type(typ):
            return self.emit.emit_push_const("", StringType(), frame)
        if self._is_struct_type(typ):
            return self._new_struct_default(typ, frame)
        return ""

    def _new_struct_default(self, typ, frame) -> str:
        code = self.emit.emit_new_instance(typ.struct_name, frame)
        struct_decl = self.structs.get(typ.struct_name)
        if struct_decl is None:
            return code
        for member in struct_decl.members:
            code += self.emit.emit_dup(frame)
            code += self._default_value(member.member_type, frame)
            code += self.emit.emit_put_field(f"{typ.struct_name}/{member.name}", member.member_type, frame)
        return code

    def _copy_struct_from_temp(self, struct_type, src_idx: int, frame) -> str:
        code = self._new_struct_default(struct_type, frame)
        struct_decl = self.structs.get(struct_type.struct_name)
        if struct_decl is None:
            return code
        for member in struct_decl.members:
            code += self.emit.emit_dup(frame)
            code += self.emit.emit_read_var("_struct_src", struct_type, src_idx, frame)
            code += self.emit.emit_get_field(f"{struct_type.struct_name}/{member.name}", member.member_type, frame)
            code += self.emit.emit_put_field(f"{struct_type.struct_name}/{member.name}", member.member_type, frame)
        return code

    def _copy_struct_expr(self, expr_code: str, struct_type, frame) -> str:
        tmp_idx = frame.get_new_index()
        code = expr_code
        code += self.emit.emit_write_var("_struct_src", struct_type, tmp_idx, frame)
        code += self._copy_struct_from_temp(struct_type, tmp_idx, frame)
        return code

    def _env_lookup(self, name: str, env: list[dict]):
        for item in reversed(env):
            if item["name"] == name:
                return item
        return None

    def _infer_expr_from_env(self, node: Expr, env: list[dict]):
        if isinstance(node, IntLiteral):
            return IntType()
        if isinstance(node, FloatLiteral):
            return FloatType()
        if isinstance(node, StringLiteral):
            return StringType()
        if isinstance(node, Identifier):
            item = self._env_lookup(node.name, env)
            return item["type"] if item else IntType()
        if isinstance(node, FuncCall):
            return self.functions[node.name].type.return_type
        if isinstance(node, AssignExpr):
            rhs_type = self._infer_expr_from_env(node.rhs, env)
            if isinstance(node.lhs, Identifier):
                item = self._env_lookup(node.lhs.name, env)
                if item and item.get("auto_unresolved"):
                    item["type"] = rhs_type
                    item["auto_unresolved"] = False
                    self.auto_decl_types[item["decl_id"]] = rhs_type
            return rhs_type
        if isinstance(node, MemberAccess):
            return self._member_type(self._infer_expr_from_env(node.obj, env), node.member)
        if isinstance(node, PrefixOp):
            if node.operator == "!":
                return IntType()
            return self._infer_expr_from_env(node.operand, env)
        if isinstance(node, PostfixOp):
            return self._infer_expr_from_env(node.operand, env)
        if isinstance(node, StructLiteral):
            return IntType()
        if isinstance(node, BinaryOp):
            if node.operator in ["+", "-", "*", "/"]:
                left_type = self._infer_expr_from_env(node.left, env)
                right_type = self._infer_expr_from_env(node.right, env)
                return FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            return IntType()
        return IntType()

    def _scan_auto_stmt(self, stmt: Stmt, env: list[dict]):
        if isinstance(stmt, VarDecl):
            if stmt.var_type is None:
                if stmt.init_value is not None:
                    typ = self._infer_expr_from_env(stmt.init_value, env)
                    self.auto_decl_types[id(stmt)] = typ
                    env.append({"name": stmt.name, "type": typ, "decl_id": id(stmt), "auto_unresolved": False})
                else:
                    env.append({"name": stmt.name, "type": IntType(), "decl_id": id(stmt), "auto_unresolved": True})
            else:
                env.append({"name": stmt.name, "type": stmt.var_type, "decl_id": id(stmt), "auto_unresolved": False})
        elif isinstance(stmt, ExprStmt):
            self._infer_expr_from_env(stmt.expr, env)
        elif isinstance(stmt, BlockStmt):
            old_len = len(env)
            for child in stmt.statements:
                self._scan_auto_stmt(child, env)
            del env[old_len:]
        elif isinstance(stmt, IfStmt):
            self._infer_expr_from_env(stmt.condition, env)
            self._scan_auto_stmt(stmt.then_stmt, env.copy())
            if stmt.else_stmt:
                self._scan_auto_stmt(stmt.else_stmt, env.copy())
        elif isinstance(stmt, WhileStmt):
            self._infer_expr_from_env(stmt.condition, env)
            self._scan_auto_stmt(stmt.body, env.copy())
        elif isinstance(stmt, ForStmt):
            local_env = env.copy()
            if stmt.init:
                self._scan_auto_stmt(stmt.init, local_env)
            if stmt.condition:
                self._infer_expr_from_env(stmt.condition, local_env)
            if stmt.update:
                self._infer_expr_from_env(stmt.update, local_env)
            self._scan_auto_stmt(stmt.body, local_env)
        elif isinstance(stmt, SwitchStmt):
            self._infer_expr_from_env(stmt.expr, env)
            for case in stmt.cases:
                case_env = env.copy()
                for child in case.statements:
                    self._scan_auto_stmt(child, case_env)
            if stmt.default_case:
                default_env = env.copy()
                for child in stmt.default_case.statements:
                    self._scan_auto_stmt(child, default_env)
        elif isinstance(stmt, ReturnStmt) and stmt.expr is not None:
            self._infer_expr_from_env(stmt.expr, env)

    def _infer_function_return(self, node: FuncDecl):
        env = [{"name": p.name, "type": p.param_type, "decl_id": id(p), "auto_unresolved": False} for p in node.params]

        def find_return(stmt, local_env):
            if isinstance(stmt, ReturnStmt):
                return self._infer_expr_from_env(stmt.expr, local_env) if stmt.expr is not None else VoidType()
            if isinstance(stmt, VarDecl) or isinstance(stmt, ExprStmt):
                self._scan_auto_stmt(stmt, local_env)
                return None
            if isinstance(stmt, BlockStmt):
                scoped = local_env.copy()
                for child in stmt.statements:
                    typ = find_return(child, scoped)
                    if typ is not None:
                        return typ
            if isinstance(stmt, IfStmt):
                self._infer_expr_from_env(stmt.condition, local_env)
                typ = find_return(stmt.then_stmt, local_env.copy())
                if typ is not None:
                    return typ
                if stmt.else_stmt:
                    return find_return(stmt.else_stmt, local_env.copy())
            if isinstance(stmt, WhileStmt):
                self._infer_expr_from_env(stmt.condition, local_env)
                return find_return(stmt.body, local_env.copy())
            if isinstance(stmt, ForStmt):
                scoped = local_env.copy()
                if stmt.init:
                    self._scan_auto_stmt(stmt.init, scoped)
                if stmt.condition:
                    self._infer_expr_from_env(stmt.condition, scoped)
                if stmt.update:
                    self._infer_expr_from_env(stmt.update, scoped)
                return find_return(stmt.body, scoped)
            return None

        typ = find_return(node.body, env)
        return typ if typ is not None else VoidType()

    def _stmt_always_returns(self, stmt: Stmt) -> bool:
        if isinstance(stmt, ReturnStmt):
            return True
        if isinstance(stmt, BlockStmt):
            return bool(stmt.statements) and self._stmt_always_returns(stmt.statements[-1])
        if isinstance(stmt, IfStmt):
            return stmt.else_stmt is not None and self._stmt_always_returns(stmt.then_stmt) and self._stmt_always_returns(stmt.else_stmt)
        return False

    def _infer_type(self, node: Expr, o: Access):
        if isinstance(node, IntLiteral):
            return IntType()
        if isinstance(node, FloatLiteral):
            return FloatType()
        if isinstance(node, StringLiteral):
            return StringType()
        if isinstance(node, Identifier):
            return self._lookup_symbol(node.name, o.sym).type
        if isinstance(node, AssignExpr):
            return self._infer_type(node.rhs, o)
        if isinstance(node, FuncCall):
            return self.functions[node.name].type.return_type
        if isinstance(node, MemberAccess):
            obj_type = self._infer_type(node.obj, o)
            if not self._is_struct_type(obj_type):
                return IntType()
            return self._member_type(obj_type, node.member)
        if isinstance(node, PrefixOp):
            if node.operator == "!":
                return IntType()
            if node.operator in ["++", "--"]:
                return self._infer_type(node.operand, o)
            return self._infer_type(node.operand, o)
        if isinstance(node, PostfixOp):
            return self._infer_type(node.operand, o)
        if isinstance(node, StructLiteral):
            return IntType()
        if isinstance(node, BinaryOp):
            if node.operator in ["+", "-", "*", "/", "%"]:
                left_type = self._infer_type(node.left, o)
                right_type = self._infer_type(node.right, o)
                if is_float_type(left_type) or is_float_type(right_type):
                    return FloatType()
                return IntType()
            if node.operator in ["<", "<=", ">", ">=", "==", "!=", "&&", "||"]:
                return IntType()
        return IntType()

    def visit_program(self, node: Program, o: Any = None):
        self.emit = Emitter(f"{self.class_name}.j")
        self.emit.print_out(self.emit.emit_prolog(self.class_name))
        self.structs = {}

        for io_sym in IO_SYMBOL_LIST:
            self.functions[io_sym.name] = io_sym

        for decl in node.decls:
            if isinstance(decl, StructDecl):
                self.structs[decl.name] = decl

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                return_type = decl.return_type if decl.return_type else self._infer_function_return(decl)
                param_types = [p.param_type for p in decl.params]
                self.functions[decl.name] = Symbol(
                    decl.name, FunctionType(param_types, return_type), CName(self.class_name)
                )

        for decl in node.decls:
            if isinstance(decl, StructDecl):
                self.visit(decl, None)
            if isinstance(decl, FuncDecl):
                self.visit(decl, None)

        self.emit.emit_epilog()

    def visit_func_decl(self, node: FuncDecl, o: Any = None):
        self.auto_decl_types = {}
        env = [{"name": p.name, "type": p.param_type, "decl_id": id(p), "auto_unresolved": False} for p in node.params]
        for stmt in node.body.statements:
            self._scan_auto_stmt(stmt, env)
        self.current_return_type = node.return_type if node.return_type else self.functions[node.name].type.return_type
        frame = Frame(node.name, self.current_return_type)
        frame.enter_scope(True)
        frame.loop_continue_labels = []
        frame.loop_break_labels = []
        frame.switch_break_labels = []

        if node.name == "main":
            mtype = FunctionType([StringArrayType()], VoidType())
        else:
            mtype = FunctionType([p.param_type for p in node.params], self.current_return_type)

        self.emit.print_out(self.emit.emit_method(node.name, mtype, True))

        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))

        local_syms: list[Symbol] = []
        if node.name == "main":
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", StringArrayType(), start_label, end_label
                )
            )

        for param in node.params:
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(idx, param.name, param.param_type, start_label, end_label)
            )
            local_syms.append(Symbol(param.name, param.param_type, Index(idx)))

        sub_body = SubBody(frame, local_syms)
        sub_body.is_func_body = True
        self.visit(node.body, sub_body)

        if is_void_type(self.current_return_type):
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        self.emit.print_out(self.emit.emit_end_method(frame))

    def visit_block_stmt(self, node: BlockStmt, o: SubBody = None):
        frame = o.frame
        is_func_body = getattr(o, "is_func_body", False)
        old_sym_len = len(o.sym)
        old_index = frame.get_curr_index()
        if is_func_body:
            o.is_func_body = False
        for stmt in node.statements:
            o = self.visit(stmt, o)
        if not is_func_body:
            del o.sym[old_sym_len:]
            frame.set_curr_index(old_index)
        return o

    def visit_var_decl(self, node: VarDecl, o: SubBody = None):
        frame = o.frame
        idx = frame.get_new_index()
        if node.var_type:
            var_type = node.var_type
        elif node.init_value is not None:
            var_type = self._infer_type(node.init_value, Access(frame, o.sym))
        else:
            var_type = self.auto_decl_types.get(id(node), IntType())
        self.emit.print_out(
            self.emit.emit_var(
                idx, node.name, var_type, frame.get_start_label(), frame.get_end_label()
            )
        )
        if node.init_value is not None:
            if isinstance(node.init_value, StructLiteral):
                rhs_code, _ = self.visit(node.init_value, (Access(frame, o.sym), var_type))
            else:
                rhs_code, rhs_type = self.visit(node.init_value, Access(frame, o.sym))
                if self._is_struct_type(var_type) and self._is_struct_type(rhs_type):
                    rhs_code = self._copy_struct_expr(rhs_code, var_type, frame)
                else:
                    rhs_code = self._coerce(rhs_code, rhs_type, var_type, frame)
            self.emit.print_out(rhs_code)
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        else:
            self.emit.print_out(self._default_value(var_type, frame))
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        o.sym.append(Symbol(node.name, var_type, Index(idx)))
        return o

    def visit_expr_stmt(self, node: ExprStmt, o: SubBody = None):
        code, expr_type = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        if not is_void_type(expr_type):
            self.emit.print_out(self.emit.emit_pop(o.frame))
        return o

    def visit_if_stmt(self, node: IfStmt, o: SubBody = None):
        frame = o.frame
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        else_label = frame.get_new_label()
        end_label = frame.get_new_label()
        then_returns = self._stmt_always_returns(node.then_stmt)
        else_returns = node.else_stmt is not None and self._stmt_always_returns(node.else_stmt)
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(else_label, frame))
        self.visit(node.then_stmt, o)
        if not then_returns:
            self.emit.print_out(self.emit.emit_goto(end_label, frame))
        self.emit.print_out(self.emit.emit_label(else_label, frame))
        if node.else_stmt:
            self.visit(node.else_stmt, o)
        if not (then_returns and else_returns):
            self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_while_stmt(self, node: WhileStmt, o: SubBody = None):
        frame = o.frame
        start_label = frame.get_new_label()
        end_label = frame.get_new_label()
        frame.loop_continue_labels.append(start_label)
        frame.loop_break_labels.append(end_label)
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))
        self.visit(node.body, o)
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.loop_continue_labels.pop()
        frame.loop_break_labels.pop()
        return o

    def visit_return_stmt(self, node: ReturnStmt, o: SubBody = None):
        if node.expr is None:
            self.emit.print_out(self.emit.emit_return(VoidType(), o.frame))
            return o
        code, ret_type = self.visit(node.expr, Access(o.frame, o.sym))
        code = self._coerce(code, ret_type, self.current_return_type, o.frame)
        self.emit.print_out(code)
        self.emit.print_out(self.emit.emit_return(self.current_return_type, o.frame))
        return o

    def visit_binary_op(self, node: BinaryOp, o: Access = None):
        frame = o.frame
        if node.operator == "&&":
            false_label = frame.get_new_label()
            end_label = frame.get_new_label()
            left_code, _ = self.visit(node.left, o)
            right_code, _ = self.visit(node.right, o)
            code = left_code
            code += self.emit.emit_if_false(false_label, frame)
            code += right_code
            code += self.emit.emit_if_false(false_label, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_goto(end_label, frame)
            code += self.emit.emit_label(false_label, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_label(end_label, frame)
            return code, IntType()
        if node.operator == "||":
            true_label = frame.get_new_label()
            end_label = frame.get_new_label()
            left_code, _ = self.visit(node.left, o)
            right_code, _ = self.visit(node.right, o)
            code = left_code
            code += self.emit.emit_if_true(true_label, frame)
            code += right_code
            code += self.emit.emit_if_true(true_label, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_goto(end_label, frame)
            code += self.emit.emit_label(true_label, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_label(end_label, frame)
            return code, IntType()
        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)

        if node.operator in ["+", "-"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            left_code = self._coerce(left_code, left_type, result_type, frame)
            right_code = self._coerce(right_code, right_type, result_type, frame)
            return (
                left_code
                + right_code
                + self.emit.emit_add_op(node.operator, result_type, frame),
                result_type,
            )
        if node.operator in ["*", "/"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            left_code = self._coerce(left_code, left_type, result_type, frame)
            right_code = self._coerce(right_code, right_type, result_type, frame)
            return (
                left_code
                + right_code
                + self.emit.emit_mul_op(node.operator, result_type, frame),
                result_type,
            )
        if node.operator == "%":
            return left_code + right_code + self.emit.emit_mod(frame), IntType()
        if node.operator == "&&":
            return left_code + right_code + self.emit.emit_and_op(frame), IntType()
        if node.operator == "||":
            return left_code + right_code + self.emit.emit_or_op(frame), IntType()
        if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
            op_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            left_code = self._coerce(left_code, left_type, op_type, frame)
            right_code = self._coerce(right_code, right_type, op_type, frame)
            return left_code + right_code + self.emit.emit_re_op(node.operator, op_type, frame), IntType()
        raise RuntimeError(f"Unsupported operator: {node.operator}")

    def visit_assign_expr(self, node: AssignExpr, o: Access = None):
        if isinstance(node.lhs, Identifier):
            lhs_sym = self._lookup_symbol(node.lhs.name, o.sym)
            if isinstance(node.rhs, StructLiteral):
                rhs_code, rhs_type = self.visit(node.rhs, (o, lhs_sym.type))
            else:
                rhs_code, rhs_type = self.visit(node.rhs, o)
                if self._is_struct_type(lhs_sym.type) and self._is_struct_type(rhs_type):
                    rhs_code = self._copy_struct_expr(rhs_code, lhs_sym.type, o.frame)
                    rhs_type = lhs_sym.type
                else:
                    rhs_code = self._coerce(rhs_code, rhs_type, lhs_sym.type, o.frame)
            idx = lhs_sym.value.value
            code = rhs_code + self.emit.emit_dup(o.frame) + self.emit.emit_write_var(
                node.lhs.name, lhs_sym.type, idx, o.frame
            )
            return code, lhs_sym.type
        if isinstance(node.lhs, MemberAccess):
            obj_code, obj_type = self.visit(node.lhs.obj, o)
            member_type = self._member_type(obj_type, node.lhs.member)
            if isinstance(node.rhs, StructLiteral):
                rhs_code, rhs_type = self.visit(node.rhs, (o, member_type))
            else:
                rhs_code, rhs_type = self.visit(node.rhs, o)
                rhs_code = self._coerce(rhs_code, rhs_type, member_type, o.frame)
            code = obj_code + rhs_code + self.emit.emit_dup_x1(o.frame)
            code += self.emit.emit_put_field(f"{obj_type.struct_name}/{node.lhs.member}", member_type, o.frame)
            return code, member_type
        raise RuntimeError("Minimal codegen only supports identifier assignment")

    def visit_func_call(self, node: FuncCall, o: Access = None):
        frame = o.frame
        fn_sym = self.functions[node.name]
        fn_type = fn_sym.type
        code = ""
        for arg, param_type in zip(node.args, fn_type.param_types):
            arg_code, arg_type = self.visit(arg, o)
            arg_code = self._coerce(arg_code, arg_type, param_type, frame)
            code += arg_code
        code += self.emit.emit_invoke_static(f"{fn_sym.value.value}/{node.name}", fn_type, frame)
        return code, fn_type.return_type

    def visit_identifier(self, node: Identifier, o: Access = None):
        sym = self._lookup_symbol(node.name, o.sym)
        return self.emit.emit_read_var(node.name, sym.type, sym.value.value, o.frame), sym.type

    def visit_int_literal(self, node: IntLiteral, o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: FloatLiteral, o: Access = None):
        return self.emit.emit_push_fconst(str(node.value), o.frame), FloatType()

    def visit_string_literal(self, node: StringLiteral, o: Access = None):
        return self.emit.emit_push_const(node.value, StringType(), o.frame), StringType()

    def visit_struct_decl(self, node: StructDecl, o: Any = None):
        struct_emit = Emitter(f"{node.name}.j")
        struct_emit.print_out(struct_emit.emit_prolog(node.name))
        for member in node.members:
            struct_emit.print_out(
                f".field public {member.name} {struct_emit.get_jvm_type(member.member_type)}\n"
            )
        struct_emit.print_out("\n.method public <init>()V\n")
        struct_emit.print_out("\taload_0\n")
        struct_emit.print_out("\tinvokespecial java/lang/Object/<init>()V\n")
        ctor_frame = Frame(f"{node.name}.<init>", VoidType())
        ctor_frame.push()
        for member in node.members:
            if is_string_type(member.member_type) or self._is_struct_type(member.member_type):
                struct_emit.print_out("\taload_0\n")
                struct_emit.print_out(self._default_value(member.member_type, ctor_frame))
                struct_emit.print_out(struct_emit.emit_put_field(f"{node.name}/{member.name}", member.member_type, ctor_frame))
        struct_emit.print_out("\treturn\n")
        struct_emit.print_out(f".limit stack {max(1, ctor_frame.get_max_op_stack_size())}\n")
        struct_emit.print_out(".limit locals 1\n")
        struct_emit.print_out(".end method\n")
        struct_emit.emit_epilog()
        return None

    def visit_member_decl(self, node: MemberDecl, o: Any = None):
        return None

    def visit_param(self, node: Param, o: Any = None):
        return None

    def visit_int_type(self, node: IntType, o: Any = None):
        return node

    def visit_float_type(self, node: FloatType, o: Any = None):
        return node

    def visit_string_type(self, node: StringType, o: Any = None):
        return node

    def visit_void_type(self, node: VoidType, o: Any = None):
        return node

    def visit_struct_type(self, node: StructType, o: Any = None):
        return node

    def visit_for_stmt(self, node: ForStmt, o: Any = None):
        frame = o.frame
        if node.init is not None:
            if isinstance(node.init, VarDecl):
                o = self.visit(node.init, o)
            else:
                o = self.visit(node.init, o)
        cond_label = frame.get_new_label()
        continue_label = frame.get_new_label()
        break_label = frame.get_new_label()
        frame.loop_continue_labels.append(continue_label)
        frame.loop_break_labels.append(break_label)
        self.emit.print_out(self.emit.emit_label(cond_label, frame))
        if node.condition is not None:
            cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
            self.emit.print_out(cond_code)
            self.emit.print_out(self.emit.emit_if_false(break_label, frame))
        self.visit(node.body, o)
        self.emit.print_out(self.emit.emit_label(continue_label, frame))
        if node.update is not None:
            update_code, update_type = self.visit(node.update, Access(frame, o.sym))
            self.emit.print_out(update_code)
            if not is_void_type(update_type):
                self.emit.print_out(self.emit.emit_pop(frame))
        self.emit.print_out(self.emit.emit_goto(cond_label, frame))
        self.emit.print_out(self.emit.emit_label(break_label, frame))
        frame.loop_continue_labels.pop()
        frame.loop_break_labels.pop()
        return o

    def visit_switch_stmt(self, node: SwitchStmt, o: Any = None):
        frame = o.frame
        old_sym_len = len(o.sym)
        old_index = frame.get_curr_index()
        expr_type = self._infer_type(node.expr, Access(frame, o.sym))
        tmp_idx = frame.get_new_index()
        end_label = frame.get_new_label()
        default_label = frame.get_new_label() if node.default_case is not None else end_label
        case_labels = [frame.get_new_label() for _ in node.cases]
        self.emit.print_out(
            self.emit.emit_var(
                tmp_idx, "_switch", expr_type, frame.get_start_label(), frame.get_end_label()
            )
        )
        expr_code, _ = self.visit(node.expr, Access(frame, o.sym))
        self.emit.print_out(expr_code)
        self.emit.print_out(self.emit.emit_write_var("_switch", expr_type, tmp_idx, frame))
        frame.switch_break_labels.append(end_label)
        for case_node, case_label in zip(node.cases, case_labels):
            self.emit.print_out(self.emit.emit_read_var("_switch", expr_type, tmp_idx, frame))
            case_code, _ = self.visit(case_node.expr, Access(frame, o.sym))
            self.emit.print_out(case_code)
            self.emit.print_out(self.emit.emit_re_op("==", expr_type, frame))
            self.emit.print_out(self.emit.emit_if_true(case_label, frame))
        self.emit.print_out(self.emit.emit_goto(default_label, frame))
        for case_node, case_label in zip(node.cases, case_labels):
            self.emit.print_out(self.emit.emit_label(case_label, frame))
            self.visit(case_node, o)
        if node.default_case is not None:
            self.emit.print_out(self.emit.emit_label(default_label, frame))
            self.visit(node.default_case, o)
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.switch_break_labels.pop()
        del o.sym[old_sym_len:]
        frame.set_curr_index(old_index)
        return o

    def visit_case_stmt(self, node: CaseStmt, o: Any = None):
        for stmt in node.statements:
            o = self.visit(stmt, o)
        return o

    def visit_default_stmt(self, node: DefaultStmt, o: Any = None):
        for stmt in node.statements:
            o = self.visit(stmt, o)
        return o

    def visit_break_stmt(self, node: BreakStmt, o: Any = None):
        frame = o.frame
        if hasattr(frame, "switch_break_labels") and frame.switch_break_labels:
            self.emit.print_out(self.emit.emit_goto(frame.switch_break_labels[-1], frame))
            return o
        if hasattr(frame, "loop_break_labels") and frame.loop_break_labels:
            self.emit.print_out(self.emit.emit_goto(frame.loop_break_labels[-1], frame))
            return o
        raise RuntimeError("BreakStmt not supported in minimal codegen")

    def visit_continue_stmt(self, node: ContinueStmt, o: Any = None):
        frame = o.frame
        if hasattr(frame, "loop_continue_labels") and frame.loop_continue_labels:
            self.emit.print_out(self.emit.emit_goto(frame.loop_continue_labels[-1], frame))
            return o
        raise RuntimeError("ContinueStmt not supported in minimal codegen")

    def visit_prefix_op(self, node: PrefixOp, o: Any = None):
        frame = o.frame
        if node.operator == "+":
            return self.visit(node.operand, o)
        if node.operator == "-":
            operand_code, operand_type = self.visit(node.operand, o)
            return operand_code + self.emit.emit_neg_op(operand_type, frame), operand_type
        if node.operator == "!":
            operand_code, _ = self.visit(node.operand, o)
            false_label = frame.get_new_label()
            end_label = frame.get_new_label()
            code = operand_code
            code += self.emit.emit_if_false(false_label, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_goto(end_label, frame)
            code += self.emit.emit_label(false_label, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_label(end_label, frame)
            return code, IntType()
        if node.operator in ["++", "--"]:
            delta_op = "+" if node.operator == "++" else "-"
            if isinstance(node.operand, Identifier):
                sym = self._lookup_symbol(node.operand.name, o.sym)
                one_code = self.emit.emit_push_fconst("1.0", frame) if is_float_type(sym.type) else self.emit.emit_push_iconst(1, frame)
                code = self.emit.emit_read_var(node.operand.name, sym.type, sym.value.value, frame)
                code += one_code
                code += self.emit.emit_add_op(delta_op, sym.type, frame)
                code += self.emit.emit_dup(frame)
                code += self.emit.emit_write_var(node.operand.name, sym.type, sym.value.value, frame)
                return code, sym.type
            if isinstance(node.operand, MemberAccess):
                obj_code, obj_type = self.visit(node.operand.obj, o)
                member_type = self._member_type(obj_type, node.operand.member)
                one_code = self.emit.emit_push_fconst("1.0", frame) if is_float_type(member_type) else self.emit.emit_push_iconst(1, frame)
                code = obj_code
                code += self.emit.emit_dup(frame)
                code += self.emit.emit_get_field(f"{obj_type.struct_name}/{node.operand.member}", member_type, frame)
                code += one_code
                code += self.emit.emit_add_op(delta_op, member_type, frame)
                code += self.emit.emit_dup_x1(frame)
                code += self.emit.emit_put_field(f"{obj_type.struct_name}/{node.operand.member}", member_type, frame)
                return code, member_type
        raise RuntimeError("PrefixOp not supported in minimal codegen")

    def visit_postfix_op(self, node: PostfixOp, o: Any = None):
        frame = o.frame
        if node.operator in ["++", "--"]:
            delta_op = "+" if node.operator == "++" else "-"
            if isinstance(node.operand, Identifier):
                sym = self._lookup_symbol(node.operand.name, o.sym)
                one_code = self.emit.emit_push_fconst("1.0", frame) if is_float_type(sym.type) else self.emit.emit_push_iconst(1, frame)
                code = self.emit.emit_read_var(node.operand.name, sym.type, sym.value.value, frame)
                code += self.emit.emit_dup(frame)
                code += one_code
                code += self.emit.emit_add_op(delta_op, sym.type, frame)
                code += self.emit.emit_write_var(node.operand.name, sym.type, sym.value.value, frame)
                return code, sym.type
            if isinstance(node.operand, MemberAccess):
                obj_code, obj_type = self.visit(node.operand.obj, o)
                member_type = self._member_type(obj_type, node.operand.member)
                tmp_idx = frame.get_new_index()
                one_code = self.emit.emit_push_fconst("1.0", frame) if is_float_type(member_type) else self.emit.emit_push_iconst(1, frame)
                code = obj_code
                code += self.emit.emit_dup(frame)
                code += self.emit.emit_get_field(f"{obj_type.struct_name}/{node.operand.member}", member_type, frame)
                code += self.emit.emit_dup(frame)
                code += self.emit.emit_write_var("_postfix_old", member_type, tmp_idx, frame)
                code += one_code
                code += self.emit.emit_add_op(delta_op, member_type, frame)
                code += self.emit.emit_put_field(f"{obj_type.struct_name}/{node.operand.member}", member_type, frame)
                code += self.emit.emit_read_var("_postfix_old", member_type, tmp_idx, frame)
                return code, member_type
        raise RuntimeError("PostfixOp not supported in minimal codegen")

    def visit_member_access(self, node: MemberAccess, o: Any = None):
        obj_code, obj_type = self.visit(node.obj, o)
        member_type = self._member_type(obj_type, node.member)
        return (
            obj_code + self.emit.emit_get_field(f"{obj_type.struct_name}/{node.member}", member_type, o.frame),
            member_type,
        )

    def visit_struct_literal(self, node: StructLiteral, o: Any = None):
        access, expected_type = o
        frame = access.frame
        code = self.emit.emit_new_instance(expected_type.struct_name, frame)
        struct_decl = self.structs[expected_type.struct_name]
        for value, member in zip(node.values, struct_decl.members):
            code += self.emit.emit_dup(frame)
            if isinstance(value, StructLiteral):
                value_code, _ = self.visit(value, (access, member.member_type))
            else:
                value_code, value_type = self.visit(value, access)
                value_code = self._coerce(value_code, value_type, member.member_type, frame)
            code += value_code
            code += self.emit.emit_put_field(
                f"{expected_type.struct_name}/{member.name}", member.member_type, frame
            )
        return code, expected_type
