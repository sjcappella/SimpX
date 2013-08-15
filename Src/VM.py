performTaint = False
performSE = False

# Function to run the virtual machine
def run(instructions, symbolTable, l_performTaint, l_performSE):
	#self.instructions = instructions
	#self.symbolTable = symbolTable
	
	global performTaint, performSE
	performTaint = l_performTaint
	performSE = l_performSE

	memory = []
	programCounter = 0

	print("Execute Loop Start")
	while True:
		#print(programCounter)
		# Execute the next instruction and return the updated progarm state
		programState = __execute(instructions, programCounter, symbolTable, memory)
		
		# Next instruction to execute, update symbol table, updated memory contents
		programCounter = programState[0]
		symbolTable = programState[1]
		memory = programState[2]


		if programCounter == -1:
			print("Program encounter an error! Aborted!")
			break
		if programCounter == -2:
			print("Program terminated successfully.")
			break
		

# Function to execute each instruction
def __execute(instructions, programCounter, symbolTable, memory):
	instruction = instructions[programCounter]
	# Perform unary operation
	if instruction.instruction_type == "UN_OP":
		programState = __unOpInst(instruction, programCounter, symbolTable, memory)
	# Perform binary operation
	elif instruction.instruction_type == "BIN_OP":
		programState = __binOpInst(instruction, programCounter, symbolTable, memory)
	# Perform input
	elif instruction.instruction_type == "INPUT":
		programState = __inputInst(instruction, programCounter, symbolTable, memory)
	# Print output
	elif instruction.instruction_type == "PRINT_OUTPUT":
		programState = __printOutInst(instruction, programCounter, symbolTable, memory)
	# Assign values
	elif instruction.instruction_type == "ASSIGN":
		programState = __assignInst(instruction, programCounter, symbolTable, memory)
	# Goto (must take all the instructions to calculate where to return to)
	elif instruction.instruction_type == "GOTO":
		programState = __gotoInst(instructions, programCounter, symbolTable, memory)
	# Store 
	elif instruction.instruction_type == "STORE":
		programState = __storeInst(instruction, programCounter, symbolTable, memory)
	# Assert
	elif instruction.instruction_type == "ASSERT":
		programState = __assertInst(instruction, programCounter, symbolTable, memory)
	# Boolean (must take all the instructions to calculate where to return to)
	elif instruction.instruction_type == "BOOLEAN":
		programState = __booleanInst(instruction, programCounter, symbolTable, memory)
	elif instruction.instruction_type == "TERMINATE_PROGRAM":
		programState = (-2, programCounter, symbolTable, memory)
	else:
		programState = (programCounter + 1, symbolTable, memory)
		

	# Return the updated program state
	return programState

# Function to perform the unary operation instructions
def __unOpInst(instruction, programCounter, symbolTable, memory):
	print("Executing unary op instruction.")
	lhs = __symTableLookUp(instruction.data[1], symbolTable)
	rhs = __symTableLookUp(instruction.data[3], symbolTable)
	instruction.printInstruction()
	print("Unary op on %d and %d.") % (lhs, rhs)
	
	if instruction.data[2] == '*':
		answer = lhs * rhs
	if instruction.data[2] == '+':
		answer = lhs + rhs
	if instruction.data[2] == '-':
		answer = lhs - rhs

	symbolTable[instruction.data[0]] = answer

	programCounter += 1
	return (programCounter, symbolTable, memory)

# Function to perform the binary operation instructions
def __binOpInst(instruction, programCounter, symbolTable, memory):
	print("Executing binary op instruction.")
	lhs = __symTableLookUp(instruction.data[1], symbolTable)
	rhs = __symTableLookUp(instruction.data[3], symbolTable)
	instruction.printInstruction()
	print("Binary op on %d and %d.") % (lhs, rhs)
	
	if instruction.data[2] == '*':
		answer = lhs * rhs
	if instruction.data[2] == '/':
		answer = math.floor(lhs / rhs)
	if instruction.data[2] == '+':
		answer = lhs + rhs
	if instruction.data[2] == '-':
		answer = lhs - rhs
	if instruction.data[2] == '^':
		answer = lhs ^ rhs
	if instruction.data[2] == '|':
		answer = lhs | rhs
	if instruction.data[2] == '&':
		answer = lhs & rhs
	if instruction.data[2] == '%':
		answer = lhs % rhs

	symbolTable[instruction.data[0]] = answer

	programCounter += 1
	return (programCounter, symbolTable, memory)

# Function to perform the input operation instructions
def __inputInst(instruction, programCounter, symbolTable, memory):
	print("Executing input instruction.")
	print("User input interrupt! Enter an integer:")
	while True:
		try:
			user_input = int(raw_input())
			break
		except ValueError:
			print("ONLY INTEGERS ACCEPTED!")
			print("Enter an integer:")
	
	symbolTable[instruction.data[0]] = user_input
	programCounter += 1
	return (programCounter, symbolTable, memory)

# Function to perform output instructions
def __printOutInst(instruction, programCounter, symbolTable, memory):
	print("Executing print instruction.")
	print("Console output interrupt.")
	value = __symTableLookUp(instruction.data[0], symbolTable)
	print(">>> %d") % (value)
	programCounter += 1
	return (programCounter, symbolTable, memory)

# Function perform assignment instructions
def __assignInst(instruction, programCounter, symbolTable, memory):
	print("Executing assign instruction.")
	symbolTable[instruction.data[0]] = __symTableLookUp(instruction.data[1], symbolTable)
	programCounter += 1
	return (programCounter, symbolTable, memory)

# Function to perform goto instructions
def __gotoInst(instructions, programCounter, symbolTable, memory):
	print("Executing goto instruction.")
	target_address = "BB_" + str(__symTableLookUp(instructions[programCounter].data[0], symbolTable)) + ":BEGIN"
	# If we don't find the destination, then we need to crash
	programCounter = -1
	for x in range(len(instructions)):
		if instructions[x].instruction_type == target_address: 
			print("Jumping to: %s") % (target_address)
			programCounter = x
	return (programCounter, symbolTable, memory)

# Function to perform store instructions
def __storeInst(instruction, programCounter, symbolTable, memory):
	print("Executing store instruction.")
	return (programCounter + 1, symbolTable, memory)

# Function to perform assert instructions
def __assertInst(instruction, programCounter, symbolTable, memory):
	print("Executing assert instruction.")
	return (programCounter + 1, symbolTable, memory)

# Function to perform boolean instructions
def __booleanInst(instruction, programCounter, symbolTable, memory):
	print("Executing boolean instruction.")
	return (programCounter + 1, symbolTable, memory)

# Function to perform symbol table looks
def __symTableLookUp(label, symbolTable):
	print(label)
	try:
		int(label)
		return int(label)
	except:
		if label in symbolTable:
			if symbolTable[label] == '':
				return 0
			else:
				return int(symbolTable[label])
		else:
			return 0
