# Flo Programming Language

**A modern, expressive, backend-focused programming language**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

Flo is a brand-new, high-level, modern programming language designed for backend and server-side development. It features:

- **Readable and Expressive Syntax**: Clean, PHP-inspired syntax that's easy to learn
- **Extensive Standard Library**: Built-in support for HTTP, databases, JSON, authentication, and more
- **Backend First**: Direct support for HTTP servers, routing, async I/O, and common backend workflows
- **Compile and Run**: Instantly runnable with the Flo CLI (`flo run file.flo`)
- **Modern Features**: Async/await, pattern matching, decorators, and more

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/FoundationINCCorporateTeam/Flo-Lang.git
cd Flo-Lang
```

2. Run your first Flo program:
```bash
python3 src/flo_cli.py run examples/hello.flo
```

### Hello World

Create a file `hello.flo`:

```flo
print("Hello, Flo!")
```

Run it:
```bash
python3 src/flo_cli.py run hello.flo
```

## Language Features

### Variables and Types

Flo is dynamically typed by default, with optional static typing for safety:

```flo
# Variables
name = "Alice"
age = 30
score = 95.5
is_active = true
```

### Functions

Functions in Flo are first-class citizens and can be defined in multiple ways:

```flo
# Regular function
func greet(name) {
    print("Hello,", name)
}

# Arrow function
func add(a, b) => a + b

# Anonymous function
multiply = (x, y) => x * y
```

### Control Flow

```flo
# If-else
if score > 90 => print("Grade: A")
else if score > 80 => print("Grade: B")
else => print("Grade: C")

# While loop
i = 0
while i < 5 {
    print(i)
    i = i + 1
}

# For loop
for num range(1, 10) {
    print(num)
}
```

### Collections

```flo
# Lists
numbers = [1, 2, 3, 4, 5]
first = numbers[0]

# Dictionaries
person = {
    name: "Bob",
    age: 25,
    email: "bob@example.com"
}

email = person["email"]
```

### HTTP Server Example

Here's a complete HTTP API server in Flo:

```flo
@app
    @route "/hello"
    get = => "Hello, Flo!"

    @route "/user/:id"
    get = (id) => {
        name: "User " + id,
        id: id
    }

    @route "/api/status"
    get = => {
        status: "ok",
        version: "1.0.0"
    }

@main =>
    app.listen(5000)
```

### Async/Await

Flo supports asynchronous programming:

```flo
async func fetchData(url) {
    response = await http.get(url)
    return response
}
```

### Error Handling

Robust error handling with try/catch/finally:

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

## Standard Library

Flo comes with an extensive standard library:

### HTTP & Web
- `http`, `https` - Server & client
- `websocket`, `socket` - WebSocket and socket programming
- `template`, `html` - Template rendering

### Data Processing
- `json`, `xml`, `yaml` - Data format parsing
- `csv` - CSV file handling

### Database
- `db`, `sql` - Database abstraction
- `mongo` - MongoDB support
- `redis`, `cache` - Caching

### Authentication & Security
- `auth`, `jwt` - Authentication
- `hash`, `crypto` - Cryptography
- `bcrypt` - Password hashing

### File System
- `fs`, `path`, `io` - File system operations

### Date & Time
- `time`, `datetime`, `tz` - Time and date handling

### Utilities
- `log`, `syslog` - Logging
- `mail`, `smtp` - Email
- `os`, `env`, `cli` - System interaction
- `task`, `sched`, `worker` - Task scheduling

...and hundreds more!

## CLI Commands

### Run a Flo Program
```bash
python3 src/flo_cli.py run myapp.flo
```

### Build a Flo Program
```bash
python3 src/flo_cli.py build myapp.flo
```

### Interactive REPL
```bash
python3 src/flo_cli.py repl
```

### Help
```bash
python3 src/flo_cli.py help
```

## Project Structure

```
Flo-Lang/
├── src/
│   ├── flo/
│   │   ├── lexer/       # Tokenizer
│   │   ├── parser/      # Parser (AST builder)
│   │   ├── interpreter/ # Interpreter
│   │   └── stdlib/      # Standard library
│   └── flo_cli.py       # CLI tool
├── examples/            # Example programs
├── docs/               # Documentation
├── tests/              # Test suite
└── README.md           # This file
```

## Examples

Check out the `examples/` directory for sample programs:

- `hello.flo` - Hello World
- `basics.flo` - Basic syntax demonstration
- `collections.flo` - Lists and dictionaries
- `fibonacci.flo` - Recursive and iterative implementations
- `advanced_functions.flo` - Higher-order functions and closures
- `rest_api.flo` - REST API demonstration
- `web_app.flo` - Complete web application example

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Getting Started Guide](docs/GETTING_STARTED.md) - Learn Flo basics
- [Language Reference](docs/LANGUAGE_REFERENCE.md) - Complete syntax reference
- [Standard Library](docs/STDLIB.md) - Built-in modules and functions
- [Contributing Guide](CONTRIBUTING.md) - How to contribute

## Language Philosophy

Flo is designed with these principles:

1. **Easy to Learn**: Clean syntax with minimal boilerplate
2. **Powerful**: Rich feature set for backend development
3. **Expressive**: Write less code to do more
4. **Consistent**: Predictable behavior and error messages
5. **Modern**: Built for contemporary backend workflows

## Contributing

We welcome contributions! Please feel free to submit issues and pull requests.

## License

Flo is released under the MIT License. See [LICENSE](LICENSE) for details.

## Roadmap

- [x] Core language implementation
- [x] Basic standard library
- [x] CLI tool
- [ ] Full standard library
- [ ] Compiler optimizations
- [ ] Package manager
- [ ] IDE support
- [ ] Production-ready runtime

## Community

- GitHub: [FoundationINCCorporateTeam/Flo-Lang](https://github.com/FoundationINCCorporateTeam/Flo-Lang)
- Issues: [Report bugs and request features](https://github.com/FoundationINCCorporateTeam/Flo-Lang/issues)

## Credits

Created by the Flo Language Team

---

**Ready to build the backend of the future with Flo!** 🚀