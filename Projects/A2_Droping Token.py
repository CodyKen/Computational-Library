import turtle

g_data_source = [0] * 64
g_order_pool = []
g_move_pool = []
g_columns = []
g_x = -999
g_flag = 1 # To freeze the game when there is a ending game result



def onMouseMotion(event):
    """
    Use the internal function of turtle to keep track of mouse motion
    Update the g_x according to the current x position of mouse
    :param event
    :return:None
    """
    global g_x
    x, y = event.x, event.y
    g_x = x


def onMouseClick(x, y):
    """
    The main function of playing the game. Get the column users click by
     the x coordinate of mouse click, then show the ball and play the game.
     Update g_order_pool according to the column user picked
     Invoke function locate(), write_title(), draw_normal(), draw_win()
    :param x: x coordinate of mouse click
    :param y: y coordinate of mouse click
    """
    global g_flag
    try:
        if g_data_source[get_order(x) - 1] == 0 and g_flag == 1:
            g_order_pool.append(get_order(x))
            locate()
            write_title()
            draw_normal()

            if stop():
                count = -1
                for i in g_data_source:
                    count += 1
                    if i == 9:
                        write_title()
                        draw_win(count)
                        g_flag = 0  #Freeze the game

    except:
        return


def write_title():
    """
    Change title correspondingly.
    Being called in function onMouseClick()
    Invoke function stop()
    Being invoked in function onMouseClick()
    :return:None
    """
    if not stop() and len(g_order_pool) % 2 != 0:
        turtle.title('CONNECT 4 - Player 2 Turn')
    elif not stop() and len(g_order_pool) % 2 == 0:
        turtle.title('CONNECT 4 - Player 1 Turn')
    elif stop() and len(g_order_pool) % 2 != 0:
        turtle.title('Winner ! Player 1')
    elif stop() and len(g_order_pool) % 2 == 0:
        turtle.title('Winner ! Player 2')
    elif 0 not in g_data_source:
        turtle.title('Game Tied !')


def get_orders():
    """
    Start the whole game.
    Invoke function onMouseClick()
    :return: None
    """
    s = turtle.Screen()
    turtle.title('CONNECT 4 - Player 1 Turn')
    s.onclick(onMouseClick)


def draw_normal():
    """
    When there is no winner. Draw the balls.
    Being invoked in function onMouseClick()
    :return: None
    """
    pos = g_move_pool[len(g_move_pool) - 1]

    s = turtle.Screen()
    s.tracer(0)

    if len(g_order_pool) % 2 != 0:

        t = turtle.Turtle('circle')
        t.color('blue')
        t.shapesize(3, 3)
        t.up()
        t.goto(calculate_Xcoordinate(pos), calculate_Ycoordinate(pos))

        s.update()
        s.tracer(1)

    else:

        t = turtle.Turtle('circle')
        t.color('purple')
        t.shapesize(3, 3)
        t.up()
        t.goto(calculate_Xcoordinate(pos), calculate_Ycoordinate(pos))

        s.update()
        s.tracer(1)


def draw_win(p_pos):
    """
    When there is a winner, draw the balls and outline the balls.
    Being called in function onMouseClick()
    :param p_pos:
    :return:
    """
    s = turtle.Screen()
    s.tracer(0)

    if len(g_order_pool) % 2 != 0:  # Player1 wins
        t = turtle.Turtle('circle')
        t.color('blue')
        t.color('red', t.color()[1])
        t.shapesize(3, 3, 10)
        t.up()
        t.goto(calculate_Xcoordinate(p_pos), calculate_Ycoordinate(p_pos))

    elif len(g_order_pool) % 2 == 0:  # Player2 wins
        t = turtle.Turtle('circle')
        t.color('purple')
        t.color('red', t.color()[1])
        t.shapesize(3, 3, 10)
        t.up()
        t.goto(calculate_Xcoordinate(p_pos), calculate_Ycoordinate(p_pos))

    s.update()
    s.tracer(1)


def createColumnTracker(p_x, p_y, p_num, p_margin):
    """
    Create the 8 column trackers by specific size and equal gap.
    :param p_x: x coordinate of the first one
    :param p_y: y coordinate of the first one
    :param p_num: The number of the columns
    :param p_margin: the gap
    :return: A list of columns, being used in function checkcolumn()
    """
    cols = []

    t = turtle.Turtle('square')
    t.up()
    t.shapesize(1, 3, 5)  # Create each column trackers with 3-time wider, 5-pixel border.

    each_size = 60 + p_margin
    for i in range(p_num):
        t.goto(p_x + i * each_size, p_y)
        cols.append(t)
        t = t.clone()

    return cols


