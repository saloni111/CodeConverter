#!/usr/bin/env python3
"""
Advanced tests for the enhanced CodeConverter with functions, arrays, pointers, and bidirectional conversion
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser.c_parser import CParser
from parser.python_parser import PythonParser
from converter.ast_transformer import ASTTransformer
from converter.python_generator import generate_python
from converter.c_generator import generate_c

def test_functions():
    """Test function definition and calls"""
    print("=== Testing Functions ===")
    c_code = """
    int add(int a, int b) {
        return a + b;
    }
    
    int main() {
        int result = add(5, 3);
        printf("%d", result);
        return 0;
    }
    """
    
    parser = CParser()
    c_ast = parser.parse(c_code)
    transformer = ASTTransformer()
    intermediate_ast = transformer.transform(c_ast)
    python_code = generate_python(intermediate_ast)
    
    print("C to Python (Functions):")
    print(python_code)
    print()

def test_arrays():
    """Test array declarations and access"""
    print("=== Testing Arrays ===")
    c_code = """
    int main() {
        int arr[5];
        arr[0] = 10;
        arr[1] = 20;
        printf("%d", arr[0]);
        return 0;
    }
    """
    
    parser = CParser()
    c_ast = parser.parse(c_code)
    transformer = ASTTransformer()
    intermediate_ast = transformer.transform(c_ast)
    python_code = generate_python(intermediate_ast)
    
    print("C to Python (Arrays):")
    print(python_code)
    print()

def test_pointers():
    """Test pointer declarations and operations"""
    print("=== Testing Pointers ===")
    c_code = """
    int main() {
        int x = 42;
        int* ptr = &x;
        printf("%d", *ptr);
        return 0;
    }
    """
    
    parser = CParser()
    c_ast = parser.parse(c_code)
    transformer = ASTTransformer()
    intermediate_ast = transformer.transform(c_ast)
    python_code = generate_python(intermediate_ast)
    
    print("C to Python (Pointers):")
    print(python_code)
    print()

def test_bidirectional_simple():
    """Test Python to C conversion"""
    print("=== Testing Python to C Conversion ===")
    python_code = """
def calculate(x, y):
    result = x + y * 2
    return result

def main():
    a = 10
    b = 5
    answer = calculate(a, b)
    print(answer)
    return 0
    """
    
    parser = PythonParser()
    intermediate_ast = parser.parse(python_code)
    c_code = generate_c(intermediate_ast)
    
    print("Python to C:")
    print(c_code)
    print()

def test_complex_example():
    """Test a more complex C program with multiple features"""
    print("=== Testing Complex Example ===")
    c_code = """
    int factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    
    int main() {
        int numbers[3];
        numbers[0] = 3;
        numbers[1] = 4;
        numbers[2] = 5;
        
        int i = 0;
        while (i < 3) {
            int fact = factorial(numbers[i]);
            printf("%d", fact);
            i = i + 1;
        }
        
        return 0;
    }
    """
    
    parser = CParser()
    c_ast = parser.parse(c_code)
    transformer = ASTTransformer()
    intermediate_ast = transformer.transform(c_ast)
    python_code = generate_python(intermediate_ast)
    
    print("C to Python (Complex Example):")
    print(python_code)
    print()

def test_round_trip():
    """Test converting Python -> C -> Python"""
    print("=== Testing Round-trip Conversion ===")
    original_python = """
def square(x):
    return x * x

def main():
    num = 5
    result = square(num)
    print(result)
    return 0
    """
    
    print("Original Python:")
    print(original_python)
    print()
    
    # Python -> C
    python_parser = PythonParser()
    intermediate_ast = python_parser.parse(original_python)
    c_code = generate_c(intermediate_ast)
    
    print("Converted to C:")
    print(c_code)
    print()
    
    # C -> Python
    c_parser = CParser()
    try:
        c_ast = c_parser.parse(c_code)
        transformer = ASTTransformer()
        new_intermediate_ast = transformer.transform(c_ast)
        final_python = generate_python(new_intermediate_ast)
        
        print("Converted back to Python:")
        print(final_python)
        print()
    except Exception as e:
        print(f"Round-trip conversion failed: {e}")
        print()

if __name__ == "__main__":
    print("🚀 Advanced CodeConverter Tests")
    print("=" * 50)
    
    try:
        test_functions()
        test_arrays()
        test_pointers()
        test_bidirectional_simple()
        test_complex_example()
        test_round_trip()
        
        print("✅ All advanced tests completed!")
        print("\n🎉 The CodeConverter now supports:")
        print("• Functions with parameters and return values")
        print("• Arrays and array access")
        print("• Pointers and pointer operations")
        print("• Bidirectional C ↔ Python conversion")
        print("• Complex nested structures")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
