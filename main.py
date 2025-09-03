import argparse
import os
from parser.c_parser import CParser
from parser.python_parser import PythonParser
from converter.ast_transformer import ASTTransformer
from converter.python_generator import generate_python
from converter.c_generator import generate_c

def detect_input_language(filename):
    """Detect input language based on file extension"""
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.c':
        return 'c'
    elif ext == '.py':
        return 'python'
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bidirectional C ↔ Python Code Converter")
    parser.add_argument("input", help="Input file (.c or .py)")
    parser.add_argument("--target", choices=["python", "c"], help="Target language (auto-detected if not specified)")
    parser.add_argument("--output", help="Output file", required=True)
    args = parser.parse_args()

    # Detect input and target languages
    input_lang = detect_input_language(args.input)
    
    if args.target:
        target_lang = args.target
    else:
        # Auto-detect target based on input
        target_lang = 'python' if input_lang == 'c' else 'c'

    print(f"Input file: {args.input} ({input_lang})")
    print(f"Target language: {target_lang}")
    print(f"Output file: {args.output}")

    # Read input file
    with open(args.input) as f:
        input_code = f.read()

    # Parse based on input language
    if input_lang == 'c':
        parser_obj = CParser()
        source_ast = parser_obj.parse(input_code)
        transformer = ASTTransformer()
        intermediate_ast = transformer.transform(source_ast)
    else:  # python
        parser_obj = PythonParser()
        intermediate_ast = parser_obj.parse(input_code)

    # Generate output based on target language
    if target_lang == "python":
        output_code = generate_python(intermediate_ast)
    elif target_lang == "c":
        output_code = generate_c(intermediate_ast)
    else:
        raise ValueError(f"Unsupported target language: {target_lang}")

    # Write output
    with open(args.output, "w") as out_f:
        out_f.write(output_code)
    
    print(f"Conversion complete! {input_lang.upper()} → {target_lang.upper()}")
    print(f"Output written to {args.output}") 