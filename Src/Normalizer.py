t_count = 0
temp_val = ""
code = ""
symbolTable = dict()


# Main function to call to normalize the  code
def normalize(ASTList):
	global code
	for x in range(len(ASTList)):
		convertToIR(ASTList[x], x+1) 
	print(code)
	for key, value in symbolTable.items():
		print(key, value)

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
	if ASTNode.token_type == "BOOLEAN_EXPRESSION":
		booleanNodes(ASTNode)
	
# Function to handle statement nodes
def statementNodes(ASTNode):
	global code, temp_val, t_count, symbolTable
	# Generate code for declaring a new variable
	if ASTNode.statement_type == "VAR_ID":
		code += ("\tvar_" + ASTNode.children[1].value + "\n")
		symbolTable['var_' + ASTNode.children[1].value] = '0'
	
	# Generate code for goto statements
	if ASTNode.statement_type == "GOTO":
		convertToIRRec(ASTNode.children[1])
		code += "\tgoto( BB_" + temp_val + ":BEGIN )\n"

	# Generate code for assert statements
	if ASTNode.statement_type == "ASSERT":
		convertToIRRec(ASTNode.children[1])
		code += "\tassert( " + temp_val + " )\n"

	# Generate code for assigning an old variable
	if ASTNode.statement_type == "ASSIGN":
		convertToIRRec(ASTNode.children[2])
		code += ("\tvar_" + ASTNode.children[0].value + " := " + temp_val + "\n")

	# Generate code for assigning a new variable
	if ASTNode.statement_type == "ASSIGN_NEW":
		# Make sure to add variable to symbol table 
		convertToIRRec(ASTNode.children[3])
		code += ("\tvar_" + ASTNode.children[1].value + " := " + temp_val + "\n")
		symbolTable['var_' + ASTNode.children[1].value] = temp_val 
	
	# Generate code for printing statements
	if ASTNode.statement_type == "PRINT_OUTPUT":
		convertToIRRec(ASTNode.children[2])
		code += "\tprint_output( " + temp_val + " )\n"
		
	# Generate code for store statements
	if ASTNode.statement_type == "STORE":
		convertToIRRec(ASTNode.children[2])
		temp_val_1 = temp_val
		convertToIRRec(ASTNode.children[4])
		temp_val_2 = temp_val
		code += "\tstore( " + temp_val_1 + " , " + temp_val_2 + " )\n"
	
	# Generate code for boolean expressions
	if ASTNode.statement_type == "BOOLEAN":
		convertToIRRec(ASTNode.children[2])
		temp_val_1 = temp_val
		convertToIRRec(ASTNode.children[6])
		temp_val_2 = temp_val
		convertToIRRec(ASTNode.children[9])
		temp_val_3 = temp_val
		code += "\tif( " + temp_val_1 + " ):\n"
		code += "\tgoto( BB_" + temp_val_2 + ":BEGIN )\n"
		code += "\telse goto( BB_" + temp_val_3 + ":BEGIN )\n"
			
# Function to handle factor nodes
def factorNodes(ASTNode):
	global code, temp_val, t_count
	
	# Check for 32-Bit usigned integers
	if ASTNode.factor_type == "32_BIT_USIGN_INT":
		temp_val = str(ASTNode.value)
	
	# Check for variables
	if ASTNode.factor_type == "ID":
		temp_val = "var_" + str(ASTNode.value)
	
	# Check for a unary operation
	if ASTNode.factor_type == "UNARY_FACTOR":
		convertToIRRec(ASTNode.children[1])
		symbol = ASTNode.children[0].symbol
		temp_val_1 = temp_val
		temp_val = "t_"+ str(t_count)
		# Negate operation
		if symbol == "-":
			code += "\t" + temp_val + " := -1 * " + temp_val_1 + "\n"
		# Positive operation
		if symbol == "+":
			code += "\t" + temp_val + " := 1 * " + temp_val_1 + "\n"
		# Increment operation
		if symbol == "++":
			code += "\t" + temp_val + " := " + temp_val_1 + " + 1\n"
		# Decrement operation
		if symbol == "--":
			code += "\t" + temp_val + " := " + temp_val_1 + " - 1\n"
		# Dereference operation (get value at that memory address)
		if symbol == "&":
			code += "\t" + temp_val + " := load( " + temp_val_1 + " )\n"
		t_count += 1 
		# Add variable to symbol table
		symbolTable[temp_val] = ''

	# Check for a paren expression
	if ASTNode.factor_type == "PAREN_EXPRESSION":
		# Might need some logic here
		convertToIRRec(ASTNode.children[1])
	
	# Check for an input statement
	if ASTNode.factor_type == "GET_INPUT":
		temp_val = "t_" + str(t_count)
		code += "\t" + temp_val + " := get_input()\n" 
		t_count += 1
		# Add variable to symbol table
		symbolTable[temp_val] = ''
	
	# Check for a load statement
	if ASTNode.factor_type == "LOAD":
		convertToIRRec(ASTNode.children[2])
		temp_val_1 = temp_val
		temp_val = "t_" + str(t_count)
		code += "\t" + temp_val + " := load( " + temp_val_1 + " )\n"
		t_count += 1
		# Add variable to symbol table
		symbolTable[temp_val] = ''

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
	# Add variable to the symbol table
	symbolTable[temp_val] = ''

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
	# Add variable to the symbol table
	symbolTable[temp_val] = ''

# Function to handle boolean nodes
def booleanNodes(ASTNode):
	global code, temp_val, t_count
	convertToIRRec(ASTNode.children[0])
	temp_val_1 = temp_val
	convertToIRRec(ASTNode.children[2])
	temp_val_2 = temp_val
	symbol = ASTNode.children[1].symbol
	temp_val = temp_val_1 + " " + symbol + " " + temp_val_2

