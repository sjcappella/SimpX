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

	while programCounter != -1:
		print("Loop Start")
		# Execute the next instruction and return the updated progarm state
		programState = __execute(instructions[programCounter], symbolTable, memory)
		# Next instruction to execute, update symbol table, updated memory contents
		programCounter = programState[0]
		symbolTable = programState[1]
		memory = programState[2]
		

# Function to execute each instruction
def __execute(instruction, symbolTable, memory):
	return (-1, symbolTable, memory)