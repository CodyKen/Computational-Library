import random

g_data_source_dict = {}
g_direct_control = ''       # later it will be changed into a list
FINAL_ANSWER_DICT = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: ' '}

def check_direct_four_letters(a):
    """
     For the control key user input, check whether the number of the letters
     is 4 and every letter is separated by space
    :param a: type is str
    :return: True of False
    """
    if len(a) == 4:
        return True

    print('Make sure the number of the letters is 4 '
          'and every letter is separated by space!')
    return False


def check_direct_identical(a):
    """
    For the control key user input, check whether there are same letters
    :param a: type is str
    :return: True of False
    """
    set_lst = set(a)
    if len(set_lst) == len(a):
        return True

    print("Make sure you didn't enter the same letter!")
    return False


def check_direct_each_len(a):
    """
    For the control key user input, check whether the length of the key is 1
    :param a: type is str
    :return: True of False
    """
    temp_lst = []
    for i in a:
        if len(i) == 1:
            temp_lst.append(i)

    if len(temp_lst) == 4:
        return True

    print('Make sure each control key is one letter!')
    return False


def direction_control_key():
    """
    Allow user to input the key to manipulate the tiles
    Being called in function play(), need to call function check_direct_four_letters(),
    check_direct_identical() and check_direct_each_len() to check whether the input is valid
    Update the g_direct_control_str with the operation key
    :return:None
    """
    while True:
        global g_direct_control

        a = input('Enter the four letters used for '
                  'left, right, up and down move >:')

        # g_direct_control_str = a  # To make the code shorter, use another variable 'a'
        # to represent g_direct_control_str

        if all(x.isalpha() or x.isspace() for x in a):
            a = a.split()

        else:
            print('Please only type in English letters separated by space!')
            continue

        if check_direct_four_letters(a) and check_direct_identical(a) \
                and check_direct_each_len(a):
            g_direct_control = [i.lower() for i in a]       # Now g_direct_control becomes a list
            break


def game_type():
    """
    Let user choose 3-column or 4-column
    Being called in function row_and_column()
    :return: type is str, indicate the type of the game
    """
    while True:
        test_source = ['1', '2', 'q','Q']
        game_type_choose = input('Enter “1” for 8-puzzle, “2” for 15-puzzle'
                                 ' or “q” to end the game >')

        if game_type_choose in test_source:
            return game_type_choose

        print('Make sure you only type in one element, 1 or 2 or q!')


def count_reverse_order(p_lst):
    """
    Count the number of the reverse order numbers of a given list
    Being called in function solvable()
    :param p_lst: type is list, used to calculate the number
    :return: type is int, indicate the number of the reversed order numbers
    """
    n = len(p_lst)
    ans = 0
    for i in range(n):
        for j in range(i):
            if p_lst[j] > p_lst[i]:
                ans += 1

    return ans


def row_and_column():
    """
    Generate the row and column of the puzzle according to the chosen game type
    Being called in function init(), need to call function game_type() before return
    :return: row and column associated with the game type, type is int
    """

    n = game_type()
    if n == '1':
        return 3

    elif n == '2':
        return 4



def solvable(p_list, p_blank_index, p_column):
    """
    Check whether the random puzzle is solvable.
    If column is odd, then the number of reverse order numbers of the random puzzle list must be even
    If column is even, then(the difference between the last line and the blank tile line) + the number
     of the reverse order numbers is even.
    Being invoked in init(), need to call count_reverse_order() before return
    :param p_list: type is list, a copy of the random puzzle list WITHOUT 0 to calculate
        the reverse numbers
    :param p_blank_index: type is int, used to find the line of the blank tile
    :param p_column: type is int, indicate the total column number
    :return: whether puzzle is solvable(T/F)
    """

    p_list.remove(0)
    number = count_reverse_order(p_list)

    if p_column % 2 != 0:  # column is odd

        if number % 2 == 0:  # reverse num is even
            return True
        else:
            return False

    else:                   # column is even
        blank_line = p_blank_index // p_column + 1

        if (number + abs(p_column - blank_line)) % 2 == 0:  # result of this equation is even
            return True
        else:
            return False



