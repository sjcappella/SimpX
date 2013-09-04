# SimpX


### Description:
This projects aims to demonstrate how virtual machines, dynamic taint analysis, and symbolic execution engines work.

### Instructions:
Running this platform should be relatively easy. Clone the project onto your local machine and move into the directory. Create an example source code file (at least one should be provided when checking out the project) and feed it into the program via the following command: 
	
	$ python SimpX.py <path/to/input/file.input>

More options will be added later. 

### Input Language Specification:
#### Grammar:

	<program> ::= <statement_list>
	<statement_list> ::= <statement_list> <statement>
					  |	 <statement>
	<statement> ::= __VAR__ <id>	
#### Variables:
All variables that are used but have not been initialized/declared will be evaluated to be 0 by the interpreter.

#### Using Memory
The following statements are equivalent:

	var y := load(4)

Is the same as:

	var x := 4
	var y := load(x)

And the same as:
	
	var x := 4
	var y := &x

Each operation will consult the interpreter's dynamic memory and retrieve the value located at that memory location.
