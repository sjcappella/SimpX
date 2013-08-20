import VMInstruction
import shlex

t_count = 0
temp_val = ""
code = ""
symbolTable = dict()
instructions = []


# Main function to call to normalize the  code
def normalize(ASTList):
	global code
	for x in range(len(ASTList)):
		convertToIR(ASTList[x], x+1)
	code += ("TERMINATE_PROGRAM\n")
	instructions.append(VMInstruction.Instruction("TERMINATE_PROGRAM", None)) 
	print("===== IR CODE =====")
	print(code)
	print("===== SYMBOL TABLE =====")
	for key, value in symbolTable.items():
		print(key, value)
	print("===== VM INSTRUCTIONS =====")
	for x in range(len(instructions)):
		instructions[x].printInstruction()

	# Should do some file output for the IR, Symbol Table and VM Instructions
	return (instructions, symbolTable)

# Conver an AST to IR
def convertToIR(AST, block_ID):
	global code, instructions
	code_segment = "BB_" + str(block_ID) + ":BEGIN"
	code += ("BB_%d:BEGIN\n") % (block_ID)
	instructions.append(VMInstruction.Instruction(code_segment, None))
	convertToIRRec(AST)
	code += ("BB_%d:END\n") % (block_ID)
	code_segment = "BB_" + str(block_ID) + ":END"
	instructions.append(VMInstruction.Instruction(code_segment, None))
	
# Recursive function to convert to IR
def convertToIRRec(ASTNode):
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
		var_id = "var_" + ASTNode.children[1].value
		code += ("\t" + var_id + "\n")
		symbolTable[var_id] = ''
		instructions.append(VMInstruction.Instruction("VAR_ID", (var_id, "")))
	
	# Generate code for goto statements
	if ASTNode.statement_type == "GOTO":
		convertToIRRec(ASTNode.children[1])
		code += "\tgoto( BB_" + temp_val + ":BEGIN )\n"
		instructions.append(VMInstruction.Instruction("GOTO", (temp_val, "")))

	# Generate code for assert statements
	if ASTNode.statement_type == "ASSERT":
		convertToIRRec(ASTNode.children[1])
		code += "\tassert( " + temp_val + " )\n"
		instructions.append(VMInstruction.Instruction("ASSERT", shlex.split(temp_val)))

	# Generate code for assigning an old variable
	if ASTNode.statement_type == "ASSIGN":
		convertToIRRec(ASTNode.children[2])
		var_id = "var_" + ASTNode.children[0].value
		code += ("\t" + var_id + " := " + temp_val + "\n")
		instructions.append(VMInstruction.Instruction("ASSIGN", (var_id, temp_val)))

	# Generate code for assigning a new variable
	if ASTNode.statement_type == "ASSIGN_NEW":
		# Make sure to add variable to symbol table 
		convertToIRRec(ASTNode.children[3])
		var_id = "var_" + ASTNode.children[1].value
		code += ("\t" + var_id + " := " + temp_val + "\n")
		symbolTable[var_id] = temp_val
		instructions.append(VMInstruction.Instruction("ASSIGN", (var_id, temp_val))) 
	
	# Generate code for printing statements
	if ASTNode.statement_type == "PRINT_OUTPUT":
		convertToIRRec(ASTNode.children[2])
		code += "\tprint_output( " + temp_val + " )\n"
		instructions.append(VMInstruction.Instruction("PRINT_OUTPUT", (temp_val, "")))
		
	# Generate code for store statements
	if ASTNode.statement_type == "STORE":
		convertToIRRec(ASTNode.children[2])
		temp_val_1 = temp_val
		convertToIRRec(ASTNode.children[4])
		temp_val_2 = temp_val
		code += "\tstore( " + temp_val_1 + " , " + temp_val_2 + " )\n"
		instructions.append(VMInstruction.Instruction("STORE", (temp_val_1, temp_val_2)))
	
	# Generate code for boolean expressions
	if ASTNode.statement_type == "BOOLEAN":
		convertToIRRec(ASTNode.children[2])
		temp_val_1 = temp_val
		convertToIRRec(ASTNode.children[6])
		temp_val_2 = temp_val
		convertToIRRec(ASTNode.children[9])
		temp_val_3 = temp_val
		block_1 = "BB_" + temp_val_2 + ":BEGIN"
		block_2 = "BB_" + temp_val_3 + ":BEGIN"
		code += "\tif( " + temp_val_1 + " ):\n"
		code += "\tgoto( " + block_1 + " )\n"
		code += "\telse goto( " + block_2 + " )\n"
		temp_val_1 = shlex.split(temp_val_1)
		temp_val_1 = tuple(temp_val_1)
		instructions.append(VMInstruction.Instruction("BOOLEAN", (temp_val_1 + (temp_val_2,) + (temp_val_3,))))
			
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
			instructions.append(VMInstruction.Instruction("UN_OP", (temp_val, "-1", "*", temp_val_1)))
		# Positive operation
		if symbol == "+":
			code += "\t" + temp_val + " := 1 * " + temp_val_1 + "\n"
			instructions.append(VMInstruction.Instruction("UN_OP", (temp_val, "1", "*", temp_val_1)))
		# Increment operation
		if symbol == "++":
			code += "\t" + temp_val + " := " + temp_val_1 + " + 1\n"
			instructions.append(VMInstruction.Instruction("UN_OP", (temp_val, temp_val, "+", "1")))
		# Decrement operation
		if symbol == "--":
			code += "\t" + temp_val + " := " + temp_val_1 + " - 1\n"
			instructions.append(VMInstruction.Instruction("UN_OP", (temp_val, temp_val, "+", "1")))
		# Dereference operation (get value at that memory address)
		if symbol == "&":
			code += "\tload( " + temp_val + " , " + temp_val_1 + " )\n"
			instructions.append(VMInstruction.Instruction("LOAD", (temp_val, temp_val_1)))
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
		instructions.append(VMInstruction.Instruction("INPUT", (temp_val, "")))
	
	# Check for a load statement
	if ASTNode.factor_type == "LOAD":
		convertToIRRec(ASTNode.children[2])
		temp_val_1 = temp_val
		temp_val = "t_" + str(t_count)
		code += "\tload( " + temp_val + " , " + temp_val_1 + " )\n"
		t_count += 1
		# Add variable to symbol table
		symbolTable[temp_val] = ''
		instructions.append(VMInstruction.Instruction("LOAD", (temp_val, temp_val_1)))

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
	instructions.append(VMInstruction.Instruction("BIN_OP", (temp_val, temp_val_1, symbol, temp_val_2)))

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
	instructions.append(VMInstruction.Instruction("BIN_OP", (temp_val, temp_val_1, symbol, temp_val_2)))

# Function to handle boolean nodes
def booleanNodes(ASTNode):
	global code, temp_val, t_count
	convertToIRRec(ASTNode.children[0])
	temp_val_1 = temp_val
	convertToIRRec(ASTNode.children[2])
	temp_val_2 = temp_val
	symbol = ASTNode.children[1].symbol
	temp_val = temp_val_1 + " " + symbol + " " + temp_val_2