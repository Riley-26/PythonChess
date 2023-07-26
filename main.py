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
        
        if self.game_over == False:
            return f"{self.name}'s turn"
        
    def choose_move(self, old_location, new_location):
        old_location = old_location.upper()
        new_location = new_location.upper()
        chosen_piece = board_dict[old_location]
        try:
            if old_location in board_dict:
                #Check if piece is in way
                if chosen_piece.valid_move(old_location, new_location):
                    board.update_board(old_location, new_location)
                    for line in board.grid:
                        print(*line)
                else:
                    raise KeyError
            else:
                raise KeyError
        except KeyError:
            print("Invalid move, please try again.")
            print(self.choose_move(input(f"{self.name}, choose the current location of your piece: "), input("Now choose a new location for the piece: ")))
        
        return ""
    

class Board:
    #Define board layout
    def __init__(self):
        self.size = 8
        self.checker = None
        self.grid = []
        self.line = []
        self.dict = {}
        self.chars = chars
    
    #Create the board
    def create_board(self):
        black_pawn_num = 0
        white_pawn_num = 0
        for i in range(self.size, 0, -1):
            global valid_dict
            global board_dict
            self.line = []
            for j in self.chars:
                self.dict = {}
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
                
                #self.grid stores key-value pairs of the location and the short-name of the object, which will be displayed to the user
                if self.dict.get(j.upper() + str(i)) != "   0":
                    self.line.append("[" + j.upper() + str(i) + ": " + self.dict.get(j.upper() + str(i)).short_name + "]")
                else:
                    self.line.append("[" + j.upper() + str(i) + ": " + self.dict.get(j.upper() + str(i)) + "]")
                #Board dictionary stores key-value pairs of the location and object
                board_dict.update(self.dict)
            
            self.grid.append(self.line)
        
        return ""
    
    def update_board(self, old_location, new_location):
        #Update the new location in the board dictionary
        if board_dict[new_location] == "   0":
            board_dict[new_location] = board_dict[old_location]
            board_dict[old_location] = "   0"
        elif board_dict[new_location].short_name != board_dict[old_location].short_name:
            board_dict[new_location] = board_dict[old_location]
            board_dict[old_location] = "   0"
        
        #Update the new location in the displayed board
        for x, item in enumerate(board.grid):
            for y in range(len(item)):
                if (8 - int(new_location[1])) == x:
                    if char_codes[new_location[0].lower()] - 1 == y:
                        print(x, y)
                        board.grid[x][y] = "[" + str(new_location) + ": " + str(board_dict[new_location].short_name) + "]"
                elif (8 - int(old_location[1])) == x:
                    if char_codes[old_location[0].lower()] - 1 == y:
                        board.grid[x][y] = "[" + str(old_location) + ": " + "   0" + "]"

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

    def valid_move(self, old_location, new_location):
        #Define set moves
        global char_codes
        valid = False
        #Checks if the input is valid
        if board_dict[old_location].colour == self.colour:
            if len(new_location) == 2 and len(old_location) == 2:
                if new_location[0].lower() in chars and old_location[0].lower() in chars:
                    if int(new_location[1]) in char_indices and int(old_location[1]) in char_indices:
                        valid = True
                    else:
                        return valid
                else:
                    return valid
            else:
                return valid
        
        old_location_num = int(old_location[1])
        new_location_num = int(new_location[1])
        
        #Check if there is a piece in the way
        if board_dict.get(new_location) != "   0":
                valid = False
        #Checks if it's black
        if self.colour == "b-":
            print(self.colour)
            #Makes sure the new location is further into the board than old location
            if new_location_num >= old_location_num:
                return valid
            #Check if a piece can be taken
            if new_location_num == old_location_num - 1:
                if (int(char_codes.get(new_location[0].lower())) == int(char_codes.get(old_location[0].lower())) + 1) or (int(char_codes.get(new_location[0].lower())) == int(char_codes.get(old_location[0].lower())) - 1):
                    if board_dict[new_location].short_name == "w-":
                        board_dict[new_location].taken = True
                        board_dict[new_location].taken()
                        board.update_board(old_location, new_location)
                        
                        valid = True
                        return True
                    elif board_dict[new_location].short_name == "b-":
                        valid = False
                        return valid
            #Standard move
            if new_location_num <= 8:
                #Pawn changes to any piece if it reaches end of board
                if new_location_num == 8:
                    valid = True
                    self.change_piece(input("Choose what you would like the pawn to change to: "))
                    return valid
                #Move one place
                elif new_location_num == old_location_num - 1:
                    valid = True
            #Pawn can move two places on first move
            if old_location_num == 7:
                if new_location_num == 5:
                    valid = True
                elif new_location_num == 6:
                    valid = True
                else:
                    valid = False
                    return valid
            
        #Checks if it's white
        elif self.colour == "w-":
            print(self.colour)
            #Makes sure the new location is further into the board than old location
            if new_location_num <= old_location_num:
                return valid
            #Check if a piece can be taken
            if new_location_num == old_location_num + 1:
                if (int(char_codes.get(new_location[0].lower())) == int(char_codes.get(old_location[0].lower())) - 1) or (int(char_codes.get(new_location[0].lower())) == int(char_codes.get(old_location[0].lower())) + 1):
                    if board_dict[new_location].short_name == "w-":
                        board_dict[new_location].taken = True
                        board_dict[new_location].taken()
                        board.update_board(old_location, new_location)
                        
                        valid = True
                        return True
                    elif board_dict[new_location].short_name == "b-":
                        valid = False
                        return valid
            #Standard move
            if new_location_num >= 1:
                #Pawn changes to any piece if it reaches end of board
                if new_location_num == 1:
                    valid = True
                    self.change_piece(input("Choose what you would like the pawn to change to: "))
                    return valid
                #Move one place
                elif new_location_num == old_location_num + 1:
                    valid = True
            #Pawn can move two places on first move
            if old_location_num == 2:
                if new_location_num == 4:
                    valid = True
                elif new_location_num == 3:
                    valid = True
                else:
                    valid = False
                    return valid
        
        return valid

    #Pawn change at end of board
    def change_piece(self, new_piece, new_location):
        if new_piece in new_pieces:
            board_dict[new_location] = new_piece_objects[new_piece]
            return True
        else:
            return False

