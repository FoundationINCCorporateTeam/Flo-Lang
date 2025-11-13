# Flo Standard Library Documentation

This document describes the standard library modules available in Flo.

## Built-in Functions

These functions are available without importing any modules:

### `print(...args)`

Print values to the console.

```flo
print("Hello")
print("x =", 42)
print("Multiple", "values")
```

### `len(obj)`

Get the length of a collection or string.

```flo
len([1, 2, 3])        # 3
len("hello")          # 5
len({a: 1, b: 2})     # 2
```

### `str(obj)`

Convert a value to a string.

```flo
str(42)      # "42"
str(3.14)    # "3.14"
str(true)    # "True"
```

### `int(obj)`

Convert a value to an integer.

```flo
int(3.14)    # 3
int("42")    # 42
```

### `float(obj)`

Convert a value to a float.

```flo
float(42)     # 42.0
float("3.14") # 3.14
```

### `type(obj)`

Get the type name of a value.

```flo
type(42)          # "int"
type("hello")     # "str"
type([1, 2, 3])   # "list"
```

### `range(start, end)`

Generate a list of numbers.

```flo
range(0, 5)      # [0, 1, 2, 3, 4]
range(1, 10)     # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## HTTP Module

**Status**: In Development

The HTTP module provides server and client functionality.

### Server Example (Planned Syntax)

```flo
@app
    @route "/hello"
    get = => "Hello, World!"
    
    @route "/user/:id"
    get = (id) => {
        id: id,
        name: "User " + id
    }

@main =>
    app.listen(8000)
```

### HTTP Methods

- `GET` - Retrieve resources
- `POST` - Create resources
- `PUT` - Update resources
- `DELETE` - Delete resources

## JSON Module

**Status**: Implemented

Parse and stringify JSON data.

### Functions

#### `json.parse(text)`

Parse JSON string to object.

```flo
data = json.parse('{"name": "Alice", "age": 30}')
print(data["name"])  # Alice
```

#### `json.stringify(obj, indent=None)`

Convert object to JSON string.

```flo
person = {name: "Bob", age: 25}
jsonText = json.stringify(person)
print(jsonText)  # {"name": "Bob", "age": 25}
```

#### Aliases

- `json.encode(obj)` - Alias for `json.stringify`
- `json.decode(text)` - Alias for `json.parse`

## Database Module

**Status**: Planned

Database abstraction layer for SQL and NoSQL databases.

### Planned Features

```flo
# SQL Database
db = sql.connect("postgresql://localhost/mydb")
users = db.table("users")

user = users.find(1)
allUsers = users.all()
activeUsers = users.where("active", true)

# MongoDB
mongo = mongo.connect("mongodb://localhost/mydb")
collection = mongo.collection("users")

doc = collection.findOne({name: "Alice"})
```

## Authentication Module

**Status**: Planned

Authentication and authorization utilities.

### Planned Features

```flo
# JWT
token = jwt.encode({userId: 123}, "secret")
payload = jwt.decode(token, "secret")

# Password Hashing
hashed = hash.make("password123")
valid = hash.verify("password123", hashed)

# Bcrypt
hashed = bcrypt.hash("password", 10)
valid = bcrypt.compare("password", hashed)
```

## File System Module

**Status**: Planned

File system operations.

### Planned Features

```flo
# Read file
content = fs.read("file.txt")

# Write file
fs.write("output.txt", "Hello, World!")

# Check if file exists
if fs.exists("file.txt") => print("File exists")

# List directory
files = fs.list("/path/to/dir")

# Path operations
fullPath = path.join("dir", "file.txt")
extension = path.ext("file.txt")  # ".txt"
```

## Time/Date Module

**Status**: Planned

Date and time handling.

### Planned Features

```flo
# Current time
now = time.now()

# Format time
formatted = time.format(now, "YYYY-MM-DD HH:mm:ss")

# Parse time
parsed = time.parse("2024-01-01", "YYYY-MM-DD")

# Time zones
utc = tz.utc()
local = tz.local()
```

## Logging Module

**Status**: Planned

Logging utilities.

### Planned Features

```flo
# Basic logging
log.info("Information message")
log.warn("Warning message")
log.error("Error message")
log.debug("Debug message")

# Custom logger
logger = log.create("myapp")
logger.info("Custom log message")
```

## Mail Module

**Status**: Planned

Email sending functionality.

### Planned Features

```flo
# Send email
mail.send({
    to: "recipient@example.com",
    from: "sender@example.com",
    subject: "Hello",
    body: "Email body"
})

# SMTP
smtp = smtp.connect("smtp.example.com", 587)
smtp.login("user", "password")
smtp.send(message)
```

## Crypto Module

**Status**: Planned

Cryptographic functions.

### Planned Features

```flo
# Hashing
md5 = crypto.md5("data")
sha256 = crypto.sha256("data")

# Encryption
encrypted = crypto.encrypt("data", "key")
decrypted = crypto.decrypt(encrypted, "key")

# Random
randomBytes = crypto.randomBytes(32)
uuid = crypto.uuid()
```

## Task/Scheduler Module

**Status**: Planned

Task scheduling and background jobs.

### Planned Features

```flo
# Schedule task
task.every("5 minutes", () => {
    print("Task running every 5 minutes")
})

# Cron-style scheduling
task.cron("0 0 * * *", () => {
    print("Daily task")
})

# Background worker
worker.run(longRunningTask)
```

## WebSocket Module

**Status**: Planned

WebSocket support for real-time communication.

### Planned Features

```flo
# WebSocket server
ws = websocket.server(8080)

ws.onConnect = (client) => {
    print("Client connected")
}

ws.onMessage = (client, message) => {
    print("Received:", message)
    client.send("Echo: " + message)
}
```

## Cache/Redis Module

**Status**: Planned

Caching and Redis support.

### Planned Features

```flo
# In-memory cache
cache.set("key", "value", 3600)  # TTL in seconds
value = cache.get("key")

# Redis
redis = redis.connect("localhost", 6379)
redis.set("key", "value")
value = redis.get("key")
```

## Template Module

**Status**: Planned

Template rendering for HTML and other formats.

### Planned Features

```flo
# Render template
html = template.render("index.html", {
    title: "Welcome",
    user: user
})

# String templates
text = template.string("Hello, {{name}}!", {name: "Alice"})
```

## Additional Modules (Planned)

- `xml` - XML parsing and generation
- `yaml` - YAML parsing and generation
- `csv` - CSV file handling
- `os` - Operating system interface
- `env` - Environment variables
- `cli` - Command-line argument parsing
- `session` - Session management
- `socket` - Low-level socket programming
- `html` - HTML parsing and generation

## Module Usage

Modules can be imported and used in your Flo programs:

```flo
# Using built-in functions (always available)
print("Hello")
len([1, 2, 3])

# Using modules (syntax may vary)
json.parse('{"key": "value"}')
http.get("https://api.example.com")
```

## Contributing

Help us build the standard library! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

**Note**: This documentation reflects the current state and planned features of the Flo standard library. Features marked as "Planned" are under development.
