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
        
        global king_location_b
        global king_location_w
        
        try:
            if old_location in board_dict:
                chosen_piece = board_dict[old_location]
                #Check if piece is in way
                if chosen_piece.valid_move(old_location, new_location):
                    for line in board.grid:
                        print(*line)
                    return ""
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
    
    def update_board(self, old_location, new_location, new_piece, empty):
        #Update the new location in the displayed board
        #Update the new location in the board dictionary
        
        #1 = Mid move, checks if piece is blocking check
        global taken_piece
        if empty == 1:
            if board_dict[new_location] == "   0":
                board.grid[8 - int(new_location[1])][int(char_codes[new_location[0].lower()]) - 1] = "[" + str(new_location) + ": " + str(board_dict[old_location].short_name) + "]"
            elif board_dict[new_location].colour[0] != board_dict[old_location].colour[0]:
                taken_piece = board_dict[new_location]
            board_dict[new_location] = board_dict[old_location]
            board_dict[old_location] = "   0"
            board.grid[8 - int(old_location[1])][int(char_codes[old_location[0].lower()]) - 1] = "[" + str(old_location) + ": " + "   0" + "]"
        #2 = If piece cannot move due to it blocking check
        elif empty == 2:
            board.grid[8 - int(old_location[1])][int(char_codes[old_location[0].lower()]) - 1] = "[" + str(old_location) + ": " + str(board_dict[old_location].short_name) + "]"
            if board_dict[new_location] == board_dict[old_location]:
                board.grid[8 - int(new_location[1])][int(char_codes[new_location[0].lower()]) - 1] = "[" + str(new_location) + ": " + "   0" + "]"
                board_dict[new_location] = board_dict[new_location]
            else:
                board_dict[new_location] = taken_piece
                board.grid[8 - int(new_location[1])][int(char_codes[new_location[0].lower()]) - 1] = "[" + str(new_location) + ": " + taken_piece.short_name + "]"
        #0 = Generic move
        elif empty == 0:
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
        
    def check_move(self, old_location, location, state):
        valid = False
        
        location_num = int(location[1])
        location_column = location[0].lower()
        
        b_check = False
        w_check = False
        
        global king_valid_moves_w
        global king_valid_moves_b
        global king_location_w
        global king_location_b
        global check_piece_b
        global check_piece_w
        
        if state == True:
            if self.colour[0] == "b":
                king_valid_moves_b = []
                player1.in_check = False
            elif self.colour[0] == "w":
                king_valid_moves_w = []
                player2.in_check = False
            
            king_iter_row = -1
            king_iter_col = -2
        
            for i in range(9):
                king_iter_col += 1
                if king_iter_col == 2:
                    king_iter_col = -1
                    king_iter_row += 1
                    if king_iter_row == 2:
                        break
                        
                if (king_iter_row + location_num < 9 and king_iter_row + location_num > 0) and (king_iter_col + char_codes[location_column] < 9 and king_iter_col + char_codes[location_column] > 0):
                    if self.colour[0] == "b":
                        king_valid_moves_b.append(chars[char_codes[location_column] + (king_iter_col - 1)].upper() + str(location_num + king_iter_row))
                    elif self.colour[0] == "w":
                        king_valid_moves_w.append(chars[char_codes[location_column] + (king_iter_col - 1)].upper() + str(location_num + king_iter_row))
        
        if board_dict[old_location].colour[0] == "b":
            #Check all horizontal moves
            for i in range(char_codes[location_column] - 1, 0, -1):
                #Checks row to see if king is in check, starts from current position and checks backwards, to find blockages
                if board_dict[chars[i - 1].upper() + str(location_num)] == board_dict[old_location]:
                    continue
                elif board_dict[chars[i - 1].upper() + str(location_num)] != "   0":
                    if board_dict[chars[i - 1].upper() + str(location_num)].short_name == "w-Qu" or board_dict[chars[i - 1].upper() + str(location_num)].short_name == "w-Rk":
                        b_check = True
                        check_piece_b = chars[i - 1].upper() + str(location_num)
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
                        check_piece_b = chars[i - 1].upper() + str(location_num)
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
                        check_piece_b = location_column.upper() + str(i)
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
                        check_piece_b = location_column.upper() + str(i)
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
                                    check_piece_b = chars[dia_col_b - 1].upper() + str(dia_num_b)
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
                                    check_piece_b = chars[dia_col_b - 1].upper() + str(dia_num_b)
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
                                    check_piece_b = chars[dia_col_b - 1].upper() + str(dia_num_b)
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
                                    check_piece_b = chars[dia_col_b - 1].upper() + str(dia_num_b)
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
                
            #Check all knight moves
            kn_iter_b = -1
            for i in range(-2, 3):
                #Check bounds
                if i == 0:
                    continue
                
                if abs(i) == 2 and (location_num + i < 9 and location_num + i > 0):
                    if kn_iter_b == -1 and (char_codes[location_column] - 1 < 9 and char_codes[location_column] - 1 > 0):
                        if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + i)] != "   0":
                            if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + i)].short_name == "w-Kn":
                                b_check = True
                                check_piece_b = chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + i)
                                return b_check
                        kn_iter_b = 1
                    elif kn_iter_b == 1 and (char_codes[location_column] + 1 < 9 and char_codes[location_column] + 1 > 0):
                        if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + i)] != "   0":
                            if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + i)].short_name == "w-Kn":
                                b_check = True
                                check_piece_b = chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + i)
                                return b_check
                        kn_iter_b = -2
                elif abs(i) == 1 and (location_num + i < 9 and location_num + i > 0):
                    if kn_iter_b == -2 and (char_codes[location_column] - 2 < 9 and char_codes[location_column] - 2 > 0):
                        if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + i)] != "   0":
                            if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + i)].short_name == "w-Kn":
                                b_check = True
                                check_piece_b = chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + i)
                                return b_check
                        kn_iter_b = 2
                    elif kn_iter_b == 2 and (char_codes[location_column] + 2 < 9 and char_codes[location_column] + 2 > 0):
                        if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + i)] != "   0":
                            if board_dict[chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + i)].short_name == "w-Kn":
                                b_check = True
                                check_piece_b = chars[char_codes[location_column] + kn_iter_b - 1].upper() + str(location_num + i)
                                return b_check
                        
                else:
                    continue
            
            #Check pawn moves
            pawn_iter_b = -1
            for i in range(2):
                if location_num - 1 > 0 and board_dict[chars[char_codes[location_column] + pawn_iter_b - 1].upper() + str(location_num - 1)] != "   0":
                    if board_dict[chars[char_codes[location_column] + pawn_iter_b - 1].upper() + str(location_num - 1)].short_name[0:3] == "w-P":
                        b_check = True
                        check_piece_b = chars[char_codes[location_column] + pawn_iter_b - 1].upper() + str(location_num - 1)
                        return b_check
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
                        check_piece_w = chars[i - 1].upper() + str(location_num)
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
                        check_piece_w = chars[i - 1].upper() + str(location_num)
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
                        check_piece_w = location_column.upper() + str(i)
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
                        check_piece_w = location_column.upper() + str(i)
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
                                    check_piece_w = chars[dia_col_w - 1].upper() + str(dia_num_w)
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
                                    check_piece_w = chars[dia_col_w - 1].upper() + str(dia_num_w)
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
                                    check_piece_w = chars[dia_col_w - 1].upper() + str(dia_num_w)
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
                                    check_piece_w = chars[dia_col_w - 1].upper() + str(dia_num_w)
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
                    if (location_num + kn_iter_w < 9 and location_num + kn_iter_w > 0) and (char_codes[location_column] + 1 < 9 and char_codes[location_column] - 1 > 0):
                        if board_dict[chars[char_codes[location_column] - 1].upper() + str(location_num + kn_iter_w)] != "   0":
                            if board_dict[chars[char_codes[location_column] - 1].upper() + str(location_num + kn_iter_w)].short_name == "b-Kn":
                                w_check = True
                                check_piece_b = chars[char_codes[location_column] - 1].upper() + str(location_num + kn_iter_w)
                                return w_check
                        elif board_dict[chars[char_codes[location_column] + 1].upper() + str(location_num + kn_iter_w)] != "   0":
                            if board_dict[chars[char_codes[location_column] + 1].upper() + str(location_num + kn_iter_w)].short_name == "b-Kn":
                                w_check = True
                                check_piece_b = chars[char_codes[location_column] + 1].upper() + str(location_num + kn_iter_w)
                                return w_check
                        
                elif abs(kn_iter_w) == 1:
                    if (location_num + kn_iter_w < 9 and location_num + kn_iter_w > 0) and (char_codes[location_column] + 2 < 9 and char_codes[location_column] - 2 > 0):
                        if board_dict[chars[char_codes[location_column] - 2].upper() + str(location_num + kn_iter_w)] != "   0":
                            if board_dict[chars[char_codes[location_column] - 2].upper() + str(location_num + kn_iter_w)].short_name == "b-Kn":
                                w_check = True
                                check_piece_b = chars[char_codes[location_column] - 2].upper() + str(location_num + kn_iter_w)
                                return w_check
                        elif board_dict[chars[char_codes[location_column] + 2].upper() + str(location_num + kn_iter_w)] != "   0":
                            if board_dict[chars[char_codes[location_column] + 2].upper() + str(location_num + kn_iter_w)].short_name == "b-Kn":
                                w_check = True
                                check_piece_b = chars[char_codes[location_column] + 2].upper() + str(location_num + kn_iter_w)
                                return w_check
                    
                    kn_iter_w += 1
                    
                elif kn_iter_w == 0:
                    kn_iter_w += 1
                        
            #Check pawn moves
            pawn_iter_w = -1
            for i in range(2):
                if location_num + 1 < 9 and board_dict[chars[char_codes[location_column] + pawn_iter_w - 1].upper() + str(location_num + 1)] != "   0":
                    if board_dict[chars[char_codes[location_column] + pawn_iter_w - 1].upper() + str(location_num + 1)].short_name[0:3] == "b-P":
                        w_check = True
                        check_piece_w = chars[char_codes[location_column] + pawn_iter_w - 1].upper() + str(location_num + 1)
                        return w_check
                pawn_iter_w = 1
                
        #Do for both colours
        if board_dict[old_location].colour[0] == "b":
            return b_check
        elif board_dict[old_location].colour[0] == "w":
            return w_check

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
    
    def can_block(self, block_range, loc):
        global board_keys
        can_block = True
        
        if board_dict[loc].colour[0] == "b":
            for i in block_range:
                #Check pawn blocks
                if board_dict[loc[0] + str(int(loc[1]) + 1)] == "   0" or board_dict[loc[0] + str(int(loc[1]) + 2)] == "   0":
                    continue
                if board_dict[loc[0] + str(int(loc[1]) + 1)].short_name[0:2] == "b-P":
                    can_block = True
                elif board_dict[loc[0] + str(int(loc[1]) + 2)].short_name[0:2] == "b-P":
                    can_block = True
                
                #Check knight blocks
                if char_codes[loc[0].lower()] + 1 <= 8 and int(loc[1]) + 2 <= 8:
                    if board_dict[chars[char_codes[loc[0].lower()] + 1] + str(int(loc[1]) + 2)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] + 1] + str(int(loc[1]) + 2)].short_name == "b-Kn":
                        can_block = True
                if char_codes[loc[0].lower()] + 1 <= 8 and int(loc[1]) - 2 >= 1:
                    if board_dict[chars[char_codes[loc[0].lower()] + 1] + str(int(loc[1]) - 2)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] + 1] + str(int(loc[1]) - 2)].short_name == "b-Kn":
                        can_block = True
                if char_codes[loc[0].lower()] - 1 >= 1 + int(loc[1]) + 2 <= 8:
                    if board_dict[chars[char_codes[loc[0].lower()] - 1] + str(int(loc[1]) + 2)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] - 1] + str(int(loc[1]) + 2)].short_name == "b-Kn":
                        can_block = True
                if char_codes[loc[0].lower()] - 1 >= 1 + int(loc[1]) - 2 >= 1:
                    if board_dict[chars[char_codes[loc[0].lower()] - 1] + str(int(loc[1]) - 2)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] - 1] + str(int(loc[1]) - 2)].short_name == "b-Kn":
                        can_block = True
                    
                if char_codes[loc[0].lower()] + 2 <= 8 and int(loc[1]) + 1 <= 8:
                    if board_dict[chars[char_codes[loc[0].lower()] + 2] + str(int(loc[1]) + 1)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] + 2] + str(int(loc[1]) + 1)].short_name == "b-Kn":
                        can_block = True
                if char_codes[loc[0].lower()] + 2 <= 8 and int(loc[1]) - 1 >= 1:
                    if board_dict[chars[char_codes[loc[0].lower()] + 2] + str(int(loc[1]) - 1)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] + 2] + str(int(loc[1]) - 1)].short_name == "b-Kn":
                        can_block = True
                if char_codes[loc[0].lower()] - 2 >= 1 + int(loc[1]) + 1 <= 8:
                    if board_dict[chars[char_codes[loc[0].lower()] - 2] + str(int(loc[1]) + 1)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] - 2] + str(int(loc[1]) + 1)].short_name == "b-Kn":
                        can_block = True
                if char_codes[loc[0].lower()] - 2 >= 1 + int(loc[1]) - 1 >= 1:
                    if board_dict[chars[char_codes[loc[0].lower()] - 2] + str(int(loc[1]) - 1)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] - 2] + str(int(loc[1]) - 1)].short_name == "b-Kn":
                        can_block = True
                        
                #Check vertical blocks
                for j in char_indices:
                    if board_dict[block_range[i][0] + str(j)] == "   0":
                        continue
                    if board_dict[block_range[i][0] + str(j)].short_name == "b-Rk" or board_dict[block_range[i][0] + str(j)].short_name == "b-Qu":
                        can_block = True
                
                #Check horizontal blocks
                for j in chars:
                    if board_dict[j.upper() + block_range[i][1]] == "   0":
                        continue
                    if board_dict[j.upper() + block_range[i][1]].short_name == "b-Rk" or board_dict[j.upper() + block_range[i][1]].short_name == "b-Qu":
                        can_block = True

                #Check diagonal blocks
                for j in board_keys:
                    if abs(char_codes[block_range[i][0]] - block_range[i][1]) == abs(char_codes[j[0]] - j[1]):
                        if board_dict[j] == "   0":
                            continue
                        if board_dict[j].short_name == "b-Bs" or board_dict[j].short_name == "b-Qu":
                            can_block = True
                            
        elif board_dict[loc].colour[0] == "w":
            for i in block_range:
                #Check pawn blocks
                if board_dict[loc[0] + str(int(loc[1]) - 1)] == "   0" or board_dict[loc[0] - str(int(loc[1]) + 2)] == "   0":
                    continue
                if board_dict[loc[0] + str(int(loc[1]) - 1)].short_name[0:2] == "w-P":
                    can_block = True
                elif board_dict[loc[0] + str(int(loc[1]) - 2)].short_name[0:2] == "w-P":
                    can_block = True
                
                #Check knight blocks
                if char_codes[loc[0].lower()] + 1 <= 8 and int(loc[1]) + 2 <= 8:
                    if board_dict[chars[char_codes[loc[0].lower()] + 1] + str(int(loc[1]) + 2)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] + 1] + str(int(loc[1]) + 2)].short_name == "w-Kn":
                        can_block = True
                if char_codes[loc[0].lower()] + 1 <= 8 and int(loc[1]) - 2 >= 1:
                    if board_dict[chars[char_codes[loc[0].lower()] + 1] + str(int(loc[1]) - 2)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] + 1] + str(int(loc[1]) - 2)].short_name == "w-Kn":
                        can_block = True
                if char_codes[loc[0].lower()] - 1 >= 1 + int(loc[1]) + 2 <= 8:
                    if board_dict[chars[char_codes[loc[0].lower()] - 1] + str(int(loc[1]) + 2)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] - 1] + str(int(loc[1]) + 2)].short_name == "w-Kn":
                        can_block = True
                if char_codes[loc[0].lower()] - 1 >= 1 + int(loc[1]) - 2 >= 1:
                    if board_dict[chars[char_codes[loc[0].lower()] - 1] + str(int(loc[1]) - 2)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] - 1] + str(int(loc[1]) - 2)].short_name == "w-Kn":
                        can_block = True
                    
                if char_codes[loc[0].lower()] + 2 <= 8 and int(loc[1]) + 1 <= 8:
                    if board_dict[chars[char_codes[loc[0].lower()] + 2] + str(int(loc[1]) + 1)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] + 2] + str(int(loc[1]) + 1)].short_name == "w-Kn":
                        can_block = True
                if char_codes[loc[0].lower()] + 2 <= 8 and int(loc[1]) - 1 >= 1:
                    if board_dict[chars[char_codes[loc[0].lower()] + 2] + str(int(loc[1]) - 1)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] + 2] + str(int(loc[1]) - 1)].short_name == "w-Kn":
                        can_block = True
                if char_codes[loc[0].lower()] - 2 >= 1 + int(loc[1]) + 1 <= 8:
                    if board_dict[chars[char_codes[loc[0].lower()] - 2] + str(int(loc[1]) + 1)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] - 2] + str(int(loc[1]) + 1)].short_name == "w-Kn":
                        can_block = True
                if char_codes[loc[0].lower()] - 2 >= 1 + int(loc[1]) - 1 >= 1:
                    if board_dict[chars[char_codes[loc[0].lower()] - 2] + str(int(loc[1]) - 1)] == "   0":
                        continue
                    if board_dict[chars[char_codes[loc[0].lower()] - 2] + str(int(loc[1]) - 1)].short_name == "w-Kn":
                        can_block = True
                        
                #Check vertical blocks
                for j in char_indices:
                    if board_dict[block_range[i][0] + str(j)] == "   0":
                        continue
                    if board_dict[block_range[i][0] + str(j)].short_name == "w-Rk" or board_dict[block_range[i][0] + str(j)].short_name == "w-Qu":
                        can_block = True
                
                #Check horizontal blocks
                for j in chars:
                    if board_dict[j.upper() + block_range[i][1]] == "   0":
                        continue
                    if board_dict[j.upper() + block_range[i][1]].short_name == "w-Rk" or board_dict[j.upper() + block_range[i][1]].short_name == "w-Qu":
                        can_block = True

                #Check diagonal blocks
                for j in board_keys:
                    if abs(char_codes[block_range[i][0]] - block_range[i][1]) == abs(char_codes[j[0]] - j[1]):
                        if board_dict[j] == "   0":
                            continue
                        if board_dict[j].short_name == "w-Bs" or board_dict[j].short_name == "w-Qu":
                            can_block = True

        
        return can_block

