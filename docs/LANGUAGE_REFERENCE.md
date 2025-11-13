# Flo Language Reference

## Table of Contents

1. [Introduction](#introduction)
2. [Syntax](#syntax)
3. [Data Types](#data-types)
4. [Operators](#operators)
5. [Control Flow](#control-flow)
6. [Functions](#functions)
7. [Collections](#collections)
8. [Error Handling](#error-handling)
9. [Modules](#modules)

## Introduction

Flo is a modern, expressive programming language designed for backend development. This document provides a comprehensive reference to the language syntax and features.

## Syntax

### Comments

Comments in Flo start with `#`:

```flo
# This is a single-line comment
x = 42  # Inline comment
```

### Statements

Statements can be terminated with newlines or semicolons:

```flo
x = 10
y = 20; z = 30
```

### Blocks

Blocks can be written with or without braces:

```flo
# With braces
if x > 0 {
    print("positive")
}

# Without braces (single statement)
if x > 0 
    print("positive")
```

## Data Types

### Numbers

Flo supports integers and floating-point numbers:

```flo
x = 42        # Integer
y = 3.14      # Float
z = -10       # Negative number
```

### Strings

Strings can be enclosed in single or double quotes:

```flo
name = "Alice"
greeting = 'Hello'
```

String escaping:
```flo
text = "Line 1\nLine 2"  # Newline
path = "C:\\Users\\Alice" # Backslash
```

### Booleans

```flo
is_active = true
is_disabled = false
```

### Null

```flo
value = null
```

### Lists

```flo
numbers = [1, 2, 3, 4, 5]
mixed = [1, "two", 3.0, true]
empty = []
```

### Dictionaries

```flo
person = {
    name: "Bob",
    age: 30,
    active: true
}

# Access with bracket notation
name = person["name"]
```

## Operators

### Arithmetic Operators

- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division
- `%` Modulo

```flo
sum = 10 + 5
diff = 10 - 5
product = 10 * 5
quotient = 10 / 5
remainder = 10 % 3
```

### Comparison Operators

- `==` Equal to
- `!=` Not equal to
- `<` Less than
- `>` Greater than
- `<=` Less than or equal to
- `>=` Greater than or equal to

```flo
result = x == y
result = x != y
result = x < y
```

### Logical Operators

- `&&` Logical AND
- `||` Logical OR
- `!` Logical NOT

```flo
result = x > 0 && y > 0
result = x > 0 || y > 0
result = !is_active
```

### Assignment Operator

```flo
x = 10
x = x + 5  # x is now 15
```

## Control Flow

### If-Else Statements

Arrow syntax (single expression):

```flo
if x > 0 => print("positive")
else => print("non-positive")
```

Block syntax:

```flo
if x > 0 {
    print("positive")
} else if x < 0 {
    print("negative")
} else {
    print("zero")
}
```

### Ternary Operator

```flo
result = condition ? value_if_true : value_if_false
```

### While Loops

```flo
i = 0
while i < 10 {
    print(i)
    i = i + 1
}
```

### For Loops

```flo
# Iterate over a range
for i range(0, 10) {
    print(i)
}

# Iterate over a list
for item items {
    print(item)
}
```

## Functions

### Function Declaration

Regular function:

```flo
func greet(name) {
    print("Hello,", name)
}

greet("Alice")
```

### Arrow Functions

Single expression:

```flo
func add(a, b) => a + b

result = add(5, 3)  # 8
```

### Anonymous Functions

```flo
# Assigned to variable
square = (x) => x * x

# Without parameters
hello = => print("Hello!")
```

### Return Statement

```flo
func max(a, b) {
    if a > b {
        return a
    }
    return b
}
```

### Async Functions

```flo
async func fetchData(url) {
    response = await http.get(url)
    return response
}
```

## Collections

### List Operations

```flo
# Create list
numbers = [1, 2, 3, 4, 5]

# Access element
first = numbers[0]

# Length
size = len(numbers)
```

### Dictionary Operations

```flo
# Create dictionary
person = {
    name: "Alice",
    age: 30
}

# Access value
name = person["name"]

# Check key exists
if person["email"] => print("Has email")
```

## Error Handling

### Try-Catch-Finally

```flo
try {
    result = riskyOperation()
    print(result)
} catch error {
    print("Error:", error)
} finally {
    print("Cleanup")
}
```

## Modules

### Built-in Functions

- `print(...args)` - Print to console
- `len(obj)` - Get length of collection
- `str(obj)` - Convert to string
- `int(obj)` - Convert to integer
- `float(obj)` - Convert to float
- `type(obj)` - Get type name
- `range(start, end)` - Generate range

### Standard Library

Import modules using decorators (syntax varies):

```flo
# HTTP module
@http
    server.listen(8000)

# JSON module
json.parse(text)
json.stringify(obj)
```

## Best Practices

1. Use descriptive variable names
2. Keep functions small and focused
3. Handle errors appropriately
4. Comment complex logic
5. Use consistent formatting

## Examples

### Hello World

```flo
print("Hello, World!")
```

### Factorial Function

```flo
func factorial(n) {
    if n <= 1 => return 1
    return n * factorial(n - 1)
}

print(factorial(5))  # 120
```

### Simple HTTP Server

```flo
@app
    @route "/hello"
    get = => "Hello, Flo!"

@main =>
    app.listen(8000)
```
