#include <iostream>
#include <array>
#include <string>
#include <algorithm>
#include <vector>
#include <map>
#include <limits>


using namespace std;

std::string colour_from_bool(bool is_white) {
    /*
    * Turns a boolean colour identifier into a string representation of the colour
    */
    if (is_white) {
        return "White";
    }
    return "Black";
}

std::string postostr(std::pair<int, int> pos) {
    /*
    * Turns a pair containing the position of a square on the board into a string representation of the position
    */
    return "(" + std::to_string(pos.first) + ", " + std::to_string(pos.second) + ")";
}

bool pieces_in_vector(std::vector<std::string> vec, std::vector<std::string> items) {
    /*
    * TODO: Find out what this function does and why it does it
    */
    for (std::string item : items) {
        for (std::string element : vec) {
            if (item == element) {
                return true;
            }
        }
    }
    return false;
}

bool position_in_vector(std::vector<std::pair<int, int>> vec, std::pair<int, int> pos) {
    /*
    * TODO: Find out what this function does and why it does it
    */
    for (std::pair<int, int> it: vec) {
        if (it == pos) {
            return true;
        }
    }
    return false;
}

bool char_in_str(std::string str, char chr) {
    /*
    * Checks for a character in a given string
    */
    for (char current_char : str) {
        if (current_char == chr) {
            return true;
        }
    }
    return false;
}

int flip_ints(int num, bool is_white) {
    /*
    * Ensures integers have the correct sign for their colour
    */
    if (!is_white) {
        return num * -1;
    }
    return num;
}

std::pair<std::string, float> minimax(std::string boardstate, bool white_to_play, int depth) {
    ChessBoard* board = new ChessBoard();
    board->set_board_state(boardstate);
    board->white_to_move = white_to_play;

    std::vector<std::pair<std::pair<int, int>, std::pair<int, int>>> moves = board->all_legal_moves();

    if (moves.empty() || depth == 0) {
        float score = static_cast<float>(board->material_difference());
        delete board;
        return {boardstate, score};
    }

    std::pair<std::string, float> best_result;
    float best_score = white_to_play ? -std::numeric_limits<float>::infinity()
                                      :  std::numeric_limits<float>::infinity();

    for (const auto& move : moves) {
        ChessBoard* new_board = board->copy_board();
        new_board->move_piece(move.first, move.second);

        std::string new_state = new_board->board_state();
        bool next_turn = !white_to_play;

        std::pair<std::string, float> result = minimax(new_state, next_turn, depth - 1);

        float score = result.second;

        if ((white_to_play && score > best_score) || (!white_to_play && score < best_score)) {
            best_score = score;
            best_result = {new_state, score};
        }

        delete new_board;
    }

    delete board;
    return best_result;
}

class Piece {
    /*
    * The Piece class stores base behaviour for all pieces
    */
    public:
        bool is_white; // Tracks if the piece is black or white
        bool immortal; // Tracks if the piece is currently immortal (in the case of the Panda)
        bool has_moved; // Tracks if the piece has moved this game (for castling)
        bool en_passantable; // Tracks if the piece has moved forwards in such a way that it could be en-passanted
        int time_until_hatch; // Tracks how many moves remain until the 'hatch' even (for eggs)
        int abs_value;

        Piece(bool is_white, int value) {
            // Generic constructor for pieces
            this -> is_white = is_white;
            immortal = false;
            has_moved = false;
            en_passantable = false;
            time_until_hatch = -1;
            abs_value = value;
        }

        bool operator!=(const std::nullptr_t& null) const {
            /*
            * This code seems to me to be entirely useless and nonsensical, but I'm sure that If I remove ir or change it then the code will break
            */
            return (this != nullptr);
        }

        virtual std::string name() const {
            /*
            * The name function returns a tring that represents the Piece - for displaying the piece on a string board
            */
            return "Piece   ";
        }

        virtual int as_int() const {
            /*
            * Integer representations of pieces are the most efficient (and confusing!)
            */
            return 0;
        }
        
        virtual std::vector<std::pair<int, int>> moves() const {
            /*
            * Returns a vector of all moves that the piece can make relative to where it is
            * Note that in this case 'moves' is different to 'takes' (for the purposes of things such as pawns)
            */
            return {};
        }

        virtual std::vector<std::pair<int, int>> takes() const {
            /*
            * Returns a vector of all 'takes' moves that the piece can make relative to where it is
            */
            return moves();
        }

        virtual std::vector<std::pair<std::pair<int, int>, int>> direction_moves() const {
            /*
            * Returns a vector that contains the direction moves available. 
            * Direction moves are 'sliding' moves that pieces such as the rook can perform.
            * The direction comes in the form D, L
            * The D is the directional component ({-1, 0}, {1, 1}, etc.)
            * The L is the maximum limit to those moves (how much 'reach' the move has)
            */
            return {};
        }

        virtual std::vector<std::pair<std::pair<int, int>, int>> direction_takes() const {
            /*
            * Returns a vector that contains the directional takes available.
            */
            return direction_moves();
        }

        virtual std::vector<std::pair<std::pair<int, int>, std::pair<int, int>>> dependant_moves() const {
            /*
            * Returns a vector containing all dependant moves available.
            * Dependant moves indicate a move that can be made provided another space is free
            * Dependant moves contain 2 relative vectors, and the piece may move to the first vector if the second is empty.
            */
            return {};
        }

        virtual std::vector<std::pair<std::pair<int, int>, std::pair<int, int>>> dependant_takes() const {
            /*
            * Returns a vector containing all dependant takes available
            */
            return dependant_moves();
        }

        virtual void move() {
            /*
            * Tracks movement of pieces
            */
            has_moved = true;
        }

        virtual void take() {
            /*
            * Tracks movement of pieces
            */
            has_moved = true;
        }

        virtual void tick() {} // Some pieces (the Egg) specifically care about game time so for the sake of simplicity each piece has a tick function

        int value() {
            if (is_white) {
                return abs_value;
            } 
            return -abs_value;
        }

};

class Pawn : public Piece {
    public:
        int forwards; // Representation of which direction is 'forwards' for the pawn (who cares about the direction of the board)

        Pawn(bool is_white) : Piece(is_white, 1) {
            this -> en_passantable = false;
            if (is_white) {
                this -> forwards = -1;
            } else {
                this -> forwards = 1;
            }
        }

        std::string name() const {
            return (colour_from_bool(is_white) + "Pawn   ");
        }

        int as_int() const {
            /*
            * The pawn has 3 unique states for the purpose of storing a board as a series of integers:
            * 1. A pawn that has not yet moves (may move forwards 2 or 3 spaces)
            * 2. A pawn that has _just_ moved forwards 2 or 3 spaces (may be en-passanted)
            * 3. A pawn that has moved, but cannot be taked by en-passant.
            */
            if (has_moved) {
                if (en_passantable) {
                    return 2;
                } else {
                    return 3;
                }
            } else {
                return 1;
            }
        }
    
        std::vector<std::pair<int, int>> moves() const {
            // Seems as good a time as any to mention that the board has X, Y the wrong way round. It's a consistent mistake so causes no errors but readability
            return {{forwards, 0}};
        }

        std::vector<std::pair<int, int>> takes() const {
            return {{forwards, -1}, {forwards, 1}};
        }

        std::vector<std::pair<std::pair<int, int>, int>> direction_moves() const {
            if (!has_moved) {
                return {{{forwards, 0}, 3}};
            }
            return {};
        }

