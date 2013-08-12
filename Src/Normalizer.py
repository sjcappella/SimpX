#class Normalizer:
	# Constructor function
#	def __init__(self, ASTList):
#	self.ASTList = ASTList
#	normalize()

t_count = 0

# Main function to call to normalize the  code
def normalize(ASTList):
	for x in range(len(ASTList)):
		convertToIR(ASTList[x], x+1) 

# Conver an AST to IR
def convertToIR(AST, block_ID):
	print("BB_%d:") % (block_ID)
	convertToIRRec(AST)
	
# Recursive function to convert to IR
def convertToIRRec(ASTNode):
	if ASTNode.token_type == "STATEMENT":
		print(ASTNode.statement_type)
		if len(ASTNode.children) == 2:
			print("2")

# Function to handle statement nodes
def statementNodes(ASTNode):
	if ASTNode.statement_type == "ASSIGN_NEW":
		pass
	if ASTNode.statement_type == "VAR_ID":
		pass
	if ASTNode.statement_type == "ASSIGN":
		pass
	if ASTNode.statement_type == "STORE":
		pass
	if ASTNode.statement_type == "GOTO":
		pass
	if ASTNode.statement_type == "ASSERT":
		pass
	if ASTNode.statement_type == "BOOLEAN":
		pass
	if ASTNode.statement_type == "PRINT_OUTPUT":
		pass
	pass

