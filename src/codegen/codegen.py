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

    def _lookup_symbol(self, name: str, sym_list: list[Symbol]) -> Symbol:
        for sym in reversed(sym_list):
            if sym.name == name:
                return sym
        raise RuntimeError(f"Undeclared symbol: {name}")

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
            if not isinstance(obj_type, StructType):
                return IntType()
            struct_decl = self.structs.get(obj_type.struct_name)
            if struct_decl is None:
                return IntType()
            for member in struct_decl.members:
                if member.name == node.member:
                    return member.member_type
            return IntType()
        if isinstance(node, PrefixOp):
            if node.operator == "!":
                return IntType()
            if node.operator in ["++", "--"]:
                return IntType()
            return self._infer_type(node.operand, o)
        if isinstance(node, PostfixOp):
            return IntType()
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
            if isinstance(decl, FuncDecl):
                return_type = decl.return_type if decl.return_type else VoidType()
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
        self.current_return_type = node.return_type if node.return_type else VoidType()
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
        self.visit(node.body, sub_body)

        if is_void_type(self.current_return_type):
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        self.emit.print_out(self.emit.emit_end_method(frame))

    def visit_block_stmt(self, node: BlockStmt, o: SubBody = None):
        for stmt in node.statements:
            o = self.visit(stmt, o)
        return o

    def visit_var_decl(self, node: VarDecl, o: SubBody = None):
        frame = o.frame
        idx = frame.get_new_index()
        var_type = node.var_type if node.var_type else self._infer_type(node.init_value, Access(frame, o.sym))
        self.emit.print_out(
            self.emit.emit_var(
                idx, node.name, var_type, frame.get_start_label(), frame.get_end_label()
            )
        )
        if node.init_value is not None:
            if isinstance(node.init_value, StructLiteral):
                rhs_code, _ = self.visit(node.init_value, (Access(frame, o.sym), var_type))
            else:
                rhs_code, _ = self.visit(node.init_value, Access(frame, o.sym))
            self.emit.print_out(rhs_code)
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
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(else_label, frame))
        self.visit(node.then_stmt, o)
        self.emit.print_out(self.emit.emit_goto(end_label, frame))
        self.emit.print_out(self.emit.emit_label(else_label, frame))
        if node.else_stmt:
            self.visit(node.else_stmt, o)
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_while_stmt(self, node: WhileStmt, o: SubBody = None):
        frame = o.frame
        start_label = frame.get_new_label()
        end_label = frame.get_new_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))
        self.visit(node.body, o)
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_return_stmt(self, node: ReturnStmt, o: SubBody = None):
        if node.expr is None:
            self.emit.print_out(self.emit.emit_return(VoidType(), o.frame))
            return o
        code, ret_type = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        self.emit.print_out(self.emit.emit_return(ret_type, o.frame))
        return o

    def visit_binary_op(self, node: BinaryOp, o: Access = None):
        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)
        frame = o.frame

        if node.operator in ["+", "-"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            return (
                left_code
                + right_code
                + self.emit.emit_add_op(node.operator, result_type, frame),
                result_type,
            )
        if node.operator in ["*", "/"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
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
            return left_code + right_code + self.emit.emit_re_op(node.operator, op_type, frame), IntType()
        raise RuntimeError(f"Unsupported operator: {node.operator}")

    def visit_assign_expr(self, node: AssignExpr, o: Access = None):
        if isinstance(node.lhs, Identifier):
            lhs_sym = self._lookup_symbol(node.lhs.name, o.sym)
            if isinstance(node.rhs, StructLiteral):
                rhs_code, rhs_type = self.visit(node.rhs, (o, lhs_sym.type))
            else:
                rhs_code, rhs_type = self.visit(node.rhs, o)
            idx = lhs_sym.value.value
            code = rhs_code + self.emit.emit_dup(o.frame) + self.emit.emit_write_var(
                node.lhs.name, lhs_sym.type, idx, o.frame
            )
            return code, rhs_type
        if isinstance(node.lhs, MemberAccess):
            obj_code, obj_type = self.visit(node.lhs.obj, o)
            member_type = IntType()
            if isinstance(obj_type, StructType) and obj_type.struct_name in self.structs:
                for member in self.structs[obj_type.struct_name].members:
                    if member.name == node.lhs.member:
                        member_type = member.member_type
                        break
            if isinstance(node.rhs, StructLiteral):
                rhs_code, rhs_type = self.visit(node.rhs, (o, member_type))
            else:
                rhs_code, rhs_type = self.visit(node.rhs, o)
            code = obj_code + rhs_code + self.emit.emit_dup_x1(o.frame)
            code += self.emit.emit_put_field(f"{obj_type.struct_name}/{node.lhs.member}", member_type, o.frame)
            return code, rhs_type
        raise RuntimeError("Minimal codegen only supports identifier assignment")

    def visit_func_call(self, node: FuncCall, o: Access = None):
        frame = o.frame
        fn_sym = self.functions[node.name]
        fn_type = fn_sym.type
        code = ""
        for arg in node.args:
            arg_code, _ = self.visit(arg, o)
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
        struct_emit.print_out("\treturn\n")
        struct_emit.print_out(".limit stack 1\n")
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
        if hasattr(frame, "loop_break_labels") and frame.loop_break_labels:
            self.emit.print_out(self.emit.emit_goto(frame.loop_break_labels[-1], frame))
            return o
        if hasattr(frame, "switch_break_labels") and frame.switch_break_labels:
            self.emit.print_out(self.emit.emit_goto(frame.switch_break_labels[-1], frame))
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
        if node.operator in ["++", "--"] and isinstance(node.operand, Identifier):
            sym = self._lookup_symbol(node.operand.name, o.sym)
            code = self.emit.emit_read_var(node.operand.name, sym.type, sym.value.value, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_add_op("+" if node.operator == "++" else "-", IntType(), frame)
            code += self.emit.emit_dup(frame)
            code += self.emit.emit_write_var(node.operand.name, sym.type, sym.value.value, frame)
            return code, IntType()
        raise RuntimeError("PrefixOp not supported in minimal codegen")

    def visit_postfix_op(self, node: PostfixOp, o: Any = None):
        frame = o.frame
        if node.operator in ["++", "--"] and isinstance(node.operand, Identifier):
            sym = self._lookup_symbol(node.operand.name, o.sym)
            code = self.emit.emit_read_var(node.operand.name, sym.type, sym.value.value, frame)
            code += self.emit.emit_dup(frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_add_op("+" if node.operator == "++" else "-", IntType(), frame)
            code += self.emit.emit_write_var(node.operand.name, sym.type, sym.value.value, frame)
            return code, IntType()
        raise RuntimeError("PostfixOp not supported in minimal codegen")

    def visit_member_access(self, node: MemberAccess, o: Any = None):
        obj_code, obj_type = self.visit(node.obj, o)
        member_type = IntType()
        if isinstance(obj_type, StructType) and obj_type.struct_name in self.structs:
            for member in self.structs[obj_type.struct_name].members:
                if member.name == node.member:
                    member_type = member.member_type
                    break
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
                value_code, _ = self.visit(value, access)
            code += value_code
            code += self.emit.emit_put_field(
                f"{expected_type.struct_name}/{member.name}", member.member_type, frame
            )
        return code, expected_type