        std::vector<std::pair<std::pair<int, int>, int>> direction_takes() const {
            return {};
        }
};

class Rook : public Piece {
    public:
        Rook(bool is_white) : Piece(is_white, 4) {
        }

        std::string name() const {
            return (colour_from_bool(is_white) + "Rook   ");
        }

        int as_int() const {
            /*
            * Rooks are another of the pieces that care if they have moved (for the purpose of castling)
            */
            if (has_moved) {
                return 4;
            } else {
                return 5;
            }
        }
        
        std::vector<std::pair<std::pair<int, int>, int>> direction_moves() const {
            return {{{1,0},10},{{0,1},10},{{-1,0},10},{{0,-1},10}};
            // The board is only 10 sqaures long so a limit of 10 is in practice limitless
        }
};

class King : public Piece {
    public:
        King(bool is_white) : Piece(is_white, 100) {}

        std::string name() const {
            return colour_from_bool(is_white) + "King   ";
        }

        int as_int() const {
            if (!has_moved) {
                return 6;
            }
            return 7;
        }

        std::vector<std::pair<int, int>> moves() const {
            return {{1, 1}, {1, 0}, {1, -1}, {0, 1}, {0, -1}, {-1, 1}, {-1, 0}, {-1, -1}};
        }
};

class Cleric : public Piece {
    public:
        Cleric(bool is_white) : Piece(is_white, 4) {}

        std::string name() const {
            return colour_from_bool(is_white) + "Cleric ";
        }

        int as_int() const {
            return 10;
        }

        std::vector<std::pair<int, int>> moves() const {
            // The cleric can move literally everywhere on the map, so this just adds each square to the 'moves'
            std::vector<std::pair<int, int>> moves = {};
            for (int row = -10; row < 10; row++) {
                for (int col = -10; col < 10; col ++) {
                    moves.push_back({row, col});
                }
            }
            return moves;
            // In theory this would be quicker if it contained a hard-coded value for each square. :shrug:
        }

        std::vector<pair<int, int>> takes() const {return {};} // Default behaviour is to copy the 'moves' function, so this replaces that

        std::vector<std::pair<std::pair<int, int>, int>> direction_takes() const {
            return {{{1, 1}, 10}, {{1, -1}, 10}, {{-1, 1}, 10}, {{-1, -1}, 10}};
        }
};

class Panda : public Piece {
    public:
        Panda(bool is_white) : Piece(is_white, 3) {}

        std::string name() const {
            return colour_from_bool(is_white) + "Panda  ";
        }

        int as_int() const {
            if (!immortal) {
                return 11;
            }
            return 12;
        }

        std::vector<std::pair<int, int>> moves() const {
            return {{1, 1}, {1, 0}, {1, -1}, {0, 1}, {0, -1}, {-1, 1}, {-1, 0}, {-1, -1}};
        }

        std::vector<std::pair<std::pair<int, int>, int>> direction_moves() const {
            return {{{1, 0}, 2}, {{0, 1}, 2}, {{0, -1}, 2}, {{-1, 0}, 2}};
        }

        std::vector<std::pair<std::pair<int, int>, int>> direction_takes() const {return {};}

        void take() {
            immortal = true;
        }

        void tick() {
            immortal = false;
        }

        // Take is applied after tick, so the panda stays immortal for a turn cycle after it takes
};

class Frog : public Piece {
    public:
        Frog(bool is_white) : Piece(is_white, 5) {}

        std::string name() const {
            return colour_from_bool(is_white) + "Frog   ";
        }

        int as_int() const {
            return 9;
        }

        std::vector<std::pair<int, int>> moves() const {
            return {{3, 0}, {2, 2}, {2, 0}, {2, -2}, {1, 1}, {1, 0}, {1, -1}, {0, 3}, {0, 2}, {0, 1}, {0, -1}, {0, -2}, {0, -3}, {-1, 1}, {-1, 0}, {-1, -1}, {-2, 2}, {-2, 0}, {-2, -2}, {-3, 0}};
        }
};

class Dog : public Piece {
    public:
        Dog(bool is_white) : Piece(is_white, 6) {}

         std::string name() const {
            return colour_from_bool(is_white) + "Dog    ";
        }

        int as_int() const {
            return 8;
        }

        std::vector<std::pair<int, int>> moves() const {
            return {{2, 1}, {2, -1}, {1, 2}, {1, -2}, {-1, 2}, {-1, -2}, {-2, 1}, {-2, -1}};
        }
};

class Chicken : public Piece {
    public:
        Chicken(bool is_white) : Piece(is_white, 4) {}

        // NOTE: The chicken's legal moves are calculated by a method in the ChessBoard class becauase of the complexities of the piece.

        std::string name() const {
            return colour_from_bool(is_white) + "Chicken";
        }

        int as_int() const {
            if (!has_moved) {
                return 13;
            }
            if (!immortal) {
                return 14;
            }
            return 15;
        }
};

class Egg : public Piece {
    public:
        Egg(bool is_white) : Piece(is_white, 3) {
            int time_until_hatch = 6;
        }

        std::string name() const {
            return colour_from_bool(is_white) + "Egg    ";
        }

        int as_int() const {
            return 15 + time_until_hatch;
        }
        
        void tick() {
            time_until_hatch--;
        }
};

class Blob0 : public Piece {
    public:
        Blob0(bool is_white) : Piece(is_white, 5) {}

        std::string name() const {
            return colour_from_bool(is_white) + "Blob0  ";
        }

        int as_int() const {
            return 22;
        }

        std::vector<std::pair<int, int>> moves() const {
            return {{1, 1}, {1, 0}, {1, -1}, {0, 1}, {0, -1}, {-1, 1}, {-1, 0}, {-1, -1}};
        } 

        std::vector<std::pair<std::pair<int, int>, int>> direction_moves() const {
            return {{{1, 0}, 2}, {{0, 1}, 2}, {{0, -1}, 2}, {{-1, 0}, 2}};
        }

        std::vector<std::pair<std::pair<int, int>, std::pair<int, int>>> dependant_moves() const {
            return {{{1, 1}, {2, 1}}, {{1, 1}, {1, 2}}, {{1, -1}, {2, -1}}, {{1, -1}, {1, -2}}, {{-1, 1}, {-1, 2}}, {{-1, 1}, {-2, 1}}, {{-1, -1}, {-1, -2}}, {{-1, -1}, {-2, -1}}};
        }
};

class Blob1 : public Piece {
    public:
        Blob1(bool is_white) : Piece(is_white, 3) {}

        std::string name() const {
            return colour_from_bool(is_white) + "Blob1  ";
        }

        int as_int() const {
            return 23;
        }

        std::vector<std::pair<std::pair<int, int>, int>> direction_moves() const {
            return {{{1, 0}, 2}, {{0, 1}, 2}, {{0, -1}, 2}, {{-1, 0}, 2}};
        }
};

class Blob2 : public Piece {
    public:
        Blob2(bool is_white) : Piece(is_white, 2) {}

        std::string name() const {
            return colour_from_bool(is_white) + "Blob2  ";
        }

        int as_int() const {
            return 24;
        }

        std::vector<std::pair<int, int>> moves() const {
            return {{1, 1}, {1, 0}, {1, -1}, {0, 1}, {0, -1}, {-1, 1}, {-1, 0}, {-1, -1}};
        }
};

