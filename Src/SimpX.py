import sys
import Parser as Parser

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
   print("Source Code to execute and analyze:")
   for x in range(len(source_code)):
      print(source_code[x])

   # Send source code for lexical analysis and parsing
   ASTs = []
   for x in range(len(source_code)):
      AST = Parser.parse(source_code[x], x+1)
      ASTs.append(AST)

   return ASTs

def main(argv):
   
   if (len(argv)) < 2:
   	print("No input file given. Quitting.")
   	exit()
   else:
   	lexAndParse(argv[1])
   
   

if __name__ == "__main__":
    main(sys.argv)