def checkcolumn():
    """
    Outline the columns correspondingly by the position of the mouse
    :return: None
    """
    for t in g_columns:
        cx = t.xcor()  # center x position
        if abs(g_x - cx) <= 30:
            if t.color()[0] == t.color()[1]:  # if not outlined
                t.color('blue', t.color()[1])
        else:
            if t.color()[0] != t.color()[1]:  # if outlined
                t.color(t.color()[1])

    s.ontimer(checkcolumn, 100)

    return


def calculate_Xcoordinate(p_pos):
    """
    Convert the column number into the turtle x coordinate.
    pos means the index of the element in the g_data_source.
    a means the column of this element.
    x means the x coordinate of the position of the ball .
    :param p_pos: index of the element in the g_data_source
    :return:x coordinate
    """
    a = p_pos % 8

    if a == 0:
        return 40
    elif a == 1:
        return 120
    elif a == 2:
        return 200
    elif a == 3:
        return 280
    elif a == 4:
        return 360
    elif a == 5:
        return 440
    elif a == 6:
        return 520
    elif a == 7:
        return 600



def calculate_Ycoordinate(p_pos):
    """
    Convert the column number into the turtle y coordinate.
    pos means the index of the element in the g_data_source.
    a means the column of this element.
    x means the x coordinate of the position of the ball .
    :param p_pos: index of the element in the g_data_source
    :return:y coordinate
    """
    a = p_pos // 8

    if a == 0:
        return 543.125
    elif a == 1:
        return 476.25
    elif a == 2:
        return 409.375
    elif a == 3:
        return 342.5
    elif a == 4:
        return 271.625
    elif a == 5:
        return 203.75
    elif a == 6:
        return 136.875
    elif a == 7:
        return 70



def get_order(p_x):
    """
    Get the coordinate of the user click and covert it into the column(if any)

    :param p_x: x coordinate of the user click
    :return: column of the user click
    """

    if abs(p_x - 40) <= 30:
        return 1
    elif abs(p_x - 120) <= 30:
        return 2
    elif abs(p_x - 200) <= 30:
        return 3
    elif abs(p_x - 280) <= 30:
        return 4
    elif abs(p_x - 360) <= 30:
        return 5
    elif abs(p_x - 440) <= 30:
        return 6
    elif abs(p_x - 520) <= 30:
        return 7
    elif abs(p_x - 600) <= 30:
        return 8



def get_first_pos_index():
    """
    Get the column user clicked in g_order_pool and get the first position index in
    the g_data_source.
    Being called in function locate()
    :return: first position index
    """
    target_column = g_order_pool[len(g_order_pool) - 1]
    first_pos_index = target_column - 1
    return first_pos_index


def check_stop_drop(p_pos):
    """
    Check whether the ball will continue to drop or not to get
    the index of the element to be changed in g_data_source.
    Being invoked in function locate()
    :param p_pos: the index of the first element in this column.
    :return: Bool
    """
    if p_pos >= 56:
        return False
    elif g_data_source[(p_pos + 8)] == 1 or g_data_source[(p_pos + 8)] == 2:
        return False
    else:
        return True


def get_which_user():
    """
    Detect which player should drop the ball.
    Being called in function locate()
    :return: 1 and 2 correspond to the first and second player, respectively.
    """
    return 1 if len(g_order_pool) % 2 != 0 else 2


def locate():
    """
    Get the index of the element to be changed in g_data_source.
    Update the g_move_pool according to this index.
    Update the g_data_source according to the player.
    Invoke function get_first_pos_index(), check_stop_drop(), get_which_user()
    Being called in function onMouseClick()
    :return: None
    """
    p_pos = get_first_pos_index()
    while check_stop_drop(p_pos):
        p_pos += 8
    g_move_pool.append(p_pos)
    g_data_source[p_pos] = get_which_user()



def check_vertical(p_pos):
    """
    Check vertical win condition
    Being called in function stop()
    :param p_pos: the index of the newest ball in g_data_source
    :return: If vertical win, return the list of index of the 4 winning ball in g_data_source
            else return False
    """
    check_lst1 = [p_pos, p_pos + 8, p_pos + 16, p_pos + 24]
    check_lst2 = []
    check_lst3 = []
    try:
        for i in check_lst1:
            check_lst2.append(g_data_source[i])
        a = set(check_lst2)
        if len(a) == 1:  # In 4 downward return True(stop)
            check_lst3.append(p_pos)
            check_lst3.append(p_pos + 8)
            check_lst3.append(p_pos + 16)
            check_lst3.append(p_pos + 24)

            return check_lst3
        else:
            return False

    except:
        return False  # If beyond the chess_table return False


