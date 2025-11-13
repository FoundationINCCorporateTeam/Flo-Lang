"""
Parser for the Flo programming language
Builds an Abstract Syntax Tree from tokens
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from ..lexer import Token, TokenType


# AST Node types
@dataclass
class ASTNode:
    pass


@dataclass
class NumberLiteral(ASTNode):
    value: float


@dataclass
class StringLiteral(ASTNode):
    value: str


@dataclass
class BooleanLiteral(ASTNode):
    value: bool


@dataclass
class NullLiteral(ASTNode):
    pass


@dataclass
class Identifier(ASTNode):
    name: str


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode


@dataclass
class Assignment(ASTNode):
    target: str
    value: ASTNode


@dataclass
class FunctionCall(ASTNode):
    function: ASTNode
    arguments: List[ASTNode]


@dataclass
class MemberAccess(ASTNode):
    object: ASTNode
    member: str


@dataclass
class IndexAccess(ASTNode):
    object: ASTNode
    index: ASTNode


@dataclass
class ListLiteral(ASTNode):
    elements: List[ASTNode]


@dataclass
class DictLiteral(ASTNode):
    pairs: List[tuple]  # [(key, value), ...]


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_block: List[ASTNode]
    else_block: Optional[List[ASTNode]] = None


@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: List[ASTNode]


@dataclass
class ForStatement(ASTNode):
    variable: str
    iterable: ASTNode
    body: List[ASTNode]


@dataclass
class FunctionDef(ASTNode):
    name: Optional[str]
    parameters: List[str]
    body: List[ASTNode]
    is_async: bool = False


@dataclass
class ReturnStatement(ASTNode):
    value: Optional[ASTNode] = None


@dataclass
class TryStatement(ASTNode):
    try_block: List[ASTNode]
    catch_variable: Optional[str]
    catch_block: Optional[List[ASTNode]]
    finally_block: Optional[List[ASTNode]]


@dataclass
class AwaitExpression(ASTNode):
    expression: ASTNode


@dataclass
class Decorator(ASTNode):
    name: str
    arguments: List[ASTNode]


@dataclass
class DecoratedFunction(ASTNode):
    decorators: List[Decorator]
    function: FunctionDef


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg: str):
        token = self.current()
        raise SyntaxError(f"Parser error at {token.line}:{token.column}: {msg}")
    
    def current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def peek(self, offset: int = 0) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def advance(self) -> Token:
        token = self.current()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current()
        if token.type != token_type:
            self.error(f"Expected {token_type.name}, got {token.type.name}")
        return self.advance()
    
    def skip_newlines(self):
        while self.current().type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self) -> Program:
        statements = []
        
        while self.current().type != TokenType.EOF:
            self.skip_newlines()
            if self.current().type == TokenType.EOF:
                break
            
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        self.skip_newlines()
        
        # Decorators
        if self.current().type == TokenType.AT:
            return self.parse_decorated()
        
        # Control flow
        if self.current().type == TokenType.IF:
            return self.parse_if()
        
        if self.current().type == TokenType.WHILE:
            return self.parse_while()
        
        if self.current().type == TokenType.FOR:
            return self.parse_for()
        
        if self.current().type == TokenType.FUNC:
            return self.parse_function()
        
        if self.current().type == TokenType.RETURN:
            return self.parse_return()
        
        if self.current().type == TokenType.TRY:
            return self.parse_try()
        
        # Expression statement (assignment or expression)
        expr = self.parse_expression()
        
        # Optional semicolon or newline
        if self.current().type in (TokenType.SEMICOLON, TokenType.NEWLINE):
            self.advance()
        
        return expr
    
    def parse_decorated(self) -> ASTNode:
        decorators = []
        
        while self.current().type == TokenType.AT:
            self.advance()
            name = self.expect(TokenType.IDENTIFIER).value
            args = []
            
            if self.current().type == TokenType.LPAREN:
                self.advance()
                while self.current().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    if self.current().type == TokenType.COMMA:
                        self.advance()
                self.expect(TokenType.RPAREN)
            
            decorators.append(Decorator(name, args))
            self.skip_newlines()
        
        # Parse the function being decorated
        if self.current().type == TokenType.FUNC:
            func = self.parse_function()
            return DecoratedFunction(decorators, func)
        
        # Or it might be a decorator on an assignment
        return decorators[0] if len(decorators) == 1 else decorators
    
    def parse_if(self) -> IfStatement:
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        
        # Arrow syntax: if condition => statement/expression
        if self.current().type == TokenType.ARROW:
            self.advance()
            # Allow return statements in arrow syntax
            if self.current().type == TokenType.RETURN:
                then_stmt = self.parse_return()
            else:
                then_stmt = self.parse_expression()
            then_block = [then_stmt]
            else_block = None
            
            self.skip_newlines()
            if self.current().type == TokenType.ELSE:
                self.advance()
                if self.current().type == TokenType.ARROW:
                    self.advance()
                    if self.current().type == TokenType.RETURN:
                        else_stmt = self.parse_return()
                    else:
                        else_stmt = self.parse_expression()
                    else_block = [else_stmt]
        else:
            # Block syntax
            then_block = self.parse_block()
            else_block = None
            
            self.skip_newlines()
            if self.current().type == TokenType.ELSE:
                self.advance()
                else_block = self.parse_block()
        
        return IfStatement(condition, then_block, else_block)
    
    def parse_while(self) -> WhileStatement:
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        body = self.parse_block()
        return WhileStatement(condition, body)
    
    def parse_for(self) -> ForStatement:
        self.expect(TokenType.FOR)
        variable = self.expect(TokenType.IDENTIFIER).value
        # "in" keyword would be nice but we'll use simple syntax
        iterable = self.parse_expression()
        body = self.parse_block()
        return ForStatement(variable, iterable, body)
    
    def parse_function(self) -> FunctionDef:
        is_async = False
        if self.current().type == TokenType.ASYNC:
            is_async = True
            self.advance()
        
        self.expect(TokenType.FUNC)
        
        # Function name (optional for lambdas)
        name = None
        if self.current().type == TokenType.IDENTIFIER:
            name = self.advance().value
        
        # Parameters
        parameters = []
        if self.current().type == TokenType.LPAREN:
            self.advance()
            while self.current().type != TokenType.RPAREN:
                param = self.expect(TokenType.IDENTIFIER).value
                parameters.append(param)
                if self.current().type == TokenType.COMMA:
                    self.advance()
            self.expect(TokenType.RPAREN)
        
        # Arrow function or block function
        if self.current().type == TokenType.ARROW:
            self.advance()
            expr = self.parse_expression()
            body = [ReturnStatement(expr)]
        else:
            body = self.parse_block()
        
        return FunctionDef(name, parameters, body, is_async)
    
    def parse_return(self) -> ReturnStatement:
        self.expect(TokenType.RETURN)
        
        # Check if there's a return value
        if self.current().type in (TokenType.NEWLINE, TokenType.SEMICOLON, TokenType.EOF):
            return ReturnStatement()
        
        value = self.parse_expression()
        return ReturnStatement(value)
    
    def parse_try(self) -> TryStatement:
        self.expect(TokenType.TRY)
        try_block = self.parse_block()
        
        catch_variable = None
        catch_block = None
        finally_block = None
        
        self.skip_newlines()
        if self.current().type == TokenType.CATCH:
            self.advance()
            if self.current().type == TokenType.IDENTIFIER:
                catch_variable = self.advance().value
            catch_block = self.parse_block()
        
        self.skip_newlines()
        if self.current().type == TokenType.FINALLY:
            self.advance()
            finally_block = self.parse_block()
        
        return TryStatement(try_block, catch_variable, catch_block, finally_block)
    
    def parse_block(self) -> List[ASTNode]:
        statements = []
        
        # Check for brace block
        if self.current().type == TokenType.LBRACE:
            self.advance()
            self.skip_newlines()
            
            while self.current().type != TokenType.RBRACE:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
                self.skip_newlines()
            
            self.expect(TokenType.RBRACE)
        else:
            # Single statement (Flo allows braces to be optional)
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return statements
    
    def parse_expression(self) -> ASTNode:
        return self.parse_assignment()
    
    def parse_assignment(self) -> ASTNode:
        expr = self.parse_ternary()
        
        if self.current().type == TokenType.ASSIGN:
            if isinstance(expr, Identifier):
                self.advance()
                value = self.parse_expression()
                return Assignment(expr.name, value)
            else:
                self.error("Invalid assignment target")
        
        return expr
    
    def parse_ternary(self) -> ASTNode:
        expr = self.parse_or()
        
        # Ternary with ? :
        if self.current().type == TokenType.QUESTION:
            self.advance()
            then_expr = self.parse_expression()
            self.expect(TokenType.COLON)
            else_expr = self.parse_expression()
            return IfStatement(expr, [then_expr], [else_expr])
        
        return expr
    
    def parse_or(self) -> ASTNode:
        left = self.parse_and()
        
        while self.current().type == TokenType.OR:
            op = self.advance().value
            right = self.parse_and()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_and(self) -> ASTNode:
        left = self.parse_equality()
        
        while self.current().type == TokenType.AND:
            op = self.advance().value
            right = self.parse_equality()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_equality(self) -> ASTNode:
        left = self.parse_comparison()
        
        while self.current().type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.advance().value
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_additive()
        
        while self.current().type in (TokenType.LESS_THAN, TokenType.GREATER_THAN,
                                       TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op = self.advance().value
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        
        while self.current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_unary()
        
        while self.current().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance().value
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        if self.current().type in (TokenType.NOT, TokenType.MINUS):
            op = self.advance().value
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        if self.current().type == TokenType.AWAIT:
            self.advance()
            expr = self.parse_unary()
            return AwaitExpression(expr)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        expr = self.parse_primary()
        
        while True:
            # Member access
            if self.current().type == TokenType.DOT:
                self.advance()
                member = self.expect(TokenType.IDENTIFIER).value
                expr = MemberAccess(expr, member)
            
            # Function call
            elif self.current().type == TokenType.LPAREN:
                self.advance()
                args = []
                while self.current().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    if self.current().type == TokenType.COMMA:
                        self.advance()
                self.expect(TokenType.RPAREN)
                expr = FunctionCall(expr, args)
            
            # Index access
            elif self.current().type == TokenType.LBRACKET:
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = IndexAccess(expr, index)
            
            else:
                break
        
        return expr
    
    def parse_primary(self) -> ASTNode:
        # Numbers
        if self.current().type == TokenType.NUMBER:
            value = self.advance().value
            return NumberLiteral(value)
        
        # Strings
        if self.current().type == TokenType.STRING:
            value = self.advance().value
            return StringLiteral(value)
        
        # Booleans
        if self.current().type == TokenType.TRUE:
            self.advance()
            return BooleanLiteral(True)
        
        if self.current().type == TokenType.FALSE:
            self.advance()
            return BooleanLiteral(False)
        
        # Null
        if self.current().type == TokenType.NULL:
            self.advance()
            return NullLiteral()
        
        # Identifiers
        if self.current().type == TokenType.IDENTIFIER:
            name = self.advance().value
            return Identifier(name)
        
        # Parenthesized expression
        if self.current().type == TokenType.LPAREN:
            self.advance()
            
            # Check for lambda with parameters
            if self.peek().type in (TokenType.IDENTIFIER, TokenType.RPAREN):
                params = []
                while self.current().type != TokenType.RPAREN:
                    param = self.expect(TokenType.IDENTIFIER).value
                    params.append(param)
                    if self.current().type == TokenType.COMMA:
                        self.advance()
                self.expect(TokenType.RPAREN)
                
                if self.current().type == TokenType.ARROW:
                    self.advance()
                    expr = self.parse_expression()
                    return FunctionDef(None, params, [ReturnStatement(expr)])
            
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        # List literal
        if self.current().type == TokenType.LBRACKET:
            self.advance()
            self.skip_newlines()
            elements = []
            while self.current().type != TokenType.RBRACKET:
                self.skip_newlines()
                elements.append(self.parse_expression())
                if self.current().type == TokenType.COMMA:
                    self.advance()
                self.skip_newlines()
            self.expect(TokenType.RBRACKET)
            return ListLiteral(elements)
        
        # Dict literal
        if self.current().type == TokenType.LBRACE:
            self.advance()
            self.skip_newlines()
            pairs = []
            while self.current().type != TokenType.RBRACE:
                self.skip_newlines()
                # Key can be identifier or string
                if self.current().type == TokenType.IDENTIFIER:
                    key = self.advance().value
                    key_node = StringLiteral(key)
                else:
                    key_node = self.parse_expression()
                
                self.expect(TokenType.COLON)
                value = self.parse_expression()
                pairs.append((key_node, value))
                
                if self.current().type == TokenType.COMMA:
                    self.advance()
                self.skip_newlines()
            self.expect(TokenType.RBRACE)
            return DictLiteral(pairs)
        
        # Arrow function without params
        if self.current().type == TokenType.ARROW:
            self.advance()
            expr = self.parse_expression()
            return FunctionDef(None, [], [ReturnStatement(expr)])
        
        self.error(f"Unexpected token: {self.current().type.name}")
