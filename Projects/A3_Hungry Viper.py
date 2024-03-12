import turtle
import random
import itertools
from functools import partial

g_snake = turtle.Turtle('square')  # initial snake
g_monster = turtle.Turtle('square')  # initial monster
g_stop = False  # True means stop the game, False means continue
g_last_move = None  # remember the last move of the snake
g_contact = 0  # record the contact
g_reality_time = 0  # record the timing
g_numbers_pool = []  # food number pool
g_coordinates = []  # food number coordinate
g_real_tail_length = 5  # real tail length
g_short_tail_length = 0  # short tail length
g_stamps = []  # stamps pool
g_stamps_pos = []  # stamps coordinate pool
g_keypressed = 'Paused'  # initial command is paused
g_window = turtle.Screen()  # initial the game window
g_note = turtle.Turtle()  # initial the game status bar
g_reminder = turtle.Turtle()  # initial the welcome reminder

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = \
    "Up", "Down", "Left", "Right", "space"

HEADING_BY_KEY = {KEY_UP: 90, KEY_DOWN: 270, KEY_LEFT: 180, KEY_RIGHT: 0}


def set_initial_outlook():
    """
    Set the initial outlook of the game, update g_window, g_snake, g_monster, g_reminder
    :return: None
    """
    global g_window, g_note, g_reminder

    # set window screen
    g_window.setup(580, 660)
    g_window.tracer(0)

    # set status area
    status_window = turtle.Turtle()
    status_window.pensize(2)
    status_window.goto(250, 210)
    status_window.clear()
    status_window.goto(250, 290)
    status_window.goto(-250, 290)
    status_window.goto(-250, 210)
    status_window.goto(250, 210)

    # set play area
    status_window.goto(250, -290)
    status_window.goto(-250, -290)
    status_window.goto(-250, 210)
    status_window.hideturtle()

    # set initial snake
    g_snake.color('red')
    g_snake.left(90)
    g_snake.up()

    # set initial monster
    g_monster.color('purple')
    g_monster.up()
    g_monster_x = [random.randrange(-210, -110, 20), random.randrange(110, 210, 20)]
    g_monster_y = [random.randrange(-210, -110, 20), random.randrange(110, 210, 20)]
    g_monster.goto(random.choice(g_monster_x), random.choice(g_monster_y))

    # write the status note
    update_status()

    # write reminder
    g_reminder.hideturtle()
    g_reminder.up()
    g_reminder.goto(-80, 110)
    g_reminder.write('Snake by CodyKen\nClick anywhere to start\nHave fun!', font=('Arial', 16, 'bold'))

    # All setting done
    g_window.update()


def update_status():
    """
    Update the status bar thorough out the game. Update g_window, g_note
    Being called in set_initial_outlook(), key_space(), on_arrow_key_space(), snake()
    :return: None
    """
    global g_window, g_note, g_reality_time
    g_note.clear()
    g_note.hideturtle()
    g_note.up()
    g_note.goto(-190, 240)
    g_note.write("Contact:  " + str(g_contact) + "    Time:  " + str(g_reality_time) +
                 "    Motion:  " + str(g_keypressed), align="left", font=("Arial", 16, "bold"))
    g_window.update()


def set_numbers():
    """
    Set the food number and randomly put them on the screen,
    Being called in game_start()
    :return: None
    """
    global g_coordinates
    coordinate_pool = list(itertools.product(range(-240, 240, 20), range(-280, 200, 20)))
    g_coordinates = random.sample(coordinate_pool, 5)
    # each of the turtle draws the number
    for i in range(5):
        t = turtle.Turtle()
        g_numbers_pool.append(t)
        t.up()
        t.hideturtle()
        t.goto(g_coordinates[i][0] - 0.9, g_coordinates[i][1] - 7.9)
        t.write(str(i + 1), font=2)


