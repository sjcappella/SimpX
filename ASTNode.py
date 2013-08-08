# Terminology has gotten mixed up between token_type and statement_type.
# The correct use is token_type in the ASTNode class and statement type
# should only be used in Statmenet nodes. Need to fix this.




# Will be used as the general class case
class ASTNode:
	# Class constructor
	def __init__(self, line_number, token_type, children):
		self.line_number = line_number
		self.token_type = token_type
		self.children = children

	def printNode():
		print("Line Number: %d") % (self.line_number)
		print("Token Type: %s") % (self.token_type)

	def prettyPrint(indent, last):
		print("PRETTY PRINT WAS CALLED!")
		print(indent)
		
		if last == True:
			print("\\--> ")
		else:
			print("|--> ")
			indent += "  "

		print(statement_type)
		for x in range(len(children)):
			children[x].prettyPrint(indent, x == 0)


# Statement node in AST
class StatementNode(ASTNode):
	def __init__(self, line_number, token_type, statement_type, children):
		pass

	

# Expression node in AST
class ExpressionNode(ASTNode):
	def __init__(self, line_number, token_type, children):
		this.line_number = line_number
		this.token_type = token_type
		this.children = children
		pass

# Addop node in AST
class AddopNode(ASTNode):
	def __init__(self, line_number, symbol):
		self.line_number = line_number
		self.symbol = symbol

# Term node in AST
class Term(ASTNode):
	pass



# Factor class in AST (this on may need a little work)
# Should consider adding a factor type to distinguish between
# factors of the same length
class FactorNode(ASTNode):
	# Constructure for 32_BIT_USIGN_INT
	def __init__(self, line_number, statement_type, value):
		self.line_number = line_number
		self.statement_type = statement_type
		this.value = value
		self.children = None 

	# Constructure for ID
	def __init__(self, line_number, statement_type, label):
		self.line_number = line_number
		self.statement_type = statement_type
		this.label = label
		self.children = None 



# Boolean expression class in AST
class BooleanExpression(ASTNode):
	def __init__(self, line_number, statement_type, children):
		self.line_number = line_number
		self.statement_type = statement_type
		self.children = children

# Addop node in AST
class AddopNode(ASTNode):
	def __init__(self, line_number, symbol):
		self.line_number = line_number
		self.token_type = "ADDOP_NODE"
		self.symbol = symbol

	def printNode(self):
		print("Line Number: %d") % (self.line_number)
		print("Token Type:  %s") % (self.token_type)
		print("Symbol:      %s") % (self.symbol)


# Mulop node in AST
class MulopNode(ASTNode):
	def __init__(self, line_number, symbol):
		self.line_number = line_number
		self.token_type = "MULOP_NODE"
		self.symbol = symbol

	def printNode(self):
		print("Line Number: %d") % (self.line_number)
		print("Token Type:  %s") % (self.token_type)
		print("Symbol:      %s") % (self.symbol)

# Relationship Operator class in AST
class RelopNode(ASTNode):
	def __init__(self, line_number, symbol):
		self.line_number = line_number
		self.token_type = "RELOP_NODE"
		self.symbol = symbol

	def printNode(self):
		print("Line Number: %d") % (self.line_number)
		print("Token Type:  %s") % (self.token_type)
		print("Symbol:      %s") % (self.symbol)


# Unary Operator class in AST
class UnaryNode(ASTNode):
	def __init__(self, line_number, symbol):
		self.line_number = line_number
		self.token_type = "UNARY_NODE"
		self.symbol = symbol

	def printNode(self):
		print("Line Number: %d") % (self.line_number)
		print("Token Type:  %s") % (self.token_type)
		print("Symbol:      %s") % (self.symbol)

