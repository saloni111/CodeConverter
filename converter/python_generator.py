from .ast_nodes import (Program, VarDecl, Assignment, Print, If, While, For,
                        Function, FunctionCall, Return, Array, ArrayAccess,
                        Pointer, Dereference, AddressOf)

def generate_python(ast, indent=0):
    lines = []
    ind = '    ' * indent
    for stmt in ast.statements:
        if isinstance(stmt, VarDecl):
            if stmt.value is not None:
                lines.append(f"{ind}{stmt.var_name} = {_format_expression(stmt.value)}")
            else:
                lines.append(f"{ind}{stmt.var_name} = None")
        elif isinstance(stmt, Assignment):
            lines.append(f"{ind}{_format_expression(stmt.var_name)} = {_format_expression(stmt.value)}")
        elif isinstance(stmt, Print):
            lines.append(f"{ind}print({_format_expression(stmt.value)})")
        elif isinstance(stmt, If):
            lines.append(f"{ind}if {stmt.condition}:")
            for s in stmt.then_body:
                lines.extend(generate_python(Program([s]), indent+1).split('\n'))
            if stmt.else_body:
                lines.append(f"{ind}else:")
                for s in stmt.else_body:
                    lines.extend(generate_python(Program([s]), indent+1).split('\n'))
        elif isinstance(stmt, While):
            lines.append(f"{ind}while {stmt.condition}:")
            for s in stmt.body:
                lines.extend(generate_python(Program([s]), indent+1).split('\n'))
        elif isinstance(stmt, For):
            # For simplicity, convert C for-loops to Python while-loops
            if stmt.init:
                lines.extend(generate_python(Program([stmt.init]), indent).split('\n'))
            lines.append(f"{ind}while {stmt.condition if stmt.condition else 'True'}:")
            for s in stmt.body:
                lines.extend(generate_python(Program([s]), indent+1).split('\n'))
            if stmt.increment:
                lines.extend(generate_python(Program([stmt.increment]), indent+1).split('\n'))
        elif isinstance(stmt, Function):
            # Generate Python function
            params_str = ', '.join([param[1] for param in stmt.params])
            lines.append(f"{ind}def {stmt.name}({params_str}):")
            if stmt.body:
                for s in stmt.body:
                    lines.extend(generate_python(Program([s]), indent+1).split('\n'))
            else:
                lines.append(f"{ind}    pass")
        elif isinstance(stmt, FunctionCall):
            args_str = ', '.join([_format_expression(arg) for arg in stmt.args])
            lines.append(f"{ind}{stmt.name}({args_str})")
        elif isinstance(stmt, Return):
            if stmt.value:
                lines.append(f"{ind}return {_format_expression(stmt.value)}")
            else:
                lines.append(f"{ind}return")
        elif isinstance(stmt, Array):
            # Arrays in Python are lists
            if stmt.values:
                lines.append(f"{ind}{stmt.name} = {_format_expression(stmt.values)}")
            elif stmt.size:
                lines.append(f"{ind}{stmt.name} = [None] * {_format_expression(stmt.size)}")
            else:
                lines.append(f"{ind}{stmt.name} = []")
        elif isinstance(stmt, Pointer):
            # Pointers in Python are simulated with references
            if stmt.value:
                lines.append(f"{ind}{stmt.name} = {_format_expression(stmt.value)}")
            else:
                lines.append(f"{ind}{stmt.name} = None")
    return '\n'.join(lines)

def _format_expression(expr):
    """Format expressions for Python output"""
    if isinstance(expr, ArrayAccess):
        return f"{_format_expression(expr.array_name)}[{_format_expression(expr.index)}]"
    elif isinstance(expr, Dereference):
        # In Python, we simulate pointer dereferencing by accessing the variable directly
        return f"{_format_expression(expr.pointer_name)}"
    elif isinstance(expr, AddressOf):
        # In Python, we simulate address-of by returning the variable name
        return f"{_format_expression(expr.var_name)}"
    elif isinstance(expr, FunctionCall):
        args_str = ', '.join([_format_expression(arg) for arg in expr.args])
        return f"{expr.name}({args_str})"
    else:
        return str(expr) 