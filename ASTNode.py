import sys

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

	def prettyPrint(self, indent, last):
		sys.stdout.write(indent)
		
		if last == True:
			sys.stdout.write("\\--> ")
			indent += "  "
		else:
			sys.stdout.write("|--> ",)
			indent += "| "

		sys.stdout.write(self.token_type)
		sys.stdout.write("\n")
		for x in range(len(self.children)):
			self.children[x].prettyPrint(indent, x == (len(self.children)-1))


# Generic tokens
class ASTGeneric(ASTNode):
	def __init__(self, line_number, token_type):
		self.line_number = line_number
		self.token_type = token_type
		self.children = []

# Statement node in AST
class StatementNode(ASTNode):
	def __init__(self, line_number, token_type, statement_type, children):
		self.line_number = line_number
		self.token_type = token_type
		self.statement_type = statement_type
		self.children = children
		pass

	

# Expression node in AST
class ExpressionNode(ASTNode):
	def __init__(self, line_number, token_type, children):
		self.line_number = line_number
		self.token_type = token_type
		self.children = children
		pass

# Term node in AST
class Term(ASTNode):
	pass



# Factor class in AST (this on may need a little work)
# Should consider adding a factor type to distinguish between
# factors of the same length
class FactorNode(ASTNode):
	
	# Constructor factors
	def __init__(self, line_number, token_type, value, children):
		self.line_number = line_number
		self.token_type = token_type
		self.value = value
		self.children = children

	def prettyPrint(self, indent, last):
		sys.stdout.write(indent)
		
		if last == True:
			sys.stdout.write("\\--> ")
			indent += "  "
		else:
			sys.stdout.write("|--> ",)
			indent += "| "

		if self.children == None:
			sys.stdout.write(str(self.value))
		else:
			sys.stdout.write("FACTOR")
					
		sys.stdout.write("\n")
		if self.children != None:
			for x in range(len(self.children)):
				self.children[x].prettyPrint(indent, x == (len(self.children)-1))



# Boolean expression class in AST
class BooleanExpression(ASTNode):
	def __init__(self, line_number, token_type, children):
		self.line_number = line_number
		self.token_type = token_type
		self.children = children

# Addop node in AST
class AddopNode(ASTNode):
	def __init__(self, line_number, symbol):
		self.line_number = line_number
		self.token_type = "ADDOP_NODE"
		self.symbol = symbol
		self.children = []

	def printNode(self):
		print("Line Number: %d") % (self.line_number)
		print("Token Type:  %s") % (self.token_type)
		print("Symbol:      %s") % (self.symbol)

	def prettyPrint(self, indent, last):
		sys.stdout.write(indent)
		
		if last == True:
			sys.stdout.write("\\--> ")
			indent += "  "
		else:
			sys.stdout.write("|--> ",)
			indent += "| "

		sys.stdout.write(self.symbol)
		sys.stdout.write("\n")


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

	def prettyPrint(self, indent, last):
		sys.stdout.write(indent)
		
		if last == True:
			sys.stdout.write("\\--> ")
			indent += "  "
		else:
			sys.stdout.write("|--> ",)
			indent += "| "

		sys.stdout.write(self.symbol)
		sys.stdout.write("\n")

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

	def prettyPrint(self, indent, last):
		sys.stdout.write(indent)
		
		if last == True:
			sys.stdout.write("\\--> ")
			indent += "  "
		else:
			sys.stdout.write("|--> ",)
			indent += "| "

		sys.stdout.write(self.symbol)
		sys.stdout.write("\n")

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

	def prettyPrint(self, indent, last):
		sys.stdout.write(indent)
		
		if last == True:
			sys.stdout.write("\\--> ")
			indent += "  "
		else:
			sys.stdout.write("|--> ",)
			indent += "| "

		sys.stdout.write(self.symbol)
		sys.stdout.write("\n")
		

