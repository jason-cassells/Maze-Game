To create a valid configuration file do the following:
	> Create a .txt file in the /Config directory called "Conf" followed by the next number in the sequence E.g 5

In order for this game to run as intended the game must contain, 25 valid squares (or a 5 * 5 grid)
A square is represented by a 1, seperated by a comma therefore

1, 1, 1
1, 1, 1
1, 1, 1

is a 3 * 3 grid of 9 valid squares, please format your file accordingly.

In addition all grids must be enclosed by 0's representing the walls

0, 0 ,0, 0, 0
0, 1, 1, 1, 0
0, 1, 1, 1, 0
0, 1, 1, 1, 0
0, 0 ,0, 0, 0

would be an example of this.

it is possible to have non-square maps as long as they contain 25 valid squares
for example:

0, 0 ,0, 0, 0, 0, 0 ,0, 0, 0, 0
0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0
0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0
0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0
0, 0 ,0, 0, 0, 0 ,0, 0, 0, 0, 0

Please end your file with no trailing lines.