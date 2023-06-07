# Computer-Organization-group-project
NOTE: All the necessary files are in the master branch.
There are a total of four questions in this assignment: 1. Designing and Implementing the assembler. 2. Designing and Implementing the simulator. 3. Extending the functionality of the assembler-simulator set-up to handle simple floating-point computations. 4. A bonus question based on the assembler and simulator.

Our instructions:

1.	addi(l, pc): Performs an immediate addition operation. Adds the values of reg[l[10:13]] and l[13:16] (converted to integers), and stores the result in reg[l[7:10]]. Returns the incremented value of pc.
2.	subi(l, pc): Performs an immediate subtraction operation. Subtracts the value of l[13:16] (converted to an integer) from reg[l[10:13]], and stores the result in reg[l[7:10]]. Returns the incremented value of pc.
3.	reset(): Resets the global variables reg and memory by setting all register values to zero.
4.	inc(l, pc): Increments the value of reg[l[10:13]] by 1 and stores the result in reg[l[7:10]]. Returns the incremented value of pc.
5.	dec(l, pc): Decrements the value of reg[l[10:13]] by 1 and stores the result in reg[l[7:10]]. Returns the incremented value of pc.