class Blob3 : public Piece {
    public:
        Blob3(bool is_white) : Piece(is_white, 1) {}

        std::string name() const {
            return colour_from_bool(is_white) + "Blob3  ";
        }

        int as_int() const {
            return 25;
        }

        std::vector<std::pair<int, int>> moves() const {
            return {{1, 0}, {0, 1}, {0, -1}, {-1, 0}};
        }
};

class ChessBoard {
    public:
        array<array<Piece*, 10>, 10> squares; // Primary array containing the 'chessboard'
        Piece* forced_move; // When a piece such as the Dog takes then the board forces it to make another move
        bool white_to_move; // Tracks whose turn it is
        std::map<std::pair<int, int>, std::vector<std::pair<int, int>>> moves_map; // Tracks legal moves
        // For each position on the board, where can the piece in that position move to?

        ChessBoard() {
            for (int row = 0; row < 10; row++) {
                for (int col = 0; col < 10; col++) {
                    squares[row][col] = nullptr;
                }
            }
            forced_move = nullptr;
            white_to_move = true;
            std::map<std::pair<int, int>, std::vector<std::pair<int, int>>> moves_map;
        }

        ChessBoard* copy_board() const {
            /*
            * Creates a duplicate of the board for examining what future boards could do
            */
            ChessBoard* new_board = new ChessBoard();
            new_board -> set_board_state(this -> arr_board_state());
            new_board -> white_to_move = white_to_move;
            return new_board;
        }
        
        void set_board_state(std::string board_state) {
            if (board_state.length() != 100) {
                cout << "Out of Range Input for board state str";
                throw std::out_of_range("Board State String must be exactly 100 characters long, not " + board_state.length());
            }

            // Deletes every piece currently on the board
            for (int row = 0; row < 10; row++) {
                for (int col = 0; col < 10; col++) {
                    if (square_in_position({row, col}) != nullptr) {
                        delete squares[row][col]; // Apparently memory management is a real thing (?!?!?!?)
                        squares[row][col] = nullptr;
                    }
                }
            }

            int row =  0, col = 0;
            for (char current_char : board_state) {
                squares[row][col] = piece_from_char(current_char);
                if (col == 9) {
                    row++;
                    col = 0;
                } else {
                    col++;
                }
            }
        }

        void set_board_state(array<array<int, 10>, 10> board_state) {
            // Deletes every piece currently on the board
            for (int row = 0; row < 10; row++) {
                for (int col = 0; col < 10; col++) {
                    squares[row][col] = nullptr;
                }
            }

            // Iterates through the boardstate and adds the correct pieces based on the integer array
            for (int row = 0; row < 10; row ++) {
                for (int col = 0; col < 10; col++) {
                    int current_int = board_state[row][col];
                    squares[row][col] = piece_from_int(current_int);
                }
            }
        }
        
        std::string board_state() const {
            std::string board_state_str = "";
            for (array<Piece*, 10> row : squares) {
                for (Piece* square : row) {
                    board_state_str += char_from_piece(square);
                }
            }
            return board_state_str;
        }
        
        array<array<int, 10>, 10> arr_board_state() const {
            array<array<int, 10>, 10> state_array = {};
            for (int row = 0; row < 10; row++) {
                for (int col = 0; col < 10; col++) {
                    if (squares[row][col] == nullptr) {
                        state_array[row][col] = 0;
                        continue;
                    }
                    Piece* current_piece = square_in_position({row, col});
                    if (current_piece == nullptr) {
                        state_array[row][col] = 0;
                    } else {
                        state_array[row][col] = flip_ints(current_piece -> as_int(), current_piece -> is_white);
                    }
                }
            }
            return state_array;
        } 
        
        static Piece* piece_from_char(char current_char) {
            if (isspace(current_char) != 0) {return nullptr;}
            char lower = std::tolower(current_char);
            bool is_white = false;
            if (islower(current_char) != 0) {
                is_white = true;
            }
            if (lower == 'k') {return new King(is_white);}
            else if (current_char == '(' || current_char == ')') {
                Piece* king = new King(current_char == '(');
                king -> has_moved = true;
                return king;
            }
            else if (lower == 'p') {return new Pawn(is_white);}
            else if (current_char == '/' || current_char == '?') {
                Piece* pawn = new Pawn(current_char == '/');
                pawn -> has_moved = true;
                return pawn;
            }
            else if (lower == 'e') {
                Piece* pawn = new Pawn(is_white);
                pawn -> has_moved = true;
                pawn -> en_passantable = true;
                return pawn;
            }
            else if (lower == 'r') {return new Rook(is_white);}
            else if (lower == 'm') {
                Piece* rook = new Rook(is_white);
                rook -> has_moved = true;
                return rook;
            }
            else if (lower == 'c') {return new Cleric(is_white);}
            else if (lower == 'd') {return new Dog(is_white);}
            else if (lower == 'f') {return new Frog(is_white);}
            else if (lower == 'a') {return new Panda(is_white);}
            else if (lower == 'i') {
                Piece* panda_ptr = new Pawn(is_white);
                panda_ptr -> immortal = true;
                return panda_ptr;
                }
            else if (lower == 'h') {return new Chicken(is_white);}
            else if (lower == 'o') {
                Piece* chicken_ptr = new Chicken(is_white);
                chicken_ptr -> has_moved = true;
                return chicken_ptr;
            }
            else if (lower == 'z') {return new Blob0(is_white);}
            else if (lower == 'x') {return new Blob1(is_white);}
            else if (lower == 'v') {return new Blob2(is_white);}
            else if (lower == 'j') {return new Blob3(is_white);}
            else if (char_in_str("654321^%$|\"!", current_char)) {
                bool white;
                int hatch_time;
                if (char_in_str("654321", current_char)) {
                    white = true;
                    hatch_time = int(current_char);
                } else {
                    white = false;
                    if (current_char == '^') {
                        hatch_time = 6;
                    } else if (current_char == '%') {
                        hatch_time = 5;
                    } else if (current_char == '$') {
                        hatch_time = 4;
                    } else if (current_char == '|') {
                        hatch_time = 3;
                    } else if (current_char == '\"') {
                        hatch_time = 2;
                    } else if (current_char == '!') {
                        hatch_time = 1;
                    }
                }
                Piece* egg = new Egg(white);
                egg -> time_until_hatch = hatch_time;
                return egg;
            }
            else {
                cout << "An invalid character was entered: " << current_char << "/n";
                return nullptr;
            }
        }