def eat_numbers():
    """
    Being called when the snake eat the food item, update the true tail length after eating the numbers
    Being called in snake()
    :return: None
    """
    global g_numbers_pool, g_real_tail_length
    for i in range(5):
        if g_numbers_pool[i] == False:
            continue
        elif g_numbers_pool[i] == None:
            continue
        elif g_snake.distance(g_numbers_pool[i].position()) <= 10:
            g_numbers_pool[i].clear()
            g_numbers_pool[i] = False
            g_real_tail_length += i + 1
            return
    return


def get_number_not_hidden_not_eaten():
    """
    Get through the number list to check food item that can be operated
    Being called in hide_show_numbers()
    :return:  The list containing all the number that can be operated
    """
    sample_lst = []
    count = 0
    for i in g_numbers_pool:
        count += 1
        if i != False:
            sample_lst.append(count)
    return sample_lst


def hide_show_numbers():
    """
    Hide the number if it is unhidden, shou the number if it is hidden, all random
    Being called in game_start(), call the get_number_not_hidden_not_eaten()
    :return: None
    """
    if g_numbers_pool == [False] * 5 or g_monster.distance(g_snake.position()) <= 15:
        return
    else:
        food_number = random.choice(get_number_not_hidden_not_eaten())

        if g_numbers_pool[food_number - 1] == None:
            tt = turtle.Turtle()
            tt.up()
            tt.hideturtle()
            tt.goto(g_coordinates[food_number - 1][0] - 0.9, g_coordinates[food_number - 1][1] - 7.9)
            tt.write(str(food_number), font=2)
            tt.goto(g_coordinates[food_number - 1][0] + 0.9, g_coordinates[food_number - 1][1] + 7.9)
            g_numbers_pool[food_number - 1] = tt

        else:
            g_numbers_pool[food_number - 1].clear()
            g_numbers_pool[food_number - 1] = None
        g_window.ontimer(hide_show_numbers, 5000)


def key_space():
    """
    change the motion of the snake after pressing the key space, update g_keypressed
    Call the update_status()
    :return: None
    """
    global g_last_move, g_keypressed
    # check game over
    if not g_stop:
        if g_keypressed == 'Paused':
            g_keypressed = g_last_move
            update_status()
            g_window.update()

        else:
            g_last_move = g_keypressed
            g_keypressed = 'Paused'
            update_status()
            g_window.update()


def update_time():
    """
    Update the timing in the status bar, update g_note
    Being called in game_start()
    :return: None
    """
    global g_note, g_reality_time
    if g_stop:
        return
    else:
        g_reality_time += 1
        g_note.clear()
        g_note.hideturtle()
        g_note.up()
        g_note.goto(-190, 240)
        g_note.write("Contact:  " + str(g_contact) + "    Time:  " + str(g_reality_time) +
                     "    Motion:  " + str(g_keypressed), align="left", font=("Arial", 16, "bold"))
        g_window.ontimer(update_time, 1000)


def on_arrow_key_pressed(p_key):
    """
    Change the heading of the snake after pressing the key, update g_keypressed
    Call update_status(), set_snake_heading(p)
    :param p_key:
    :return:None
    """
    global g_keypressed
    # check stop
    if g_stop:
        return
    else:
        g_keypressed = p_key
        set_snake_heading(p_key)
        update_status()


def set_snake_heading(p_key):
    """
    Change the heading of the snake
    Being called in on_arrow_key_pressed(p)
    :param p_key: key being pressed
    :return: None
    """
    if p_key in HEADING_BY_KEY.keys():
        g_snake.setheading(HEADING_BY_KEY[p_key])


