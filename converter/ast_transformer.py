from converter.ast_nodes import Program, VarDecl, Assignment, Print, If, While, For
from pycparser.c_ast import FileAST, Decl, Assignment as CAssignment, Constant, FuncCall, ID, If as CIf, While as CWhile, For as CFor, FuncDef, BinaryOp

class ASTTransformer:
    def transform(self, c_ast):
        statements = []
        for ext in getattr(c_ast, 'ext', []):
            stmt = self._transform_node(ext)
            if stmt:
                if isinstance(stmt, list):
                    statements.extend(stmt)
                else:
                    statements.append(stmt)
        return Program(statements)

    def _transform_node(self, node):
        if isinstance(node, Decl):
            var_type = getattr(node.type, 'type', None)
            var_name = node.name
            value = None
            if node.init:
                value = self._transform_expr(node.init)
            return VarDecl(var_type, var_name, value)
        elif hasattr(node, 'body') and hasattr(node.body, 'block_items'):
            stmts = []
            for item in node.body.block_items or []:
                s = self._transform_node(item)
                if s:
                    stmts.append(s)
            return stmts
        elif isinstance(node, CAssignment):
            return Assignment(self._transform_expr(node.lvalue), self._transform_expr(node.rvalue))
        elif isinstance(node, CIf):
            condition = self._transform_expr(node.cond)
            then_body = [self._transform_node(s) for s in (node.iftrue.block_items or [])] if node.iftrue else []
            else_body = [self._transform_node(s) for s in (node.iffalse.block_items or [])] if node.iffalse else []
            return If(condition, then_body, else_body if else_body else None)
        elif isinstance(node, CWhile):
            condition = self._transform_expr(node.cond)
            body = [self._transform_node(s) for s in (node.stmt.block_items or [])] if node.stmt else []
            return While(condition, body)
        elif isinstance(node, CFor):
            init = self._transform_node(node.init) if node.init else None
            condition = self._transform_expr(node.cond) if node.cond else None
            increment = self._transform_node(node.next) if node.next else None
            body = [self._transform_node(s) for s in (node.stmt.block_items or [])] if node.stmt else []
            return For(init, condition, increment, body)
        elif isinstance(node, FuncDef):
            # Process the body of the function
            if hasattr(node.body, 'block_items') and node.body.block_items:
                stmts = []
                for item in node.body.block_items:
                    s = self._transform_node(item)
                    if s:
                        stmts.append(s)
                return stmts
        elif isinstance(node, FuncCall):
            if getattr(node.name, 'name', '') == 'printf':
                args = node.args.exprs if node.args else []
                if args:
                    # If first arg is a string and there is a second arg, print the second arg
                    if len(args) > 1 and getattr(args[0], 'type', None) == 'string':
                        return Print(self._transform_expr(args[1]))
                    # Otherwise, print the first arg
                    return Print(self._transform_expr(args[0]))
        return None

    def _transform_expr(self, expr):
        if isinstance(expr, Constant):
            return expr.value
        elif isinstance(expr, ID):
            return expr.name
        elif isinstance(expr, BinaryOp):
            left = self._transform_expr(expr.left)
            right = self._transform_expr(expr.right)
            return f"{left} {expr.op} {right}"
        return str(expr) 