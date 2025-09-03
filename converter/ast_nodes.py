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

class Function(ASTNode):
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params  # list of (type, name) tuples
        self.return_type = return_type
        self.body = body

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Return(ASTNode):
    def __init__(self, value=None):
        self.value = value

class Array(ASTNode):
    def __init__(self, name, size, element_type, values=None):
        self.name = name
        self.size = size
        self.element_type = element_type
        self.values = values  # initialization values

class ArrayAccess(ASTNode):
    def __init__(self, array_name, index):
        self.array_name = array_name
        self.index = index

class Pointer(ASTNode):
    def __init__(self, name, target_type, value=None):
        self.name = name
        self.target_type = target_type
        self.value = value

class Dereference(ASTNode):
    def __init__(self, pointer_name):
        self.pointer_name = pointer_name

class AddressOf(ASTNode):
    def __init__(self, var_name):
        self.var_name = var_name 