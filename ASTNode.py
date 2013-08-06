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

# Expression node in AST
class ExpressionNode(ASTNode):
	def __init__(self, line_number, token_type, children):
		pass

# Addop node in AST
class AddopNode(ASTNode):
	def __init__(self, line_number, symbol):
		this.line_number = line_number
		this.symbol = symbol

# Term node in AST
class Term(ASTNode):
	pass

# Mulop node in AST
class MulopNode(ASTNode):
	def __init__(self, line_number, symbol):
		this.line_number = line_number
		this.symbol = symbol

# Factor class in AST (this on may need a little work)
class FactorNode(ASTNode):
	pass

# Boolean expression class in AST
class BooleanExpression(ASTNode):
	pass

# Relationship Operator class in AST
class RelopNode(ASTNode):
	def __init__(self, line_number, symbol):
		this.line_number = line_number
		this.symbol = symbol

# Unary Operator class in AST
class UnaryNode(ASTNode):
	def __init__(self, line_number, symbol):
		this.line_number = line_number
		this.symbol = symbol
