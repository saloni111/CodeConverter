from .ast_nodes import Program, VarDecl, Assignment, Print, If, While, For

def generate_python(ast, indent=0):
    lines = []
    ind = '    ' * indent
    for stmt in ast.statements:
        if isinstance(stmt, VarDecl):
            if stmt.value is not None:
                lines.append(f"{ind}{stmt.var_name} = {stmt.value}")
            else:
                lines.append(f"{ind}{stmt.var_name} = None")
        elif isinstance(stmt, Assignment):
            lines.append(f"{ind}{stmt.var_name} = {stmt.value}")
        elif isinstance(stmt, Print):
            lines.append(f"{ind}print({stmt.value})")
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
    return '\n'.join(lines) 