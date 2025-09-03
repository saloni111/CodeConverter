from .ast_nodes import (Program, VarDecl, Assignment, Print, If, While, For,
                        Function, FunctionCall, Return, Array, ArrayAccess,
                        Pointer, Dereference, AddressOf)

def generate_c(ast, indent=0):
    """Generate C code from our AST"""
    lines = []
    ind = '    ' * indent
    
    for stmt in ast.statements:
        if isinstance(stmt, VarDecl):
            var_type = stmt.var_type or 'int'
            if stmt.value is not None:
                lines.append(f"{ind}{var_type} {stmt.var_name} = {_format_c_expression(stmt.value)};")
            else:
                lines.append(f"{ind}{var_type} {stmt.var_name};")
        elif isinstance(stmt, Assignment):
            lines.append(f"{ind}{stmt.var_name} = {_format_c_expression(stmt.value)};")
        elif isinstance(stmt, Print):
            lines.append(f'{ind}printf("%s\\n", {_format_c_expression(stmt.value)});')
        elif isinstance(stmt, If):
            lines.append(f"{ind}if ({stmt.condition}) {{")
            for s in stmt.then_body:
                lines.extend(generate_c(Program([s]), indent+1).split('\n'))
            if stmt.else_body:
                lines.append(f"{ind}}} else {{")
                for s in stmt.else_body:
                    lines.extend(generate_c(Program([s]), indent+1).split('\n'))
            lines.append(f"{ind}}}")
        elif isinstance(stmt, While):
            lines.append(f"{ind}while ({stmt.condition}) {{")
            for s in stmt.body:
                lines.extend(generate_c(Program([s]), indent+1).split('\n'))
            lines.append(f"{ind}}}")
        elif isinstance(stmt, For):
            init_str = generate_c(Program([stmt.init]), 0).strip() if stmt.init else ""
            if init_str.endswith(';'):
                init_str = init_str[:-1]  # Remove semicolon
            condition_str = stmt.condition if stmt.condition else ""
            increment_str = generate_c(Program([stmt.increment]), 0).strip() if stmt.increment else ""
            if increment_str.endswith(';'):
                increment_str = increment_str[:-1]  # Remove semicolon
            
            lines.append(f"{ind}for ({init_str}; {condition_str}; {increment_str}) {{")
            for s in stmt.body:
                lines.extend(generate_c(Program([s]), indent+1).split('\n'))
            lines.append(f"{ind}}}")
        elif isinstance(stmt, Function):
            # Generate C function
            return_type = stmt.return_type or 'void'
            params_str = ', '.join([f"{param[0]} {param[1]}" for param in stmt.params])
            lines.append(f"{ind}{return_type} {stmt.name}({params_str}) {{")
            if stmt.body:
                for s in stmt.body:
                    lines.extend(generate_c(Program([s]), indent+1).split('\n'))
            lines.append(f"{ind}}}")
        elif isinstance(stmt, FunctionCall):
            args_str = ', '.join([_format_c_expression(arg) for arg in stmt.args])
            lines.append(f"{ind}{stmt.name}({args_str});")
        elif isinstance(stmt, Return):
            if stmt.value:
                lines.append(f"{ind}return {_format_c_expression(stmt.value)};")
            else:
                lines.append(f"{ind}return;")
        elif isinstance(stmt, Array):
            element_type = stmt.element_type or 'int'
            if stmt.size:
                lines.append(f"{ind}{element_type} {stmt.name}[{_format_c_expression(stmt.size)}];")
            else:
                lines.append(f"{ind}{element_type} {stmt.name}[];")
        elif isinstance(stmt, Pointer):
            target_type = stmt.target_type or 'int'
            if stmt.value:
                lines.append(f"{ind}{target_type}* {stmt.name} = {_format_c_expression(stmt.value)};")
            else:
                lines.append(f"{ind}{target_type}* {stmt.name};")
    
    return '\n'.join(lines)

def _format_c_expression(expr):
    """Format expressions for C output"""
    if isinstance(expr, ArrayAccess):
        return f"{_format_c_expression(expr.array_name)}[{_format_c_expression(expr.index)}]"
    elif isinstance(expr, Dereference):
        return f"*{_format_c_expression(expr.pointer_name)}"
    elif isinstance(expr, AddressOf):
        return f"&{_format_c_expression(expr.var_name)}"
    elif isinstance(expr, FunctionCall):
        args_str = ', '.join([_format_c_expression(arg) for arg in expr.args])
        return f"{expr.name}({args_str})"
    else:
        return str(expr)