class Rook(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour + "Rk"

    def valid_move(self):
        pass
    
    def castling(self):
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
black_pawns, white_pawns = [Pawn(black, "pawn", i) for i in range(1, 9)], [Pawn(white, "pawn", i) for i in range(1, 9)]
black_rook, white_rook = Rook(black, "rook"), Rook(white, "rook")
black_bishop, white_bishop = Bishop(black, "bishop"), Bishop(white, "bishop")
black_knight, white_knight = Knight(black, "knight"), Knight(white, "knight")
black_queen, white_queen = Queen(black, "queen"), Queen(white, "queen")
black_king, white_king = King(black, "king"), King(white, "king")

valid_dict = {
    "black_pieces" : {
        "pawn": black_pawns,
        "rook": black_rook,
        "bishop": black_bishop,
        "knight": black_knight,
        "queen": black_queen,
        "king": black_king,
    },

    "white_pieces" : {
        "pawn": white_pawns,
        "rook": white_rook,
        "bishop": white_bishop,
        "knight": white_knight,
        "queen": white_queen,
        "king": white_king,
    }
}

new_pieces = ("rook", "knight", "queen", "bishop")
new_piece_objects = {
    "rook": Rook,
    "knight": Knight,
    "queen": Queen,
    "bishop": Bishop
}
char_codes = {}
chars = [chr(i) for i in range(ord("a"), ord("h")+1)]
char_indices = [i for i in range(1, 9)]
for i in range(len(chars)):
    char_codes[chars[i]] = char_indices[i]

#Main game loop
def game_loop():
    global current_move
    game_state = True
    #Print initial board
    for line in board.grid:
        print(*line)
        
    #Keep game running, and check if someone has won/lost
    while game_state:
        #Keep track of the current move
        player_names[current_move].__repr__()
        player_names[current_move].choose_move(input(f"{player_names[current_move].name}, choose the current location of your piece: "), input("Now choose a new location for the piece: "))
        if current_move == 0:
            player_names[current_move].is_turn
            
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
#Current move 
current_move = 0
player1 = Player("black", input("Player 1 (Black), choose your name: "), 0)
player2 = Player("white", input("Player 2 (White), choose your name: "), 1)
player_names = [player1, player2]
board_dict = {}

board.create_board()

game_loop()
