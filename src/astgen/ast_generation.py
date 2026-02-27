"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language."""

    # ========================================================================
    # Program and Declarations
    # ========================================================================
    
    def visitProgram(self, ctx: TyCParser.ProgramContext):
        """program : (structDecl | funcDecl)* EOF"""
        decls = []
        for i in range(ctx.getChildCount() - 1):  # -1 to skip EOF
            child = ctx.getChild(i)
            if child.getRuleIndex() != -1:  # Ignore terminal nodes
                result = self.visit(child)
                if result:
                    decls.append(result)
        return Program(decls)

    def visitStructDecl(self, ctx: TyCParser.StructDeclContext):
        """structDecl : STRUCT ID LB structMember* RB SEMICOLON"""
        name = ctx.ID().getText()
        members = [self.visit(m) for m in ctx.structMember()]
        members = [m for m in members if m is not None]
        return StructDecl(name, members)

    def visitStructMember(self, ctx: TyCParser.StructMemberContext):
        """structMember : type ID SEMICOLON"""
        member_type = self.visit(ctx.type_())
        name = ctx.ID().getText()
        return MemberDecl(member_type, name)

    def visitFuncDecl(self, ctx: TyCParser.FuncDeclContext):
        """funcDecl : returnType? ID LP paramList? RP block"""
        # Return type
        return_type = None
        if ctx.returnType():
            return_type = self.visit(ctx.returnType())
        
        # Function name
        name = ctx.ID().getText()
        
        # Parameters
        params = []
        if ctx.paramList():
            for param in ctx.paramList().param():
                params.append(self.visit(param))
        
        # Body
        body = self.visit(ctx.block())
        
        return FuncDecl(return_type, name, params, body)

    def visitParam(self, ctx: TyCParser.ParamContext):
        """param : type ID"""
        param_type = self.visit(ctx.type_())
        name = ctx.ID().getText()
        return Param(param_type, name)

    def visitReturnType(self, ctx: TyCParser.ReturnTypeContext):
        """returnType : VOID | type"""
        if ctx.VOID():
            return VoidType()
        return self.visit(ctx.type_())

    # ========================================================================
    # Type System
    # ========================================================================

    def visitType(self, ctx: TyCParser.TypeContext):
        """type : INT | FLOAT | STRING | ID"""
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()
        else:
            return StructType(ctx.ID().getText())

    # ========================================================================
    # Statements
    # ========================================================================

    def visitStatement(self, ctx: TyCParser.StatementContext):
        """statement : varDecl | exprStmt | ifStmt | whileStmt | forStmt | 
                                   switchStmt | block | returnStmt | breakStmt | continueStmt"""
        return self.visitChildren(ctx)

    def visitBlock(self, ctx: TyCParser.BlockContext):
        """block : LB statement* RB"""
        statements = []
        for stmt in ctx.statement():
            result = self.visit(stmt)
            if result:
                statements.append(result)
        return BlockStmt(statements)

    def visitVarDecl(self, ctx: TyCParser.VarDeclContext):
        """varDecl : AUTO ID (ASSIGN expr)? SEMICOLON
                   | type ID (ASSIGN expr | ASSIGN struct_lit)? SEMICOLON"""
        # Check if it's AUTO or explicit type
        if ctx.AUTO():
            var_type = None
            name = ctx.ID().getText()
        else:
            var_type = self.visit(ctx.type_())
            name = ctx.ID().getText()
        
        # Check for initialization
        init_value = None
        if ctx.expr():
            init_value = self.visit(ctx.expr())
        elif ctx.struct_lit():
            init_value = self.visit(ctx.struct_lit())
        
        return VarDecl(var_type, name, init_value)

    def visitExprStmt(self, ctx: TyCParser.ExprStmtContext):
        """exprStmt : expr SEMICOLON"""
        expr = self.visit(ctx.expr())
        return ExprStmt(expr)

    def visitIfStmt(self, ctx: TyCParser.IfStmtContext):
        """ifStmt : IF LP expr RP statement (ELSE statement)?"""
        condition = self.visit(ctx.expr())
        statements = ctx.statement()
        then_stmt = self.visit(statements[0])
        else_stmt = None
        if ctx.ELSE() and len(statements) > 1:
            else_stmt = self.visit(statements[1])
        return IfStmt(condition, then_stmt, else_stmt)

    def visitWhileStmt(self, ctx: TyCParser.WhileStmtContext):
        """whileStmt : WHILE LP expr RP statement"""
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.statement())
        return WhileStmt(condition, body)

    def visitForStmt(self, ctx: TyCParser.ForStmtContext):
        """forStmt : FOR LP forInit? SEMICOLON forCond? SEMICOLON forUpdate? RP statement"""
        init = None
        if ctx.forInit():
            init = self.visit(ctx.forInit())
        
        condition = None
        if ctx.forCond():
            condition = self.visit(ctx.forCond())
        
        update = None
        if ctx.forUpdate():
            update = self.visit(ctx.forUpdate())
        
        body = self.visit(ctx.statement())
        return ForStmt(init, condition, update, body)

    def visitForInit(self, ctx: TyCParser.ForInitContext):
        """forInit : forVarDecl | expr"""
        if ctx.forVarDecl():
            return self.visit(ctx.forVarDecl())
        else:
            return ExprStmt(self.visit(ctx.expr()))

    def visitForVarDecl(self, ctx: TyCParser.ForVarDeclContext):
        """forVarDecl : AUTO ID (ASSIGN expr)? 
                      | type ID (ASSIGN expr | ASSIGN struct_lit)?"""
        if ctx.AUTO():
            var_type = None
            name = ctx.ID().getText()
        else:
            var_type = self.visit(ctx.type_())
            name = ctx.ID().getText()
        
        init_value = None
        if ctx.expr():
            init_value = self.visit(ctx.expr())
        elif ctx.struct_lit():
            init_value = self.visit(ctx.struct_lit())
        
        return VarDecl(var_type, name, init_value)

    def visitForCond(self, ctx: TyCParser.ForCondContext):
        """forCond : expr"""
        return self.visit(ctx.expr())

    def visitForUpdate(self, ctx: TyCParser.ForUpdateContext):
        """forUpdate : lhs ASSIGN assignExpr | inc_dec"""
        if ctx.ASSIGN():
            lhs = self.visit(ctx.lhs())
            rhs = self.visit(ctx.assignExpr())
            return AssignExpr(lhs, rhs)
        else:
            return self.visit(ctx.inc_dec())

    def visitSwitchStmt(self, ctx: TyCParser.SwitchStmtContext):
        """switchStmt : SWITCH LP expr RP LB caseClause* defaultClause? caseClause* RB"""
        expr = self.visit(ctx.expr())
        
        cases = []
        default_clause = None
        
        # Process all case clauses
        for case in ctx.caseClause():
            cases.append(self.visit(case))
        
        # Process default clause
        if ctx.defaultClause():
            default_clause = self.visit(ctx.defaultClause())
        
        return SwitchStmt(expr, cases, default_clause)

    def visitCaseClause(self, ctx: TyCParser.CaseClauseContext):
        """caseClause : CASE expr COLON statement*"""
        expr = self.visit(ctx.expr())
        statements = [self.visit(stmt) for stmt in ctx.statement()]
        return CaseStmt(expr, statements)

    def visitDefaultClause(self, ctx: TyCParser.DefaultClauseContext):
        """defaultClause : DEFAULT COLON statement*"""
        statements = [self.visit(stmt) for stmt in ctx.statement()]
        return DefaultStmt(statements)

    def visitReturnStmt(self, ctx: TyCParser.ReturnStmtContext):
        """returnStmt : RETURN expr? SEMICOLON"""
        expr = None
        if ctx.expr():
            expr = self.visit(ctx.expr())
        return ReturnStmt(expr)

    def visitBreakStmt(self, ctx: TyCParser.BreakStmtContext):
        """breakStmt : BREAK SEMICOLON"""
        return BreakStmt()

    def visitContinueStmt(self, ctx: TyCParser.ContinueStmtContext):
        """continueStmt : CONTINUE SEMICOLON"""
        return ContinueStmt()

    # ========================================================================
    # Expressions
    # ========================================================================

    def visitExpr(self, ctx: TyCParser.ExprContext):
        """expr : assignExpr"""
        return self.visit(ctx.assignExpr())

    def visitAssignExpr(self, ctx: TyCParser.AssignExprContext):
        """assignExpr : lhs ASSIGN assignExpr | orExpr"""
        if ctx.ASSIGN():
            lhs = self.visit(ctx.lhs())
            rhs = self.visit(ctx.assignExpr())
            return AssignExpr(lhs, rhs)
        else:
            return self.visit(ctx.orExpr())

    def visitLhs(self, ctx: TyCParser.LhsContext):
        """lhs : ID (ACCESS ID)* 
              | LP lhs RP (ACCESS ID)*"""
        # Handle both alternatives
        ids = ctx.ID()
        if ids:
            # First alternative: ID (ACCESS ID)*
            name = ids[0].getText()
            result = Identifier(name)
            
            # Process member accesses
            for i in range(1, len(ids)):
                member = ids[i].getText()
                result = MemberAccess(result, member)
        else:
            # Second alternative: LP lhs RP (ACCESS ID)*
            result = self.visit(ctx.lhs())
            
            # Process member accesses after parentheses
            for member_id in ids:
                member = member_id.getText()
                result = MemberAccess(result, member)
        
        return result

    def visitOrExpr(self, ctx: TyCParser.OrExprContext):
        """orExpr : andExpr (OR andExpr)*"""
        and_exprs = ctx.andExpr()
        result = self.visit(and_exprs[0])
        for i in range(1, len(and_exprs)):
            right = self.visit(and_exprs[i])
            result = BinaryOp(result, "||", right)
        return result

    def visitAndExpr(self, ctx: TyCParser.AndExprContext):
        """andExpr : equalExpr (AND equalExpr)*"""
        equal_exprs = ctx.equalExpr()
        result = self.visit(equal_exprs[0])
        for i in range(1, len(equal_exprs)):
            right = self.visit(equal_exprs[i])
            result = BinaryOp(result, "&&", right)
        return result

    def visitEqualExpr(self, ctx: TyCParser.EqualExprContext):
        """equalExpr : relationalExpr ((EQUAL | NOT_EQUAL) relationalExpr)*"""
        rel_exprs = ctx.relationalExpr()
        result = self.visit(rel_exprs[0])
        
        for i in range(1, len(rel_exprs)):
            # Determine operator from text between operands
            operator = "=="
            # Look at tokens to find the operator
            for j in range(ctx.getChildCount()):
                child = ctx.getChild(j)
                if hasattr(child, 'getSymbol'):
                    sym = child.getSymbol()
                    if sym.type == TyCParser.NOT_EQUAL:
                        operator = "!="
                    elif sym.type == TyCParser.EQUAL:
                        operator = "=="
            right = self.visit(rel_exprs[i])
            result = BinaryOp(result, operator, right)
        return result

    def visitRelationalExpr(self, ctx: TyCParser.RelationalExprContext):
        """relationalExpr : addiExpr ((LESS | EQUAL_LESS | GRAT | EQUAL_GRAT) addiExpr)*"""
        addi_exprs = ctx.addiExpr()
        result = self.visit(addi_exprs[0])
        
        for i in range(1, len(addi_exprs)):
            right = self.visit(addi_exprs[i])
            
            # Find operator - look at children between operands
            operator = "<"  # default
            for j in range(ctx.getChildCount()):
                child = ctx.getChild(j)
                if hasattr(child, 'getSymbol'):
                    symbol_type = child.getSymbol().type
                    if symbol_type == TyCParser.LESS:
                        operator = "<"
                    elif symbol_type == TyCParser.EQUAL_LESS:
                        operator = "<="
                    elif symbol_type == TyCParser.GRAT:
                        operator = ">"
                    elif symbol_type == TyCParser.EQUAL_GRAT:
                        operator = ">="
            
            result = BinaryOp(result, operator, right)
        return result

    def visitAddiExpr(self, ctx: TyCParser.AddiExprContext):
        """addiExpr : multiExpr ((ADD | SUB) multiExpr)*"""
        multi_exprs = ctx.multiExpr()
        result = self.visit(multi_exprs[0])
        
        for i in range(1, len(multi_exprs)):
            right = self.visit(multi_exprs[i])
            
            # Find operator
            operator = "+"  # default
            for j in range(ctx.getChildCount()):
                child = ctx.getChild(j)
                if hasattr(child, 'getSymbol'):
                    symbol_type = child.getSymbol().type
                    if symbol_type == TyCParser.ADD:
                        operator = "+"
                    elif symbol_type == TyCParser.SUB:
                        operator = "-"
            
            result = BinaryOp(result, operator, right)
        return result

    def visitMultiExpr(self, ctx: TyCParser.MultiExprContext):
        """multiExpr : unaryExpr ((MUL | DIV | MOD) unaryExpr)*"""
        unary_exprs = ctx.unaryExpr()
        result = self.visit(unary_exprs[0])
        
        for i in range(1, len(unary_exprs)):
            right = self.visit(unary_exprs[i])
            
            # Find operator
            operator = "*"  # default
            for j in range(ctx.getChildCount()):
                child = ctx.getChild(j)
                if hasattr(child, 'getSymbol'):
                    symbol_type = child.getSymbol().type
                    if symbol_type == TyCParser.MUL:
                        operator = "*"
                    elif symbol_type == TyCParser.DIV:
                        operator = "/"
                    elif symbol_type == TyCParser.MOD:
                        operator = "%"
            
            result = BinaryOp(result, operator, right)
        return result

    def visitUnaryExpr(self, ctx: TyCParser.UnaryExprContext):
        """unaryExpr : (ADD | SUB | NOT) unaryExpr
                     | (INCREMENT | DECREMENT) unaryExpr
                     | postfixExpr"""
        if ctx.ADD() or ctx.SUB() or ctx.NOT():
            op = ctx.getChild(0).getText()
            operand = self.visit(ctx.unaryExpr())
            return PrefixOp(op, operand)
        elif ctx.INCREMENT() or ctx.DECREMENT():
            op = ctx.getChild(0).getText()
            operand = self.visit(ctx.unaryExpr())
            return PrefixOp(op, operand)
        else:
            return self.visit(ctx.postfixExpr())

    def visitPostfixExpr(self, ctx: TyCParser.PostfixExprContext):
        """postfixExpr : primaryExpr postfixIncDec?"""
        result = self.visit(ctx.primaryExpr())
        if ctx.postfixIncDec():
            op = ctx.postfixIncDec().getChild(0).getText()
            result = PostfixOp(op, result)
        return result

    def visitPrimaryExpr(self, ctx: TyCParser.PrimaryExprContext):
        """primaryExpr : atom (ACCESS ID)*"""
        result = self.visit(ctx.atom())
        
        # Process member accesses
        id_count = 0
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            if hasattr(child, 'getSymbol') and child.getSymbol().type == TyCParser.ACCESS:
                member = ctx.ID(id_count).getText()
                result = MemberAccess(result, member)
                id_count += 1
        
        return result

    def visitAtom(self, ctx: TyCParser.AtomContext):
        """atom : literal
                | ID
                | funcCall
                | struct_lit
                | LP expr RP"""
        if ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.ID():
            return Identifier(ctx.ID().getText())
        elif ctx.funcCall():
            return self.visit(ctx.funcCall())
        elif ctx.struct_lit():
            return self.visit(ctx.struct_lit())
        elif ctx.expr():
            return self.visit(ctx.expr())

    def visitLiteral(self, ctx: TyCParser.LiteralContext):
        """literal : INT_LIT | FLOAT_LIT | STRING_LIT"""
        if ctx.INT_LIT():
            return IntLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())

    def visitFuncCall(self, ctx: TyCParser.FuncCallContext):
        """funcCall : ID LP argList? RP"""
        name = ctx.ID().getText()
        args = []
        if ctx.argList():
            args = self.visit(ctx.argList())
        return FuncCall(name, args)

    def visitArgList(self, ctx: TyCParser.ArgListContext):
        """argList : expr (COMMA expr)*"""
        args = [self.visit(expr) for expr in ctx.expr()]
        return args

    def visitStruct_lit(self, ctx: TyCParser.Struct_litContext):
        """struct_lit : LB (expr (COMMA expr)*)? RB"""
        values = [self.visit(expr) for expr in ctx.expr()]
        return StructLiteral(values)

    def visitInc_dec(self, ctx: TyCParser.Inc_decContext):
        """inc_dec : (INCREMENT | DECREMENT) lhs
                   | lhs (INCREMENT | DECREMENT)"""
        if ctx.lhs():
            lhs = self.visit(ctx.lhs())
            first_child = ctx.getChild(0).getText()
            if first_child in ("++", "--"):
                # Prefix
                return PrefixOp(first_child, lhs)
            else:
                # Postfix
                last_child = ctx.getChild(1).getText()
                return PostfixOp(last_child, lhs)
