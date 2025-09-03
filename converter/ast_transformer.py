from converter.ast_nodes import (Program, VarDecl, Assignment, Print, If, While, For, 
                                Function, FunctionCall, Return, Array, ArrayAccess, 
                                Pointer, Dereference, AddressOf)
from pycparser.c_ast import (FileAST, Decl, Assignment as CAssignment, Constant, 
                            FuncCall as CFuncCall, ID, If as CIf, While as CWhile, 
                            For as CFor, FuncDef, BinaryOp, Return as CReturn,
                            ArrayDecl, ArrayRef, PtrDecl, UnaryOp)

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
            # Handle different declaration types
            if isinstance(node.type, ArrayDecl):
                return self._transform_array_decl(node)
            elif isinstance(node.type, PtrDecl):
                return self._transform_pointer_decl(node)
            else:
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
            # Transform function definition
            func_name = node.decl.name
            return_type = getattr(node.decl.type.type, 'type', 'void')
            
            # Extract parameters
            params = []
            if node.decl.type.args:
                for param in node.decl.type.args.params:
                    param_type = getattr(param.type, 'type', None)
                    param_name = param.name
                    params.append((param_type, param_name))
            
            # Transform function body
            body = []
            if hasattr(node.body, 'block_items') and node.body.block_items:
                for item in node.body.block_items:
                    s = self._transform_node(item)
                    if s:
                        body.append(s)
            
            return Function(func_name, params, return_type, body)
        elif isinstance(node, CReturn):
            value = self._transform_expr(node.expr) if node.expr else None
            return Return(value)
        elif isinstance(node, CFuncCall):
            func_name = getattr(node.name, 'name', '')
            if func_name == 'printf':
                args = node.args.exprs if node.args else []
                if args:
                    # If first arg is a string and there is a second arg, print the second arg
                    if len(args) > 1 and getattr(args[0], 'type', None) == 'string':
                        return Print(self._transform_expr(args[1]))
                    # Otherwise, print the first arg
                    return Print(self._transform_expr(args[0]))
            else:
                # Regular function call
                args = [self._transform_expr(arg) for arg in (node.args.exprs if node.args else [])]
                return FunctionCall(func_name, args)
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
        elif isinstance(expr, ArrayRef):
            array_name = self._transform_expr(expr.name)
            index = self._transform_expr(expr.subscript)
            return ArrayAccess(array_name, index)
        elif isinstance(expr, UnaryOp):
            if expr.op == '*':  # Dereference
                operand = self._transform_expr(expr.expr)
                return Dereference(operand)
            elif expr.op == '&':  # Address-of
                operand = self._transform_expr(expr.expr)
                return AddressOf(operand)
        elif isinstance(expr, CFuncCall):
            func_name = getattr(expr.name, 'name', '')
            args = [self._transform_expr(arg) for arg in (expr.args.exprs if expr.args else [])]
            return FunctionCall(func_name, args)
        return str(expr)
    
    def _transform_array_decl(self, node):
        """Transform array declaration"""
        array_name = node.name
        array_type = node.type
        element_type = getattr(array_type.type, 'type', 'int')
        
        # Get array size
        size = None
        if array_type.dim:
            size = self._transform_expr(array_type.dim)
        
        # Get initialization values
        values = None
        if node.init:
            values = self._transform_expr(node.init)
        
        return Array(array_name, size, element_type, values)
    
    def _transform_pointer_decl(self, node):
        """Transform pointer declaration"""
        pointer_name = node.name
        target_type = getattr(node.type.type, 'type', 'int')
        
        value = None
        if node.init:
            value = self._transform_expr(node.init)
        
        return Pointer(pointer_name, target_type, value) 