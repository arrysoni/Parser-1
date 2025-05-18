import ASTNodeDefs as AST

# TAs Lakshmi Sivani Devarapalli and Jaideep Kukkadapu have helped me debug and find my error in block() and statement() and also understand the flow of the program


class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
        self.tokens = []

    # Move to the next position in the code.
    def advance(self):
        # TODO: Students need to complete the logic to advance the position.
        self.position += 1
        # Making sure that the position does not go beyond the length of the code
        if (self.position) < len(self.code):
            # Selecting the char at the particular position
            self.current_char = self.code[self.position]
        else:
            self.current_char = None

    # Skip whitespaces.
    def skip_whitespace(self):
        # TODO: Complete logic to skip whitespaces.
        # Making sure that current_char exists, it can be a white space as well
        while self.current_char is not None and (self.current_char.isspace()):
            self.advance()

    # Tokenize an identifier.
    # IDENTIFIER ::= [a-zA-Z_][a-zA-Z0-9_]*
    def identifier(self):
        result = ''
        # TODO: Complete logic for handling identifiers.
        # Checking [a-zA-Z_]
        if (self.current_char >= 'a' and self.current_char <= 'z') or \
            (self.current_char >= 'A' and self.current_char <= 'Z') or \
                self.current_char == '_':
            result += self.current_char
            self.advance()

        # Checking the rest of the identifiers if they exist: [a-zA-Z0-9_]*
        while self.current_char is not None and (
            (self.current_char >= 'a' and self.current_char <= 'z') or
            (self.current_char >= 'A' and self.current_char <= 'Z') or
            (self.current_char >= '0' and self.current_char <= '9') or
            self.current_char == '_'
        ):
            result += self.current_char
            self.advance()

        return ('IDENTIFIER', result)

    # Tokenize a number.
    # NUMBER ::= [0-9]+
    def number(self):
        # TODO: Implement logic to tokenize numbers.
        result = ''
        while self.current_char is not None and (self.current_char >= '0' and self.current_char <= '9'):
            result += self.current_char
            self.advance()

        return ('NUMBER', int(result))

    def token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                ident = self.identifier()
                if ident[1] == 'if':
                    return ('IF', 'if')
                elif ident[1] == 'else':
                    return ('ELSE', 'else')
                elif ident[1] == 'while':
                    return ('WHILE', 'while')
                return ident
            if self.current_char.isdigit():
                return self.number()

            # TODO: Add logic for operators and punctuation tokens.
            # Handle operators and punctuation that were provided in the tokens.txt file
            if self.current_char == '+':
                self.advance()
                return ('PLUS', '+')
            elif self.current_char == '-':
                self.advance()
                return ('MINUS', '-')
            elif self.current_char == '*':
                self.advance()
                return ('MULTIPLY', '*')
            elif self.current_char == '/':
                self.advance()
                return ('DIVIDE', '/')

            # Special case: '==' cannot be included as a single character
            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ('EQ', '==')
                return ('EQUALS', '=')

            # # Special case: '!=' cannot be included as a single character
            elif self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ('NEQ', '!=')
                raise ValueError(
                    f"Unexpected character after '!': {self.current_char}")

            elif self.current_char == '<':
                self.advance()
                return ('LESS', '<')
            elif self.current_char == '>':
                self.advance()
                return ('GREATER', '>')
            elif self.current_char == '(':
                self.advance()
                return ('LPAREN', '(')
            elif self.current_char == ')':
                self.advance()
                return ('RPAREN', ')')
            elif self.current_char == ',':
                self.advance()
                return ('COMMA', ',')
            elif self.current_char == ':':
                self.advance()
                return ('COLON', ':')

            raise ValueError(
                f"Illegal character at position {self.position}: {self.current_char}")

        return ('EOF', None)

    # Collect all tokens into a list.
    def tokenize(self):
        # TODO: Implement the logic to collect tokens.
        # While tokens exist
        while True:
            token = self.token()
            self.tokens.append(token)
            # Stop at EOF
            if token[0] == 'EOF':
                break
        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens.pop(0)  # Start with the first token

    def advance(self):
        # Move to the next token in the list.
        # TODO: Ensure the parser doesn't run out of tokens.
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = ('EOF', None)

    def parse(self):
        """
        Entry point for the parser. It will process the entire program.
        TODO: Implement logic to parse multiple statements and return the AST for the entire program.
        """
        # The parse method transforms the source code from its raw text form into a structured tree (AST): from lecture slides
        return self.program()

    def program(self):
        """
        Program consists of multiple statements.
        TODO: Loop through and collect statements until EOF is reached.
        """
        # Parse through multiple statemnents or expressios until it reaches EOF
        # program ::= statement*
        statements = []
        while self.current_token[0] != 'EOF':
            # TODO: Parse each statement and append it to the list.
            single_statement = self.statement()
            # Appending a single statement to the list of statements
            statements.append(single_statement)
            print('Single Statement:', single_statement)
            # TODO: Return an AST node that represents the program.
        return AST.Block(statements).statements

    def statement(self):
        """
        Determines which type of statement to parse.
        - If it's an identifier, it could be an assignment or function call.
        - If it's 'if', it parses an if-statement.
        - If it's 'while', it parses a while-statement.

        TODO: Dispatch to the correct parsing function based on the current token.
        """
        # statement ::= assign_stmt | if_stmt | while_stmt | expr_stmt | function_call
        # Stop processing if EOF is reached
        if self.current_token[0] == 'EOF':
            return None
        if self.current_token[0] == 'IDENTIFIER':
            if self.peek() == 'EQUALS':  # Assignment
                return self.assign_stmt()  # AST of assign_stmt
            elif self.peek() == 'LPAREN':  # Function call
                return self.function_call()  # AST of function call
            else:
                raise ValueError(
                    f"Unexpected token after identifier: {self.current_token}")
        elif self.current_token[0] == 'IF':
            return self.if_stmt()  # AST of if stmt
        elif self.current_token[0] == 'WHILE':
            return self.while_stmt()  # AST of while stmt
        # I got a ValueError after which i decided to include this under def statement
        elif self.current_token[0] == 'COLON':
            # Skip processing if a colon is encountered unexpectedly
            self.advance()
            return None

        else:
            # TODO: Handle additional statements if necessary.
            raise ValueError(f"Unexpected token: {self.current_token}")

    def assign_stmt(self):
        """
        Parses assignment statements.
        Example:
        x = 5 + 3
        TODO: Implement parsing for assignments, where an identifier is followed by '=' and an expression.
        """
        # assign_stmt ::= IDENTIFIER '=' expression
        identifier = self.current_token
        self.advance()
        # Assignment statements always have an '=' after the identifier
        self.expect('EQUALS')
        # The statement to be assigned to the identifier is defined as 'expression'
        expression = self.expression()
        return AST.Assignment(identifier, expression)

    def if_stmt(self):
        """
        Parses an if-statement, with an optional else block.
        Example:
        if condition:
            # statements
        else:
            # statements
        TODO: Implement the logic to parse the if condition and blocks of code.
        """
        # if_stmt ::= 'if' boolean_expression ':' block ('else' ':' block)?
        if self.current_token[0] != 'IF':
            raise ValueError(f"Expected 'IF', got {self.current_token}")
        self.advance()

        # The condition for 'if'
        condition = self.boolean_expression()

        # Grammar defines a colon after 'if' and 'else'
        if self.current_token[0] != 'COLON':
            raise ValueError(f"Expected ':', got {self.current_token}")
        self.advance()

        # Get 'if' block
        if_block = self.block()
        else_block = None

        # Similar implementation as the 'IF' above
        if self.current_token[0] == 'ELSE':
            self.advance()
            if self.current_token[0] != 'COLON':
                raise ValueError(f"Expected ':', got {self.current_token}")
            self.advance()
            # Get 'else' block
            else_block = self.block()

        return AST.IfStatement(condition, if_block, else_block)

    def while_stmt(self):
        """
        Parses a while-statement.
        Example:
        while condition:
            # statements
        TODO: Implement the logic to parse while loops with a condition and a block of statements.
        """
        # while_stmt ::= 'while' boolean_expression ':' block
        # Ensure the current token is 'WHILE'
        if self.current_token[0] != 'WHILE':
            raise ValueError(f"Expected 'WHILE', got {self.current_token}")
        self.advance()

        # The condition for 'while'
        condition = self.boolean_expression()

        # # Grammar defines a colon after 'while'
        if self.current_token[0] != 'COLON':
            raise ValueError(f"Expected ':', got {self.current_token}")
        self.advance()

        # Get block 'while'
        block = self.block()

        return AST.WhileStatement(condition, block)

    def block(self):
        """
        Parses a block of statements. A block is a collection of statements grouped by indentation.
        Example:
        if condition:
            # This is a block
            x = 5
            y = 10
        TODO: Implement logic to capture multiple statements as part of a block.
        """
        # block ::= statement*
        statements = []

        while self.current_token[0] not in ['EOF', 'ELSE']:
            # Stop parsing if EOF is reached while parsing
            if self.current_token[0] == 'EOF':
                break

            # Primarily, blocks are defined for 'if', 'else', 'while', 'function block'
            if self.current_token[0] == "IF":
                statements.append(self.if_stmt())
            elif self.current_token[0] == "WHILE":
                statements.append(self.while_stmt())
            else:
                statements.append(self.statement())

        # Return an AST Block with parsed statements or an empty Block if none were found
        return AST.Block(statements) if statements else AST.Block([])

    def expression(self):
        """
        Parses an expression. Handles operators like +, -, etc.
        Example:
        x + y - 5
        TODO: Implement logic to parse binary operations (e.g., addition, subtraction) with correct precedence.
        """
        # expression ::= term (( '+' | '-' ) term)*
        left = self.term()
        while self.current_token[0] in ['PLUS', 'MINUS']:
            # Store the operator token
            op = self.current_token
            print('op', op)
            self.advance()
            # Parse the right side of the operation
            right = self.term()
            print('right', right)
            # Parse the left side of the operation
            left = AST.BinaryOperation(left, op, right)
            print('left', left)

        return left

    def boolean_expression(self):
        """
        Parses a boolean expression. These are comparisons like ==, !=, <, >.
        Example:
        x == 5
        TODO: Implement parsing for boolean expressions.
        """
        # write your code here, for reference check expression function
        # boolean_expression ::= term (( '==' | '!=' | '>' | '<' ) term)*
        # Get the left expression
        left = self.expression()

        # Check if the current token is a comparison operator
        if self.current_token[0] in ['EQ', 'NEQ', 'LESS', 'GREATER']:
            op = self.current_token
            self.advance()
            # Get the right expression
            right = self.expression()
            return AST.BooleanExpression(left, op, right)

        # If no comparison operator is found, return just the left expression
        return left

    def term(self):
        """
        Parses a term. A term consists of factors combined by * or /.
        Example:
        x * y / z
        TODO: Implement the parsing for multiplication and division.
        """
        # term ::= factor (( '*' | '/' ) factor)*
        left = self.factor()

        # Handle * and / operators
        while self.current_token[0] in ['MULTIPLY', 'DIVIDE']:
            op = self.current_token
            self.advance()

            right = self.factor()
            # Create a BinaryOperation AST node
            left = AST.BinaryOperation(left, op, right)

        return left

    def factor(self):
        """
        Parses a factor. Factors are the basic building blocks of expressions.
        Example:
        - A number
        - An identifier (variable)
        - A parenthesized expression
        TODO: Handle these cases and create appropriate AST nodes.
        """

        # factor ::= NUMBER | IDENTIFIER | '(' expression ')'
        if self.current_token[0] == 'NUMBER':
            # Handle a numeric literal
            value = self.current_token
            self.advance()
            return value
        elif self.current_token[0] == 'IDENTIFIER':
            # Handle a variable/identifier
            name = self.current_token
            self.advance()
            return name

        elif self.current_token[0] == 'LPAREN':
            # Handle a parenthesized expression
            self.advance()
            expr = self.expression()
            if self.current_token[0] != 'RPAREN':
                raise ValueError(f"Expected ')', got {self.current_token}")
            self.advance()
            return expr
        else:
            raise ValueError(
                f"Unexpected token in factor: {self.current_token}")

    def function_call(self):
        """
        Parses a function call.
        Example:
        myFunction(arg1, arg2)
        TODO: Implement parsing for function calls with arguments.
        """
        # function_call ::= IDENTIFIER '(' arg_list? ')'
        func_name = self.current_token
        self.advance()

        # Ensure the next token is '('
        if self.current_token[0] != 'LPAREN':
            raise ValueError(f"Expected '(', got {self.current_token}")
        self.advance()

        # Parse the argument list
        args = self.arg_list()

        # Ensure the next token is ')'
        if self.current_token[0] != 'RPAREN':
            raise ValueError(f"Expected ')', got {self.current_token}")
        self.advance()

        return AST.FunctionCall(func_name, args)

    def arg_list(self):
        """
        Parses a list of arguments in a function call.
        Example:
        arg1, arg2, arg3
        TODO: Implement the logic to parse comma-separated arguments.
        """
        # arg_list ::= expression (',' expression)*
        args = []
        # If the next token is ')', the argument list is empty
        if self.current_token[0] == 'RPAREN':
            return args

        # Parse the first argument
        args.append(self.expression())

        # Parse additional arguments separated by commas
        while self.current_token[0] == 'COMMA':
            self.advance()
            args.append(self.expression())

        return args

    def expect(self, token_type):

        if self.current_token[0] == token_type:
            self.advance()  # Move to the next token
        else:
            raise ValueError(
                f"Expected {token_type} but got {self.current_token[0]}")

    def peek(self):
        if self.tokens:
            return self.tokens[0][0]
        else:
            return None
