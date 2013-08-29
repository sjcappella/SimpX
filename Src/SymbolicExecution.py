import threading
import time

# Extend the thread class for the symbolic interpreter
class SymbolicInterpreter(threading.Thread):
	def __init__(self, instructions, currentInstruction, symVariables, symMemory, precondition):
		threading.Thread.__init__(self)
		self.instructions = instructions
		self.currentInstruction = currentInstruction
		self.symVariables = symVariables
		self.symMemory = symMemory
		self.precondition = precondition

	def run(self):
		print("\n\nSymbolic Execution")

		# Should figure out symbolic memory?
		programCounter = self.currentInstruction

		# Symbolically execute the instructions
		while True:
			programCounter = self.__execute(programCounter)

			# Check
			if programCounter == -2:
				break

	def __execute(self, programCounter):
		instruction = self.instructions[programCounter]
		# Perform unary operation
		if instruction.instruction_type == "UN_OP":
			programCounter = self.__symUnOp(instruction, programCounter)

		# Perform binary operation
		elif instruction.instruction_type == "BIN_OP":
			programCounter = self.__symBinOp(instruction, programCounter)
		
		# Perform input
		elif instruction.instruction_type == "INPUT":
			#programState = __inputInst(instruction, programCounter, symbolTable, memory)
			print("Sym_input")
		# Print output
		elif instruction.instruction_type == "PRINT_OUTPUT":
			#programState = __printOutInst(instruction, programCounter, symbolTable, memory)
			print("Sym_out")
		
		# Assign values
		elif instruction.instruction_type == "ASSIGN":
			#programState = __assignInst(instruction, programCounter, symbolTable, memory)
			programCounter = self.__symAssign(instruction, programCounter)

		# Goto (must take all the instructions to calculate where to return to)
		elif instruction.instruction_type == "GOTO":
			#programState = __gotoInst(instructions, programCounter, symbolTable, memory)
			print("Sym_goto")
		# Store 
		elif instruction.instruction_type == "STORE":
			#programState = __storeInst(instruction, programCounter, symbolTable, memory)
			print("Sym_store")
		# Load
		elif instruction.instruction_type == "LOAD":
			#programState = __loadInst(instruction, programCounter, symbolTable, memory)
			print("Sym_load")
		# Assert
		elif instruction.instruction_type == "ASSERT":
			#programState = __assertInst(instruction, programCounter, symbolTable, memory)
			print("Sym_assert")
		# Boolean (must take all the instructions to calculate where to return to)
		elif instruction.instruction_type == "BOOLEAN":
			#programState = __booleanInst(instructions, programCounter, symbolTable, memory)
			print("Sym_bool")
		# Check for terminate statement
		elif instruction.instruction_type == "TERMINATE_PROGRAM":
			return -2
		# Keep the program going even if we don't recognize the instruction (consider error instead)
		else:
			return programCounter + 1
			
		# Return the updated program state
		return programCounter

	def __symUnOp(self, instruction, programCounter):
		print("sym_un_op")
		self.symVariables[instruction.data[0]] = instruction.data[1] + " " + instruction.data[2] +  " " + instruction.data[3]
		if self.precondition == "":
			self.precondition = "(" + instruction.data[0] + " = " + self.symVariables[instruction.data[0]] + ")"
		else:
			self.precondition += " ^ (" + instruction.data[0] + " = " + self.symVariables[instruction.data[0]] + ")"
		print("Path Condition: %s") % (self.precondition)

		programCounter += 1
		return programCounter

	def __symBinOp(self, instruction, programCounter):
		print("sym_bin_op")
		self.symVariables[instruction.data[0]] = instruction.data[1] + " " + instruction.data[2] +  " " + instruction.data[3]
		if self.precondition == "":
			self.precondition = "(" + instruction.data[0] + " = " + self.symVariables[instruction.data[0]] + ")"
		else:
			self.precondition += " ^ (" + instruction.data[0] + " = " + self.symVariables[instruction.data[0]] + ")"
		print("Path Condition: %s") % (self.precondition)
		
		programCounter += 1
		return programCounter

	def __symAssign(self, instruction, programCounter):
		print("sym_assign")
		self.symVariables[instruction.data[0]] = instruction.data[1]
		if self.precondition == "":
			self.precondition = "(" + instruction.data[0] + " = " + instruction.data[1] + ")"
		else:
			self.precondition += " ^ (" + instruction.data[0] + " = " + instruction.data[1] + ")"
		print("Path Condition: %s") % (self.precondition)

		programCounter += 1
		return programCounter
			
