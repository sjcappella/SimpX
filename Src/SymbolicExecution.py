import threading
import time

# Extend the thread class for the symbolic interpreter
class symbolicInterpreter(threading.Thread):
	def __init__(self, instructions, currentInstruction, precondition):
		threading.Thread.__init__(self)
		self.instructions = instructions
		self.currentInstruction = currentInstruction
		self.precondition = precondition

	def run(self):
		print("Symbolic Execution")