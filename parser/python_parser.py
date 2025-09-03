import ast
from converter.ast_nodes import (Program, VarDecl, Assignment, Print, If, While, For,
                                Function, FunctionCall, Return, Array, ArrayAccess)

class PythonParser:
    """Parser for converting Python AST to our intermediate AST"""
    
    def parse(self, python_code):
        """Parse Python code and return our intermediate AST"""
        try:
            python_ast = ast.parse(python_code)
            statements = []
            
            for node in python_ast.body:
                stmt = self._transform_python_node(node)
                if stmt:
                    statements.append(stmt)
            
            return Program(statements)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}")
    
    def _transform_python_node(self, node):
        """Transform a Python AST node to our intermediate representation"""
        if isinstance(node, ast.Assign):
            # Handle assignments like x = 5
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id
                value = self._transform_python_expr(node.value)
                # Determine if this is a declaration or assignment
                # For simplicity, treat as VarDecl with type inference
                return VarDecl('int', var_name, value)
            elif len(node.targets) == 1 and isinstance(node.targets[0], ast.Subscript):
                # Array assignment like arr[0] = 5
                target = self._transform_python_expr(node.targets[0])
                value = self._transform_python_expr(node.value)
                return Assignment(target, value)
        
        elif isinstance(node, ast.Expr):
            # Handle expression statements (like function calls)
            return self._transform_python_expr(node.value)
        
        elif isinstance(node, ast.FunctionDef):
            # Handle function definitions
            params = [(self._infer_type(arg.arg), arg.arg) for arg in node.args.args]
            body = []
            for stmt in node.body:
                transformed = self._transform_python_node(stmt)
                if transformed:
                    body.append(transformed)
            return Function(node.name, params, 'int', body)  # Default return type
        
        elif isinstance(node, ast.Return):
            value = self._transform_python_expr(node.value) if node.value else None
            return Return(value)
        
        elif isinstance(node, ast.If):
            condition = self._transform_python_expr(node.test)
            then_body = []
            for stmt in node.body:
                transformed = self._transform_python_node(stmt)
                if transformed:
                    then_body.append(transformed)
            
            else_body = []
            for stmt in node.orelse:
                transformed = self._transform_python_node(stmt)
                if transformed:
                    else_body.append(transformed)
            
            return If(condition, then_body, else_body if else_body else None)
        
        elif isinstance(node, ast.While):
            condition = self._transform_python_expr(node.test)
            body = []
            for stmt in node.body:
                transformed = self._transform_python_node(stmt)
                if transformed:
                    body.append(transformed)
            return While(condition, body)
        
        return None
    
    def _transform_python_expr(self, expr):
        """Transform Python expressions"""
        if isinstance(expr, ast.Constant):
            return expr.value
        elif isinstance(expr, ast.Name):
            return expr.id
        elif isinstance(expr, ast.BinOp):
            left = self._transform_python_expr(expr.left)
            right = self._transform_python_expr(expr.right)
            op = self._get_operator(expr.op)
            return f"{left} {op} {right}"
        elif isinstance(expr, ast.Compare):
            left = self._transform_python_expr(expr.left)
            # Handle single comparison for simplicity
            if len(expr.ops) == 1 and len(expr.comparators) == 1:
                op = self._get_compare_op(expr.ops[0])
                right = self._transform_python_expr(expr.comparators[0])
                return f"{left} {op} {right}"
        elif isinstance(expr, ast.Call):
            func_name = self._transform_python_expr(expr.func)
            if func_name == 'print':
                # Convert print to our Print node
                if expr.args:
                    return Print(self._transform_python_expr(expr.args[0]))
            else:
                # Regular function call
                args = [self._transform_python_expr(arg) for arg in expr.args]
                return FunctionCall(func_name, args)
        elif isinstance(expr, ast.Subscript):
            # Array access like arr[0]
            array_name = self._transform_python_expr(expr.value)
            index = self._transform_python_expr(expr.slice)
            return ArrayAccess(array_name, index)
        elif isinstance(expr, ast.List):
            # Python list -> Array initialization
            values = [self._transform_python_expr(item) for item in expr.elts]
            return values
        
        return str(expr)
    
    def _get_operator(self, op):
        """Convert Python AST operators to string"""
        if isinstance(op, ast.Add):
            return '+'
        elif isinstance(op, ast.Sub):
            return '-'
        elif isinstance(op, ast.Mult):
            return '*'
        elif isinstance(op, ast.Div):
            return '/'
        elif isinstance(op, ast.Mod):
            return '%'
        return str(op)
    
    def _get_compare_op(self, op):
        """Convert Python comparison operators to string"""
        if isinstance(op, ast.Lt):
            return '<'
        elif isinstance(op, ast.Gt):
            return '>'
        elif isinstance(op, ast.LtE):
            return '<='
        elif isinstance(op, ast.GtE):
            return '>='
        elif isinstance(op, ast.Eq):
            return '=='
        elif isinstance(op, ast.NotEq):
            return '!='
        return str(op)
    
    def _infer_type(self, param_name):
        """Simple type inference for parameters"""
        # For now, default to int
        # In a more sophisticated version, you could analyze usage
        return 'int'