        static Piece* piece_from_int(int num) {
            bool is_white = num > 0;
            num = abs(num);
            if (num == 0) {
                return nullptr;
            }
            else if (num == 1) {
                return new Pawn(is_white);
            }    
            else if (num == 2) {
                Piece* pawn = new Pawn(is_white);
                pawn -> en_passantable = true;
                pawn -> has_moved = true;
                return pawn;
            }    
            else if (num == 3) {
                Piece* moved_pawn = new Pawn(is_white);
                moved_pawn -> has_moved = true;
                return moved_pawn;
            }    
            else if (num == 4) {
                return new Rook(is_white);
            }    
            else if (num == 5) {
                Piece* rook = new Rook(is_white);
                rook -> has_moved = true;
                return rook;
            }    
            else if (num == 6) {
                return new King(is_white);
            }    
            else if (num == 7) {
                Piece* king = new King(is_white);
                king -> has_moved = true;
                return king;
            }    
            else if (num == 8) {
                return new Dog(is_white);
            }    
            else if (num == 9) {
                return new Frog(is_white);
            }    
            else if (num == 10) {
                return new Cleric(is_white);
            }    
            else if (num == 11) {
                return new Panda(is_white);
            }    
            else if (num == 12) {
                Piece* panda = new Panda(is_white);
                panda -> immortal = true;
                return panda;
            }    
            else if (num == 13) {
                return new Chicken(is_white);
            }    
            else if (num == 14) {
                Piece* chicken = new Chicken(is_white);
                chicken -> has_moved = true;
                return chicken;
            }    
            else if (num == 15) {
                Piece* immortal_chicken = new Chicken(is_white);
                immortal_chicken -> has_moved = true;
                immortal_chicken -> immortal = true;
                return immortal_chicken;
            }    
            else if (16 <= num && num <= 21) {
                Piece* egg = new Egg(is_white);
                egg -> time_until_hatch = 22 - num;
                return egg;
            }   
            else if (num == 22) {
                return new Blob0(is_white);
            }    
            else if (num == 23) {
                return new Blob1(is_white);
            }    
            else if (num == 24) {
                return new Blob2(is_white);
            }    
            else if (num == 25) {
                return new Blob3(is_white);
            }    
            else {
                cout << "Invalid int) { " << num << "\n";
                return nullptr;
            }
            
        }
        
        static char char_from_piece(Piece* current_piece) {
            std::string piece_name = current_piece -> name().substr(5);
            char return_char;
            if (current_piece == nullptr) {return ' ';}
            else if (piece_name == "King   ") {return_char = 'k';} // TODO The king has another character for if it has moved.
            else if (piece_name == "Pawn   ") {
                if (!current_piece -> has_moved) {
                    return_char = 'p';
                } else if (current_piece -> en_passantable) {
                    return_char = 'e';
                } else {
                    if (current_piece -> is_white) {
                        return '/';
                    }
                    return '?';
                }
            }
            else if (piece_name == "Rook   ") {return_char = 'r';} // TODO The rook has another character for if it has moved.
            else if (piece_name == "Cleric ") {return_char = 'c';}
            else if (piece_name == "Dog    ") {return_char = 'd';}
            else if (piece_name == "Frog   ") {return_char = 'f';}
            else if (piece_name == "Panda  ") {
                if (current_piece -> immortal) {
                    return_char = 'i';
                } else {
                    return_char = 'a';
                }
            }
            else if (piece_name == "Chicken") {
                if (current_piece -> has_moved) {
                    return_char = 'h';
                } else {
                    return_char = 'o';
                }
            }
            else if (piece_name == "Blob0  ") {return_char = 'z';}
            else if (piece_name == "Blob1  ") {return_char = 'x';}
            else if (piece_name == "Blob2  ") {return_char = 'v';}
            else if (piece_name == "Blob3  ") {return_char = 'j';}
            else if (piece_name == "Egg    ") {
                array<char, 6> char_options;
                if (current_piece -> is_white) {
                    char_options = {'6', '5', '4', '3', '2', '1'};
                } else {
                    char_options = {'^', '%', '$', '|', '"', '!'};
                }
                return char_options[current_piece -> time_until_hatch];
            }
            else {
                cout << "An invalid piece exists: " << current_piece -> name() << "/n";
                return ' ';
            }
            if (!current_piece->is_white) {
                return_char = std::toupper(return_char);
            }
            return return_char;
        }
        
        static Piece* piece_for_promotion(std::pair<int, int> position) {
            int row = position.first, col = position.second;
            bool is_white;
            if (row == 0) {
                is_white = true;
            } else if (row == 9) {
                is_white = false;
            } else {
                throw std::out_of_range("Promotion position must be on the first or last file\n");
            }
            if (col == 0 || col == 9) {
                Piece* rook = new Rook(is_white);
                rook -> has_moved = true;
                return rook;
            } else if (col == 1 || col == 8) {
                return new Dog(is_white);
            } else if (col == 2) {
                Piece* chick = new Chicken(is_white);
                chick -> has_moved = true;
                return chick;
            } else if (col == 3) {
                return new Blob0(is_white);
            } else if (col == 4 || col == 5) {
                return new Panda(is_white);
            } else if (col == 6) {
                return new Cleric(is_white);
            } else if (col == 7) {
                return new Frog(is_white);
            }
            return nullptr;
        }
        
        Piece* square_in_position(std::pair<int, int> position) const {
            if (!is_valid_position(position)) {
                return nullptr;
            }
            return squares[position.first][position.second];
        }

        static bool is_valid_position(std::pair<int, int> position) {
            return 0 <= position.first && 9 >= position.first && 0 <= position.second && 9 >= position.second;
        }
        
        void print_board() const {
            for (array row : squares) { 
                std::string row_str = "";
                for (Piece* piece_ptr : row) { 
                    if (piece_ptr == nullptr) {
                        row_str += "|            |";
                    }
                    else {
                        row_str += "|" + piece_ptr -> name() + "|";
                    }
                }
                cout << "____________________________________________________________________________________________________________________________________________\n";
                cout << row_str << "\n";
            }
            cout << "____________________________________________________________________________________________________________________________________________\n" << endl;
        }

        void place_piece(Piece* piece_ptr, std::pair<int, int> position) {
            if (square_in_position(position) == nullptr) {
                squares[position.first][position.second] = piece_ptr;
            }
        }

        void remove_piece(std::pair<int, int> position) {
            delete squares[position.first][position.second];
            squares[position.first][position.second] = nullptr;
        }

        void tick_all_pieces() {
            for (std::array<Piece*, 10> row : squares) {
                for (Piece* piece : row) {
                    if (piece != nullptr) {
                        piece -> tick();
                        if (piece -> time_until_hatch == 0) {
                            std::pair<int, int> piece_position = find_piece(piece);
                            bool is_white = piece -> is_white;
                            delete piece;
                            piece = nullptr;
                            squares[piece_position.first][piece_position.second] = new Chicken(is_white);
                        }
                    }
                }
            }
        }
        
        void change_turn() {
            white_to_move = !(white_to_move);
        }
        
        std::pair<int, int> find_piece(Piece* piece) const {
            return {-1, -1};
            // I am a stupid stupid man and spent 2 hours trying to find the bug in the very complex would_check_self function only to discover that apparently this piece of shit isnt working for whatever reason.
            // I blame pointers
            for (int row = 0; row < 10; row++) {
                for (int col = 0; col < 10; col++) {
                    if (squares[row][col] == piece) {
                        return {row, col};
                    }
                }
            } 
            return {-1, -1};
            // I am a dumb dumb man and don't know how to properly indicate the lack of the piece without returning this stupid pair

            // This 1 very simple function has caused me so much pain.
        }
        
        std::vector<std::pair<int, int>> piece_positions_relative(std::vector<std::pair<int, int>> piece_positions, std::pair<int, int> position_of_piece) const {
            std::vector<std::pair<int, int>> moves = {};
            for (std::pair<int, int> pos: piece_positions) {
                std::pair<int, int> new_position = {pos.first + position_of_piece.first, pos.second + position_of_piece.second};
                if (is_valid_position(new_position)) {
                    moves.push_back({new_position});
                }
            }
            return moves;
        }

