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
	'''statement	: VAR ID
					| VAR ID ASSIGN expressions
             		| STORE LPAREN expressions COMMA expressions RPAREN
             		| GOTO expressions 
             		| ASSERT bool_statement
             		| IF bool_expression THEN GOTO expressions ELSE GOTO expressions
             		| PRINT_OUTPUT LPAREN expressions RPAREN'''

# Production rules for expressions
def p_expressions(p):
	'''expressions 	: LOAD LPAREN expressions RPAREN 
              		| expressions binary_op expression
              		| unary_op expressions  
              		| expression'''

# Production rules for an expression
def p_expression(p):
	'''expression	: ID
              		| 32_BIT_USIGN_INT 
              		| GET_INPUT LPAREN RPAREN'''

# Production rules for boolean expressions
def p_bool_expression(p):
	'''bool_expression 	: LPAREN bool_expression bool_op bool_statement RPAREN
                   		| LPAREN bool_statement bool_op bool_statement RPAREN'''

# Production rules for boolean statements
def p_bool_statement(p):
	'''bool_statement 	: expressions
                  		| TRUE
                  		| FALSE'''

# Production rules for binary operators
def p_binary_op(p):
	'''binary_op 	: PLUS
					| MINUS
					| MULTIPLY
					| DIVIDE
					| MODULO
					| XOR'''

# Production rules for boolean operators
def p_bool_op(p): 
	'''bool_op 		: INCLUSIVE_OR
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
	p = parser.parse(tracking=True)

	print(p)