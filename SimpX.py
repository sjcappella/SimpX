import sys
import Lexer as Lexer

def callLexer(file_path):
	file = open(file_path)
   	file_data = ""
   	while 1:
   		line = file.readline()
   		if not line:
   			break
   		pass
   		file_data += line

   	print(file_data)
   	Lexer.lexInput(file_data)


def main(argv):
   
   if (len(argv)) < 2:
   	print("No input file given. Quitting.")
   	exit()
   else:
   	callLexer(argv[1])
   
   

if __name__ == "__main__":
    main(sys.argv)