def init():
    """
    Generate the solvable random puzzle list according to the chosen game type
    Being called in function generate_puzzle(), need to call function row__and_column() and solvable()
     before return
    :return:chess_list, type is list, random and solvable
    """
    column = row_and_column()
    chess_list = [i for i in range(column ** 2)]

    while True:

        random.shuffle(chess_list)
        p_blank_index = chess_list.index(0)
        p_list = [i for i in chess_list]

        if solvable(p_list, p_blank_index,column):
            chess_list[p_blank_index] = ' '
            return chess_list
        else:
            continue


def generate_puzzle():
    """
    Generate the solvable puzzle dictionary according to the chosen game type
    Being called in function play(), need to call function init() in this function before return
    Update the g_data_source_dict according to the random list generated by function init()
    :return:g_data_source_dict, type is dictionary
    """
    raw_data_source_lst = init()

    dict_len = len(raw_data_source_lst)
    key_list = [i for i in range(dict_len)]
    value_list = [i for i in raw_data_source_lst]

    for key in key_list:
        g_data_source_dict[key] = value_list[key]

    return g_data_source_dict


def adjust_output(p_num):
    """
    Show the final game screen
    Being called in function output()
    :param p_num: type is int, test whether is 2 digits to adjust the gap
    :return: None
    """
    if p_num != ' ' and (p_num - 10) >= 0:
        print(p_num, end='   ')

    else:
        print(p_num, end='    ')


def output(p_dict):
    """
    Show the basic game screen, must invoke adjust_output to adjust the screen again
    Being called in function play()
    :param p_dict: type is dictionary, show the values of this according to the keys
    :return: None
    """
    keys_pool = sorted(p_dict.keys())
    values_pool = [p_dict[i] for i in keys_pool]
    column = len(values_pool) ** (1 / 2)

    n = 0

    for i in values_pool:
        n += 1
        if n % column == 0:
            print(i, end='\n')
        else:
            adjust_output(i)




def check_left(p_blank_key, p_column, p_blank_line):
    """
    Check whether the blank can go left
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, indicate part of the hint or showing the blank cannot go this way
    """
    if (p_blank_key - 1) // p_column + 1 == p_blank_line:
        return 'right -'     # direction where tiles can go
    else:
        return False


def check_right(p_blank_key, p_column, p_blank_line):
    """
    Check whether the blank can go right
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, indicate part of the hint or showing the blank cannot go this way
    """
    if (p_blank_key + 1) // p_column + 1 == p_blank_line:
        return 'left -'     # direction where tiles can go
    else:
        return False


def check_up(p_blank_key, p_column):
    """
    Check whether the blank can go up
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, indicate part of the hint or showing the blank cannot go this way
    """
    if (p_blank_key - p_column) in range(len(g_data_source_dict)):
        return 'down -'     # direction where tiles can go
    else:
        return False



def check_down(p_blank_key, p_column):
    """
    Check whether the blank can go down
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, indicate part of the hint or showing the blank cannot go this way
    """
    if (p_blank_key + p_column) in range(len(g_data_source_dict)):
        return 'up -'      # direction where tiles can go
    else:
        return False



def can_left_right_up_down(p_blank_key, p_column, p_blank_line):
    """
    Form the answer of hint when the blank can go left, right, up, down
    Being called in function user_hint(), need to call small function to check the direction
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, showing the key user can input or showing the blank cannot go this way
    """
    if check_left(p_blank_key, p_column, p_blank_line) \
        and check_right(p_blank_key, p_column, p_blank_line) \
        and check_up(p_blank_key, p_column) \
        and check_down(p_blank_key, p_column):

        ans = (check_left(p_blank_key, p_column, p_blank_line) + g_direct_control[1]) + ',' + \
                 (check_right(p_blank_key, p_column, p_blank_line) + g_direct_control[0]) + ',' + \
                 (check_up(p_blank_key, p_column) + g_direct_control[3]) + ',' + \
                 (check_down(p_blank_key, p_column) + g_direct_control[2])
        return ans

    else:
        return False



def can_left_right_up(p_blank_key, p_column, p_blank_line):
    """
    Form the answer of hint when the blank can go left, right, up
    Being called in function user_hint(), need to call small function to check the direction
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, showing the key user can input or showing the blank cannot go this way
    """
    if check_left(p_blank_key, p_column, p_blank_line) \
        and check_right(p_blank_key, p_column, p_blank_line) \
        and check_up(p_blank_key, p_column):

        ans = (check_left(p_blank_key, p_column, p_blank_line) + g_direct_control[1]) + ',' + \
                 (check_right(p_blank_key, p_column, p_blank_line) + g_direct_control[0]) + ',' + \
                 (check_up(p_blank_key, p_column) + g_direct_control[3])
        return ans

    else:
        return False


