# CodeConverter

A simple, extensible tool to convert C code to Python (Java coming soon) using Abstract Syntax Trees (AST).

## Features
- Parses C code using pycparser
- Converts C code to Python via an intermediate, language-agnostic AST
- Supports variable declarations, assignments, print, if/else, while, and for loops
- Modular and easy to extend for more languages and features
- Includes automated tests

## Usage
```bash
python main.py input.c --lang python --output output.py
```

## Example
C input:
```c
int a = 0;
for (a = 0; a < 3; a = a + 1) {
    if (a % 2 == 0) {
        printf("%d", a);
    } else {
        printf("odd");
    }
}
```
Python output:
```python
a = 0
a = 0
while a < 3:
    if a % 2 == 0:
        print(a)
    else:
        print(odd)
    a = a + 1
```

## Setup
```bash
pip install -r requirements.txt
```

## Run Tests
```bash
python tests/test_converter.py
```

## Project Structure
- `main.py`: CLI entry point
- `parser/`: C parser using pycparser
- `converter/`: AST nodes, transformer, and code generators
- `tests/`: Automated tests 