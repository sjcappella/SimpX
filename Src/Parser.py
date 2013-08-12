###########################################################
# This section defines tokens used by the lexer. Both the #
# lexer and parser should be in 1 file based on the way   #
# the libraries have been created.                        #
###########################################################
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
   'GREATER_THAN',    # >
   'LESS_THAN',       # <
   'GREATER_THAN_EQ', # >=
   'LESS_THAN_EQ',    # <=
   'XOR',             # ^
   'INCLUSIVE_OR'    # |
)

# List of reserved words
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
  'print_output' : 'PRINT_OUTPUT'
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
t_GREATER_THAN      = r'\>'
t_LESS_THAN         = r'\<'
t_GREATER_THAN_EQ   = r'\>='
t_LESS_THAN_EQ      = r'\<='
t_XOR               = r'\^'
t_INCLUSIVE_OR      = r'\|'

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


###########################################################
# This ends the lexer section and begins the grammar and  #
# inlined production rules of the grammar.                #
###########################################################


import yacc as yacc
import ASTNode 

line_number = -1
AST = None

# Production rule for program
def p_start(p):
	'''start	: statement_list'''
	p[0] = p[1]
	global AST
	AST = p[0]

# Production rules for statement lists
def p_statement_list(p):
	'''statement_list	: statement_list statement
						| statement
						|'''
	if len(p) == 2:
		p[0] = p[1]
	if len(p) == 3:
		p[0] = (p[1], p[2])

# Production rules for statements (may need to add a special rule for ID to keep track of it)
def p_statement(p):
	'''statement	: VAR id
					| VAR id ASSIGN expression
					| id ASSIGN expression
             		| STORE LPAREN expression COMMA expression RPAREN
             		| GOTO expression 
             		| ASSERT bool_expression
             		| IF LPAREN bool_expression RPAREN THEN GOTO expression ELSE GOTO expression
             		| PRINT_OUTPUT LPAREN expression RPAREN'''
	
    # Production rules of length 2
	if len(p) == 3:
		# VAR ID
		if p[1] == 'var':
			p[1] = ASTNode.ASTGeneric(line_number, "var")
			p[0] = ASTNode.StatementNode(line_number, "STATEMENT", "VAR_ID", (p[1], p[2]))
		# GOTO expression
		if p[1] == 'goto':
			p[1] = ASTNode.ASTGeneric(line_number, "goto")
			p[0] = ASTNode.StatementNode(line_number, "STATEMENT", "GOTO", (p[1], p[2]))
		# ASSERT bool_expression
		if p[1] == 'assert':
			p[1] = ASTNode.ASTGeneric(line_number, "assert")
			p[0] = ASTNode.StatementNode(line_number, "STATEMENT", "ASSERT", (p[1], p[2]))
		pass
	# Production rules of length 4
	if len(p) == 4:
		# id ASSIGN expression
		p[2] = ASTNode.ASTGeneric(line_number, ":=")
		p[0] = ASTNode.StatementNode(line_number, "STATEMENT", "ASSIGN", (p[1], p[2], p[3]))
		pass
	# Production rules of length 5
	if len(p) == 5:
		# VAR ID ASSIGN expression
		if p[1] == 'var':
			p[1] = ASTNode.ASTGeneric(line_number, "var")
			p[3] = ASTNode.ASTGeneric(line_number, ":=")
			p[0] = ASTNode.StatementNode(line_number, "STATEMENT", "ASSIGN_NEW", (p[1], p[2], p[3], p[4]))
		# PRINT_OUTPUT LPAREN expression RPAREN
		if p[1] == 'print_output':
			p[1] = ASTNode.ASTGeneric(line_number, "print_output")
			p[2] = ASTNode.ASTGeneric(line_number, "(")
			p[4] = ASTNode.ASTGeneric(line_number, ")")
			p[0] = ASTNode.StatementNode(line_number, "STATEMENT", "PRINT_OUTPUT", (p[1], p[2], p[3], p[4]))
		pass
	# Production rules of length 7
	if len(p) == 7:
		# STORE LPAREN expression COMMA expression RPAREN
		p[1] = ASTNode.ASTGeneric(line_number, "store")
		p[2] = ASTNode.ASTGeneric(line_number, "(")
		p[4] = ASTNode.ASTGeneric(line_number, ",")
		p[6] = ASTNode.ASTGeneric(line_number, ")")
		p[0] = ASTNode.StatementNode(line_number, "STATEMENT", "STORE", (p[1], p[2], p[3], p[4], p[5], p[6]))
		pass
	# Production rules of length 11
	if len(p) == 11:
		# IF LPAREN bool_expression RPAREN THEN GOTO expression ELSE GOTO expression
		p[1] = ASTNode.ASTGeneric(line_number, "if")
		p[2] = ASTNode.ASTGeneric(line_number, "(")
		p[4] = ASTNode.ASTGeneric(line_number, ")")
		p[5] = ASTNode.ASTGeneric(line_number, "then")
		p[6] = ASTNode.ASTGeneric(line_number, "goto")
		p[8] = ASTNode.ASTGeneric(line_number, "else")
		p[9] = ASTNode.ASTGeneric(line_number, "goto")
		p[0] = ASTNode.StatementNode(line_number, "STATEMENT", "BOOLEAN", (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]))
		pass

