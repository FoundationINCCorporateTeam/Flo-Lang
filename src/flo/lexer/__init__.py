"""
Lexer for the Flo programming language
Tokenizes Flo source code into a stream of tokens
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    FUNC = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    IMPORT = auto()
    EXPORT = auto()
    CLASS = auto()
    TRAIT = auto()
    MATCH = auto()
    OF = auto()
    ASYNC = auto()
    AWAIT = auto()
    TRY = auto()
    CATCH = auto()
    FINALLY = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    ARROW = auto()       # =>
    FAT_ARROW = auto()   # =>
    QUESTION = auto()    # ?
    COLON = auto()       # :
    DOT = auto()         # .
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    NEWLINE = auto()
    
    # Special
    AT = auto()          # @
    HASH = auto()        # #
    
    EOF = auto()
    UNKNOWN = auto()


@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"


class Lexer:
    KEYWORDS = {
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'func': TokenType.FUNC,
        'return': TokenType.RETURN,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'null': TokenType.NULL,
        'import': TokenType.IMPORT,
        'export': TokenType.EXPORT,
        'class': TokenType.CLASS,
        'trait': TokenType.TRAIT,
        'match': TokenType.MATCH,
        'of': TokenType.OF,
        'async': TokenType.ASYNC,
        'await': TokenType.AWAIT,
        'try': TokenType.TRY,
        'catch': TokenType.CATCH,
        'finally': TokenType.FINALLY,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, msg: str):
        raise SyntaxError(f"Lexer error at {self.line}:{self.column}: {msg}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        char = self.source[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.peek() == '#':
            while self.peek() and self.peek() != '\n':
                self.advance()
    
    def read_string(self, quote: str) -> str:
        value = ""
        self.advance()  # Skip opening quote
        
        while True:
            char = self.peek()
            if char is None:
                self.error("Unterminated string")
            if char == quote:
                self.advance()
                break
            if char == '\\':
                self.advance()
                next_char = self.peek()
                if next_char == 'n':
                    value += '\n'
                elif next_char == 't':
                    value += '\t'
                elif next_char == 'r':
                    value += '\r'
                elif next_char == '\\':
                    value += '\\'
                elif next_char == quote:
                    value += quote
                else:
                    value += next_char if next_char else ''
                self.advance()
            else:
                value += char
                self.advance()
        
        return value
    
    def read_number(self) -> float:
        value = ""
        has_dot = False
        
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            if self.peek() == '.':
                if has_dot:
                    break
                has_dot = True
            value += self.peek()
            self.advance()
        
        return float(value) if has_dot else int(value)
    
    def read_identifier(self) -> str:
        value = ""
        
        while self.peek() and (self.peek().isalnum() or self.peek() in '_'):
            value += self.peek()
            self.advance()
        
        return value
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.peek() is None:
                break
            
            # Comments
            if self.peek() == '#':
                self.skip_comment()
                continue
            
            line = self.line
            column = self.column
            char = self.peek()
            
            # Newlines (significant in Flo)
            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', line, column))
                self.advance()
                continue
            
            # Strings
            if char in '"\'':
                value = self.read_string(char)
                self.tokens.append(Token(TokenType.STRING, value, line, column))
                continue
            
            # Numbers
            if char.isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, line, column))
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                value = self.read_identifier()
                token_type = self.KEYWORDS.get(value, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, value, line, column))
                continue
            
            # Two-character operators
            if char == '=' and self.peek(1) == '>':
                self.tokens.append(Token(TokenType.ARROW, '=>', line, column))
                self.advance()
                self.advance()
                continue
            
            if char == '=' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.EQUAL, '==', line, column))
                self.advance()
                self.advance()
                continue
            
            if char == '!' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', line, column))
                self.advance()
                self.advance()
                continue
            
            if char == '<' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', line, column))
                self.advance()
                self.advance()
                continue
            
            if char == '>' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', line, column))
                self.advance()
                self.advance()
                continue
            
            if char == '&' and self.peek(1) == '&':
                self.tokens.append(Token(TokenType.AND, '&&', line, column))
                self.advance()
                self.advance()
                continue
            
            if char == '|' and self.peek(1) == '|':
                self.tokens.append(Token(TokenType.OR, '||', line, column))
                self.advance()
                self.advance()
                continue
            
            # Single-character operators and delimiters
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '=': TokenType.ASSIGN,
                '<': TokenType.LESS_THAN,
                '>': TokenType.GREATER_THAN,
                '!': TokenType.NOT,
                '?': TokenType.QUESTION,
                ':': TokenType.COLON,
                '.': TokenType.DOT,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                ';': TokenType.SEMICOLON,
                '@': TokenType.AT,
            }
            
            if char in single_char_tokens:
                self.tokens.append(Token(single_char_tokens[char], char, line, column))
                self.advance()
                continue
            
            # Unknown character
            self.error(f"Unexpected character: {char}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
