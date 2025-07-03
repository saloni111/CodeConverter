import argparse
from parser.c_parser import CParser
from converter.ast_transformer import ASTTransformer
from converter.python_generator import generate_python

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="C to Python/Java Code Converter")
    parser.add_argument("input", help="Input C file")
    parser.add_argument("--lang", choices=["python", "java"], default="python", help="Target language")
    parser.add_argument("--output", help="Output file", required=True)
    args = parser.parse_args()

    print(f"Input file: {args.input}")
    print(f"Target language: {args.lang}")
    print(f"Output file: {args.output}")

    with open(args.input) as f:
        c_code = f.read()

    parser = CParser()
    c_ast = parser.parse(c_code)

    transformer = ASTTransformer()
    lang_ast = transformer.transform(c_ast)

    if args.lang == "python":
        output_code = generate_python(lang_ast)
    else:
        raise NotImplementedError("Java generation not implemented yet.")

    with open(args.output, "w") as out_f:
        out_f.write(output_code)
    print(f"Conversion complete. Output written to {args.output}") 