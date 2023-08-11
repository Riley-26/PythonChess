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
        try:
            if old_location in board_dict:
                chosen_piece = board_dict[old_location]
                #Check if piece is in way
                if chosen_piece.valid_move(old_location, new_location):
                    for line in board.grid:
                        print(*line)
                    return "Valid Move"
                else:
                    raise KeyError
            else:
                raise KeyError
        except (KeyError, AttributeError):
            for line in board.grid:
                print(*line)
            print("Invalid move, please try again.")
        
            return self.choose_move(input(f"{self.name}, choose the current location of your piece: "), input("Now choose a new location for the piece: "))
    

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
    
    def update_board(self, old_location, new_location, new_piece):
        #Update the new location in the displayed board
        # for x, item in enumerate(board.grid):
        #     for y in range(len(item)):
        #         print(x, y, item)
        #         if (8 - int(new_location[1])) == x:
        #             if char_codes[new_location[0].lower()] - 1 == y:
        #                 if new_piece == False:
        #                     if board_dict[old_location] != "   0":
        #                         board.grid[x][y] = "[" + str(new_location) + ": " + str(board_dict[old_location].short_name) + "]"
        #                 else:
        #                     board.grid[x][y] = "[" + str(new_location) + ": " + new_piece.short_name + "]"
        #         elif (8 - int(old_location[1])) == x:
        #             if char_codes[old_location[0].lower()] - 1 == y:
        #                 board.grid[x][y] = "[" + str(old_location) + ": " + "   0" + "]"
                
        #Update the new location in the board dictionary
        if new_piece == False:
            if board_dict[old_location].colour[0] == "b":
                board.grid[8 - int(old_location[1])][int(char_codes[old_location[0].lower()]) - 1] = "[" + str(old_location) + ": " + "   0" + "]"
                board.grid[8 - int(new_location[1])][int(char_codes[new_location[0].lower()]) - 1] = "[" + str(new_location) + ": " + str(board_dict[old_location].short_name) + "]"
            elif board_dict[old_location].colour[0] == "w":
                board.grid[8 - int(old_location[1])][int(char_codes[old_location[0].lower()]) - 1] = "[" + str(old_location) + ": " + "   0" + "]"
                board.grid[8 - int(new_location[1])][int(char_codes[new_location[0].lower()]) - 1] = "[" + str(new_location) + ": " + str(board_dict[old_location].short_name) + "]"
                
            board_dict[new_location] = board_dict[old_location]
            board_dict[old_location] = "   0"
        else:
            board.grid[int(char_codes[new_location[0]] - 1)][int(new_location[1]) - 1] = "[" + str(new_location) + ": " + new_piece.short_name + "]"
            
        return ""

    
#Superclass for each piece, universal rules for the pieces
class Piece:
    def __init__(self, colour, piece_name):
        self.colour = colour
        self.piece_taken = False
        self.clear_move = False
        self.piece_name = piece_name
        
    def valid_input(self, old_location, new_location):
        if board_dict[old_location] != "   0":
            if board_dict[old_location].colour == player_names[current_move].colour:
                if len(new_location) == 2 and len(old_location) == 2:
                    if new_location[0].lower() in chars and old_location[0].lower() in chars:
                        if int(new_location[1]) in char_indices and int(old_location[1]) in char_indices:
                            valid = True
                            return valid
                        else:
                            valid = False
                            return valid
                    else:
                        valid = False
                        return valid
                else:
                    valid = False
                    return valid
            else:
                valid = False
                return valid
        else:
            valid = False
            return valid