        std::vector<std::pair<int, int>> moves_from_position(std::pair<int, int> position, bool check_colour) const {
            Piece* target_piece = square_in_position(position);
            if (target_piece == nullptr || (target_piece -> is_white != white_to_move && check_colour)) {
                return {};
            }

            if (target_piece -> name().substr(5) == "Chicken") {
                return chicken_moves(position);
            }
            
            // Standard Moves
            std::vector<std::pair<int, int>> moves = {};

            std::vector<std::pair<int, int>> available_moves = piece_positions_relative(target_piece -> moves(), position);
            for (std::pair<int, int> move : available_moves) {
                if (square_in_position(move) == nullptr && is_valid_position(move)) {
                    moves.push_back(move);
                }
            }

            // Sliding Moves
            for (std::pair<std::pair<int, int>, int> direction_limit : target_piece -> direction_moves()) {
                std::pair<int, int> direction = direction_limit.first;
                int limit = direction_limit.second;
                for (int i = 1; i <= limit; i++) {
                    std::pair<int, int> next_position = {position.first + (direction.first * i), position.second + (direction.second * i)};
                    if (square_in_position(next_position) != nullptr || !is_valid_position(next_position)) {
                        break;
                    } else {
                        moves.push_back(next_position);
                    }
                }
            }

            // Dependant Moves
            for (std::pair<std::pair<int, int>, std::pair<int, int>> dependancy_position : target_piece -> dependant_moves()) {
                std::vector<std::pair<int, int>> relatives = piece_positions_relative({dependancy_position.first, dependancy_position.second}, position);
                if (relatives.size() != 2) {
                    continue;
                }
                Piece* dependancy = square_in_position(relatives[0]);
                Piece* position_dependant = square_in_position(relatives[1]);
                if (dependancy == nullptr && position_dependant != nullptr && position_dependant -> is_white != target_piece -> is_white) {
                    moves.push_back(relatives[1]);
                }
            }
            return moves;
        }

        std::vector<std::pair<int, int>> takes_from_position(std::pair<int, int> position, bool check_colour) const {
            Piece* target_piece = square_in_position(position);
            if (target_piece == nullptr || (target_piece -> is_white != white_to_move && check_colour)) {
                return {};
            }

            
            if (target_piece -> name().substr(5) == "Chicken") {
                return chicken_takes(position);
            }
            
            // Standard Takes
            std::vector<std::pair<int, int>> takes = {};
            std::vector<std::pair<int, int>> available_takes = piece_positions_relative(target_piece -> takes(), position);
            for (std::pair<int, int> take : available_takes) {
                Piece* take_piece = square_in_position(take);
                if (take_piece != nullptr && take_piece -> is_white != target_piece -> is_white) {
                    takes.push_back(take);
                }
            }

            // Sliding Takes
            for (std::pair<std::pair<int, int>, int> direction_limit : target_piece -> direction_takes()) {
                std::pair<int, int> direction = direction_limit.first;
                int limit = direction_limit.second;
                for (int i = 1; i <= limit; i++) {
                    std::pair<int, int> next_position = {position.first + (direction.first * i), position.second + (direction.second * i)};
                    Piece* next_piece = square_in_position(next_position);
                    if (next_piece != nullptr) {
                        if (next_piece -> is_white != target_piece -> is_white && !next_piece -> immortal) {
                            takes.push_back(next_position);
                        } 
                    break;
                    }
                }
            }

            // Dependant Takes
            for (std::pair<std::pair<int, int>, std::pair<int, int>> dependancy_position : target_piece -> dependant_takes()) {
                std::vector<std::pair<int, int>> relatives = piece_positions_relative({dependancy_position.first, dependancy_position.second}, position);
                if (relatives.size() != 2) {
                    continue;
                }
                std::pair<int, int> dependancy = relatives[0];
                std::pair<int, int> position_dependant = relatives[1];
                if (square_in_position(dependancy) == nullptr && square_in_position(position_dependant) != nullptr && square_in_position(position_dependant) -> is_white != target_piece -> is_white) {
                    takes.push_back(position_dependant);
                }
            }
            
            return takes;
        }

        std::vector<std::pair<int, int>> adjacent_positions(std::pair<int, int> position, std::vector<std::pair<int, int>> discovered) const {
            if (square_in_position(position) == nullptr) {
                return {};
            }

            if (square_in_position(position) -> name().substr(5) != "Chicken") {
                return {{position}};
            }
            discovered.push_back(position);

            // Get relative positions of all pieces surrounding the position and iterate through them
            for (std::pair<int, int> adjacent_position : piece_positions_relative({{1, 1}, {1, 0}, {1, -1}, {0, 1}, {0, -1}, {-1, 1}, {-1, 0}, {-1, -1}}, position)) {
                // If the position has not already been discovered, recurse the function on the newly discovered piece
                if (std::find(discovered.begin(), discovered.end(), adjacent_position) == discovered.end() && square_in_position(adjacent_position) != nullptr) {
                    std::vector<std::pair<int, int>> newly_discovered = adjacent_positions(adjacent_position, discovered);
                    discovered.reserve(discovered.size() + newly_discovered.size());
                    discovered.insert(discovered.end(), newly_discovered.begin(), newly_discovered.end());
                }
            }
            return discovered;
        }

        std::vector<std::pair<int, int>> chicken_moves(std::pair<int, int> position) const {
            Piece* piece = square_in_position(position);
            if (piece == nullptr || piece -> name().substr(5) != "Chicken") {
                return {};
            }
            std::vector<std::string> piece_names = {};
            for (std::pair<int, int> current_position : adjacent_positions(position, {})) {
                Piece* current_piece = square_in_position(current_position);
                if (square_in_position(current_position) != nullptr) {
                    piece_names.push_back(current_piece -> name().substr(5));
                }
            }

            std::vector<std::string>::iterator last = std::unique(piece_names.begin(), piece_names.end());
            piece_names.erase(last, piece_names.end());

            Piece* chicken = square_in_position(position);
            bool is_white = chicken -> is_white;
            std::vector<std::pair<int, int>> moves = {};
            Piece* new_piece = nullptr;

            for (std::string piece_name : piece_names) {
                if (piece_name == "Pawn   ") {
                    new_piece = new Pawn(is_white);
                    new_piece -> has_moved = chicken -> has_moved;
                } else if (piece_name == "Rook   ") {
                    new_piece = new Rook(is_white);
                } else if (piece_name == "King   ") {
                    new_piece = new King(is_white);
                } else if (piece_name == "Dog    ") {
                    new_piece = new Dog(is_white);
                } else if (piece_name == "Frog   ") {
                    new_piece = new Frog(is_white);
                } else if (piece_name == "Cleric ") {
                    new_piece = new Cleric(is_white);
                } else if (piece_name == "Panda  ") {
                    new_piece = new Panda(is_white);
                } else if (piece_name == "Blob0  ") {
                    new_piece = new Blob0(is_white);
                } else if (piece_name == "Blob1  ") {
                    new_piece = new Blob1(is_white);
                } else if (piece_name == "Blob2  ") {
                    new_piece = new Blob2(is_white);
                } else if (piece_name == "Blob3  ") {
                    new_piece = new Blob3(is_white);
                } else if (piece_name == "Chicken") {
                    continue;
                } else if (piece_name == "Egg    ") {
                    continue;
                } else {
                    cout << "ERROR - " << piece_name << " is unexpected Piece Type. \n";
                    cout << "(" << piece_name.length() << ")\n";
                    Piece* new_piece = nullptr;
                }
                if (new_piece == nullptr) {
                    cout << "new_piece == nullptr\n";
                }

                ChessBoard* new_board = copy_board();
                new_board -> squares[position.first][position.second] = new_piece;

                std::vector<std::pair<int, int>> piece_moves = new_board -> moves_from_position(position, false);
                moves.reserve(moves.size() + piece_moves.size());
                moves.insert(moves.end(), piece_moves.begin(), piece_moves.end());
                delete new_piece;
                delete new_board;
                new_piece = nullptr;
                new_board = nullptr;
            }

            std::sort(moves.begin(), moves.end());
            moves.erase(std::unique(moves.begin(), moves.end()), moves.end());
            
            return moves;
        }