def snake():
    """
    The main function of snake, in charge of the snake move, eat, grow
    Update g_snake, g_stamps, g_stamps_pos, g_short_tail_length,
    Being called in game_start(), call test_border(), test_cross_itself(), update_status(),
    eat_numbers(), snake_grow(), draw_win(), snake_normal_move()
    :return: None
    """
    global g_stop, g_snake, g_stamps, g_stamps_pos, \
        g_keypressed, g_short_tail_length, g_real_tail_length
    # check stop
    if g_stop:
        return

    if test_border() and test_cross_itself():
        # find the state of the snake and choose the way it should move.
        if g_keypressed == "Paused":
            update_status()
            g_window.ontimer(snake, 200)
        else:
            eat_numbers()
            # check whether extending
            if g_short_tail_length < g_real_tail_length:
                snake_grow()
                update_status()
                g_window.ontimer(snake, 400)
            else:
                # print(g_turtle_numbers)
                # check whether winning or not
                if g_numbers_pool == [False] * 5:
                    draw_win()
                    g_stop = True
                else:
                    snake_normal_move()
                    update_status()
                    # print(g_delay,'g_delay, fast')
                    g_window.ontimer(snake, 200)
    else:
        update_status()
        g_window.ontimer(snake, 200)


def snake_normal_move():
    """
    Move the snake and show on the screen, update g_snake, g_stamps, g_stamps_pos
    Being called in snake()
    :return: None
    """
    global g_snake, g_stamps, g_stamps_pos
    g_snake.color('blue', 'black')
    a = g_snake.stamp()
    g_stamps.append(a)
    g_snake.forward(20)
    # print(g_snake.xcor(), g_snake.ycor())
    g_stamps_pos.append(g_snake.pos())
    g_snake.color('red')
    g_snake.clearstamp(g_stamps[0])
    g_stamps_pos = g_stamps_pos[1:]
    g_stamps = g_stamps[1:]


def draw_win():
    """
    Draw the winning picture
    Being called in snake()
    :return: None
    """
    global g_snake
    g_snake.goto(g_snake.xcor() + 11, g_snake.ycor() + 1)
    g_snake.write("WINNER!!", align="left")
    g_snake.goto(g_snake.xcor() - 11, g_snake.ycor() - 1)
    g_window.update()


def snake_grow():
    """
    Make the snake grow after consuming food, update g_short_tail_length, g_snake, g_stamps, g_stamps_pos
    Being called in snake()
    :return: None
    """
    global g_short_tail_length, g_snake, g_stamps, g_stamps_pos
    g_short_tail_length += 1
    g_snake.color('blue', 'black')
    a = g_snake.stamp()
    g_stamps.append(a)
    g_snake.forward(20)
    g_stamps_pos.append(g_snake.pos())
    g_snake.color('red')


def monster_smart_move():
    """
    Make monster head to the direction of the snake head, update g_monster
    Divide the region into 4 parts, monster check the position of the snake inside each part
    Being called in monster()
    :return: None
    """
    global g_monster, g_snake
    if 45.0 <= g_monster.towards(g_snake.pos()) < 135.0:
        g_monster.setheading(HEADING_BY_KEY[KEY_UP])
    elif 135 <= g_monster.towards(g_snake.pos()) < 225.0:
        g_monster.setheading(HEADING_BY_KEY[KEY_LEFT])
    elif 225.0 <= g_monster.towards(g_snake.pos()) < 315.0:
        g_monster.setheading(HEADING_BY_KEY[KEY_DOWN])
    else:
        g_monster.setheading(HEADING_BY_KEY[KEY_RIGHT])

    g_monster.forward(10)


def draw_lose():
    """
    Draw the picture when the snake is caught by monster
    Being called in monster()
    :return: None
    """
    global g_stop
    g_monster.goto(g_monster.xcor() - 30, g_monster.ycor())
    g_monster.write("Game Over!!", font=4)
    g_stop = True
    g_monster.goto(g_monster.xcor() + 30, g_monster.ycor())