#Each piece
class Pawn(Piece):
    def __init__(self, colour, piece_name, pawn_num):
        super().__init__(colour, piece_name)
        self.short_name = colour[0] + "-P" + str(pawn_num)

    def valid_move(self, old_location, new_location):
        #Define set moves
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
        
        if valid == True:
            saved_loc = board_dict[old_location]
            if self.colour[0] == "w":
                if super().check_move(king_location_b, king_location_b, False) == True:
                    player1.in_check = True
                    check_piece_b.append(new_location)
                    print(f"{player1.name}'s King is in check.")
                board.update_board(old_location, new_location, False, 1)
                if super().check_move(king_location_w, king_location_w, False) == True:
                    valid = False
                    board_dict[old_location] = saved_loc
                    board.update_board(old_location, new_location, False, 2)
                    return valid
            elif self.colour[0] == "b":
                if super().check_move(king_location_w, king_location_w, False) == True:
                    player2.in_check = True
                    check_piece_w.append(new_location)
                    print(f"{player2.name}'s King is in check.")
                board.update_board(old_location, new_location, False, 1)
                if super().check_move(king_location_b, king_location_b, False) == True:
                    valid = False
                    board_dict[old_location] = saved_loc
                    board.update_board(old_location, new_location, False, 2)
                    return valid
            
            board_dict[old_location] = saved_loc
            board.update_board(old_location, new_location, False, 0)
        
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
        
        if (old_location[0].lower() == "a" and new_location[0].lower() == "f") or (old_location[0].lower() == "h" and new_location[0].lower() == "d"):
            if self.castling(old_location) == True:
                valid = True
                return valid
        
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
        
        
        if valid == True:
            saved_loc = board_dict[old_location]
            if self.colour[0] == "w":
                if super().check_move(king_location_b, king_location_b, False) == True:
                    player1.in_check = True
                    check_piece_b.append(new_location)
                    print(f"{player1.name}'s King is in check.")
                board.update_board(old_location, new_location, False, 1)
                if super().check_move(king_location_w, king_location_w, False) == True:
                    valid = False
                    board_dict[old_location] = saved_loc
                    board.update_board(old_location, new_location, False, 2)
                    return valid
            elif self.colour[0] == "b":
                if super().check_move(king_location_w, king_location_w, False) == True:
                    player2.in_check = True
                    check_piece_w.append(new_location)
                    print(f"{player2.name}'s King is in check.")
                board.update_board(old_location, new_location, False, 1)
                if super().check_move(king_location_b, king_location_b, False) == True:
                    valid = False
                    board_dict[old_location] = saved_loc
                    board.update_board(old_location, new_location, False, 2)
                    return valid
            
            board_dict[old_location] = saved_loc
            board.update_board(old_location, new_location, False, 0)
        
        return valid
    
    def castling(self, old_location):
        valid = False
        global king_location_b
        global king_location_w
        
        if self.colour[0] == "b" and player1.in_check == False:
            if king_location_b == "E8":
                if old_location.upper() == "A8" and rook_moved_b[0] == False:
                    for i in range(char_codes[king_location_b[0].lower()], char_codes[old_location[0].lower()] + 1):
                        if board_dict[chars[i - 1].upper() + old_location[1]] == "   0" and super().check_move(king_location_b, chars[i - 1].upper() + old_location[1], True) == False:
                            valid = True
                        else:
                            valid = False
                    if valid == True:
                        board_dict["C8"] = board_dict["E8"]
                        board_dict["E8"] = "   0"
                        king_location_b = "C8"
                        board_dict["D8"] = board_dict["A8"]
                        board_dict["A8"] = "   0"
                elif old_location.upper() == "H8" and rook_moved_b[1] == False:
                    for i in range(char_codes[king_location_b[0].lower()], char_codes[old_location[0].lower()] + 1):
                        if board_dict[chars[i - 1].upper() + old_location[1]] == "   0" and super().check_move(king_location_b, chars[i - 1].upper() + old_location[1], True) == False:
                            valid = True
                        else:
                            valid = False
                    if valid == True:
                        board_dict["G8"] = board_dict["E8"]
                        board_dict["E8"] = "   0"
                        king_location_b = "G8"
                        board_dict["E8"] = board_dict["H8"]
                        board_dict["H8"] = "   0"
        elif self.colour[0] == "w" and player2.in_check == False:
            if king_location_b == "E1":
                if old_location.upper() == "A1" and rook_moved_w[0] == False:
                    for i in range(char_codes[king_location_w[0].lower()], char_codes[old_location[0].lower()] + 1):
                        if board_dict[chars[i - 1].upper() + old_location[1]] == "   0" and super().check_move(king_location_w, chars[i - 1].upper() + old_location[1], True) == False:
                            valid = True
                        else:
                            valid = False
                    if valid == True:
                        board_dict["C1"] = board_dict["E1"]
                        board_dict["E1"] = "   0"
                        king_location_b = "C1"
                        board_dict["D1"] = board_dict["A1"]
                        board_dict["A1"] = "   0"
                elif old_location.upper() == "H1" and rook_moved_w[1] == False:
                    for i in range(char_codes[king_location_w[0].lower()], char_codes[old_location[0].lower()] + 1):
                        if board_dict[chars[i - 1].upper() + old_location[1]] == "   0" and super().check_move(king_location_w, chars[i - 1].upper() + old_location[1], True) == False:
                            valid = True
                        else:
                            valid = False
                    if valid == True:
                        board_dict["G1"] = board_dict["E1"]
                        board_dict["E1"] = "   0"
                        king_location_b = "G1"
                        board_dict["E1"] = board_dict["H1"]
                        board_dict["H1"] = "   0"
                
        return valid

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
        
        
        if valid == True:
            saved_loc = board_dict[old_location]
            if self.colour[0] == "w":
                if super().check_move(king_location_b, king_location_b, False) == True:
                    player1.in_check = True
                    check_piece_b.append(new_location)
                    print(f"{player1.name}'s King is in check.")
                board.update_board(old_location, new_location, False, 1)
                if super().check_move(king_location_w, king_location_w, False) == True:
                    valid = False
                    board_dict[old_location] = saved_loc
                    board.update_board(old_location, new_location, False, 2)
                    return valid
            elif self.colour[0] == "b":
                if super().check_move(king_location_w, king_location_w, False) == True:
                    player2.in_check = True
                    check_piece_w.append(new_location)
                    print(f"{player2.name}'s King is in check.")
                board.update_board(old_location, new_location, False, 1)
                if super().check_move(king_location_b, king_location_b, False) == True:
                    valid = False
                    board_dict[old_location] = saved_loc
                    board.update_board(old_location, new_location, False, 2)
                    return valid
            
            board_dict[old_location] = saved_loc
            board.update_board(old_location, new_location, False, 0)
                
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
                        iter = char_codes[new_location[0].lower()]
                        #Down right
                        for i in range(new_location_num, old_location_num):
                            if board_dict[chars[iter - 1].upper() + str(i)] == "   0" or board_dict[chars[iter - 1].upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
                                valid = True
                                iter -= 1
                                continue
                            elif i == old_location_num and board_dict[chars[iter - 1].upper() + str(i)].colour[0] == board_dict[old_location].colour[0]:
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
        
        if valid == True:
            saved_loc = board_dict[old_location]
            if self.colour[0] == "w":
                if super().check_move(king_location_b, king_location_b, False) == True:
                    player1.in_check = True
                    check_piece_b.append(new_location)
                    print(f"{player1.name}'s King is in check.")
                board.update_board(old_location, new_location, False, 1)
                if super().check_move(king_location_w, king_location_w, False) == True:
                    valid = False
                    board_dict[old_location] = saved_loc
                    board.update_board(old_location, new_location, False, 2)
                    return valid
            elif self.colour[0] == "b":
                if super().check_move(king_location_w, king_location_w, False) == True:
                    player2.in_check = True
                    check_piece_w.append(new_location)
                    print(f"{player2.name}'s King is in check.")
                board.update_board(old_location, new_location, False, 1)
                if super().check_move(king_location_b, king_location_b, False) == True:
                    valid = False
                    board_dict[old_location] = saved_loc
                    board.update_board(old_location, new_location, False, 2)
                    return valid
            
            board_dict[old_location] = saved_loc
            board.update_board(old_location, new_location, False, 0)
        
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
        global check_piece_b
        global check_piece_w
        
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
                            elif board_dict[prev_column.upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
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
                            elif board_dict[prev_column.upper() + str(i)].colour[0] != board_dict[old_location].colour[0]:
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
                            elif board_dict[chars[i - 1].upper() + str(old_location_num)].colour[0] != board_dict[old_location].colour[0]:
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
                            elif board_dict[chars[i - 1].upper() + str(old_location_num)].colour[0] != board_dict[old_location].colour[0]:
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
        
        if valid == True:
            saved_loc = board_dict[old_location]
            if self.colour[0] == "w":
                if super().check_move(king_location_b, king_location_b, False) == True:
                    player2.in_check = True
                    check_piece_b = new_location.upper()
                    print(f"{player2.name}'s King is in check.")
                board.update_board(old_location, new_location, False, 1)
                if super().check_move(king_location_w, king_location_w, False) == True:
                    valid = False
                    board_dict[old_location] = saved_loc
                    board.update_board(old_location, new_location, False, 2)
                    return valid
            elif self.colour[0] == "b":
                if super().check_move(king_location_w, king_location_w, False) == True:
                    player1.in_check = True
                    check_piece_w = new_location.upper()
                    print(f"{player1.name}'s King is in check.")
                board.update_board(old_location, new_location, False, 1)
                if super().check_move(king_location_b, king_location_b, False) == True:
                    valid = False
                    board_dict[old_location] = saved_loc
                    board.update_board(old_location, new_location, False, 2)
                    return valid
            
            board_dict[old_location] = saved_loc
            board.update_board(old_location, new_location, False, 0)
                
        return valid
            

class King(Piece):
    def __init__(self, colour, piece_name):
        super().__init__(colour, piece_name)
        self.short_name = colour[0] + "-Kg"
            
    def valid_move(self, old_location, new_location):
        if super().valid_input(old_location, new_location) == False:
            valid = False
            return valid
        
        old_location_num = int(old_location[1])
        new_location_num = int(new_location[1])
        
        prev_column = old_location[0].lower()
        new_column = new_location[0].lower()
        
        valid = False
        
        global king_location_w
        global king_location_b
        global check_piece_w
        global check_piece_b
        
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
        else:
            valid = False
            return valid
        
        if valid == True:
            if self.colour[0] == "w":
                if super().check_move(old_location, new_location, True) == True:
                    player1.in_check = True
                    print(f"{player1.name}'s King is in check.")
                    valid = False
                    return valid
                elif super().check_move(old_location, new_location, False) == False:
                    check_piece_w = ""
                    king_location_w = new_location.upper()
                    player2.in_check = False
            elif self.colour[0] == "b":
                if super().check_move(old_location, new_location, True) == True:
                    player2.in_check = True
                    print(f"{player2.name}'s King is in check.")
                    valid = False
                    return valid
                elif super().check_move(old_location, new_location, False) == False:
                    king_location_b = new_location.upper()
                    check_piece_b = ""
                    player2.in_check = False
            
            board.update_board(old_location, new_location, False, 0)
            
        return valid
        


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
king_is_valid_b = []
king_is_valid_w = []

rook_moved_b = [False, False]
rook_moved_w = [False, False]

#Main game loop
def game_loop():
    global current_move
    global check_piece_b
    global check_piece_w
    global pieces_left_b
    global pieces_left_w
    global can_block_b
    global can_block_w
    global can_take_b
    global can_take_w
    global block_range
    global board_keys
    board_keys = list(board_dict.keys())
    game_state = True
    #Print initial board
    for line in board.grid:
        print(*line)
    
    board_dict[king_location_w].check_move(king_location_w, king_location_w, True)
    board_dict[king_location_b].check_move(king_location_b, king_location_b, True)
        
    #Keep game running, and check if someone has won/lost
    while game_state:
        #Keep track of the current move
        player_names[current_move].__repr__()
        player_names[current_move].choose_move(input(f"{player_names[current_move].name}, choose the current location of your piece: "), input("Now choose a new location for the piece: "))
        king_is_valid_b = {}
        king_is_valid_w = {}
        #Check for white king in check
        for i in king_valid_moves_w:
            if i == king_location_w:
                king_is_valid_w[i] = True
                if board_dict[king_location_w].check_move(king_location_w, king_location_w, False) == True:
                    player1.in_check = True
                    print(f"{player1.name}'s King is in check.")
            king_is_valid_w[i] = board_dict[king_location_w].check_move(king_location_w, i, False)
            if king_is_valid_w[i] == False:
                if board_dict[i] == "   0":
                    continue
                elif board_dict[i].colour[0] == "w":
                    king_is_valid_w[i] = True
            
        #Check for black king in check
        for i in king_valid_moves_b:
            if i == king_location_b:
                king_is_valid_b[i] = True
                if board_dict[king_location_b].check_move(king_location_b, king_location_b, False) == True:
                    player2.in_check = True
                    print(f"{player2.name}'s King is in check.")
                continue
            saved_pos = board_dict[i]
            board_dict[i] = "   0"
            king_is_valid_b[i] = board_dict[king_location_b].check_move(king_location_b, i, False)
            board_dict[i] = saved_pos
            if king_is_valid_b[i] == False:
                if board_dict[i] == "   0":
                    continue
                elif board_dict[i].colour[0] == "b":
                    king_is_valid_b[i] = True
                    
        print([board_dict[i] for i in king_is_valid_b.keys()])
        
        pieces_left_b = [i for i in board_dict if board_dict[i] != "   0" and board_dict[i].colour[0] == "b"]
        pieces_left_w = [i for i in board_dict if board_dict[i] != "   0" and board_dict[i].colour[0] == "w"]
        
        if current_move == 1:
            current_move = 0
            #If king in check, game would end in a win
            if player1.in_check == True:
                #Check if king can move
                if False not in king_is_valid_w.values():
                    #If not, check if the piece putting the king in check can be blocked/taken
                    #if board_dict[check_piece_w].check_move(check_piece_w, check_piece_w, False):
                        #Piece can be taken
                        #continue
                    #else:
                        #Check if piece can be blocked
                    pass
            #If king not in check, game would end as a draw
            elif player1.in_check == False:
                check_piece_w = ""
                #Check if king can move
                if False not in king_is_valid_w.values():
                    #Check if there aren't any other pieces that can move
                    
                    pass
                
            
        elif current_move == 0:
            current_move = 1
            block_range = []
            can_take_b = True
            can_block_b = True
            #If king in check, game would end in a win
            if player2.in_check == True:
                #Check if the piece putting the king in check can be blocked/taken
                if board_dict[check_piece_b].check_move(check_piece_b, check_piece_b, False) == True:
                    #Piece can be taken
                    can_take_b = True
                else:
                    can_take_b = False
                    for i in board_keys:
                        if i == check_piece_b:
                            block_range_lower = board_keys.index(i)
                        elif i == king_location_b:
                            block_range_upper = board_keys.index(i)
                    print(board_keys)
                    print(block_range_lower)
                    print(block_range_upper)
                    #Check if piece can be blocked
                    #Check vertical/horizontal moves (queen and rook)
                    if board_dict[check_piece_b].short_name[2:] == "Rk" or board_dict[check_piece_b].short_name[2:] == "Qu":
                        #Horizontal rook/queen
                        if check_piece_b[1] == king_location_b[1]:
                            if char_codes[check_piece_b[0].lower()] > char_codes[king_location_b[0].lower()] == True:
                                block_range_lower, block_range_upper = block_range_upper, block_range_lower
                                
                            for i in range(block_range_lower + 1, block_range_upper):
                                block_range.append(board_keys[i])
                                
                            if board_dict[check_piece_b].can_block(block_range, check_piece_b) == True:
                                can_block_b = True
                            else:
                                can_block_b = False
                        #Vertical rook/queen
                        elif check_piece_b[0] == king_location_b[0]:
                            if check_piece_b[1] < king_location_b[1]:
                                block_range_lower, block_range_upper = block_range_upper, block_range_lower
                                
                            for i in range(block_range_lower, block_range_upper, 8):
                                if board_keys[i] == block_range_lower or board_keys[i] == block_range_upper:
                                    continue
                                block_range.append(board_keys[i])
                            
                            if board_dict[check_piece_b].can_block(block_range, check_piece_b) == True:
                                can_block_b = True
                            else:
                                can_block_b = False
                                
                    #Check diagonal moves (queen and bishop)
                    elif board_dict[check_piece_b].short_name[2:] == "Qu" or board_dict[check_piece_b].short_name[2:] == "Bs":
                        if abs(char_codes[check_piece_b[0].lower()] - int(check_piece_b[1])) == abs(char_codes[king_location_b[0].lower()] - int(king_location_b[1])):
                            if check_piece_b[1] < king_location_b[1]:
                                block_range_lower, block_range_upper = block_range_upper, block_range_lower
                            
                            if char_codes[board_keys[block_range_lower][0].lower()] > char_codes[board_keys[block_range_upper][0].lower()]:
                                for i in range(block_range_lower, block_range_upper, 7):
                                    if board_keys[i] == block_range_lower or board_keys[i] == block_range_upper:
                                        continue
                                    block_range.append(board_keys[i])
                            elif char_codes[board_keys[block_range_lower][0].lower()] < char_codes[board_keys[block_range_upper][0].lower()]:
                                for i in range(block_range_lower, block_range_upper, 9):
                                    if board_keys[i] == block_range_lower or board_keys[i] == block_range_upper:
                                        continue
                                    block_range.append(board_keys[i])
                            
                            if board_dict[check_piece_b].can_block(block_range, check_piece_b) == True:
                                can_block_b = True
                            else:
                                can_block_b = False
                                

                    #Game ends if check piece cannot be blocked or taken and king is in check and cannot move
                    print(king_is_valid_b.values())
                    if False not in king_is_valid_b.values() and can_block_b == False:
                        player2.game_over = True
                                
            #If king not in check and cannot move, game would end as a draw
            elif player2.in_check == False:
                check_piece_b = ""
                #Check if king can move
                if False not in king_is_valid_b.values():
                    #Check that there aren't any other pieces that can move
                    
                    pass
                    
            
        
        #Check if someone has won/lost
        if player1.game_over == True:
            game_state = False
            return player2.name + " wins!"
        elif player2.game_over == True:
            game_state = False
            return player1.name + " wins!"
        
    return ""

#Set game variables
board = Board()
#Current move 
current_move = 0
player1 = Player("white", input("Player 1 (White), choose your name: "), 0)
player2 = Player("black", input("Player 2 (Black), choose your name: "), 1)
player_names = [player1, player2]
board_dict = {}
past_moves = []
check_piece_b = ""
check_piece_w = ""
taken_piece = ""
can_block_b = False
can_block_w = False
can_take_b = False
can_take_w = False
block_range = []
board_keys = []

board.create_board()

game_loop()

#Draw determination, if all items in valid mvoes are true then check if king is in check, if yes check if pieces putting king in check can be taken

#Check blockages
#Check if no piece can move

#Castling
#Pawn edge of board
#En passant
#Game win
#Draw by repetition?