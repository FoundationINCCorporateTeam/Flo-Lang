#!/usr/bin/env python3
"""
Flo Programming Language CLI
Command-line interface for running and building Flo programs
"""

import sys
import os
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from flo.lexer import Lexer
from flo.parser import Parser
from flo.interpreter import Interpreter


def run_file(filepath: str):
    """Run a Flo file"""
    try:
        with open(filepath, 'r') as f:
            source = f.read()
        
        # Tokenize
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Parse
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Interpret
        interpreter = Interpreter()
        result = interpreter.run(ast)
        
        return result
    
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Runtime Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def build_file(filepath: str, output: str = None):
    """Build a Flo file (compile to bytecode)"""
    print("Build functionality coming soon!")
    print(f"Would compile: {filepath}")
    if output:
        print(f"Output to: {output}")


def repl():
    """Start Flo REPL (interactive mode)"""
    print("Flo Programming Language REPL")
    print("Version 0.1.0")
    print("Type 'exit' or press Ctrl+D to quit")
    print()
    
    interpreter = Interpreter()
    
    while True:
        try:
            line = input("flo> ")
            
            if line.strip() in ('exit', 'quit'):
                break
            
            if not line.strip():
                continue
            
            # Tokenize
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            
            # Parse
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Interpret
            result = interpreter.run(ast)
            
            if result is not None:
                print(result)
        
        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            continue
        except Exception as e:
            print(f"Error: {e}")


def show_help():
    """Show help information"""
    help_text = """
Flo Programming Language - CLI Tool

USAGE:
    flo <command> [options]

COMMANDS:
    run <file>              Run a Flo program
    build <file>            Build a Flo program (compile)
    repl                    Start interactive REPL
    help                    Show this help message
    version                 Show version information

EXAMPLES:
    flo run hello.flo       # Run hello.flo
    flo build app.flo       # Build app.flo
    flo repl                # Start REPL

For more information, visit: https://github.com/TechEdMN/Flo-Lang
"""
    print(help_text)


def show_version():
    """Show version information"""
    print("Flo Programming Language")
    print("Version 0.1.0")
    print("Copyright (c) 2025 Flo Language Team")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Flo Programming Language CLI',
        add_help=False
    )
    
    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('file', nargs='?', help='File to run or build')
    parser.add_argument('-o', '--output', help='Output file for build command')
    
    args = parser.parse_args()
    
    if not args.command:
        show_help()
        return
    
    command = args.command.lower()
    
    if command == 'run':
        if not args.file:
            print("Error: No file specified", file=sys.stderr)
            print("Usage: flo run <file>", file=sys.stderr)
            sys.exit(1)
        run_file(args.file)
    
    elif command == 'build':
        if not args.file:
            print("Error: No file specified", file=sys.stderr)
            print("Usage: flo build <file> [-o output]", file=sys.stderr)
            sys.exit(1)
        build_file(args.file, args.output)
    
    elif command == 'repl':
        repl()
    
    elif command in ('help', '--help', '-h'):
        show_help()
    
    elif command in ('version', '--version', '-v'):
        show_version()
    
    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        print("Run 'flo help' for usage information", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
