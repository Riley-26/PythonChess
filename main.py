class Player:
    def __init__(self, colour, name):
        #Initialise each Player
        self.colour = colour
        self.name = name
        self.is_turn = False
        self.in_check = False
        self.opponent_checkmated = False
        self.valid_moves = True
    
    def __repr__(self):
        #Win Conditions
        if self.in_check:
            return f"Player {self.name}'s King is in check"
        
        if self.opponent_checkmated:
            self.game_over = True
            return f"Checkmate! Player {self.name} wins!"
        
        if self.valid_moves == False and self.in_check == False:
            self.game_over = True
            return f"Draw! Player {self.name} has no valid moves to take."
        
        if self.game_over == False:
            return f"Player {self.name}'s turn"
        

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
        for i in range(self.size):
            self.line = []
            self.dict = {}
            for j in range(1, self.size + 1):
                if self.chars[i].upper() == "B" or self.chars[i].upper() == "G":
                    if self.chars[i].upper() == "B":
                        self.dict[self.chars[i].upper() + str(j)] = black_pieces["pawn"]
                    elif self.chars[i].upper() == "G":
                        self.dict[self.chars[i].upper() + str(j)] = white_pieces["pawn"]
                elif (j == 1 or j == 8) and (self.chars[i].upper() == "A" or self.chars[i].upper() == "H"):
                    if self.chars[i].upper() == "A":
                        self.dict[self.chars[i].upper() + str(j)] = black_pieces["rook"]
                    elif self.chars[i].upper() == "H":
                        self.dict[self.chars[i].upper() + str(j)] = white_pieces["rook"]
                elif (j == 2 or j == 7) and (self.chars[i].upper() == "A" or self.chars[i].upper() == "H"):
                    if self.chars[i].upper() == "A":
                        self.dict[self.chars[i].upper() + str(j)] = black_pieces["knight"]
                    elif self.chars[i].upper() == "H":
                        self.dict[self.chars[i].upper() + str(j)] = white_pieces["knight"]
                elif (j == 3 or j == 6) and (self.chars[i].upper() == "A" or self.chars[i].upper() == "H"):
                    if self.chars[i].upper() == "A":
                        self.dict[self.chars[i].upper() + str(j)] = black_pieces["bishop"]
                    elif self.chars[i].upper() == "H":
                        self.dict[self.chars[i].upper() + str(j)] = white_pieces["bishop"]
                elif j == 4 and (self.chars[i].upper() == "A" or self.chars[i].upper() == "H"):
                    if self.chars[i].upper() == "A":
                        self.dict[self.chars[i].upper() + str(j)] = black_pieces["queen"]
                    elif self.chars[i].upper() == "H":
                        self.dict[self.chars[i].upper() + str(j)] = white_pieces["queen"]
                elif j == 5 and (self.chars[i].upper() == "A" or self.chars[i].upper() == "H"):
                    if self.chars[i].upper() == "A":
                        self.dict[self.chars[i].upper() + str(j)] = black_pieces["king"]
                    elif self.chars[i].upper() == "H":
                        self.dict[self.chars[i].upper() + str(j)] = white_pieces["king"]
                else:
                    self.dict[self.chars[i].upper() + str(j)] = "   0"
                
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
                del black_pieces[self.piece_name]
            elif self.colour == white:
                del white_pieces[self.piece_name]


#Each piece
class Pawn(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour + "Pn"

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

black_pieces = {
    "pawn": Pawn(black, "pawn").short_name,
    "rook": Rook(black, "rook").short_name,
    "bishop": Bishop(black, "bishop").short_name,
    "knight": Knight(black, "knight").short_name,
    "queen": Queen(black, "queen").short_name,
    "king": King(black, "king").short_name,
}

white_pieces = {
    "pawn": Pawn(white, "pawn").short_name,
    "rook": Rook(white, "rook").short_name,
    "bishop": Bishop(white, "bishop").short_name,
    "knight": Knight(white, "knight").short_name,
    "queen": Queen(white, "queen").short_name,
    "king": King(white, "king").short_name,
}

#Main game loop
def game_loop():
    while Player().valid_moves or Player().opponent_checkmated:
        for line in board.grid:
            print(*line)
        return ""

#Set game variables
board = Board()


board.create_board()

game_loop()