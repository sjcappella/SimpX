import lex

# List of token names.   This is always required
tokens = (
   '32_BIT_USIGN_INT',
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
def t_VAR(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value,'VAR')    # Check for reserved words
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



def lexerDemo():
  # Build the lexer
  lexer = lex.lex()

  # Test it out
  data = '''
  3 + 4 * 10
    + -20 *2 >= <= ++ -- != :=

    + | || & && % ==
    > <

    4294967299
    -89 @$

    load store get_input then goto else goto
  '''

  # Give the lexer some input
  lexer.input(data)
  # Tokenize
  while True:
     tok = lexer.token()
     if not tok: break      # No more input
     print tok

def lexInput(data):
  # Build the lexer
  lexer = lex.lex()

  # give the lexer the data input
  lexer.input(data)
  while True:
     tok = lexer.token()
     if not tok: break      # No more input
     print tok