def get_line(p_pos):
    """
    Get the line number of the ball.
    Being called in function check_line()
    :param p_pos:the index of the newest ball in g-data_source
    :return: The number of line
    """
    if p_pos in range(0, 8):
        return 1
    elif p_pos in range(8, 16):
        return 2
    elif p_pos in range(16, 24):
        return 3
    elif p_pos in range(24, 32):
        return 4
    elif p_pos in range(32, 40):
        return 5
    elif p_pos in range(40, 48):
        return 6
    elif p_pos in range(48, 56):
        return 7
    elif p_pos in range(56, 64):
        return 8
    elif p_pos >= 64:
        return False


def check_line(p_pos):
    """
    Check horizontal win condition.
    Invoke function get_line()
    Being invoked in function stop()
    :param p_pos: the index of the newest ball in g_data_source
    :return: If horizontal win, return the list of index of the 4 winning ball in g_data_source
            else return False
    """
    line = get_line(p_pos)
    check_lst1 = []
    check_lst2 = []
    check_lst3 = []
    value = g_data_source[p_pos]
    for i in range(line * 8 - 8, line * 8):
        check_lst1.append(g_data_source[i])  # slice every ele in the line of pos into check_lst1
    count = 0
    for i in check_lst1:
        count += 1
        if i == value:
            check_lst2.append(count)
    for i in check_lst2:
        if (i + 1) in check_lst2 and (i + 2) in check_lst2 and (i + 3) in check_lst2:
            check_lst3.append(8 * (line - 1) + i)
            check_lst3.append(8 * (line - 1) + i + 1)
            check_lst3.append(8 * (line - 1) + i + 2)
            check_lst3.append(8 * (line - 1) + i + 3)

            return check_lst3
    return False


def get_diagonal_leftup_rightdown(pos):
    """
    Get the list of all the element's index of the leftup_rightdown diagonal of the ball.
    Being called in function check_leftup_rightdown_diagonal()
    :param p_pos:the index of the newest ball in g-data_source
    :return: the list of all the element's index of the leftup_rightdown diagonal of the ball
    """
    A = [7]
    B = [6, 15]
    C = [5, 14, 23]
    D = [4, 13, 22, 31]
    E = [3, 12, 21, 30, 39]
    F = [2, 11, 20, 29, 38, 47]
    G = [1, 10, 19, 28, 37, 46, 55]
    H = [0, 9, 18, 27, 36, 45, 54, 63]
    I = [8, 17, 26, 35, 44, 53, 62]
    J = [16, 25, 34, 43, 52, 61]
    K = [24, 33, 42, 51, 60]
    L = [32, 41, 50, 59]
    M = [40, 49, 58]
    N = [48, 57]
    O = [56]

    if pos in A:
        return A
    elif pos in B:
        return B
    elif pos in C:
        return C
    elif pos in D:
        return D
    elif pos in E:
        return E
    elif pos in F:
        return F
    elif pos in G:
        return G
    elif pos in H:
        return H
    elif pos in I:
        return I
    elif pos in J:
        return J
    elif pos in K:
        return K
    elif pos in L:
        return L
    elif pos in M:
        return M
    elif pos in N:
        return N
    elif pos in O:
        return O


def check_leftup_rightdown_diagonal(p_pos):
    """
    Check leftup_rightdown win condition.
    Invoke function get_diagonal_leftup_rightdown()
    Being invoked in function stop()
    :param p_pos: the index of the newest ball in g_data_source
    :return: If diagonal win, return the list of index of the 4 winning ball in g_data_source
            else return False
    """
    diagonal = get_diagonal_leftup_rightdown(p_pos)
    check_lst1 = []
    check_lst2 = []
    check_lst3 = []
    value = g_data_source[p_pos]
    for i in diagonal:
        check_lst1.append(g_data_source[i])  # slice every ele in the leftup_right_down diagonal of pos into check_lst1
    count = 0
    for i in check_lst1:
        count += 1
        if i == value:
            check_lst2.append(count)
    for i in check_lst2:
        if (i + 1) in check_lst2 and (i + 2) in check_lst2 and (i + 3) in check_lst2:
            check_lst3.append(diagonal[i - 1])
            check_lst3.append(diagonal[i])
            check_lst3.append(diagonal[i + 1])
            check_lst3.append(diagonal[i + 2])

            return check_lst3
    return False


