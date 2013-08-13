performTaint = False
performSE = False

# Function to run the virtual machine
def run(self, instructions, symbolTable, l_performTaint, l_performSE):
	self.instructions = instructions
	self.symbolTable = symbolTable
	
	global performTaint, performSE
	performTaint = l_performTaint
	performSE = l_performSE

	memory = []

	progamCounter = 0
	while progamCounter != -1:
		# Execute the next instruction and return the updated progarm state
		programState = execute(instructions[progamCounter], symbolTable, memory)
		# Next instruction to execute, update symbol table, updated memory contents
		programCounter = programState[0]
		symbolTable = programState[1]
		memory = programState[2]

# Funtion to execute each instruction
def __execute(instruction, symbolTable, performTaint, performSE):