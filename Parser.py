import yacc as yacc

def parse(tokens):
	parser = yacc.yacc()
	parser.parse(tokens, tracking=True)