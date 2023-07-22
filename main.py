class Player:
    def __init__(self, colour, name, player_num):
        #Initialise each Player
        self.colour = colour
        self.name = name
        self.player_num = player_num
        self.is_turn = False
        self.in_check = False
        self.opponent_checkmated = False
        self.valid_moves = True
        self.game_over = False
        self.colour_dict = valid_dict[colour + "_pieces"]
    
    def __repr__(self):
        #Win Conditions
        if self.in_check:
            return f"{self.name}'s King is in check \n {self.name}'s turn"
        elif self.opponent_checkmated:
            self.game_over = True
            return f"Checkmate! {self.name} wins!"
        elif self.valid_moves == False and self.in_check == False:
            self.game_over = True
            return f"Draw! {self.name} has no valid moves to take."
        elif self.game_over == False:
            return f"{self.name}'s turn"
        
    def choose_move(self, old_location, new_location):
        chosen_location = []
        old_location = old_location.upper()
        new_location = new_location.upper()
        try:
            if old_location in board_dict:
                board_dict[new_location] = board_dict[old_location]
                #Check if piece is in way
                print(board_dict)
            else:
                raise KeyError
        except KeyError:
            print("Invalid move, please try again.")
            print(self.choose_move(input(f"{self.name}, choose the current location of your piece: "), input("Now choose a new location for the piece: ")))
        
        return chosen_location
    

class Board:
    #Define board layout
    def __init__(self):
        self.size = 8
        self.checker = None
        self.grid = []
        self.line = []
        self.dict = {}
        self.chars = [chr(i) for i in range(ord("a"), ord("h")+1)]
    
    #Update board after each move
    def update_board(self):
        pass
    
    #Create the board
    def create_board(self):
        black_pawn_num = 0
        white_pawn_num = 0
        for i in range(self.size, 0, -1):
            global valid_dictw
            global board_dict
            self.line = []
            self.dict = {}
            for j in self.chars:
                #Layout pieces other than pawns
                if i == 8:
                    if j == "a" or j == "h":
                        self.dict[j.upper() + str(i)] = valid_dict["black_pieces"]["rook"]
                    elif j == "b" or j == "g":
                        self.dict[j.upper() + str(i)] = valid_dict["black_pieces"]["knight"]
                    elif j == "c" or j == "f":
                        self.dict[j.upper() + str(i)] = valid_dict["black_pieces"]["bishop"]
                    elif j == "d":
                        self.dict[j.upper() + str(i)] = valid_dict["black_pieces"]["queen"]
                    elif j == "e":
                        self.dict[j.upper() + str(i)] = valid_dict["black_pieces"]["king"]
                elif i == 1:
                    if j == "a" or j == "h":
                        self.dict[j.upper() + str(i)] = valid_dict["white_pieces"]["rook"]
                    elif j == "b" or j == "g":
                        self.dict[j.upper() + str(i)] = valid_dict["white_pieces"]["knight"]
                    elif j == "c" or j == "f":
                        self.dict[j.upper() + str(i)] = valid_dict["white_pieces"]["bishop"]
                    elif j == "d":
                        self.dict[j.upper() + str(i)] = valid_dict["white_pieces"]["queen"]
                    elif j == "e":
                        self.dict[j.upper() + str(i)] = valid_dict["white_pieces"]["king"]
                #Layout pawns
                elif i == 7:
                    self.dict[j.upper() + str(i)] = valid_dict["black_pieces"]["pawn"][black_pawn_num]
                    black_pawn_num += 1
                elif i == 2:
                    self.dict[j.upper() + str(i)] = valid_dict["white_pieces"]["pawn"][white_pawn_num]
                    white_pawn_num += 1
                #Layout blanks
                else:
                    self.dict[j.upper() + str(i)] = "   0"
                
                board_dict.update(self.dict)
                
            self.line.append(self.dict)
            self.grid.append(self.line)
        
        return ""

    
#Superclass for each piece, universal rules for the pieces
class Piece:
    def __init__(self, colour, piece_name):
        self.colour = colour
        self.taken = False
        self.clear_move = False
        self.piece_name = piece_name
    
    def taken(self):
        if self.taken == True:
            if self.colour == black:
                del valid_dict.black_pieces[self.piece_name]
            elif self.colour == white:
                del valid_dict.white_pieces[self.piece_name]


#Each piece
class Pawn(Piece):
    def __init__(self, colour, piece_name, pawn_num):
        super().__init__(colour, piece_name)
        self.short_name = colour + "P" + str(pawn_num)

    def valid_move(self):
        pass

class Rook(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour + "Rk"

    def valid_move(self):
        pass

class Knight(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour + "Kn"

    def valid_move(self):
        pass

class Bishop(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour + "Bs"

    def valid_move(self):
        pass

class Queen(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour + "Qu"

    def valid_move(self):
        pass

class King(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour + "Kg"

    def valid_move(self):
        pass


#Setting global variables
black = "b-"
white = "w-"
game_state = False

valid_dict = {
    "black_pieces" : {
        "pawn": [Pawn(black, "pawn", i).short_name for i in range(1, 9)],
        "rook": Rook(black, "rook").short_name,
        "bishop": Bishop(black, "bishop").short_name,
        "knight": Knight(black, "knight").short_name,
        "queen": Queen(black, "queen").short_name,
        "king": King(black, "king").short_name,
    },

    "white_pieces" : {
        "pawn": [Pawn(white, "pawn", i).short_name for i in range(1, 9)],
        "rook": Rook(white, "rook").short_name,
        "bishop": Bishop(white, "bishop").short_name,
        "knight": Knight(white, "knight").short_name,
        "queen": Queen(white, "queen").short_name,
        "king": King(white, "king").short_name,
    }
}

#Main game loop
def game_loop():
    game_state = True
    #Player 1's move is 0, Player 2's move is 1
    current_move = 0
    #Print initial board
    for line in board.grid:
        print(*line)
        
    #Keep game running, and check if someone has won/lost
    while game_state:
        #Keep track of the current move
        player_names[current_move].__repr__()
        player_names[current_move].choose_move(input(f"{player_names[current_move].name}, choose the current location of your piece: "), input("Now choose a new location for the piece: "))
        if current_move == 0:
            player_names[current_move]
            
            #Change turn
            current_move = 1
        elif current_move == 1:
            
            
            #Change turn
            current_move = 0
            
        #Move piece, and check if it is valid
        
        
        #Check if someone has won/lost
        if player1.game_over == True:
            game_state = False
        elif player2.game_over == True:
            game_state = False
        
    return ""


#Set game variables
board = Board()
player1 = Player("black", input("Player 1 (Black), choose your name: "), 0)
player2 = Player("white", input("Player 2 (White), choose your name: "), 1)
player_names = [player1, player2]
board_dict = {}

board.create_board()

game_loop()