        std::vector<std::pair<int, int>> chicken_takes(std::pair<int, int> position) const {
            Piece* piece = square_in_position(position);
            if (piece == nullptr || piece -> name().substr(5) != "Chicken") {
                return {};
            }
            
            std::vector<std::string> piece_names = {};

            for (std::pair<int, int> current_position : adjacent_positions(position, {})) {
                Piece* current_piece = square_in_position(current_position);
                if (square_in_position(current_position) != nullptr) {
                    piece_names.push_back(current_piece -> name().substr(5));
                }
            }

            std::vector<std::string>::iterator last = std::unique(piece_names.begin(), piece_names.end());
            piece_names.erase(last, piece_names.end());

            Piece* chicken = square_in_position(position);
            bool is_white = chicken -> is_white;
            std::vector<std::pair<int, int>> takes = {};
            Piece* new_piece = nullptr;

            for (std::string piece_name : piece_names) {
                if (piece_name == "Pawn   ") {
                    new_piece = new Pawn(is_white);
                    new_piece -> has_moved = chicken -> has_moved;
                } else if (piece_name == "Rook   ") {
                    new_piece = new Rook(is_white);
                } else if (piece_name == "King   ") {
                    new_piece = new King(is_white);
                } else if (piece_name == "Dog    ") {
                    new_piece = new Dog(is_white);
                } else if (piece_name == "Frog   ") {
                    new_piece = new Frog(is_white);
                } else if (piece_name == "Cleric ") {
                    new_piece = new Cleric(is_white);
                } else if (piece_name == "Panda  ") {
                    new_piece = new Panda(is_white);
                } else if (piece_name == "Blob0  ") {
                    new_piece = new Blob0(is_white);
                } else if (piece_name == "Blob1  ") {
                    new_piece = new Blob1(is_white);
                } else if (piece_name == "Blob2  ") {
                    new_piece = new Blob2(is_white);
                } else if (piece_name == "Blob3  ") {
                    new_piece = new Blob3(is_white);
                } else if (piece_name == "Chicken") {
                    continue;
                } else if (piece_name == "Egg    ") {
                    continue;
                } else {
                    cout << "ERROR - " << piece_name << " is unexpected Piece Type. \n";
                    cout << "(" << piece_name.length() << ")\n";
                    Piece* new_piece = nullptr;
                }
                if (new_piece == nullptr) {
                    cout << "new_piece == nullptr\n";
                }

                ChessBoard* new_board = copy_board();
                new_board -> squares[position.first][position.second] = new_piece;

                std::vector<std::pair<int, int>> piece_takes = new_board -> takes_from_position(position, false);
                takes.reserve(takes.size() + piece_takes.size());
                takes.insert(takes.end(), piece_takes.begin(), piece_takes.end());
                delete new_piece;
                delete new_board;
            }

            std::sort(takes.begin(), takes.end());
            takes.erase(std::unique(takes.begin(), takes.end()), takes.end());
            
            return takes;
        }

        std::vector<std::pair<int, int>> castle_moves(std::pair<int, int> position) const {
            if (square_in_position(position) == nullptr || square_in_position(position) -> name().substr(5, 4) != "King" || is_check(true)) {
                return {};
            }
            Piece* target_king = square_in_position(position);
            std::pair<int, int> start_pos;
            if (target_king -> is_white) {
                start_pos = {9, 5};
            } else {
                start_pos = {0, 5};
            }
            
            if (position != start_pos) {
                return {};
            }
            stdd:vector<std::pair<int, int>> moves = {};

            // Check kingside castling
            Piece* potential_rook = square_in_position({position.first, 9});
            if (potential_rook != nullptr && potential_rook -> name().substr(5,4) == "Rook" && !potential_rook -> has_moved) {
                std::vector<std::pair<int, int>> in_between_spaces = {{position.first, 8}, {position.first, 7}, {position.first, 6}};
                bool can_castle = true;
                for (std::pair<int, int> space : in_between_spaces) {
                    if (square_in_position(space) != nullptr) {
                        can_castle = false;
                    }
                }
                if (!would_check_self({position, {position.first, 6}}) && can_castle) {
                    moves.push_back({position.first, 7});
                }
            }

            // Check pandaside castling
            potential_rook = square_in_position({position.first, 0});
            if (potential_rook != nullptr && potential_rook -> name().substr(5,4) == "Rook" && !potential_rook -> has_moved) {
                std::vector<std::pair<int, int>> in_between_spaces = {{position.first, 1}, {position.first, 2}, {position.first, 3}, {position.first, 4}};
                bool can_castle = true;
                for (std::pair<int, int> space : in_between_spaces) {
                    if (square_in_position(space) != nullptr) {
                        can_castle = false;
                    }
                }
                if (!would_check_self({position, {position.first, 4}}) && can_castle) {
                    moves.push_back({position.first, 3});
                }
            }

            return moves;
        }

        std::vector<std::pair<int, int>> en_passant_moves(std::pair<int, int> position) const {
            if (square_in_position(position) == nullptr || !(square_in_position(position) -> name().substr(5, 4) == "Pawn" || square_in_position(position) -> name().substr(5) == "Chicken")) {
                return {};
            }
            if (square_in_position(position) -> name().substr(5) == "Chicken") {
                std::vector<std::string> piece_names = {};
                bool found_pawn = false;
                for (std::pair<int, int> adj_pos : adjacent_positions(position, {})) {
                    if (square_in_position(adj_pos) != nullptr && square_in_position(adj_pos) -> name().substr(5, 4) == "Pawn") {
                        found_pawn = true;
                    }
                }
                if (!found_pawn) {
                    return {};
                }
            }
            std::vector<std::pair<int, int>> moves = {};
            if (square_in_position(position) -> is_white) {
                if (position.first != 3 && position.first != 4) {
                    return {};
                }
                if (position.first == 3) {
                    for (std::pair<int, int> potential_position : piece_positions_relative({{1, 1}, {1, -1}, {0, 1}, {0, -1}}, position)) {
                        if (square_in_position(potential_position) != nullptr && square_in_position(potential_position) -> is_white != square_in_position(position) -> is_white && square_in_position(potential_position) -> en_passantable) {
                            moves.push_back({2, potential_position.second});
                        }
                    }
                } else {
                    for (std::pair<int, int> potential_position : piece_positions_relative({{1, 1}, {1, -1}}, position)) {
                        if (square_in_position(potential_position) != nullptr && square_in_position(potential_position) -> is_white != square_in_position(position) -> is_white && square_in_position(potential_position) -> en_passantable) {
                            moves.push_back({3, potential_position.second});
                        }
                    }
                }
            } else {
                if (position.first != 6 && position.first != 5) {
                    return {};
                }
                if (position.first == 6) {
                    for (std::pair<int, int> potential_position : piece_positions_relative({{1, 1}, {1, -1}, {0, 1}, {0, -1}}, position)) {
                        if (square_in_position(potential_position) != nullptr && square_in_position(potential_position) -> is_white != square_in_position(position) -> is_white && square_in_position(potential_position) -> en_passantable) {
                            moves.push_back({7, potential_position.second});
                        }
                    }
                } else {
                    for (std::pair<int, int> potential_position : piece_positions_relative({{1, 1}, {1, -1}}, position)) {
                        if (square_in_position(potential_position) != nullptr && square_in_position(potential_position) -> is_white != square_in_position(position) -> is_white && square_in_position(potential_position) -> en_passantable) {
                            moves.push_back({6, potential_position.second});
                        }
                    }
                }
            }
            return moves;
        }
        
