"""
Test suite for Flo Programming Language
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flo.lexer import Lexer, TokenType
from flo.parser import Parser, NumberLiteral, StringLiteral, BinaryOp, Assignment
from flo.interpreter import Interpreter


class TestLexer(unittest.TestCase):
    """Test the lexer"""
    
    def test_numbers(self):
        lexer = Lexer("42 3.14")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, 42)
        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].value, 3.14)
    
    def test_strings(self):
        lexer = Lexer('"hello" \'world\'')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "hello")
        self.assertEqual(tokens[1].type, TokenType.STRING)
        self.assertEqual(tokens[1].value, "world")
    
    def test_identifiers(self):
        lexer = Lexer("x foo_bar")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].value, "foo_bar")
    
    def test_keywords(self):
        lexer = Lexer("if else while for func return")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.IF)
        self.assertEqual(tokens[1].type, TokenType.ELSE)
        self.assertEqual(tokens[2].type, TokenType.WHILE)
        self.assertEqual(tokens[3].type, TokenType.FOR)
        self.assertEqual(tokens[4].type, TokenType.FUNC)
        self.assertEqual(tokens[5].type, TokenType.RETURN)
    
    def test_operators(self):
        lexer = Lexer("+ - * / = == != => < >")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.PLUS)
        self.assertEqual(tokens[1].type, TokenType.MINUS)
        self.assertEqual(tokens[2].type, TokenType.MULTIPLY)
        self.assertEqual(tokens[3].type, TokenType.DIVIDE)
        self.assertEqual(tokens[4].type, TokenType.ASSIGN)
        self.assertEqual(tokens[5].type, TokenType.EQUAL)
        self.assertEqual(tokens[6].type, TokenType.NOT_EQUAL)
        self.assertEqual(tokens[7].type, TokenType.ARROW)
        self.assertEqual(tokens[8].type, TokenType.LESS_THAN)
        self.assertEqual(tokens[9].type, TokenType.GREATER_THAN)
    
    def test_comments(self):
        lexer = Lexer("x = 10 # this is a comment\ny = 20")
        tokens = lexer.tokenize()
        # Comments should be skipped
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.ASSIGN)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].type, TokenType.NEWLINE)
        self.assertEqual(tokens[4].type, TokenType.IDENTIFIER)


class TestParser(unittest.TestCase):
    """Test the parser"""
    
    def test_number_literal(self):
        tokens = Lexer("42").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        self.assertIsInstance(ast.statements[0], NumberLiteral)
        self.assertEqual(ast.statements[0].value, 42)
    
    def test_string_literal(self):
        tokens = Lexer('"hello"').tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        self.assertIsInstance(ast.statements[0], StringLiteral)
        self.assertEqual(ast.statements[0].value, "hello")
    
    def test_binary_operation(self):
        tokens = Lexer("10 + 5").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        self.assertIsInstance(ast.statements[0], BinaryOp)
        self.assertEqual(ast.statements[0].operator, "+")
    
    def test_assignment(self):
        tokens = Lexer("x = 42").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 1)
        self.assertIsInstance(ast.statements[0], Assignment)
        self.assertEqual(ast.statements[0].target, "x")


class TestInterpreter(unittest.TestCase):
    """Test the interpreter"""
    
    def run_code(self, code):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        return interpreter.run(ast)
    
    def test_arithmetic(self):
        self.assertEqual(self.run_code("10 + 5"), 15)
        self.assertEqual(self.run_code("10 - 5"), 5)
        self.assertEqual(self.run_code("10 * 5"), 50)
        self.assertEqual(self.run_code("10 / 5"), 2)
    
    def test_variables(self):
        code = """
x = 10
y = 20
x + y
"""
        self.assertEqual(self.run_code(code), 30)
    
    def test_functions(self):
        code = """
func add(a, b) => a + b
add(5, 3)
"""
        self.assertEqual(self.run_code(code), 8)
    
    def test_if_statement(self):
        code = """
x = 10
if x > 5 => 1
else => 0
"""
        # This won't return the if result directly, but we can test it works
        self.run_code(code)
    
    def test_lists(self):
        code = """
numbers = [1, 2, 3]
numbers[0]
"""
        self.assertEqual(self.run_code(code), 1)
    
    def test_dictionaries(self):
        code = """
person = {name: "Alice", age: 30}
person["name"]
"""
        self.assertEqual(self.run_code(code), "Alice")
    
    def test_while_loop(self):
        code = """
sum = 0
i = 1
while i <= 5 {
    sum = sum + i
    i = i + 1
}
sum
"""
        self.assertEqual(self.run_code(code), 15)
    
    def test_for_loop(self):
        code = """
sum = 0
for i range(1, 6) {
    sum = sum + i
}
sum
"""
        self.assertEqual(self.run_code(code), 15)


class TestBuiltins(unittest.TestCase):
    """Test built-in functions"""
    
    def run_code(self, code):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        return interpreter.run(ast)
    
    def test_len(self):
        self.assertEqual(self.run_code('len([1, 2, 3])'), 3)
        self.assertEqual(self.run_code('len("hello")'), 5)
    
    def test_str(self):
        self.assertEqual(self.run_code('str(42)'), "42")
    
    def test_int(self):
        self.assertEqual(self.run_code('int(3.14)'), 3)
    
    def test_range(self):
        result = self.run_code('range(1, 5)')
        self.assertEqual(result, [1, 2, 3, 4])


if __name__ == '__main__':
    unittest.main()