def get_diagonal_rightup_leftdown(p_pos):
    """
    Get the list of all the element's index of the rightup_leftdown diagonal of the ball.
    Being called in function check_rightup_leftdown_diagonal()
    :param p_pos:the index of the newest ball in g-data_source
    :return: the list of all the element's index of the rightup_leftdown diagonal of the ball
    """
    A = [0]
    B = [1, 8]
    C = [2, 9, 16]
    D = [3, 10, 17, 24]
    E = [4, 11, 18, 25, 32]
    F = [5, 12, 19, 26, 33, 40]
    G = [6, 13, 20, 27, 34, 41, 48]
    H = [7, 14, 21, 28, 35, 42, 49, 56]
    I = [15, 22, 29, 36, 43, 50, 57]
    J = [23, 30, 37, 44, 51, 58]
    K = [31, 38, 45, 52, 59]
    L = [39, 46, 53, 60]
    M = [47, 54, 61]
    N = [55, 62]
    O = [63]

    if p_pos in A:
        return A
    elif p_pos in B:
        return B
    elif p_pos in C:
        return C
    elif p_pos in D:
        return D
    elif p_pos in E:
        return E
    elif p_pos in F:
        return F
    elif p_pos in G:
        return G
    elif p_pos in H:
        return H
    elif p_pos in I:
        return I
    elif p_pos in J:
        return J
    elif p_pos in K:
        return K
    elif p_pos in L:
        return L
    elif p_pos in M:
        return M
    elif p_pos in N:
        return N
    elif p_pos in O:
        return O


def check_rightup_leftdown_diagonal(p_pos):
    """
    Check rightup_leftdown win condition.
    Invoke function get_diagonal_rightup_leftdown()
    Being invoked in function stop()
    :param p_pos: the index of the newest ball in g_data_source
    :return: If diagonal win, return the list of index of the 4 winning ball in g_data_source
            else return False
    """
    diagonal = get_diagonal_rightup_leftdown(p_pos)
    check_lst1 = []
    check_lst2 = []
    check_lst3 = []
    value = g_data_source[p_pos]
    for i in diagonal:
        check_lst1.append(g_data_source[i])  # slice every ele in the rightup_leftdown diagonal of pos into check_lst1
    count = 0
    for i in check_lst1:
        count += 1
        if i == value:
            check_lst2.append(count)
    for i in check_lst2:
        if (i + 1) in check_lst2 and (i + 2) in check_lst2 and (i + 3) in check_lst2:
            check_lst3.append(diagonal[i - 1])
            check_lst3.append(diagonal[i])
            check_lst3.append(diagonal[i + 1])
            check_lst3.append(diagonal[i + 2])

            return check_lst3
    return False


def stop():
    """
    Check whether to stop the whole game by the winning check condition or tied condition.
    Invoke function check_line(), check_vertical(), check_leftup_rightdown_diagonal(),
        check_rightup_leftdown_diagonal()
    Being  called in function onMouseClick()
    :return: True or False, corresponding to whether stop the game
    """
    if len(g_move_pool) == 0:      # In case the game stop at the very beginning
        return False
    elif 0 not in g_data_source:     # game tied
        return True
    elif check_line(g_move_pool[len(g_move_pool) - 1]):
        for i in check_line(g_move_pool[len(g_move_pool) - 1]):
            g_data_source[i - 1] = 9
        return True
    elif check_vertical(g_move_pool[len(g_move_pool) - 1]):
        for i in check_vertical(g_move_pool[len(g_move_pool) - 1]):
            g_data_source[i] = 9
        return True
    elif check_leftup_rightdown_diagonal(g_move_pool[len(g_move_pool) - 1]):
        for i in check_leftup_rightdown_diagonal(g_move_pool[len(g_move_pool) - 1]):
            g_data_source[i] = 9
        return True
    elif check_rightup_leftdown_diagonal(g_move_pool[len(g_move_pool) - 1]):
        for i in check_rightup_leftdown_diagonal(g_move_pool[len(g_move_pool) - 1]):
            g_data_source[i] = 9
        return True
    else:
        return False


if __name__ == '__main__':
    s = turtle.Screen()
    s.setup(660, 700)
    s.setworldcoordinates(0, 0, 660, 700)
    get_orders()
    c = s.getcanvas()
    c.bind('<Motion>', onMouseMotion)

    g_columns = createColumnTracker(40, 20, 8, 20)

    checkcolumn()
    s.mainloop()