# Production rules for expressions
def p_expression(p):
	'''expression 	: expression add_op term
					| term'''
	# Production rules of length 2
	if len(p) == 2:
		# term
		p[0] = p[1]
		pass
	# Production rules of length 4
	if len(p) == 4:
		# expression add_op term
		p[0] = ASTNode.ExpressionNode(line_number, "EXPRESSION", (p[1], p[2], p[3]))
		pass
	

# Production rules for addition operations
def p_add_op(p):
	'''add_op 		: PLUS
					| MINUS'''
	if p[1] == '+':
		p[0] = ASTNode.AddopNode(line_number, '+')
	if p[1] == '-':
		p[0] = ASTNode.AddopNode(line_number, '-')
	

# Prodution rules for factor operations. We are giving the
# logical operations the same precedence as factors
def p_term(p):
	'''term 		: term mulop factor
					| factor'''
	# Production rules of length 2
	if len(p) == 2:
		# factor
		p[0] = p[1]
		pass
	# Production rules of length 4
	if len(p) == 4:
		# term mulop factor
		p[0] = ASTNode.TermNode(line_number, "TERM", (p[1], p[2], p[3]))
		pass

# Production rules for the factor operators
def p_mulop(p):
	'''mulop 		: MULTIPLY
					| DIVIDE
					| MODULO
					| XOR
					| INCLUSIVE_OR
					| ADDRESS'''
	if p[1] == '*':
		p[0] = ASTNode.MulopNode(line_number, '*')
	if p[1] == '/':
		p[0] = ASTNode.MulopNode(line_number, '/')
	if p[1] == '%':
		p[0] = ASTNode.MulopNode(line_number, '%')
	if p[1] == '^':
		p[0] = ASTNode.MulopNode(line_number, '^')
	if p[1] == '|':
		p[0] = ASTNode.MulopNode(line_number, '|')
	if p[1] == '&':
		p[0] = ASTNode.MulopNode(line_number, '&')

