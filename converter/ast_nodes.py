class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VarDecl(ASTNode):
    def __init__(self, var_type, var_name, value=None):
        self.var_type = var_type
        self.var_name = var_name
        self.value = value

class Assignment(ASTNode):
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

class Print(ASTNode):
    def __init__(self, value):
        self.value = value

class If(ASTNode):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class While(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class For(ASTNode):
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body 