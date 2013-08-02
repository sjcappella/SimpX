import yacc as yacc


# Production rule for program
def p_program(p):
	'''program	: statement_list'''

# Production rules for statement lists
def p_statement_list(p):
	'''statement_list	: statement_list statement
						| statement'''

# Production rules for statements
def p_statement(p):
	'''statement	: VAR ASSIGN expression
					| STORE LPAREN expression COMMA expression RPAREN
					| GOTO expression
					| ASSERT expression
					| IF expression THEN GOTO expression ELSE GOTO expression
					|'''

# Production rules for expressions
def p_expression(p):
	'''expression	: LOAD LPAREN expression RPAREN
					| expression binary_op expression
					| unary_op expression
					| GET_INPUT LPAREN RPAREN
					| PRINT_OUTPUT LPAREN expression RPAREN
					| value'''

# Production rules for binary operators
def p_binary_op(p):
	'''binary_op 	: PLUS
					| MINUS
					| MULTIPLY
					| DIVIDE
					| MODULO
					| XOR
					| INCLUSIVE_OR
					| LOGICAL_AND
					| LOGICAL_OR
					| LESS_THAN
					| GREATER_THAN
					| LESS_THAN_EQ
					| GREATER_THAN_EQ
					| INEQUALITY
					| EQUALITY'''

# Production rules for unary operators
def p_unary_op(p):
	'''unary_op 	: PLUS 
					| MINUS 
					| INCREMENT 
					| DECREMENT 
					| ADDRESS'''


# Production rules for 32 bit usigned integers and variables
def p_value(p):
	'''value 	: 32_BIT_USIGN_INT
				| VAR'''

def parse(tokens):
	parser = yacc.yacc()
	p = parser.parse(tokens, tracking=True)

	print(p)