#Each piece
class Pawn(Piece):
    def __init__(self, colour, piece_name, pawn_num):
        super().__init__(colour, piece_name)
        self.short_name = colour[0] + "-P" + str(pawn_num)

    def valid_move(self, old_location, new_location):
        #Define set moves
        global char_codes
        valid = False
        #Checks if the input is valid
        if super().valid_input(old_location, new_location) == False:
            valid = False
            return valid
        
        #Check if there is a piece in the way and if move is in the valid direction
        old_location_num = int(old_location[1])
        new_location_num = int(new_location[1])
        prev_column = old_location[0]
        new_column = new_location[0]
        
        #First check if both inputs are in the same column or if the new location is diagonal to the old location
        if char_codes[prev_column.lower()] + 1 == char_codes[new_column.lower()] or char_codes[prev_column.lower()] - 1 == char_codes[new_column.lower()] or prev_column == new_column:
            if board_dict[old_location].colour[0] == "b":
                #Black side first
                #Check if new location is further into the board than old location
                if old_location_num > new_location_num and new_location_num >= 1:
                    #Check diagonal blockages and valid moves
                    if old_location_num - 1 == new_location_num and prev_column != new_column:
                        if char_codes[prev_column.lower()] + 1 == char_codes[new_column.lower()] or char_codes[prev_column.lower()] - 1 == char_codes[new_column.lower()]:
                            if board_dict[new_location] != "   0" and board_dict[new_location].colour[0] != self.colour[0]:
                                valid = True
                            else:
                                valid = False
                                return valid
                        else:
                            valid = False
                            return valid
                    
                    #Same column valid moves
                    if prev_column == new_column:
                        #Check straight blockages
                        for i in range(old_location_num - 1, new_location_num, - 1):
                            if board_dict[prev_column + str(i)] == "   0":
                                valid = True
                            else:
                                valid = False
                                return valid
                        #Check first move, can move twice
                        if old_location_num == 7 and old_location_num - 2 == new_location_num or old_location_num - 1 == new_location_num:
                            valid = True
                        #Check other moves
                        elif old_location_num != 7 and old_location_num - 1 == new_location_num:
                            valid = True
                        else:
                            valid = False
                            return valid
                    
                    #Check if new location is at the end of the board
                    if new_location_num == 1:
                        self.change_piece(input("Choose what you would like the pawn to change to: "), new_location, old_location)
                        valid = True
                        return valid
                
                else:
                    valid = False
                    return valid
            
            #White side
            elif board_dict[old_location].colour[0] == "w":
                if old_location_num < new_location_num and new_location_num <= 8:
                    #Check diagonal blockages and valid moves
                    if old_location_num + 1 == new_location_num and prev_column != new_column:
                        if char_codes[prev_column.lower()] + 1 == char_codes[new_column.lower()] or char_codes[prev_column.lower()] - 1 == char_codes[new_column.lower()]:
                            if board_dict[new_location] != "   0" and board_dict[new_location].colour[0] != self.colour[0]:
                                valid = True
                            else:
                                valid = False
                                return valid
                        else:
                            valid = False
                            return valid
                    
                    #Same column valid moves
                    if prev_column == new_column:
                        #Check straight blockages
                        for i in range(old_location_num + 1, new_location_num, 1):
                            if board_dict[prev_column + str(i)] == "   0":
                                valid = True
                            else:
                                valid = False
                                return valid
                        #Check first move, can move twice
                        if old_location_num == 2 and old_location_num + 2 == new_location_num or old_location_num + 1 == new_location_num:
                            valid = True
                        #Check other moves
                        elif old_location_num != 2 and old_location_num + 1 == new_location_num:
                            valid = True
                        else:
                            valid = False
                            return valid
                    
                    #Check if new location is at the end of the board
                    if new_location_num == 8:
                        self.change_piece(input("Choose what you would like the pawn to change to: "), new_location, old_location)
                        valid = True
                        return valid
                
                #Check if new location is further into the board than old location
                else:
                    valid = False
                    return valid
        
        board.update_board(old_location, new_location, False)
        return valid


    #Pawn change at end of board
    def change_piece(self, new_piece, new_location, old_location):
        if new_piece.lower() in new_pieces:
            board_dict[new_location] = new_piece_objects[new_piece](self.colour, new_piece)
            board.update_board(old_location, new_location, board_dict[new_location])
            return True
        else:
            print("Invalid piece name, please try again.")
            self.change_piece(input("Choose what you would like the pawn to change to: "), new_location, old_location)
            

