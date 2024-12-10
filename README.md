## Logic Gate Simulator

### Overview
An interactive logic gate simulator built using Python and Pygame. This application allows users to visually create and connect various logic gates such as AND, OR, NOT, NAND, NOR, XOR, and even combine them to form advanced circuits like Half Adders and Full Adders. The simulator computes the outputs of the logic gates based on the given inputs.

### Features
- **Create and interact with logic gates**: Users can add various types of logic gates to the workspace and manipulate their inputs and outputs.
  - Gate types supported: AND, OR, NOT, NAND, NOR, XOR, Half Adder, and Full Adder.
- **Input and output manipulation**: Users can set the input values for each gate and see the corresponding output in real-time.
- **Create combinations**: Combine basic gates to form Half Adder and Full Adder circuits.
- **Drag and drop gates**: Users can move gates around the screen for better organization.
- **Connections between gates**: Click on output lines to connect them to other gates' inputs.
- **Real-time computation**: The simulator computes the output for each gate based on the connected inputs and displays the result.
- **Delete gates**: Users can delete gates by dragging them over a designated delete box.
- **Hover feature**: When hovering over a gate or connection, the program highlights the gate or connection to provide visual feedback to the user. This makes it easier to identify and manipulate the gates or connections during interaction.




### Opening the Application file

The window will open with a display of available logic gates at the top.

Click on the desired gate type to place it on the screen. The available gates are:

- AND
- OR
- NOT
- NAND
- NOR
- XOR
- Half Adder
- Full Adder

**To manipulate a gate's input**:

- Click on a gate to select it.
- Use the mouse to drag and drop gates around the screen.
- Use the right-click to connect the output of one gate to the input of another gate. The outputs of gates will be computed based on the input values.
- Click on the delete box at the bottom to remove any unwanted gates.
