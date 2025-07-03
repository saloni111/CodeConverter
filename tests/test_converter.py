import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from parser.c_parser import CParser
from converter.ast_transformer import ASTTransformer
from converter.python_generator import generate_python

DEBUG = True

def run_conversion(c_code):
    parser = CParser()
    c_ast = parser.parse(c_code)
    transformer = ASTTransformer()
    lang_ast = transformer.transform(c_ast)
    return generate_python(lang_ast)

def test_var_decl_and_assignment():
    c_code = 'int main() { int a = 5; a = 10; printf("%d", a); }'
    py_code = run_conversion(c_code)
    if DEBUG:
        print('test_var_decl_and_assignment output:')
        print(py_code)
    assert 'a = 5' in py_code
    assert 'a = 10' in py_code
    assert 'print(a)' in py_code

def test_if_else():
    c_code = '''
    int main() {
    int a = 2;
    if (a > 1) {
        printf("big");
    } else {
        printf("small");
    }
    }
    '''
    py_code = run_conversion(c_code)
    if DEBUG:
        print('test_if_else output:')
        print(py_code)
    assert 'if a > 1:' in py_code
    assert 'print(big)' in py_code or 'print("big")' in py_code
    assert 'else:' in py_code

def test_while():
    c_code = '''
    int main() {
    int i = 0;
    while (i < 3) {
        printf("%d", i);
        i = i + 1;
    }
    }
    '''
    py_code = run_conversion(c_code)
    if DEBUG:
        print('test_while output:')
        print(py_code)
    assert 'while i < 3:' in py_code
    assert 'i = i + 1' in py_code

def test_for():
    c_code = '''
    int main() {
    int a = 0;
    for (a = 0; a < 3; a = a + 1) {
        printf("%d", a);
    }
    }
    '''
    py_code = run_conversion(c_code)
    if DEBUG:
        print('test_for output:')
        print(py_code)
    assert 'while a < 3:' in py_code
    assert 'a = a + 1' in py_code

def run_all():
    test_var_decl_and_assignment()
    test_if_else()
    test_while()
    test_for()
    print('All tests passed!')

if __name__ == "__main__":
    run_all() 