# CodeConverter

Hey! 👋 This tool converts code between C and Python. It's like having a translator that speaks both languages!

## What it does

- **C → Python**: Give it C code, get Python back
- **Python → C**: Give it Python code, get C back  
- **Auto-detects** what you're converting
- **Handles functions, arrays, loops, and more**

## Quick start

1. **Install**: `pip install -r requirements.txt`
2. **Convert**: `python main.py input.c --output output.py`
3. **Done!** 🎉

## Examples

**C to Python:**
```bash
python main.py mycode.c --output mycode.py
```

**Python to C:**
```bash
python main.py mycode.py --output mycode.c
```

## What it supports

✅ **Functions** - `int add(int a, int b)` ↔ `def add(a, b):`  
✅ **Arrays** - `int arr[5]` ↔ `arr = [None] * 5`  
✅ **Loops** - `while (i < 10)` ↔ `while i < 10:`  
✅ **Variables** - `int x = 5;` ↔ `x = 5`  
✅ **Print** - `printf("hello");` ↔ `print("hello")`

## Test it

```bash
python tests/test_converter.py
python tests/test_advanced_converter.py
```

## Got questions?

- **File not found?** Check your file exists and you're in the right folder
- **Parse error?** Make sure your code is valid (C needs `int main()`)
- **Import error?** Run `pip install -r requirements.txt` first

## What it can't do

- Complex C stuff like structs, unions
- Preprocessor stuff (#include, #define)  
- Dynamic memory (malloc/free)
- Multiple files

---

That's it! Pretty simple, right? Just give it code in one language and get it back in the other. Happy converting! 🚀 