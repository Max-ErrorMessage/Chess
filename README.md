# Chess
More Compliacted Chess Game created with python using the pygame library, based on the game design on [twokie](http://twokie.com/chess).


## Differences to standard chess:
- The board is 10x10 instead of 8x8
- Pawns can move 3 squares on the first turn


## New Pieces:
### Dog
- Moves like a Knight

- When it takes a piece, it gets another move

- It cannot get more than 1 extra move within 1 player's turn

### Panda
- Moves 2 horiziontally and vertically

- Moves 1 diagonally

- Takes 1 in all directions

- For 1 move after each take the Panda cannot be taken

### Cleric
- Takes along diagonal lines

- Can teleport to any empty square on the board
### Blob
-There are 4 levels to the Blob

- Every time a Blob takes a piece, it lowers its level by 1 and duplicates itself

- The lowest level cannot duplicate itself

- The first level can move anywhere in a 5x5 square centred around itself, apart from the corners.

- The second level can move 2 spaces horizontally and vertically and 1 space diagonally

- The third level can move 1 space in all directions

- The fourth and final level can move 1 sapce horizontally and vertically

### Frog
- Moves 3 spaces horizontally and vertically

- Moves 2 spaces diagonally

- Jumps over pieces

### Chicken
- Inheirits movement from pieces next to it (including enemy pieces)

- Has no movement without inheiriting anything.

- Inherits special functions too: Double Moves after takes if next to a Dog, Brief invulnerablity after caputres if next to a Panda

- Lays an egg after a capturing a piece if inheiriting a Blob that duplicates upon capture

- Eggs hatch into another Chicken after 3 moves

## General Game Rules
- Double Move Pieces may not take a piece if there is no legal moves after taking the piece.

- Pawns can en Passant any time a pawn skips a square that they would have been able to capture.

## Board Layout
The starting board layout is:
```
| BlackRook    || BlackDog     || BlackChicken || BlackBlob0   || BlackPanda   || BlackKing    || BlackCleric  || BlackFrog    || BlackDog     || BlackRook    |
| BlackPawn    || BlackPawn    || BlackPawn    || BlackPawn    || BlackPawn    || BlackPawn    || BlackPawn    || BlackPawn    || BlackPawn    || BlackPawn    |
|              ||              ||              ||              ||              ||              ||              ||              ||              ||              |
|              ||              ||              ||              ||              ||              ||              ||              ||              ||              |
|              ||              ||              ||              ||              ||              ||              ||              ||              ||              |
|              ||              ||              ||              ||              ||              ||              ||              ||              ||              |
|              ||              ||              ||              ||              ||              ||              ||              ||              ||              |
|              ||              ||              ||              ||              ||              ||              ||              ||              ||              |
| WhitePawn    || WhitePawn    || WhitePawn    || WhitePawn    || WhitePawn    || WhitePawn    || WhitePawn    || WhitePawn    || WhitePawn    || WhitePawn    |
| WhiteRook    || WhiteDog     || WhiteChicken || WhiteBlob0   || WhitePanda   || WhiteKing    || WhiteCleric  || WhiteFrog    || WhiteDog     || WhiteRook    |
```
