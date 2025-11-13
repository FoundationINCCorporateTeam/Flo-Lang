# Getting Started with Flo

Welcome to Flo! This guide will help you get up and running with the Flo programming language.

## Installation

1. **Clone the Repository**

```bash
git clone https://github.com/FoundationINCCorporateTeam/Flo-Lang.git
cd Flo-Lang
```

2. **Prerequisites**

Flo requires Python 3.8 or higher. Check your Python version:

```bash
python3 --version
```

3. **Verify Installation**

Test the CLI:

```bash
python3 src/flo_cli.py version
```

## Your First Flo Program

### Hello World

Create a file called `hello.flo`:

```flo
print("Hello, Flo!")
```

Run it:

```bash
python3 src/flo_cli.py run hello.flo
```

Output:
```
Hello, Flo!
```

### Working with Variables

Create `variables.flo`:

```flo
# Variables are dynamically typed
name = "Alice"
age = 30
height = 5.6

print("Name:", name)
print("Age:", age)
print("Height:", height)
```

Run it:
```bash
python3 src/flo_cli.py run variables.flo
```

### Simple Calculator

Create `calculator.flo`:

```flo
# Define functions
func add(a, b) => a + b
func subtract(a, b) => a - b
func multiply(a, b) => a * b
func divide(a, b) => a / b

# Test the calculator
x = 10
y = 5

print("Addition:", add(x, y))
print("Subtraction:", subtract(x, y))
print("Multiplication:", multiply(x, y))
print("Division:", divide(x, y))
```

## Using the CLI

### Run Command

Execute a Flo program:

```bash
python3 src/flo_cli.py run myprogram.flo
```

### Build Command

Compile a Flo program (coming soon):

```bash
python3 src/flo_cli.py build myprogram.flo
```

### REPL (Interactive Mode)

Start the interactive REPL:

```bash
python3 src/flo_cli.py repl
```

Try it out:
```
flo> x = 10
flo> y = 20
flo> x + y
30
flo> print("Hello from REPL!")
Hello from REPL!
flo> exit
```

### Help Command

Get help:

```bash
python3 src/flo_cli.py help
```

## Language Basics

### Data Types

```flo
# Numbers
integer = 42
decimal = 3.14

# Strings
text = "Hello"
message = 'World'

# Booleans
is_active = true
is_disabled = false

# Null
empty = null

# Lists
numbers = [1, 2, 3, 4, 5]

# Dictionaries
person = {
    name: "Bob",
    age: 25
}
```

### Control Flow

```flo
# If-else
score = 85

if score >= 90 => print("A")
else if score >= 80 => print("B")
else if score >= 70 => print("C")
else => print("F")

# While loop
i = 1
while i <= 5 {
    print(i)
    i = i + 1
}

# For loop
for num range(1, 6) {
    print(num)
}
```

### Functions

```flo
# Regular function
func greet(name) {
    print("Hello,", name)
}

# Arrow function
func square(x) => x * x

# Anonymous function
double = (x) => x * 2

# Call functions
greet("Alice")
print(square(5))
print(double(10))
```

## Working with Collections

### Lists

```flo
# Create a list
fruits = ["apple", "banana", "orange"]

# Access elements
first = fruits[0]
print("First fruit:", first)

# Get length
count = len(fruits)
print("Number of fruits:", count)

# Iterate
for fruit fruits {
    print("Fruit:", fruit)
}
```

### Dictionaries

```flo
# Create a dictionary
user = {
    name: "Alice",
    email: "alice@example.com",
    age: 28
}

# Access values
print("Name:", user["name"])
print("Email:", user["email"])

# Modify values
user["age"] = 29
```

## Error Handling

```flo
try {
    # Risky operation
    result = 10 / 0
    print(result)
} catch error {
    print("Error occurred:", error)
} finally {
    print("Cleanup code runs always")
}
```

## Next Steps

1. **Explore Examples**: Check out the `examples/` directory for more programs
2. **Read the Language Reference**: See `docs/LANGUAGE_REFERENCE.md` for detailed syntax
3. **Try Building Something**: Start with simple programs and gradually increase complexity

## Common Tasks

### Reading User Input (Coming Soon)

```flo
# Future feature
name = input("Enter your name: ")
print("Hello,", name)
```

### Working with Files (Coming Soon)

```flo
# Future feature with fs module
content = fs.read("data.txt")
print(content)
```

### Building a Web API (Coming Soon)

```flo
# Future feature with http module
@app
    @route "/api/hello"
    get = => {status: "ok", message: "Hello!"}

@main =>
    app.listen(8000)
```

## Troubleshooting

### Syntax Errors

If you get a syntax error, check:
- Correct use of brackets, braces, and parentheses
- Proper function syntax
- Valid variable names

### Runtime Errors

Common runtime errors:
- `Undefined variable`: Variable not defined before use
- `Not a function`: Trying to call a non-function value

## Resources

- GitHub: [FoundationINCCorporateTeam/Flo-Lang](https://github.com/FoundationINCCorporateTeam/Flo-Lang)
- Language Reference: `docs/LANGUAGE_REFERENCE.md`
- Examples: `examples/` directory

## Getting Help

- Open an issue on GitHub
- Check the documentation
- Review example programs

Happy coding with Flo! 🚀