class Rook(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour[0] + "-Rk"

    def valid_move(self, old_location, new_location):
        #Check if input is valid
        if super().valid_input(old_location, new_location) == False:
            valid = False
            return valid
        
        old_location_num = int(old_location[1])
        new_location_num = int(new_location[1])
        
        prev_column = old_location[0]
        new_column = new_location[0]
        
        valid = False
        
        #Black side
        if board_dict[old_location].colour[0] == "b":
            #Check column blocks
            if prev_column == new_column:
                if board_dict[new_location] == "   0" or board_dict[new_location].colour[0] != self.colour[0]:
                    valid = True
                else:
                  valid = False
                  return valid
                  
                #Black forwards move
                if old_location_num > new_location_num:
                    for i in range(old_location_num - 1, new_location_num - 1, - 1):
                        if board_dict[prev_column + str(i)] == "   0" or board_dict[new_location].colour[0] != self.colour[0]:
                            valid = True
                            continue
                        elif board_dict[new_location].colour[0] == self.colour[0]:
                            valid = False
                            break
                        else:
                            valid = False
                            break
                        
                    if valid == False:
                        return valid
                
                #Black backwards move
                elif old_location_num < new_location_num:
                    for i in range(old_location_num + 1, new_location_num + 1):
                        if board_dict[prev_column + str(i)] == "   0" or board_dict[new_location].colour[0] != self.colour[0]:
                            valid = True
                            continue
                        elif board_dict[new_location].colour[0] == self.colour[0]:
                            valid = False
                            break
                        else:
                            valid = False
                            break
                        
                    if valid == False:
                        return valid
                    
            #Check row blocks
            elif old_location_num == new_location_num:
                if board_dict[new_location] == "   0" or board_dict[new_location].colour[0] != self.colour[0]:
                    valid = True
                else:
                  valid = False
                  return valid
                
                #Black right move
                if prev_column < new_column:
                    for i in range(int(char_codes[prev_column.lower()]) + 1, int(char_codes[new_column.lower()]) + 1):
                        if board_dict[chars[i - 1].upper() + str(new_location_num)] == "   0" or board_dict[new_location].colour[0] != self.colour[0]:
                            valid = True
                            continue
                        elif board_dict[new_location].colour[0] == self.colour[0]:
                            valid = False
                            return valid
                        else:
                            valid = False
                            break
                        
                    if valid == False:
                        return valid
                        
                #Black left move
                elif prev_column > new_column:
                    for i in range(int(char_codes[prev_column.lower()]) - 1, int(char_codes[new_column.lower()]) - 1, - 1):
                        if board_dict[chars[i - 1].upper() + str(new_location_num)] == "   0" or board_dict[new_location].colour[0] != self.colour[0]:
                            valid = True
                            continue
                        elif board_dict[new_location].colour[0] == self.colour[0]:
                            valid = False
                            return valid
                        else:
                            valid = False
                            break
                        
                    if valid == False:
                        return valid
                    
            else:
                valid = False
                return valid
                    
        #White side
        elif board_dict[old_location].colour[0] == "w":
            #Check column blocks
            if prev_column == new_column:
                if board_dict[new_location] == "   0" or board_dict[new_location].colour[0] != self.colour[0]:
                    valid = True
                else:
                  valid = False
                  return valid
                
                #White forwards move
                if old_location_num < new_location_num:
                    for i in range(old_location_num + 1, new_location_num + 1):
                        if board_dict[prev_column + str(i)] == "   0" or board_dict[new_location].colour[0] != self.colour[0]:
                            valid = True
                            continue
                        elif board_dict[new_location].colour[0] == self.colour[0]:
                            valid = False
                            return valid
                        else:
                            valid = False
                            break
                        
                    if valid == False:
                        return valid
                        
                #White backwards move
                elif old_location_num > new_location_num:
                    for i in range(old_location_num - 1, new_location_num - 1, - 1):
                        if board_dict[prev_column + str(i)] == "   0" or board_dict[new_location].colour[0] != self.colour[0]:
                            valid = True
                            continue
                        elif board_dict[new_location].colour[0] == self.colour[0]:
                            valid = False
                            return valid
                        else:
                            valid = False
                            break
                        
                    if valid == False:
                        return valid
                    
            #Check row blocks
            elif old_location_num == new_location_num:
                if board_dict[new_location] == "   0" or board_dict[new_location].colour[0] != self.colour[0]:
                    valid = True
                else:
                  valid = False
                  return valid
                
                #White right move
                if prev_column < new_column:
                    for i in range(int(char_codes[prev_column.lower()]) + 1, int(char_codes[new_column.lower()]) + 1):
                        if board_dict[chars[i - 1].upper() + str(new_location_num)] == "   0" or board_dict[new_location].colour[0] != self.colour[0]:
                            valid = True
                            continue
                        elif board_dict[new_location].colour[0] == self.colour[0]:
                            valid = False
                            return valid
                        else:
                            valid = False
                            break
                        
                    if valid == False:
                        return valid
                
                #White left move
                elif prev_column > new_column:
                    for i in range(int(char_codes[prev_column.lower()]) - 1, int(char_codes[new_column.lower()]) - 1, - 1):
                        if board_dict[chars[i - 1].upper() + str(new_location_num)] == "   0" or board_dict[new_location].colour[0] != self.colour[0]:
                            valid = True
                            continue
                        elif board_dict[new_location].colour[0] == self.colour[0]:
                            valid = False
                            return valid
                        else:
                            valid = False
                            break
                        
                    if valid == False:
                        return valid
                        
            else:
                valid = False
                return valid
        
                
        board.update_board(old_location, new_location, False)
        return valid
    
    def castling(self):
        pass

class Knight(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour[0] + "-Kn"

    def valid_move(self):
        pass

class Bishop(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour[0] + "-Bs"

    def valid_move(self):
        pass

class Queen(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour[0] + "-Qu"

    def valid_move(self):
        pass

class King(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour[0] + "-Kg"

    def valid_move(self):
        pass


#Setting global variables
black = "b-"
white = "w-"
game_state = False
black_pawns, white_pawns = [Pawn("black", "pawn", i) for i in range(1, 9)], [Pawn("white", "pawn", i) for i in range(1, 9)]
black_rook, white_rook = Rook("black", "rook"), Rook("white", "rook")
black_bishop, white_bishop = Bishop("black", "bishop"), Bishop("white", "bishop")
black_knight, white_knight = Knight("black", "knight"), Knight("white", "knight")
black_queen, white_queen = Queen("black", "queen"), Queen("white", "queen")
black_king, white_king = King("black", "king"), King("white", "king")

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