# Production rules for factors
def p_factor(p):
	'''factor 		: unary_op factor
					| LPAREN expression RPAREN
					| 32_BIT_USIGN_INT
					| ID
					| GET_INPUT LPAREN RPAREN
					| LOAD LPAREN expression RPAREN'''
	# Production rules of length 2
	if len(p) == 2:
		# 32_BIT_USIGN_INT
		if isinstance(p[1], (int, long)):
			p[0] = ASTNode.FactorNode(line_number, "FACTOR", p[1], None)
		# ID
		else:
			p[0] = ASTNode.FactorNode(line_number, "FACTOR", p[1], None)		
		pass
	# Production rules of length 3
	if len(p) == 3:
		# unary_op factor
		p[0] = ASTNode.FactorNode(line_number, "FACTOR", None, (p[1], p[2]))
		pass
	# Production rules of length 4
	if len(p) == 4:
		# LPAREN expression RPAREN
		if p[1] == '(':
			p[1] = ASTNode.ASTGeneric(line_number, "(")
			p[3] = ASTNode.ASTGeneric(line_number, ")")
			p[0] = ASTNode.FactorNode(line_number, "FACTOR", None, (p[1], p[2], p[3]))
		if p[1] == 'get_input':
			# GET_INPUT LPAREN RPAREN
			p[1] = ASTNode.ASTGeneric(line_number, "get_input")
			p[2] = ASTNode.ASTGeneric(line_number, "(")
			p[3] = ASTNode.ASTGeneric(line_number, ")")
			p[0] = ASTNode.FactorNode(line_number, "FACTOR", None, (p[1], p[2], p[3]))
		pass
	# Production rules of length 5
	if len(p) == 5:
		# LOAD LPAREN expression RPAREN
		p[1] = ASTNode.ASTGeneric(line_number, "load")
		p[2] = ASTNode.ASTGeneric(line_number, "(")
		p[4] = ASTNode.ASTGeneric(line_number, ")")
		p[0] = ASTNode.FactorNode(line_number, "FACTOR", None, (p[1], p[2], p[3], p[4]))
		pass

# Production rule for an ID so we can catch its information during production
def p_id(p):
	'''id 			: ID'''
	# Put into factor class
	p[0] = ASTNode.FactorNode(line_number, "FACTOR", p[1], None)
	
# Production rules for boolean expressions
def p_bool_expression(p):
	'''bool_expression 	: expression rel_op expression'''

	p[0] = ASTNode.BooleanExpression(line_number, "BOOLEAN_EXPRESSION", (p[1], p[2], p[3]))

# Production rules for relational operators
def p_rel_op(p): 
	'''rel_op 		: EQUALITY
					| INEQUALITY
					| LESS_THAN
					| GREATER_THAN
					| LESS_THAN_EQ
					| GREATER_THAN_EQ'''
	if p[1] == '==':
		p[0] = ASTNode.RelopNode(line_number, '==')
	if p[1] == "!=":
		p[0] = ASTNode.RelopNode(line_number, '!=')
	if p[1] == '<':
		p[0] = ASTNode.RelopNode(line_number, '<')
	if p[1] == '>':
		p[0] = ASTNode.RelopNode(line_number, '>')
	if p[1] == '<=':
		p[0] = ASTNode.RelopNode(line_number, '<=')
	if p[1] == '>=':
		p[0] = ASTNode.RelopNode(line_number, '>=')

# Production rules for unary operators
def p_unary_op(p):
	'''unary_op 	: PLUS 
					| MINUS 
					| INCREMENT 
					| DECREMENT 
					| ADDRESS'''
	if p[1] == '+':
		p[0] = ASTNode.UnaryNode(line_number, '+')
	if p[1] == '-':
		p[0] = ASTNode.UnaryNode(line_number, '-')
	if p[1] == '++':
		p[0] = ASTNode.UnaryNode(line_number, '++')
	if p[1] == '--':
		p[0] = ASTNode.UnaryNode(line_number, '--')
	if p[1] == '&':
		p[0] = ASTNode.UnaryNode(line_number, '&')

# Lex and parse the source code
def parse(source_code, line):
	global line_number 
	line_number = line

	# Build the lexer
  	lexer = lex.lex()

  	# Give the lexer the source code
  	lexer.input(source_code)
	while True:
		tok = lexer.token()
		if not tok: break      # No more input
		print tok

	# Build the parser
	parser = yacc.yacc()

	# Parse the source code
	# For testing the parser
	#p = parser.parse(source_code, debug=True, tracking=True)

	# Running the parser
	parser.parse(source_code)
	global AST
	# AST.prettyPrint("", True)

	return AST
	
