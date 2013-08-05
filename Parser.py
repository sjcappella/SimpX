import lex

# List of token names.   This is always required
tokens = (
   '32_BIT_USIGN_INT',
   'ID',
   'PLUS',            # + (also positive)
   'MINUS',           # - (also negate) 
   'MULTIPLY',        # *
   'DIVIDE',          # /
   'LPAREN',          # (
   'RPAREN',          # )
   'INCREMENT',       # ++
   'DECREMENT',       # --
   'ADDRESS',         # & (also bit wise AND)
   'MODULO',          # %
   'COMMA',           # ,
   'ASSIGN',          # :=
   'EQUALITY',        # ==
   'INEQUALITY',      # !=
   'LOGICAL_AND',     # &&
   'GREATER_THAN',    # >
   'LESS_THAN',       # <
   'GREATER_THAN_EQ', # >=
   'LESS_THAN_EQ',    # <=
   'XOR',             # ^
   'INCLUSIVE_OR',    # |
   'LOGICAL_OR'       # ||
)

reserved = {
  'var' : 'VAR',
  'store' : 'STORE',
  'load' : 'LOAD',
  'goto' : 'GOTO',
  'assert' : 'ASSERT',
  'if' : 'IF',
  'then' : 'THEN',
  'else' : 'ELSE',
  'get_input' : 'GET_INPUT',
  'print_output' : 'PRINT_OUTPUT',
  'true' : 'TRUE',
  'false' : 'FALSE'
}

# Regular expression rules for simple tokens
t_PLUS              = r'\+'
t_MINUS             = r'-'
t_MULTIPLY          = r'\*'
t_DIVIDE            = r'/'
t_LPAREN            = r'\('
t_RPAREN            = r'\)'
t_INCREMENT         = r'\+\+'
t_DECREMENT         = r'--'
t_ADDRESS           = r'&'
t_MODULO            = r'%'
t_COMMA             = r','
t_ASSIGN            = r':='
t_EQUALITY          = r'=='
t_INEQUALITY        = r'!='
t_LOGICAL_AND       = r'&&'
t_GREATER_THAN      = r'\>'
t_LESS_THAN         = r'\<'
t_GREATER_THAN_EQ   = r'\>='
t_LESS_THAN_EQ      = r'\<='
t_XOR               = r'\^'
t_INCLUSIVE_OR      = r'\|'
t_LOGICAL_OR        = r'\|\|'

tokens = list(tokens) + list(reserved.values())

# A regular expression rule with some action code
def t_32_BIT_USIGN_INT(t):
    r'\d+'
    # We are going to cheat for now and just mod max 32 bit value
    if int(t.value) > 4294967295:
      t.value = int(t.value) % 4294967295
    else:
      t.value = int(t.value)
    return t

# Define a regular expression for variables
def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value,'ID')    # Check for reserved words
  return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

############################################################################

import yacc as yacc


# Production rule for program
def p_start(p):
	'''start	: statement_list'''

# Production rules for statement lists
def p_statement_list(p):
	'''statement_list	: statement_list statement
						| statement
						|'''

# Production rules for statements
def p_statement(p):
	'''statement	: VAR ID
					| VAR ID ASSIGN expressions
					| ID ASSIGN expressions
             		| STORE LPAREN expressions COMMA expressions RPAREN
             		| GOTO expressions 
             		| ASSERT bool_statement
             		| IF bool_expression THEN GOTO expressions ELSE GOTO expressions
             		| PRINT_OUTPUT LPAREN expressions RPAREN'''
	print ("MESSAGE =====> Length of p = %d") % len(p)
	print "MESSAGE =====> Parsed a statement", p[1], p[2], p[3], p[4]
	for x in range(0, len(p)): 
		if p[x] == 'var':
			print ("MESSAGE =====> WE FOUND A VAR!!")

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
					| INCLUSIVE_OR
					| ADDRESS
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

def parse(data):
	
	parser = yacc.yacc()
	p = parser.parse(data, debug=True, tracking=True)

	print(p)