        std::vector<std::pair<int, int>> legal_moves(std::pair<int, int> position, bool prevent_checks) {
            auto it = moves_map.find(position);

            if (it != moves_map.end()) {
                return it->second;
            }

            if (square_in_position(position) == nullptr || (forced_move != nullptr && forced_move != square_in_position(position)) || square_in_position(position) -> is_white != white_to_move) {
                return {};
            }
            std::vector<std::pair<int, int>> moves = moves_from_position(position, true), takes = takes_from_position(position, true), castles = castle_moves(position), en_passants = en_passant_moves(position);

            moves.reserve(moves.size() + takes.size() + castles.size() + en_passants.size());
            moves.insert(moves.end(), takes.begin(), takes.end());
            moves.insert(moves.end(), castles.begin(), castles.end());
            moves.insert(moves.end(), en_passants.begin(), en_passants.end());

            std::sort(moves.begin(), moves.end());
            moves.erase(std::unique(moves.begin(), moves.end()), moves.end());

            if (!prevent_checks) {
                return moves;
            }

            std::vector<std::pair<int, int>> non_check_moves = {};

            for (std::pair<int, int> move : moves) {
                if (!would_check_self({position, move})) {
                    std::string checked_player;
                    if (white_to_move) {
                        checked_player = "White";
                    } else {
                        checked_player = "Black";
                    }
                    non_check_moves.push_back(move);
                }
            }
            
            moves_map.insert(std::make_pair(position, non_check_moves));

            return non_check_moves;
        }
    
        std::vector<std::pair<int, int>> moveable_squares(bool check_colour) const {
            std::vector<std::pair<int, int>> sqrs = {};
            for (int row = 0; row < 10; row++) {
                for (int col = 0; col < 10; col++) {
                    std::vector<std::pair<int, int>> moves = moves_from_position({row, col}, check_colour);
                    sqrs.reserve(sqrs.size() + moves.size());
                    sqrs.insert(sqrs.end(), moves.begin(), moves.end());
                    }
                }
            return sqrs;
        }
        
        std::vector<std::pair<int, int>> takeable_squares(bool check_colour) const {
            std::vector<std::pair<int, int>> sqrs = {};
            for (int row = 0; row < 10; row++) {
                for (int col = 0; col < 10; col++) {
                    std::vector<std::pair<int, int>> takes = takes_from_position({row, col}, check_colour);
                    sqrs.reserve(sqrs.size() + takes.size());
                    sqrs.insert(sqrs.end(), takes.begin(), takes.end());
                    }
                }
            return sqrs;
        }
        
        void move_piece(std::pair<int, int> start_position, std::pair<int, int> end_position) {
            Piece* start_piece = square_in_position(start_position);
            Piece* end_piece = square_in_position(end_position);

            if (start_piece == nullptr) {
                throw std::invalid_argument("That Piece does not exist");
            }

            bool take = false;
            if (position_in_vector(en_passant_moves(start_position), end_position)) {
                int backwards = -1;
                if (start_piece -> is_white) {
                    backwards = 1;
                }
                if (square_in_position({end_position.first + backwards, end_position.second}) != nullptr) {
                    delete square_in_position({end_position.first + backwards, end_position.second});
                    squares[end_position.first + backwards][end_position.second] = nullptr;
                } else if (square_in_position({end_position.first + (2 * backwards), end_position.second}) != nullptr) {
                    delete square_in_position({end_position.first + (2 * backwards), end_position.second});
                    squares[end_position.first + (2 * backwards)][end_position.second] = nullptr;
                }
                take = true;
            }
            
            if (position_in_vector(takes_from_position(start_position, true), end_position)) {
                take = true;
            }

            tick_all_pieces();

            std::vector<std::string> adjacent_names = {};
            if (start_piece -> name().substr(5) == "Chicken") {
                    for (std::pair<int, int> position : adjacent_positions(start_position, {})) {
                        adjacent_names.push_back(square_in_position(position) -> name().substr(5));
                    }
                }
            
            if (square_in_position(start_position) -> name().substr(5,4) == "Pawn" && (end_position.first == 0 || end_position.first == 9)) {
                delete start_piece;
                squares[start_position.first][start_position.second] = piece_for_promotion(end_position);               
            } else if (take) {
                start_piece -> take();
                if (pieces_in_vector(adjacent_names, {"Panda  "})) {
                    start_piece -> immortal = true;
                }
                if (start_piece -> name().substr(5, 3) == "Dog" || pieces_in_vector(adjacent_names, {"Dog    "})) {
                    if (forced_move == nullptr) {
                        forced_move = start_piece;
                    } else {
                        forced_move = nullptr;
                    }
                }
                if (start_piece -> name().substr(5, 4) == "Blob" || pieces_in_vector(adjacent_names, {"Blob0  ", "Blob1  ", "Blob2  "})) {
                    bool white = start_piece -> is_white;
                    if (start_piece -> name().substr(5) == "Chicken") {
                        Piece* new_egg = new Egg(white);
                        squares[start_position.first][start_position.second] = new_egg;
                    } else if (start_piece -> name().substr(9, 1) == "0") {
                        squares[start_position.first][start_position.second] = new Blob1(white);
                        squares[end_position.first][end_position.second] = new Blob1(white);
                        delete start_piece;
                    } else if (start_piece -> name().substr(9, 1) == "1") {
                        squares[start_position.first][start_position.second] = new Blob2(white);
                        squares[end_position.first][end_position.second] = new Blob2(white);
                        delete start_piece;
                    }  else if (start_piece -> name().substr(9, 1) == "2") {
                        squares[start_position.first][start_position.second] = new Blob3(white);
                        squares[end_position.first][end_position.second] = new Blob3(white);
                        delete start_piece;
                    }
                } else {
                    squares[end_position.first][end_position.second] = start_piece;
                    squares[start_position.first][start_position.second] = nullptr;
                } 
            } else {
                forced_move = nullptr;
                if (position_in_vector(castle_moves(start_position), end_position)) {
                    std::pair<int, int> rook_start, rook_end;
                    if (end_position.second == 7) {
                        rook_start = {end_position.first, 9};
                        rook_end = {end_position.first, 6};
                    } else {
                        rook_start = {end_position.first, 0};
                        rook_end = {end_position.first, 4};
                    }
                    start_piece -> move();
                    square_in_position(rook_start) -> move();
                    squares[rook_end.first][rook_end.second] = squares[rook_start.first][rook_start.second];
                    squares[rook_start.first][rook_start.second] = nullptr;

                } else {
                    start_piece -> move();
                    squares[end_position.first][end_position.second] = start_piece;
                    squares[start_position.first][start_position.second] = nullptr;
                }
            }
            
            if (forced_move == nullptr) {
                change_turn();
            }
            moves_map.clear();
        }
    
