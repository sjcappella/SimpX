# SimpX


### Description:
This projects aims to demonstrate how virtual machines, dynamic taint analysis, and symbolic execution engines work.

### Instructions:
Running this platform should be relatively easy. Clone the project onto your local machine and move into the directory. Create an example source code file (at least one should be provided when checking out the project) and feed it into the program via the following command: 
	
	$ python SimpX.py <path/to/input/file.input>

More options will be added later. 

### Input Language Specification:
#### Grammar

	<program> 			::= <statement_list>
	
	<statement_list> 	::= <statement_list> <statement>
					     |  <statement>
	
	<statement> 		::= VAR <id>	
				 		 |	VAR <id> := <expression
				 		 |  <id> := <expression>
				 		 |  store( <expression> , <expression> )
				 		 |  goto <expression>
				 		 |  assert <bool_expression>
				 		 |  if( <bool_expression> ) then goto <expression> else goto <expression>
				 		 |  print_output( <expression> )
	
	<expression> 		::= <expression> <add_op> <term>
				  		 |	<term>
	
	<add_op> 			::= + | -
	
	<term> 				::= <term> <mulop> <factor>
						 |  <term>
	
	<mulop> 			::= * | / | % | ^ | | | &
	
	<factor> 			::= <unary_op> <factor>
			  			 |  ( <expression> )
			  			 |  32_BIT_USIGN_INT
			  			 |  ID
			  			 |  get_input()
			  			 |  load( <expression> )
	
	<id> 				::= ID
	
	<bool_expression> 	::= <expression> <rel_op> <expression>
	
	<rel_op> 			::= == | != | < | > | <= | >=
	
	<unary_op> 			::= + | - | ++ | -- | &

#### Variables
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
