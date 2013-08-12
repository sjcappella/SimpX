#class Normalizer:
	# Constructor function
#	def __init__(self, ASTList):
#	self.ASTList = ASTList
#	normalize()

t_count = 0
temp_val = ""
code = ""


# Main function to call to normalize the  code
def normalize(ASTList):
	global code
	for x in range(len(ASTList)):
		convertToIR(ASTList[x], x+1) 
	print(code)

# Conver an AST to IR
def convertToIR(AST, block_ID):
	global code
	code += ("BB_%d:BEGIN\n") % (block_ID)
	convertToIRRec(AST)
	code += ("BB_%d:END\n") % (block_ID)
	
# Recursive function to convert to IR
def convertToIRRec(ASTNode):
	# Can remove this after testing
	global code
	if ASTNode.token_type == "STATEMENT":
		statementNodes(ASTNode)
	if ASTNode.token_type == "FACTOR":
		factorNodes(ASTNode)
	if ASTNode.token_type == "EXPRESSION":
		expressionNodes(ASTNode)
	if ASTNode.token_type == "TERM":
		termNodes(ASTNode)
	else:
		print(ASTNode.token_type)
		

# Function to handle statement nodes
def statementNodes(ASTNode):
	global code, temp_val, t_count
	if ASTNode.statement_type == "ASSIGN_NEW":
		# Make sure to add variable to symbol table 
		convertToIRRec(ASTNode.children[3])
		code += ("\tvar_" + ASTNode.children[1].value + " := " + temp_val + "\n") 
		pass
	if ASTNode.statement_type == "VAR_ID":
		code += ("\tvar_" + ASTNode.children[1].value + "\n")
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
	
# Function to handle factor nodes
def factorNodes(ASTNode):
	global code, temp_val, t_count
	if ASTNode.factor_type == "32_BIT_USIGN_INT":
		temp_val = str(ASTNode.value)
	if ASTNode.factor_type == "ID":
		temp_val = "var_" + str(ASTNode.value)
	if ASTNode.factor_type == "UNARY_FACTOR":
		convertToIRRec(ASTNode.children[1])
		symbol = ASTNode.children[0].symbol
		temp_val_1 = temp_val
		temp_val = "t_"+ str(t_count)
		if symbol == "-":
			code += "\t" + temp_val + " := -1 * " + temp_val_1 + "\n"
		else:
			code += "\t" + temp_val + " := 1 * " + temp_val_1 + "\n"
		t_count += 1 
	if ASTNode.factor_type == "PAREN_EXPRESSION":
		# Might need some logic here
		convertToIRRec(ASTNode.children[1])
	if ASTNode.factor_type == "GET_INPUT":
		temp_val = "t_" + str(t_count)
		code += "\t" + temp_val + " := get_input()\n" 
		t_count += 1
	if ASTNode.factor_type == "LOAD":
		convertToIRRec(ASTNode.children[2])
		temp_val_1 = temp_val
		temp_val = "t_" + str(t_count)
		code += "\t" + temp_val + " := load( " + temp_val_1 + " )\n"
		t_count += 1



# Function to handle expression nodes
def expressionNodes(ASTNode):
	global code, temp_val, t_count
	convertToIRRec(ASTNode.children[0])
	temp_val_1 = temp_val
	convertToIRRec(ASTNode.children[2])
	temp_val_2 = temp_val
	symbol = ASTNode.children[1].symbol
	temp_val = "t_" + str(t_count)
	code += "\t" + temp_val + " := " + temp_val_1 + " " + symbol + " " + temp_val_2 + "\n"
	t_count += 1



# Function to handle term nodes
def termNodes(ASTNode):
	global code, temp_val, t_count
	convertToIRRec(ASTNode.children[0])
	temp_val_1 = temp_val
	convertToIRRec(ASTNode.children[2])
	temp_val_2 = temp_val
	symbol = ASTNode.children[1].symbol
	temp_val = "t_" + str(t_count)
	code += "\t" + temp_val + " := " + temp_val_1 + " " + symbol + " " + temp_val_2 + "\n"
	t_count += 1


