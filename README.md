# 🧠 Scoping Rules and Type Checking in a Custom Language Parser

## 📚 Project Overview

This project implements a **parser for a custom programming language** that enforces **scoping rules** and performs **type checking**, similar to modern languages like C or Python. It is designed to detect and report semantic errors such as type mismatches, undeclared variables, and scope violations.

---

## 🎯 Learning Objectives

- Implement lexical and syntactic analysis
- Design and manage a **symbol table** for scoping
- Enforce **type safety** between `int` and `float`
- Emit helpful **diagnostic error messages**
- Understand how parsers process and validate code structure

---

## ✅ Features Implemented

### 1. Type Compatibility Checking
- Validates that both sides of expressions or assignments are of the same type (`int` vs `float`)
- Example:
  ```c
  int a = 10.2; // ❌ Error: Type mismatch
  a = b; // ❌ Error: b is undeclared

  int a = 10;
  int a = 5; // ❌ Error: Redeclared
  if (a > 0) {
    float a = 3.5; // ✅ Allowed: new scope
  }

  {
  int x = 5;
  }
  x = 3; // ❌ Error: x out of scope

  Supported Grammar

  statement       ::= assign_stmt | if_stmt | while_stmt | expr_stmt | function_call | decl_stmt
  decl_stmt       ::= type IDENTIFIER '=' expression
  type            ::= 'int' | 'float'
  if_stmt         ::= 'if' boolean_expression '{' block '}' ('else' '{' block '}')?
  while_stmt      ::= 'while' boolean_expression '{' block '}'
  factor          ::= NUMBER | FNUMBER | IDENTIFIER | '(' expression ')'
  FNUMBER         ::= [0-9]+\.[0-9]+
  