def monster():
    """
    The main function of monster, in charge of the monster move
    Update g_monster
    Being called in game_start(), call monster_smart_move(), draw_lose()
    :return: None
    """
    global g_monster, g_snake, g_stamps_pos, g_contact, g_stop
    # test whether the game is over
    if g_stop:
        return
    # set the heading of the monster according to the snake
    monster_smart_move()
    g_window.update()

    # test whether the monster touches the snake's body(including head)
    for tuples in g_stamps_pos:
        if g_monster.distance(tuples) <= 15:
            g_contact += 1
            # g_note.goto(-45, 240)
            g_note.clear()
            g_note.write("Contact:  " + str(g_contact) + "    Time:  " + str(g_reality_time) \
                         + "    Motion:  " + str(g_keypressed), align="left", font=("Arial", 16, "bold"))
            break

    # test whether the monster touches the head of the snake
    if g_monster.distance(g_snake.pos()) <= 15:
        draw_lose()
        return

    # Random choose the speed of the monster
    monster_timer = random.choice([9, 10, 11])
    g_window.ontimer(monster, 20 * monster_timer)


def test_border():
    """
    test whether the snake touches the boarder
    Being called in snake()
    :return: True means continue the snake, False means stop the snake
    """
    global g_snake, g_keypressed
    if g_snake.xcor() <= -239 and g_keypressed == "Left":
        return False
    elif g_snake.ycor() <= -280 and g_keypressed == "Down":
        return False
    elif g_snake.ycor() >= 200 and g_keypressed == "Up":
        return False
    elif g_snake.xcor() >= 239 and g_keypressed == "Right":
        return False
    else:
        return True



def test_cross_itself():
    """
    test whether the snake crosses itself
    Being called in snake()
    :return: True means continue the snake, False means stop the snake
    """
    global g_snake, g_keypressed
    candidate_pos_lst = []
    # Get close stamps as candidates
    for i in g_stamps_pos:
        if g_snake.distance(i) < 23:
            candidate_pos_lst.append(i)

    # Test block within candidates
    for j in range(len(candidate_pos_lst)):
        if g_keypressed == 'Left' and (g_snake.xcor() - candidate_pos_lst[j][0]) > 0 and \
                abs(g_snake.ycor() - candidate_pos_lst[j][1]) < 1:
            return False
        elif g_keypressed == 'Down' and (g_snake.ycor() - candidate_pos_lst[j][1]) > 0 and \
                abs(g_snake.xcor() - candidate_pos_lst[j][0]) < 1:
            return False
        elif g_keypressed == 'Up' and (g_snake.ycor() - candidate_pos_lst[j][1]) < 0 and \
                abs(g_snake.xcor() - candidate_pos_lst[j][0]) < 1:
            return False
        elif g_keypressed == 'Right' and (g_snake.xcor() - candidate_pos_lst[j][0]) < 0 and \
                abs(g_snake.ycor() - candidate_pos_lst[j][1]) < 1:
            return False
    return True



def game_start(x=0, y=0):
    """
    # begin the game after clicking the screen
    :param x: Take up the position
    :param y: Take up the position
    :return: None
    """
    global g_keypressed, g_note, g_reminder, g_stamps_pos, g_snake
    g_reminder.clear()
    g_window.onclick(None)
    g_keypressed = KEY_UP
    g_stamps_pos.append(g_snake.pos())
    set_numbers()
    g_window.ontimer(hide_show_numbers, 1000)
    update_time()
    monster()
    snake()


if __name__ == '__main__':
    set_initial_outlook()
    g_window.onkey(partial(on_arrow_key_pressed, KEY_UP), KEY_UP)
    g_window.onkey(partial(on_arrow_key_pressed, KEY_DOWN), KEY_DOWN)
    g_window.onkey(partial(on_arrow_key_pressed, KEY_LEFT), KEY_LEFT)
    g_window.onkey(partial(on_arrow_key_pressed, KEY_RIGHT), KEY_RIGHT)
    g_window.onkey(key_space, KEY_SPACE)
    g_window.onscreenclick(game_start)

    g_window.listen()
    g_window.mainloop()





