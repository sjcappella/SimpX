# Will be used as the general class case
class ASTNode:
	# Class constructor
	def __init__(self, line_number, token_type, children):
		self.line_number = line_number
		self.token_type = token_type
		self.children = children

# Statement node in AST
class StatementNode(ASTNode):
	def __init__(self, line_number, token_type, children, statement_type):
		pass
