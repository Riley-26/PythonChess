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
        if old_location.upper() != new_location.upper():
            if board_dict[old_location] != "   0":
                if board_dict[old_location].colour == player_names[current_move].colour:
                    if len(new_location) == 2 and len(old_location) == 2:
                        if new_location[0].lower() in chars and old_location[0].lower() in chars:
                            if int(new_location[1]) in char_indices and int(old_location[1]) in char_indices:
                                if board_dict[new_location.upper()] != "   0" and board_dict[new_location.upper()].piece_name == "king":
                                    valid = False
                                    return valid
                                else:
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
                
        board_dict[king_location_b].check_move(king_location_b, king_location_b)
        board_dict[king_location_w].check_move(king_location_w, king_location_w)
        
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
        
        #Check input
        if old_location_num == new_location_num or prev_column == new_column:
            #Check final location first, if colour is the same then the function can be skipped
            if board_dict[new_location] != "   0" and board_dict[old_location].colour[0] == board_dict[new_location].colour[0]:
                valid = False
                return valid
            else:
                #Down/upwards move
                if prev_column == new_column:
                    #Downwards move
                    if new_location_num < old_location_num:
                        for i in range(new_location_num, old_location_num):
                            if board_dict[prev_column.upper() + str(i)] == "   0":
                                valid = True
                                continue
                            elif i == new_location_num and board_dict[prev_column.upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                continue
                            else:
                                valid = False
                                break
                    #Upwards move
                    elif new_location_num > old_location_num:
                        for i in range(old_location_num + 1, new_location_num + 1):
                            if board_dict[prev_column.upper() + str(i)] == "   0":
                                valid = True
                                continue
                            elif i == new_location_num and board_dict[prev_column.upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                continue
                            else:
                                valid = False
                                break
                elif new_location_num == old_location_num:
                    #Right move
                    if prev_column < new_column:
                        for i in range(char_codes[prev_column.lower()] + 1, char_codes[new_column.lower()] + 1):
                            if board_dict[chars[i - 1].upper() + str(old_location_num)] == "   0":
                                valid = True
                                continue
                            elif i == new_location_num and board_dict[chars[i - 1].upper() + str(old_location_num)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                continue
                            else:
                                valid = False
                                break
                    #Left move
                    elif prev_column > new_column:
                        for i in range(char_codes[new_column.lower()], char_codes[prev_column.lower()]):
                            if board_dict[chars[i - 1].upper() + str(old_location_num)] == "   0":
                                valid = True
                                continue
                            elif i == new_location_num and board_dict[chars[i - 1].upper() + str(old_location_num)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                continue
                            else:
                                valid = False
                                break
                        
                if valid == False:
                    return valid
                        
        else:
            valid = False
            return valid
        
        board_dict[king_location_b].check_move(king_location_b, king_location_b)
        board_dict[king_location_w].check_move(king_location_w, king_location_w)
                
        board.update_board(old_location, new_location, False)
        return valid
    
    def castling(self):
        pass

class Knight(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour[0] + "-Kn"

    def valid_move(self, old_location, new_location):
        if super().valid_input(old_location, new_location) == False:
            valid = False
            return valid
        
        old_location_num = int(old_location[1])
        new_location_num = int(new_location[1])
        
        prev_column = old_location[0]
        new_column = new_location[0]
        
        valid = False
        
        if board_dict[old_location].colour[0] == "b":
            #Forwards and backwards moves for black side
            if new_location_num - 2 == old_location_num or new_location_num + 2 == old_location_num:
                if char_codes[new_column.lower()] - 1 == char_codes[prev_column.lower()] or char_codes[new_column.lower()] + 1 == char_codes[prev_column.lower()]:
                    valid = True
                    if board_dict[new_location] != "   0" and board_dict[new_location].colour[0] == board_dict[old_location].colour[0]:
                        valid = False
                        return valid
                else:
                    valid = False
                    return valid
            #Sideways moves for black side
            elif new_location_num - 1 == old_location_num or new_location_num + 1 == old_location_num:
                if char_codes[new_column.lower()] - 2 == char_codes[prev_column.lower()] or char_codes[new_column.lower()] + 2 == char_codes[prev_column.lower()]:
                    valid = True
                    if board_dict[new_location] != "   0" and board_dict[new_location].colour[0] == board_dict[old_location].colour[0]:
                        valid = False
                        return valid
                else:
                    valid = False
                    return valid
                
        elif board_dict[old_location].colour[0] == "w":
            #Forwards and backwards moves for white side
            if new_location_num - 2 == old_location_num or new_location_num + 2 == old_location_num:
                if char_codes[new_column.lower()] - 1 == char_codes[prev_column.lower()] or char_codes[new_column.lower()] + 1 == char_codes[prev_column.lower()]:
                    valid = True
                    if board_dict[new_location] != "   0" and board_dict[new_location].colour[0] == board_dict[old_location].colour[0]:
                        valid = False
                        return valid
                else:
                    valid = False
                    return valid
            #Sideways moves for white side
            elif new_location_num - 1 == old_location_num or new_location_num + 1 == old_location_num:
                if char_codes[new_column.lower()] - 2 == char_codes[prev_column.lower()] or char_codes[new_column.lower()] + 2 == char_codes[prev_column.lower()]:
                    valid = True
                    if board_dict[new_location] != "   0" and board_dict[new_location].colour[0] == board_dict[old_location].colour[0]:
                        valid = False
                        return valid
                else:
                    valid = False
                    return valid
            else:
                valid = False
                return valid
            
        board_dict[king_location_b].check_move(king_location_b, king_location_b)
        board_dict[king_location_w].check_move(king_location_w, king_location_w)
        
        board.update_board(old_location, new_location, False)
        return valid
        

class Bishop(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour[0] + "-Bs"

    def valid_move(self, old_location, new_location):
        if super().valid_input(old_location, new_location) == False:
            valid = False
            return valid
        
        old_location_num = int(old_location[1])
        new_location_num = int(new_location[1])
        
        prev_column = old_location[0]
        new_column = new_location[0]
        
        valid = False
        
        #Check input
        if abs(old_location_num - new_location_num) == abs(char_codes[prev_column.lower()] - char_codes[new_column.lower()]):
            #Check final location first, if invalid then the blockage checks can be skipped
            if (board_dict[new_location] != "   0" and board_dict[old_location].colour[0] == board_dict[new_location].colour[0]) or old_location_num == new_location_num or prev_column == new_column:
                valid = False
                return valid
            else:
                if new_location_num > old_location_num:
                    #Up the board
                    if old_location[0] > new_location[0]:
                        iter = char_codes[old_location[0].lower()] - 2
                        #Up left
                        for i in range(old_location_num + 1, new_location_num + 1):
                            if board_dict[chars[iter].upper() + str(i)] == "   0" or board_dict[chars[iter].upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                iter -= 1
                                continue
                            elif i == new_location_num and board_dict[chars[iter].upper() + str(i)].colour[0] == board_dict[old_location].colour[0]:
                                valid = True
                                iter -= 1
                                continue
                            else:
                                valid = False
                                iter -= 1
                                break
                            
                    elif old_location[0] < new_location[0]:
                        iter = char_codes[old_location[0].lower()]
                        #Up right
                        for i in range(old_location_num + 1, new_location_num + 1):
                            if board_dict[chars[iter].upper() + str(i)] == "   0" or board_dict[chars[iter].upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                iter += 1
                                continue
                            elif i == old_location_num and board_dict[chars[iter].upper() + str(i)].colour[0] == board_dict[old_location].colour[0]:
                                valid = True
                                iter += 1
                                continue
                            else:
                                valid = False
                                iter += 1
                                break
                        
                    if valid == False:
                        return valid
                        
                elif new_location_num < old_location_num:
                    #Down the board
                    if old_location[0] > new_location[0]:
                        iter = char_codes[new_location[0].lower()] - 1
                        #Down left
                        for i in range(new_location_num, old_location_num):
                            if board_dict[chars[iter].upper() + str(i)] == "   0" or board_dict[chars[iter].upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                iter += 1
                                continue
                            elif i == old_location_num and board_dict[chars[iter].upper() + str(i)].colour[0] == board_dict[old_location].colour[0]:
                                valid = True
                                iter += 1
                                continue
                            else:
                                valid = False
                                iter += 1
                                break
                            
                    elif old_location[0] < new_location[0]:
                        iter = char_codes[old_location[0].lower()] + 1
                        #Down right
                        for i in range(new_location_num, old_location_num):
                            if board_dict[chars[iter].upper() + str(i)] == "   0" or board_dict[chars[iter].upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                iter -= 1
                                continue
                            elif i == old_location_num and board_dict[chars[iter].upper() + str(i)].colour[0] == board_dict[old_location].colour[0]:
                                valid = True
                                iter -= 1
                                continue
                            else:
                                valid = False
                                iter -= 1
                                break
                        
                    if valid == False:
                        return valid
                      
        else:
            valid = False
            return valid
        
        board_dict[king_location_b].check_move(king_location_b, king_location_b)
        board_dict[king_location_w].check_move(king_location_w, king_location_w)
        
        board.update_board(old_location, new_location, False)
        return valid
        

class Queen(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour[0] + "-Qu"

    def valid_move(self, old_location, new_location):
        if super().valid_input(old_location, new_location) == False:
            valid = False
            return valid
        
        old_location_num = int(old_location[1])
        new_location_num = int(new_location[1])
        
        prev_column = old_location[0]
        new_column = new_location[0]
        
        valid = False
        
        #Check if horizontal/vertical or diagonal
        if abs(old_location_num - new_location_num) == abs(char_codes[prev_column.lower()] - char_codes[new_column.lower()]):
            #If diagonal
            if board_dict[new_location] != "   0" and board_dict[old_location].colour[0] == board_dict[new_location].colour[0]:
                #Check final location
                valid = False
                return valid
            else:
                if new_location_num > old_location_num:
                    #Up the board
                    if old_location[0] > new_location[0]:
                        iter = char_codes[old_location[0].lower()] - 2
                        #Up left
                        for i in range(old_location_num + 1, new_location_num + 1):
                            if board_dict[chars[iter].upper() + str(i)] == "   0" or board_dict[chars[iter].upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                iter -= 1
                                continue
                            elif i == new_location_num and board_dict[chars[iter].upper() + str(i)].colour[0] == board_dict[old_location].colour[0]:
                                valid = True
                                iter -= 1
                                continue
                            else:
                                valid = False
                                iter -= 1
                                break
                            
                    elif old_location[0] < new_location[0]:
                        iter = char_codes[old_location[0].lower()]
                        #Up right
                        for i in range(old_location_num + 1, new_location_num + 1):
                            if board_dict[chars[iter].upper() + str(i)] == "   0" or board_dict[chars[iter].upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                iter += 1
                                continue
                            elif i == old_location_num and board_dict[chars[iter].upper() + str(i)].colour[0] == board_dict[old_location].colour[0]:
                                valid = True
                                iter += 1
                                continue
                            else:
                                valid = False
                                iter += 1
                                break
                        
                    if valid == False:
                        return valid
                        
                elif new_location_num < old_location_num:
                    #Down the board
                    if old_location[0] > new_location[0]:
                        iter = char_codes[new_location[0].lower()] - 1
                        #Down left
                        for i in range(new_location_num, old_location_num):
                            if board_dict[chars[iter].upper() + str(i)] == "   0" or board_dict[chars[iter].upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                iter += 1
                                continue
                            elif i == old_location_num and board_dict[chars[iter].upper() + str(i)].colour[0] == board_dict[old_location].colour[0]:
                                valid = True
                                iter += 1
                                continue
                            else:
                                valid = False
                                iter += 1
                                break
                            
                    elif old_location[0] < new_location[0]:
                        iter = char_codes[new_location[0].lower()] - 1
                        #Down right
                        for i in range(new_location_num, old_location_num):
                            if board_dict[chars[iter].upper() + str(i)] == "   0" or board_dict[chars[iter].upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                iter -= 1
                                continue
                            elif i == old_location_num and board_dict[chars[iter].upper() + str(i)].colour[0] == board_dict[old_location].colour[0]:
                                valid = True
                                iter -= 1
                                continue
                            else:
                                valid = False
                                iter -= 1
                                break
                        
                    if valid == False:
                        return valid
                
                else:
                    valid = False
                    return valid
                
        elif old_location_num == new_location_num or prev_column == new_column:
            #If horizontal/vertical
            if board_dict[new_location] != "   0" and board_dict[old_location].colour[0] == board_dict[new_location].colour[0]:
                #Check final location
                valid = False
                return valid
            else:
                #Down/upwards move
                if prev_column == new_column:
                    #Downwards move
                    if new_location_num < old_location_num:
                        for i in range(new_location_num, old_location_num):
                            if board_dict[prev_column.upper() + str(i)] == "   0":
                                valid = True
                                continue
                            elif i == new_location_num and board_dict[prev_column.upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                continue
                            else:
                                valid = False
                                break
                    #Upwards move
                    elif new_location_num > old_location_num:
                        for i in range(old_location_num + 1, new_location_num + 1):
                            if board_dict[prev_column.upper() + str(i)] == "   0":
                                valid = True
                                continue
                            elif i == new_location_num and board_dict[prev_column.upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                continue
                            else:
                                valid = False
                                break
                            
                    if valid == False:
                        return valid
                        
                elif new_location_num == old_location_num:
                    #Right move
                    if prev_column < new_column:
                        for i in range(char_codes[prev_column.lower()] + 1, char_codes[new_column.lower()] + 1):
                            if board_dict[chars[i - 1].upper() + str(old_location_num)] == "   0":
                                valid = True
                                continue
                            elif i == new_location_num and board_dict[chars[i - 1].upper() + str(old_location_num)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                continue
                            else:
                                valid = False
                                break
                    #Left move
                    elif prev_column > new_column:
                        for i in range(char_codes[new_column.lower()], char_codes[prev_column.lower()]):
                            if board_dict[chars[i - 1].upper() + str(old_location_num)] == "   0":
                                valid = True
                                continue
                            elif i == new_location_num and board_dict[chars[i - 1].upper() + str(old_location_num)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                continue
                            else:
                                valid = False
                                break
                        
                    if valid == False:
                        return valid
                        
                else:
                    valid = False
                    return valid
                
        else:
            valid = False
            return valid
        
        board_dict[king_location_b].check_move(king_location_b, king_location_b)
        board_dict[king_location_w].check_move(king_location_w, king_location_w)
                    
        board.update_board(old_location, new_location, False)
        return valid
            

class King(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour[0] + "-Kg"
        
    def check_move(self, old_location, location):
        valid = False
        
        location_num = int(location[1])
        location_column = location[0].lower()
        
        b_check = False
        w_check = False
        
        if board_dict[old_location].colour[0] == "b":
            #Check all horizontal moves
            for i in range(char_codes[location_column] - 1, 0, -1):
                #Checks row to see if king is in check, starts from current position and checks backwards, to find blockages
                if board_dict[chars[i - 1].upper() + str(location_num)] == board_dict[old_location]:
                    continue
                elif board_dict[chars[i - 1].upper() + str(location_num)] != "   0":
                    if board_dict[chars[i - 1].upper() + str(location_num)].short_name == "w-Qu" or board_dict[chars[i - 1].upper() + str(location_num)].short_name == "w-Rk":
                        b_check = True
                        return b_check
                    elif board_dict[chars[i - 1].upper() + str(location_num)].short_name != "w-Qu" or board_dict[chars[i - 1].upper() + str(location_num)].short_name != "w-Rk":
                        break

            for i in range(char_codes[location_column] + 1, 9):
                #Checks row to see if king is in check, starts from current position and checks forwards, to find blockages
                if board_dict[chars[i - 1].upper() + str(location_num)] == board_dict[old_location]:
                    continue
                elif board_dict[chars[i - 1].upper() + str(location_num)] != "   0":
                    if board_dict[chars[i - 1].upper() + str(location_num)].short_name == "w-Qu" or board_dict[chars[i - 1].upper() + str(location_num)].short_name == "w-Rk":
                        b_check = True
                        return b_check
                    elif board_dict[chars[i - 1].upper() + str(location_num)].short_name != "w-Qu" or board_dict[chars[i - 1].upper() + str(location_num)].short_name != "w-Rk":
                        break
            
            
            #Check all vertical moves
            for i in range(location_num - 1, 0, -1):
                #Checks column to see if king is in check, starts from current position and checks downwards, to find blockages
                if board_dict[location_column.upper() + str(i)] == board_dict[old_location]:
                    continue
                elif board_dict[location_column.upper() + str(i)] != "   0":
                    if board_dict[location_column.upper() + str(i)].short_name == "w-Qu" or board_dict[location_column.upper() + str(i)].short_name == "w-Rk":
                        b_check = True
                        return b_check
                    elif board_dict[location_column.upper() + str(i)].short_name != "w-Qu" or board_dict[location_column.upper() + str(i)].short_name != "w-Rk":
                        break
                
            for i in range(location_num + 1, 9):
                #Checks column to see if king is in check, starts from current position and checks upwards, to find blockages
                if board_dict[location_column.upper() + str(i)] == board_dict[old_location]:
                    continue
                elif board_dict[location_column.upper() + str(i)] != "   0":
                    if board_dict[location_column.upper() + str(i)].short_name == "w-Qu" or board_dict[location_column.upper() + str(i)].short_name == "w-Rk":
                        b_check = True
                        return b_check
                    elif board_dict[location_column.upper() + str(i)].short_name != "w-Qu" or board_dict[location_column.upper() + str(i)].short_name != "w-Rk":
                        break
                
            
            
            #Check all diagonal moves
            dia_num_b = location_num
            dia_col_b = char_codes[location_column]
            directions = ["dr", "ur", "ul", "dl"]
            direction = directions[0]
            dia_range = self.find_range(location_num, location_column)
            for i in range(dia_range + 8):
                if (dia_col_b < 9 and dia_col_b > 0) and (dia_num_b < 9 and dia_num_b > 0):
                    if direction == "dr":
                        if (chars[dia_col_b - 1].upper() + str(dia_num_b)) != location:
                            if board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)] != "   0":
                                if board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name == "w-Bs" or board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name == "w-Qu":
                                    b_check = True
                                    return b_check
                                elif board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name != "w-Bs" or board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name != "w-Qu":
                                    dia_col_b = 9
                                    continue
                            else:
                                dia_col_b += 1
                                dia_num_b -= 1
                                continue
                        else:
                            dia_col_b += 1
                            dia_num_b -= 1
                            continue
                    elif direction == "ur":
                        if (chars[dia_col_b - 1].upper() + str(dia_num_b)) != location:
                            if board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)] != "   0":
                                if board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name == "w-Bs" or board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name == "w-Qu":
                                    b_check = True
                                    return b_check
                                elif board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name != "w-Bs" or board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name != "w-Qu":
                                    dia_col_b = 9
                                    continue
                            else:
                                dia_col_b += 1
                                dia_num_b += 1
                                continue
                        else:
                            dia_col_b += 1
                            dia_num_b += 1
                            continue
                    elif direction == "ul":
                        if (chars[dia_col_b - 1].upper() + str(dia_num_b)) != location:
                            if board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)] != "   0":
                                if board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name == "w-Bs" or board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name == "w-Qu":
                                    b_check = True
                                    return b_check
                                elif board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name != "w-Bs" or board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name != "w-Qu":
                                    dia_col_b = 9
                                    continue
                            else:
                                dia_col_b -= 1
                                dia_num_b += 1
                                continue
                        else:
                            dia_col_b -= 1
                            dia_num_b += 1
                            continue
                    elif direction == "dl":
                        if (chars[dia_col_b - 1].upper() + str(dia_num_b)) != location:
                            if board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)] != "   0":
                                if board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name == "w-Bs" or board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name == "w-Qu":
                                    b_check = True
                                    return b_check
                                elif board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name != "w-Bs" or board_dict[chars[dia_col_b - 1].upper() + str(dia_num_b)].short_name != "w-Qu":
                                    dia_col_b = 9
                                    continue
                            else:
                                dia_col_b -= 1
                                dia_num_b -= 1
                                continue
                        else:
                            dia_col_b -= 1
                            dia_num_b -= 1
                            continue
                else:
                    dia_num_b = location_num
                    dia_col_b = char_codes[location_column]
                    directions.append(directions.pop(0))
                    direction = directions[0]
                    
            
            kn_iter_b = -2
            #Check all knight moves
            for i in range(1, 6):
                if abs(kn_iter_b) == 2:
                    if location_num + 1 < 9 and location_num - 1 > 0 and char_codes[location_column] - 2 > 0 and char_codes[location_column] + 2 < 9:
                        if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num - 1)] != "   0":
                            if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num - 1)].short_name == "w-Kn":
                                b_check = True
                                return b_check
                    if location_num + 1 < 9 and location_num - 1 > 0 and char_codes[location_column] + 2 < 9 and char_codes[location_column] - 2 > 9:
                        if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + 1)] != "   0":
                            if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + 1)].short_name == "w-Kn":
                                b_check = True
                                return b_check
                            
                    kn_iter_b += 1
                        
                elif abs(kn_iter_b) == 1:
                    if location_num - 2 > 0 and location_num + 2 < 9 and char_codes[location_column] + 1 < 9 and char_codes[location_column] - 1 > 0:
                        if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num - 2)] != "   0":
                            if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num - 2)].short_name == "w-Kn":
                                b_check = True
                                return b_check
                    elif location_num + 2 < 9 and location_num - 2 > 0 and char_codes[location_column] + 1 < 9 and char_codes[location_column] - 1 > 0:
                        if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + 2)] != "   0":
                            if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + 2)].short_name == "w-Kn":
                                b_check = True
                                return b_check
                    
                    kn_iter_b += 1
                    
                elif kn_iter_b == 0:
                    kn_iter_b += 1
                        
            #Check pawn moves
            pawn_iter_b = -1
            for i in range(2):
                if board_dict[chars[char_codes[location_column] + pawn_iter_b - 1].upper() + str(location_num - 1)] != "   0":
                    if board_dict[chars[char_codes[location_column] + pawn_iter_b - 1].upper() + str(location_num - 1)].short_name[0:3] == "w-P":
                        b_check = True
                        return b_check
                    else:
                        pawn_iter_b = 1
                        

        elif board_dict[old_location].colour[0] == "w":
            #Check all horizontal moves
            for i in range(char_codes[location_column] - 1, 0, -1):
                #Checks row to see if king is in check, starts from current position and checks backwards, to find blockages
                if board_dict[chars[i - 1].upper() + str(location_num)] == board_dict[old_location]:
                    continue
                elif board_dict[chars[i - 1].upper() + str(location_num)] != "   0":
                    if board_dict[chars[i - 1].upper() + str(location_num)].short_name == "b-Qu" or board_dict[chars[i - 1].upper() + str(location_num)].short_name == "b-Rk":
                        w_check = True
                        return w_check
                    elif board_dict[chars[i - 1].upper() + str(location_num)].short_name != "b-Qu" or board_dict[chars[i - 1].upper() + str(location_num)].short_name != "b-Rk":
                        break

            for i in range(char_codes[location_column] + 1, 9):
                #Checks row to see if king is in check, starts from current position and checks forwards, to find blockages
                if board_dict[chars[i - 1].upper() + str(location_num)] == board_dict[old_location]:
                    continue
                elif board_dict[chars[i - 1].upper() + str(location_num)] != "   0":
                    if board_dict[chars[i - 1].upper() + str(location_num)].short_name == "b-Qu" or board_dict[chars[i - 1].upper() + str(location_num)].short_name == "b-Rk":
                        w_check = True
                        return w_check
                    elif board_dict[chars[i - 1].upper() + str(location_num)].short_name != "b-Qu" or board_dict[chars[i - 1].upper() + str(location_num)].short_name != "b-Rk":
                        break
            
            #Check all vertical moves
            for i in range(location_num - 1, 0, -1):
                #Checks column to see if king is in check, starts from current position and checks downwards, to find blockages
                if board_dict[location_column.upper() + str(i)] == board_dict[old_location]:
                    continue
                elif board_dict[location_column.upper() + str(i)] != "   0":
                    if board_dict[location_column.upper() + str(i)].short_name == "b-Qu" or board_dict[location_column.upper() + str(i)].short_name == "b-Rk":
                        w_check = True
                        return w_check
                    elif board_dict[location_column.upper() + str(i)].short_name != "b-Qu" or board_dict[location_column.upper() + str(i)].short_name != "b-Rk":
                        break
                
            for i in range(location_num + 1, 9):
                #Checks column to see if king is in check, starts from current position and checks upwards, to find blockages
                if board_dict[location_column.upper() + str(i)] == board_dict[old_location]:
                    continue
                elif board_dict[location_column.upper() + str(i)] != "   0":
                    if board_dict[location_column.upper() + str(i)].short_name == "b-Qu" or board_dict[location_column.upper() + str(i)].short_name == "b-Rk":
                        w_check = True
                        return w_check
                    elif board_dict[location_column.upper() + str(i)].short_name != "b-Qu" or board_dict[location_column.upper() + str(i)].short_name != "b-Rk":
                        break
                
            #Check all diagonal moves
            dia_num_w = location_num
            dia_col_w = char_codes[location_column]
            directions = ["dr", "ur", "ul", "dl"]
            direction = directions[0]
            dia_range = self.find_range(location_num, location_column)
            for i in range(dia_range + 8):
                if (dia_col_w < 9 and dia_col_w > 0) and (dia_num_w < 9 and dia_num_w > 0):
                    if direction == "dr":
                        if (chars[dia_col_w - 1].upper() + str(dia_num_w)) != location:
                            if board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)] != "   0":
                                if board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name == "b-Bs" or board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name == "b-Qu":
                                    w_check = True
                                    return w_check
                                elif board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name != "b-Bs" or board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name != "b-Qu":
                                    dia_col_w = 9
                                    continue
                            else:
                                dia_col_w += 1
                                dia_num_w -= 1
                                continue
                        else:
                            dia_col_w += 1
                            dia_num_w -= 1
                            continue
                    elif direction == "ur":
                        if (chars[dia_col_w - 1].upper() + str(dia_num_w)) != location:
                            if board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)] != "   0":
                                if board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name == "b-Bs" or board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name == "b-Qu":
                                    w_check = True
                                    return w_check
                                elif board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name != "b-Bs" or board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name != "b-Qu":
                                    dia_col_w = 9
                                    continue
                            else:
                                dia_col_w += 1
                                dia_num_w += 1
                                continue
                        else:
                            dia_col_w += 1
                            dia_num_w += 1
                            continue
                    elif direction == "ul":
                        if (chars[dia_col_w - 1].upper() + str(dia_num_w)) != location:
                            if board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)] != "   0":
                                if board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name == "b-Bs" or board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name == "b-Qu":
                                    w_check = True
                                    return w_check
                                elif board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name != "b-Bs" or board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name != "b-Qu":
                                    dia_col_w = 9
                                    continue
                            else:
                                dia_col_w -= 1
                                dia_num_w += 1
                                continue
                        else:
                            dia_col_w -= 1
                            dia_num_w += 1
                            continue
                    elif direction == "dl":
                        if (chars[dia_col_w - 1].upper() + str(dia_num_w)) != location:
                            if board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)] != "   0":
                                if board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name == "b-Bs" or board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name == "b-Qu":
                                    w_check = True
                                    return w_check
                                elif board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name != "b-Bs" or board_dict[chars[dia_col_w - 1].upper() + str(dia_num_w)].short_name != "b-Qu":
                                    dia_col_w = 9
                                    continue
                            else:
                                dia_col_w -= 1
                                dia_num_w -= 1
                                continue
                        else:
                            dia_col_w -= 1
                            dia_num_w -= 1
                            continue
                else:
                    dia_num_w = location_num
                    dia_col_w = char_codes[location_column]
                    directions.append(directions.pop(0))
                    direction = directions[0]
                    
            
            kn_iter_w = -2
            #Check all knight moves
            for i in range(1, 6):
                if abs(kn_iter_w) == 2:
                    if location_num + 1 < 9 and location_num - 1 > 0 and char_codes[location_column] - 2 > 0 and char_codes[location_column] + 2 < 9:
                        if board_dict[chars[char_codes[location_column] + kn_iter_w - 1].upper() + str(location_num - 1)] != "   0":
                            if board_dict[chars[char_codes[location_column] + kn_iter_w - 1].upper() + str(location_num - 1)].short_name == "b-Kn":
                                w_check = True
                                return w_check
                    if location_num + 1 < 9 and location_num - 1 > 0 and char_codes[location_column] + 2 < 9 and char_codes[location_column] - 2 > 9:
                        if board_dict[chars[char_codes[location_column] + kn_iter_w - 1].upper() + str(location_num + 1)] != "   0":
                            if board_dict[chars[char_codes[location_column] + kn_iter_w - 1].upper() + str(location_num + 1)].short_name == "b-Kn":
                                w_check = True
                                return w_check
                            
                    kn_iter_w += 1
                        
                elif abs(kn_iter_w) == 1:
                    if location_num - 2 > 0 and location_num + 2 < 9 and char_codes[location_column] + 1 < 9 and char_codes[location_column] - 1 > 0:
                        if board_dict[chars[char_codes[location_column] + kn_iter_w - 1].upper() + str(location_num - 2)] != "   0":
                            if board_dict[chars[char_codes[location_column] + kn_iter_w - 1].upper() + str(location_num - 2)].short_name == "b-Kn":
                                w_check = True
                                return w_check
                    elif location_num + 2 < 9 and location_num - 2 > 0 and char_codes[location_column] + 1 < 9 and char_codes[location_column] - 1 > 0:
                        if board_dict[chars[char_codes[location_column] + kn_iter_w - 1].upper() + str(location_num + 2)] != "   0":
                            if board_dict[chars[char_codes[location_column] + kn_iter_w - 1].upper() + str(location_num + 2)].short_name == "b-Kn":
                                w_check = True
                                return w_check
                    
                    kn_iter_w += 1
                    
                elif kn_iter_w == 0:
                    kn_iter_w += 1
                        
            #Check pawn moves
            pawn_iter_w = -1
            for i in range(2):
                if board_dict[chars[char_codes[location_column] + pawn_iter_w - 1].upper() + str(location_num + 1)] != "   0":
                    if board_dict[chars[char_codes[location_column] + pawn_iter_w - 1].upper() + str(location_num + 1)].short_name[0:3] == "b-P":
                        w_check = True
                        return w_check
                    else:
                        pawn_iter_w = 1
            
        
        #Do for both colours
        if board_dict[old_location].colour[0] == "b":
            return b_check
        elif board_dict[old_location].colour[0] == "w":
            return w_check
            
    
    def valid_move(self, old_location, new_location):
        if super().valid_input(old_location, new_location) == False:
            valid = False
            return valid
        
        old_location_num = int(old_location[1])
        new_location_num = int(new_location[1])
        
        prev_column = old_location[0].lower()
        new_column = new_location[0].lower()
        
        valid = False
        
        global king_valid_moves_b
        global king_valid_moves_w
        
        
                
        if new_location_num == old_location_num + 1 or new_location_num == old_location_num - 1 or new_location_num == old_location_num:
            if char_codes[new_column] == char_codes[prev_column] or char_codes[new_column] + 1 == char_codes[prev_column] or char_codes[new_column] - 1 == char_codes[prev_column]:
                if board_dict[new_location.upper()] == "   0":
                    valid = True
                elif board_dict[new_location.upper()].colour[0] != self.colour[0]:
                    valid = True
                else:
                    valid = False
                    return valid
            else:
                valid = False
                return valid
        
        if self.check_move(old_location, new_location) == False:
            board.update_board(old_location, new_location, False)
            if self.colour[0] == "b":
                king_location_b = new_location.upper()
            elif self.colour[0] == "w":
                king_location_w = new_location.upper()
            player_names[current_move].in_check = True
        else:
            print(f"{player_names[current_move].name}'s King is in check.")
            valid = False
        
        return valid
    
    
    def find_range(self, num, col):
        this_range = 0
        
        if (col == "a" or col == "h") or (num == 1 or num == 8):
            this_range = 7
        elif (col == "b" or col == "g") or (num == 7 or num == 2):
            this_range = 9
        elif (col == "c" or col == "f") or (num == 6 or num == 3):
            this_range = 11
        else:
            this_range = 13
            
        return this_range
        


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

king_valid_moves_b = []
king_valid_moves_w = []

king_location_b = "E8"
king_location_w = "E1"

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
            #Change turn
            current_move = 1
        elif current_move == 1:
            #Change turn
            current_move = 0
        
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


#Check for check after each generic move
#Lock move to blockage or king move if king in check

#Castling
#Pawn edge of board
#Game win
