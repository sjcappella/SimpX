import sys
# Class for an instruction to be executed on the VM
class Instruction:
	# Class constructor
	def __init__(self, instruction_type, data):
		self.instruction_type = instruction_type
		self.data = data

	# Print the instruction
	def printInstruction(self):
		sys.stdout.write(self.instruction_type + " -> ")
		if self.data != None:
			for x in range(len(self.data)):
				if x == 0:
					sys.stdout.write(self.data[x])
				elif self.data[x] != "":
					sys.stdout.write(", " + self.data[x])
		sys.stdout.write("\n")