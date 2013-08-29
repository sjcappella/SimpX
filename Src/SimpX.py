import sys
import Parser as Parser
import Normalizer as Normalizer
import VM as VM
import SymbolicExecution as SymbolicExecution

# Function to perform lexical analysis and parsing of source code
def lexAndParse(source_path):
   # Open source code file
   file = open(source_path)

   # Read in source code line by line
   source_code = []
   while 1:
      line = file.readline()
      if not line:
         break
      else:
         source_code.append(line)

   # Print out the original source code
   print("\n::======= INPUT SOURCE CODE START =======::\n")
   for x in range(len(source_code)):
      sys.stdout.write(source_code[x])
   print("\n::======= INPUT SOURCE CODE END =======::\n")
   
   # Send source code for lexical analysis and parsing
   print("\n::======= ASTs START =======::\n")   
   ASTs = []
   for x in range(len(source_code)):
      AST = Parser.parse(source_code[x], x+1)
      if AST != None:
         AST.prettyPrint("", True)
         ASTs.append(AST)
   print("\n::======= ASTs END =======::\n")
   return ASTs

def main(argv):

   if (len(argv)) < 2:
      print("No input file given. Quitting.")
      exit()
   else:
      ASTs = lexAndParse(argv[1])
      Instructions_and_Symbols = Normalizer.normalize(ASTs)
      instructions = Instructions_and_Symbols[0]
      symbols = Instructions_and_Symbols[1]
      symbols = VM.run(instructions, symbols, True, True)
      si = SymbolicExecution.SymbolicInterpreter(instructions, 0, symbols, None, "", 0)
      si.run()

      
# Check for main function call      
if __name__ == "__main__":
    main(sys.argv)