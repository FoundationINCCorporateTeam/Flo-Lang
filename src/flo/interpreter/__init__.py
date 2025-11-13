"""
Interpreter for the Flo programming language
Executes the Abstract Syntax Tree
"""

import asyncio
from typing import Any, Dict, List, Optional
from ..parser import *


class FloValue:
    """Base class for Flo runtime values"""
    pass


class FloFunction(FloValue):
    def __init__(self, params: List[str], body: List[ASTNode], closure: Dict[str, Any], is_async: bool = False):
        self.params = params
        self.body = body
        self.closure = closure
        self.is_async = is_async


class FloNativeFunction(FloValue):
    def __init__(self, func, is_async: bool = False):
        self.func = func
        self.is_async = is_async


class ReturnValue(Exception):
    """Used to implement return statement control flow"""
    def __init__(self, value):
        self.value = value


class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.vars: Dict[str, Any] = {}
    
    def define(self, name: str, value: Any):
        self.vars[name] = value
    
    def get(self, name: str) -> Any:
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: Any):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            # In Flo, assignment creates new variable if not exists
            self.vars[name] = value


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.setup_builtins()
    
    def setup_builtins(self):
        """Setup built-in functions and values"""
        
        # Built-in functions
        def print_func(*args):
            print(*args)
            return None
        
        def len_func(obj):
            if isinstance(obj, (list, dict, str)):
                return len(obj)
            return 0
        
        def str_func(obj):
            return str(obj)
        
        def int_func(obj):
            return int(obj)
        
        def float_func(obj):
            return float(obj)
        
        def type_func(obj):
            return type(obj).__name__
        
        def range_func(*args):
            return list(range(*args))
        
        self.global_env.define('print', FloNativeFunction(print_func))
        self.global_env.define('len', FloNativeFunction(len_func))
        self.global_env.define('str', FloNativeFunction(str_func))
        self.global_env.define('int', FloNativeFunction(int_func))
        self.global_env.define('float', FloNativeFunction(float_func))
        self.global_env.define('type', FloNativeFunction(type_func))
        self.global_env.define('range', FloNativeFunction(range_func))
    
    def eval(self, node: ASTNode, env: Environment) -> Any:
        """Evaluate an AST node"""
        
        if isinstance(node, Program):
            result = None
            for stmt in node.statements:
                result = self.eval(stmt, env)
            return result
        
        elif isinstance(node, NumberLiteral):
            return node.value
        
        elif isinstance(node, StringLiteral):
            return node.value
        
        elif isinstance(node, BooleanLiteral):
            return node.value
        
        elif isinstance(node, NullLiteral):
            return None
        
        elif isinstance(node, Identifier):
            return env.get(node.name)
        
        elif isinstance(node, BinaryOp):
            left = self.eval(node.left, env)
            right = self.eval(node.right, env)
            
            if node.operator == '+':
                return left + right
            elif node.operator == '-':
                return left - right
            elif node.operator == '*':
                return left * right
            elif node.operator == '/':
                return left / right
            elif node.operator == '%':
                return left % right
            elif node.operator == '==':
                return left == right
            elif node.operator == '!=':
                return left != right
            elif node.operator == '<':
                return left < right
            elif node.operator == '>':
                return left > right
            elif node.operator == '<=':
                return left <= right
            elif node.operator == '>=':
                return left >= right
            elif node.operator == '&&':
                return left and right
            elif node.operator == '||':
                return left or right
            else:
                raise RuntimeError(f"Unknown operator: {node.operator}")
        
        elif isinstance(node, UnaryOp):
            operand = self.eval(node.operand, env)
            
            if node.operator == '-':
                return -operand
            elif node.operator == '!':
                return not operand
            else:
                raise RuntimeError(f"Unknown unary operator: {node.operator}")
        
        elif isinstance(node, Assignment):
            value = self.eval(node.value, env)
            env.set(node.target, value)
            return value
        
        elif isinstance(node, ListLiteral):
            return [self.eval(elem, env) for elem in node.elements]
        
        elif isinstance(node, DictLiteral):
            result = {}
            for key_node, value_node in node.pairs:
                key = self.eval(key_node, env)
                value = self.eval(value_node, env)
                result[key] = value
            return result
        
        elif isinstance(node, MemberAccess):
            obj = self.eval(node.object, env)
            
            # Handle dict-like access
            if isinstance(obj, dict) and node.member in obj:
                return obj[node.member]
            
            # Handle object attributes
            if hasattr(obj, node.member):
                return getattr(obj, node.member)
            
            return None
        
        elif isinstance(node, IndexAccess):
            obj = self.eval(node.object, env)
            index = self.eval(node.index, env)
            
            try:
                return obj[index]
            except (KeyError, IndexError, TypeError):
                return None
        
        elif isinstance(node, FunctionCall):
            func = self.eval(node.function, env)
            args = [self.eval(arg, env) for arg in node.arguments]
            
            if isinstance(func, FloNativeFunction):
                return func.func(*args)
            
            elif isinstance(func, FloFunction):
                # Create new environment for function execution
                func_env = Environment(Environment(self.global_env))
                func_env.parent = func.closure
                
                # Bind parameters
                for i, param in enumerate(func.params):
                    value = args[i] if i < len(args) else None
                    func_env.define(param, value)
                
                # Execute function body
                try:
                    result = None
                    for stmt in func.body:
                        result = self.eval(stmt, func_env)
                    return result
                except ReturnValue as ret:
                    return ret.value
            
            else:
                raise RuntimeError(f"Not a function: {func}")
        
        elif isinstance(node, FunctionDef):
            func = FloFunction(node.parameters, node.body, env, node.is_async)
            # If function has a name, store it in environment
            if node.name:
                env.define(node.name, func)
            return func
        
        elif isinstance(node, IfStatement):
            condition = self.eval(node.condition, env)
            
            if condition:
                result = None
                for stmt in node.then_block:
                    result = self.eval(stmt, env)
                return result
            elif node.else_block:
                result = None
                for stmt in node.else_block:
                    result = self.eval(stmt, env)
                return result
            
            return None
        
        elif isinstance(node, WhileStatement):
            result = None
            while self.eval(node.condition, env):
                for stmt in node.body:
                    result = self.eval(stmt, env)
            return result
        
        elif isinstance(node, ForStatement):
            iterable = self.eval(node.iterable, env)
            result = None
            
            for item in iterable:
                env.define(node.variable, item)
                for stmt in node.body:
                    result = self.eval(stmt, env)
            
            return result
        
        elif isinstance(node, ReturnStatement):
            value = self.eval(node.value, env) if node.value else None
            raise ReturnValue(value)
        
        elif isinstance(node, TryStatement):
            try:
                result = None
                for stmt in node.try_block:
                    result = self.eval(stmt, env)
                return result
            except Exception as e:
                if node.catch_block:
                    catch_env = Environment(env)
                    if node.catch_variable:
                        catch_env.define(node.catch_variable, str(e))
                    
                    result = None
                    for stmt in node.catch_block:
                        result = self.eval(stmt, catch_env)
                    return result
                else:
                    raise
            finally:
                if node.finally_block:
                    for stmt in node.finally_block:
                        self.eval(stmt, env)
        
        elif isinstance(node, DecoratedFunction):
            # For now, just evaluate the function
            # Decorators would need more sophisticated handling
            return self.eval(node.function, env)
        
        elif isinstance(node, Decorator):
            # Decorators are metadata, return None for now
            return None
        
        elif isinstance(node, AwaitExpression):
            # Simplified await - would need proper async support
            expr = self.eval(node.expression, env)
            if asyncio.iscoroutine(expr):
                return asyncio.run(expr)
            return expr
        
        else:
            raise RuntimeError(f"Unknown AST node type: {type(node).__name__}")
    
    def run(self, program: Program) -> Any:
        """Run a Flo program"""
        return self.eval(program, self.global_env)
