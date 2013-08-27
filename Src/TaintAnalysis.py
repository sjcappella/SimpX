# Class to handle the taint analysis
class TaintAnalysis:
	# Constructor function
	def __init__(self):
		self.symbolTable = dict()
		self.memory = dict()

	# Function to handle taint propagation based on binary oparations
	def propagateTaintBinOp(self, resultLabel, lhs, rhs, op):
		# We will consider different operations later (eg XOR with itself removes taint)
		if (TaintAnalysis.isTaintedSym(self, lhs) or TaintAnalysis.isTaintedSym(self, rhs)):
			print("[ TAINT ] Propagating taint from %s and %s to %s based on %s.") % (str(lhs), str(rhs), str(resultLabel), str(op))
			self.symbolTable[resultLabel] = True
		else:
			self.symbolTable[resultLabel] = False

	# Function to handle taint propagation based on user input operations
	def propagateTaintInput(self, resultLabel):
		print("[ TAINT ] Propogating taint. %s is now tainted!") % (resultLabel)
		self.symbolTable[resultLabel] = True

	# Function to handle taint propagation based on assignments
	def propagateTaintAssign(self, lhs, rhs):
		if (TaintAnalysis.isTaintedSym(self, rhs)):
			print("[ TAINT ] Propagating taint from %s to %s.") % (str(rhs), str(lhs))
			self.symbolTable[lhs] = True
		else:
			self.symbolTable[lhs] = False


	# Function to handle taint propagation based on store instructions
	def propagateTaintStore(self, memoryDestination, label):
		if (TaintAnalysis.isTaintedSym(self, label)):
			print("[ TAINT ] Propagating taint from %s to memory address %s.") % (str(label), str(memoryDestination))
			self.memory[str(memoryDestination)] = True
		else:
			self.memory[str(memoryDestination)] = False

	# Function to handle taint propagation based on load instructions
	def propagateTaintLoad(self, memorySource, label):
		if (TaintAnalysis.isTaintedMem(self, memorySource)):
			print("[ TAINT ] Propagating taint from memory address %s to value %s.") % (str(memorySource), str(label))
			self.symbolTable[label] = True
		else:
			self.symbolTable[label] = False

	# Function to see if we are jumping to an address that has been tainted
	def taintedJump(self, destination):
		if (TaintAnalysis.isTaintedSym(self, destination)):
			print(" <<< UNSAFE JUMP! VALUE HAS BEEN TAINTED! >>>")


	# Function to see if a symbol is tainted or not 
	def isTaintedSym(self, symbol):
		try:
			# Symbol is an integer value, not tainted
			int(symbol)
			return False
		except:
			if symbol in self.symbolTable:
				return self.symbolTable[symbol]
			# Adding value and saying it is not tainted
			else:
				self.symbolTable[symbol] = False
				return False

	# Function to see if a memory value is tainted or not
	def isTaintedMem(self, index):
		# We are using a dictionary, so the index value will actually be a string
		if str(index) in self.memory:
			return self.memory[str(index)]
		# Adding value and saying it is not tainted
		else:
			self.memory[str(index)] = False
			return False

	# Function to print tainted results
	def printTaintedResults(self):
		# Symbols
		print("\n::VARIABLES::")
		for key, value in self.symbolTable.items():
			print(key, value)

		# Memory
		print("\n::MEMORY::")
		for key, value in self.memory.items():
			print(key, value)