        bool is_check(bool check_doubles) const {
            // Find the position of the king who may be in check
            std::pair<int, int> king_position = {-1, -1};
            for (int row = 0; row < 10; row++) {
                for (int col = 0; col < 10; col++) {
                    Piece* square = square_in_position({row, col});
                    if (square != nullptr && square -> is_white == this -> white_to_move && square -> name().substr(5, 4) == "King") {
                        king_position = {row, col};
                        break;
                    }
                }
            }

            if (king_position == std::make_pair(-1, -1)) {
                return true;
            }

            std::vector<std::pair<int, int>> take_squares = takeable_squares(false);

            // Check to see if any pieces can take the square that the king is in
            if (position_in_vector(take_squares, king_position)) {
                return true;
            }

            // Continue, now looking at double moving pieces
            if (!check_doubles) {
                return false;
            }

            for (std::pair<int, int> pos : double_hop_starting_positions()) {
                std::vector<std::pair<int, int>> takes = takes_from_position(pos, false);
                Piece* piece = square_in_position(pos);
                for (std::pair<int, int> take : takes) {
                    // Creates a new ChessBoard object and runs the move on that object, then checks to see if there is check afterwards
                    // This is definitely not the best way to do it but it's very easy to be honest
                    // So that's what I'm going with
                    ChessBoard* new_board = copy_board();
                    new_board -> move_piece(pos, take);
                    std::vector<std::pair<int, int>> additional_takes = new_board -> takes_from_position(take, true);
                    delete new_board;
                    new_board = nullptr;
                    if (position_in_vector(additional_takes, king_position)) {
                        return true;
                    }
                }

            }
            return false;
        }
    
        bool is_checkmate() {
            if (is_check(true) && all_legal_moves().size() == 0) {
                return true;
            } 
            return false;
        }

        bool would_check_self(std::pair<std::pair<int, int>, std::pair<int, int>> move) const {
            std::pair<int, int> starting_position = move.first, ending_position = move.second;
            if (square_in_position(ending_position) != nullptr && square_in_position(ending_position) -> name().substr(5, 4) == "King" && square_in_position(ending_position) -> is_white != square_in_position(starting_position) -> is_white) {
                return false;
            }
            if (position_in_vector(double_hop_starting_positions(), starting_position) && position_in_vector(takes_from_position(starting_position, false), ending_position)) {
                ChessBoard* new_board = copy_board();
                new_board -> move_piece(starting_position, ending_position);
                bool inevitable_check = true;
                for (std::pair<int, int> legal_move : new_board -> legal_moves(ending_position, false)) {
                    ChessBoard* newer_board = new_board -> copy_board();
                    newer_board -> move_piece(ending_position, legal_move);
                    newer_board -> change_turn();
                    bool check = newer_board -> is_check(false);
                    delete newer_board;
                    newer_board = nullptr;
                    if (!check) {
                        inevitable_check = false;
                    }
                }
                delete new_board;
                new_board = nullptr;
                return inevitable_check;
            }
            ChessBoard* new_board = copy_board();
            new_board -> move_piece(starting_position, ending_position);
            new_board -> change_turn();
            bool check = new_board -> is_check(true);
            delete new_board;
            new_board = nullptr;
            return check;
        }
        
        std::vector<std::pair<int, int>> double_hop_starting_positions() const {
            std::vector<std::pair<int, int>> return_vec = {};
            for (int row = 0; row < 10; row++) {
                for (int col = 0; col < 10; col++) {
                    Piece* square = square_in_position({row, col});
                    if (square != nullptr) {
                        if (square -> name().substr(5) == "Chicken") {
                            std::vector<std::pair<int, int>> adjacents = adjacent_positions({row, col}, {});
                            for (std::pair<int, int> pos : adjacents) {
                                Piece* piece = square_in_position(pos);
                                if (piece != nullptr && piece -> name().substr(5, 3) == "Dog") {
                                    return_vec.push_back({row, col});
                                }
                            }
                        } else if (square -> name().substr(5, 3) == "Dog") {
                            return_vec.push_back({row, col});
                        }
                    }
                }
            }
            return return_vec;
        }
    
        std::vector<std::pair<std::pair<int, int>, std::pair<int, int>>> all_legal_moves() {
            std::vector<std::pair<std::pair<int, int>, std::pair<int, int>>> moves = {};
            for (int row = 0; row < 10; row++) {
                for (int col = 0; col < 10; col++) {
                    std::vector<std::pair<int, int>> position_moves = legal_moves({row, col}, true);
                    moves.reserve(moves.size() + position_moves.size());
                    for (std::pair<int, int> move : position_moves) {
                        moves.push_back({{row, col}, move});
                    }
                }
            }
            
            if (moves.empty()) {
                return {};
            }

            return moves;
        }
    
        std::pair<std::pair<int, int>, std::pair<int, int>> find_mate_in(int depth, bool white_to_win) {
            std::pair<std::pair<int, int>, std::pair<int, int>> false_pair = {};
            if (depth == 0) {
                return false_pair;
            }
            if (white_to_move == white_to_win) {
                for (std::pair<std::pair<int, int>, std::pair<int, int>> move : all_legal_moves()) {
                    ChessBoard* new_board = copy_board();
                    new_board -> move_piece(move.first, move.second);
                    bool checkmate = new_board -> is_checkmate();
                    if (checkmate) {
                        delete new_board;
                        return move;
                    } else if (new_board -> is_check(true)) {
                        std::pair<std::pair<int, int>, std::pair<int, int>> mate = new_board -> find_mate_in(depth - 1, white_to_win);
                        if (mate == false_pair) {
                            delete new_board;
                        } else {
                            delete new_board;
                            return move;
                        }
                    } else {
                        delete new_board;
                    }               
                }
                return false_pair;
            } else {
                std::vector<std::pair<std::pair<int, int>, std::pair<int, int>>> moves = all_legal_moves();
                for (std::pair<std::pair<int, int>, std::pair<int, int>> move : moves) {
                    ChessBoard* new_board = copy_board();
                    new_board -> move_piece(move.first, move.second);
                    std::pair<std::pair<int, int>, std::pair<int, int>> mate = new_board -> find_mate_in(depth, white_to_win);
                    delete new_board;
                    if (mate == false_pair) {
                        return false_pair;
                    }
                }
                return {{1, 1}, {1, 1}}; 
                // Move has no significance, but serves to signify that the move does result in a mate.
            }
            return false_pair;
        }
    
        int material_difference() {
            int total = 0;
            for (std::array<Piece*, 10> row : squares) {
                for (Piece* piece : row) {
                    if (piece != nullptr) {
                        total += piece -> value();
                    }
                }
            }
            return total;
        }
    };

int main(int argc, char* argv[]) {
    std::string starting_board_state;
    bool white_to_start;
    int mate_depth;
    if (argc == 4) {
        starting_board_state = argv[1];
        if (argv[2] == "0") {
            white_to_start = false;
        } else {
            white_to_start = true;
        }
        mate_depth = std::stoi(argv[3]);
    } else {
        starting_board_state = "RDOZAKCFDRPPPPPPPPPP                                                            pppppppppprdozakcfdr";
        white_to_start = true;
        mate_depth = 3;
    }

    
}
            