def can_left_right_down(p_blank_key, p_column, p_blank_line):
    """
    Form the answer of hint when the blank can go left, right, down
    Being called in function user_hint(), need to call small function to check the direction
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, showing the key user can input or showing the blank cannot go this way
    """
    if check_left(p_blank_key, p_column, p_blank_line) \
        and check_right(p_blank_key, p_column, p_blank_line) \
        and check_down(p_blank_key, p_column):

        ans = (check_left(p_blank_key, p_column, p_blank_line) + g_direct_control[1]) + ',' + \
                 (check_right(p_blank_key, p_column, p_blank_line) + g_direct_control[0]) + ',' + \
                 (check_down(p_blank_key, p_column) + g_direct_control[2])
        return ans

    else:
        return False


def can_left_up_down(p_blank_key, p_column, p_blank_line):
    """
    Form the answer of hint when the blank can go left, up, down
    Being called in function user_hint(), need to call small function to check the direction
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, showing the key user can input or showing the blank cannot go this way
    """
    if check_left(p_blank_key, p_column, p_blank_line) \
        and check_up(p_blank_key, p_column) \
        and check_down(p_blank_key, p_column):

        ans = (check_left(p_blank_key, p_column, p_blank_line) + g_direct_control[1]) + ',' + \
                 (check_up(p_blank_key, p_column) + g_direct_control[3]) + ',' + \
                 (check_down(p_blank_key, p_column) + g_direct_control[2])
        return ans

    else:
        return False


def can_right_up_down(p_blank_key, p_column, p_blank_line):
    """
    Form the answer of hint when the blank can go right, up, down
    Being called in function user_hint(), need to call small function to check the direction
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, showing the key user can input or showing the blank cannot go this way
    """
    if check_right(p_blank_key, p_column, p_blank_line) \
        and check_up(p_blank_key, p_column) \
        and check_down(p_blank_key, p_column):

        ans = (check_right(p_blank_key, p_column, p_blank_line) + g_direct_control[0]) + ',' + \
                 (check_up(p_blank_key, p_column) + g_direct_control[3]) + ',' + \
                 (check_down(p_blank_key, p_column) + g_direct_control[2])
        return ans

    else:
        return False


def can_left_up(p_blank_key, p_column, p_blank_line):
    """
    Form the answer of hint when the blank can go left, up
    Being called in function user_hint(), need to call small function to check the direction
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, showing the key user can input or showing the blank cannot go this way
    """
    if check_left(p_blank_key, p_column, p_blank_line) \
        and check_up(p_blank_key, p_column):

        ans = (check_left(p_blank_key, p_column, p_blank_line) + g_direct_control[1]) + ',' + \
                 (check_up(p_blank_key, p_column) + g_direct_control[3])
        return ans

    else:
        return False


def can_left_down(p_blank_key, p_column, p_blank_line):
    """
    Form the answer of hint when the blank can go left, down
    Being called in function user_hint(), need to call small function to check the direction
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, showing the key user can input or showing the blank cannot go this way
    """
    if check_left(p_blank_key, p_column, p_blank_line) \
        and check_down(p_blank_key, p_column):

        ans = (check_left(p_blank_key, p_column, p_blank_line) + g_direct_control[1]) + ',' + \
                 (check_down(p_blank_key, p_column) + g_direct_control[2])
        return ans

    else:
        return False


def can_right_up(p_blank_key, p_column, p_blank_line):
    """
    Form the answer of hint when the blank can go right, up
    Being called in function user_hint(), need to call small function to check the direction
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, showing the key user can input or showing the blank cannot go this way
    """
    if check_right(p_blank_key, p_column, p_blank_line) \
        and check_up(p_blank_key, p_column):

        ans = (check_right(p_blank_key, p_column, p_blank_line) + g_direct_control[0]) + ',' + \
                 (check_up(p_blank_key, p_column) + g_direct_control[3])
        return ans

    else:
        return False


def can_right_down(p_blank_key, p_column, p_blank_line):
    """
    Form the answer of hint when the blank can go right, down
    Being called in function user_hint(), need to call small function to check the direction
    :param p_blank_key: int, current blank position in g_direct_control_str
    :param p_column: int, the column of the puzzle
    :param p_blank_line: int, current blank line
    :return: str or False, showing the key user can input or showing the blank cannot go this way
    """
    if check_right(p_blank_key, p_column, p_blank_line) \
        and check_down(p_blank_key, p_column):

        ans = (check_right(p_blank_key, p_column, p_blank_line) + g_direct_control[0]) + ',' + \
                 (check_down(p_blank_key, p_column) + g_direct_control[2])
        return ans

    else:
        return False


def user_hint():
    """
    Find the control keys user can input
    Being called in function process_input(), need to call small function to check the direction
    :return: return a str, showing the key user can input
    """
    p_column = len(g_data_source_dict) ** (1 / 2)

    p_blank_key = [k for k, v in g_data_source_dict.items() if v == ' '][0]
    p_blank_line = (p_blank_key // p_column) + 1



    L_R_U_D = can_left_right_up_down(p_blank_key, p_column, p_blank_line)
    L_R_U = can_left_right_up(p_blank_key, p_column, p_blank_line)
    L_R_D = can_left_right_down(p_blank_key, p_column, p_blank_line)
    L_U_D = can_left_up_down(p_blank_key, p_column, p_blank_line)
    R_U_D = can_right_up_down(p_blank_key, p_column, p_blank_line)
    L_U = can_left_up(p_blank_key, p_column, p_blank_line)
    L_D = can_left_down(p_blank_key, p_column, p_blank_line)
    R_U = can_right_up(p_blank_key, p_column, p_blank_line)
    R_D = can_right_down(p_blank_key, p_column, p_blank_line)


    if L_R_U_D: return L_R_U_D
    elif L_R_U: return L_R_U
    elif L_R_D: return L_R_D
    elif L_U_D: return L_U_D
    elif R_U_D: return R_U_D
    elif L_U: return L_U
    elif L_D: return L_D
    elif R_U: return R_U
    elif R_D: return R_D



def move(p_movement):
    """
    Allow user to move the tiles
    Being called in function process_input()
    :param p_movement: str, the control key user input to play this round
    Update the g_data_source_dict with the move
    :return: None
    """
    control_num = g_direct_control.index(p_movement)
    blank_key = [k for k, v in g_data_source_dict.items() if v == ' '][0]
    column = len(g_data_source_dict) ** (1 / 2)
    movement = 0

    # Notice that the direction of blank is the opposite direction of the tiles
    
    if control_num == 0:
        movement = 1
    elif control_num == 1:
        movement = -1
    elif control_num == 2:
        movement = column
    elif control_num == 3:
        movement = -column

    g_data_source_dict[blank_key], g_data_source_dict[blank_key + movement] = \
        g_data_source_dict[blank_key + movement], g_data_source_dict[blank_key]


def character_user_can_input(p_ans):
    """
    Locate the control keys user can input in a string and centrally place them in the list
    Being called in function process_input()
    :param p_ans:
    :return: type is list, indicate the control keys user can input
    """
    source = p_ans.split('-')
    one_user_can_use = [i[0] for i in source[1::]]
    return one_user_can_use


def process_input():
    """
    This function is a combination of hint, user input and user control during the play, which are conducted
    by individual small function
    Being called in function play(), need to call function user_hint(), character_user_can_input()
    and move() before the end
    Update the g_data_source_dict with the user control
    :return: None
    """
    my_ans = user_hint()

    while True:
        user_interact = input('Enter your move (' + str(my_ans) + ')>')

        user_can_input = character_user_can_input(my_ans)
        lower_user_interact = user_interact.lower()        # Make case-insensitive

        if lower_user_interact in user_can_input:
            move(lower_user_interact)
            break

        else:
            print('Invalid input! Make sure only input ONE character shown in the hint(case-insensitive)!')
            continue


def play():
    """
    main function of the game
    :return: None
    """
    print("Welcome to Kinley's puzzle game! In this game, you will "
          "be prompted to reorder the puzzle chess into an ordered one. ")
    while True:
        try:
            generate_puzzle()
            direction_control_key()
            n = 0
            while g_data_source_dict != FINAL_ANSWER_DICT:
                output(g_data_source_dict)
                process_input()
                n += 1

            output(g_data_source_dict)
            print('Congratulations! You have solved the puzzle in',n,'moves!')
        except:
            print('You have quit the game, thank you for playing!')
            break


play()
