import tkinter
import sys
from os import execl
from PIL import Image, ImageTk

main_window = tkinter.Tk()
main_window.title('Шашкореверси')
window_size = 800  # Do not set less than 400px
indent = window_size // 50
# One field size
size = (window_size - (2 * indent)) // 8  # TODO make option in menu
board = tkinter.Canvas(main_window, width=window_size + window_size // 4, height=window_size, bg='white')
board.pack()

# 0 or 1 if chip on this field and 3 if not
field = [[3, 3, 3, 3, 3, 3, 3, 3],
          [3, 3, 3, 3, 3, 3, 3, 3],
          [3, 3, 3, 3, 3, 3, 3, 3],
          [3, 3, 3, 3, 3, 3, 3, 3],
          [3, 3, 3, 3, 3, 3, 3, 3],
          [3, 3, 3, 3, 3, 3, 3, 3],
          [3, 3, 3, 3, 3, 3, 3, 3],
          [3, 3, 3, 3, 3, 3, 3, 3]]
# List of all chips
chips_list = []
# Chip and available moves for it
move_list = []
# Garbage can
elements_to_remove = []
# Turn check, white turn - True
turn = True
# Extra move checker
extra_move = False
# Chip counter ([0] - black, [1] - white)
counter = [32, 32]
counter_on_field = [0, 0]
# Attaching textures
black_chip = Image.open("./black_chip.png")
white_chip = Image.open("./white_chip.png")
# Scale textures with size
black_chip = black_chip.resize((size, size), Image.ANTIALIAS)
black_chip = ImageTk.PhotoImage(black_chip.convert('RGBA'))
white_chip = white_chip.resize((size, size), Image.ANTIALIAS)
white_chip = ImageTk.PhotoImage(white_chip.convert('RGBA'))
# Chips textures, textures[0] = black_chip   textures[1] = white_chip
textures = [black_chip, white_chip]
# Board frame
board.create_rectangle(indent - 2.5, indent - 2.5, size * 8 + indent + 2.5, size * 8 + indent + 2.5,
                       outline="gray", width=indent // 3)
# Turn displayer
turn_display = board.create_text((window_size + window_size // 4)-(((window_size + window_size // 4) - indent - (size * 8)) // 2),
                                 3 * indent, text=f"Ход: {'белые' if turn else 'черные'}",
                                 fill="black", font=("Impact", int((window_size) // 50)))
# Chip counter
chip_display = board.create_text((window_size + window_size // 4)-(((window_size + window_size // 4) - indent - (size * 8)) // 2),
                                 (5 * indent) // 1, text=f"Шашек осталось: {counter[1] if turn else counter[0]}",
                                 fill="black", font=("Impact", int((window_size) // 60)))


def restart():
    execl(sys.executable, sys.executable, *sys.argv)


def menu():  # TODO menu button command
    execl(sys.executable, sys.executable, '/../consolemenu.py')


def remove_garbage():
    for element in elements_to_remove:
        board.delete(element)
    elements_to_remove.clear()


def draw_field():
    coord_x = indent
    while coord_x < 8 * size + indent:
        coord_y = size + indent
        while coord_y < 8 * size + indent:
            board.create_rectangle(coord_x, coord_y, coord_x + size, coord_y + size, fill="black")
            board.create_rectangle(coord_x + size, coord_y - size, coord_x + (2 * size), coord_y, fill="black")
            coord_y += 2 * size
        coord_x += 2 * size


def place_chip(event):
    global turn
    global counter
    # Check for available chips
    if counter[turn] == 0:
        return
    coord_x, coord_y = (event.x - indent) // size, (event.y - indent) // size
    # If clicked in field
    if coord_x in range(0, 8) and coord_y in range(0, 8):
        chips_list.append(((board.create_image(((coord_x + 1) * size) - (size / 2 - indent),
                          ((coord_y + 1) * size) - (size / 2 - indent),
                           image=textures[turn])), (coord_x + 1, coord_y + 1)))
        counter[turn] -= 1
        counter_on_field[turn] += 1
        field[coord_x][coord_y] = turn
        turn = not turn
        # Tooggle turn label
        board.itemconfig(turn_display, text=f"Ход: {'белые' if turn else 'черные'}")
        # Toogle available chips
        board.itemconfig(chip_display, text=f"Шашек осталось: {counter[1] if turn else counter[0]}")
        # Call to trigger draw check
        make_turn(None)


def available_turns(event):
    coord_x, coord_y = (event.x - indent) // size, (event.y - indent) // size
    # Check empty neighboring fields
    try:
        if field[coord_x][coord_y - 2] == 3 and coord_y - 2 >= 0:
            elements_to_remove.append(board.create_rectangle(coord_x * size + indent,
                                                             coord_y * size - size + indent,
                                                             coord_x * size + size + indent,
                                                             coord_y * size - (2 * size) + indent,
                                                             outline="green", width=indent // 2))
            # Check if player can eat
            if field[coord_x][coord_y - 1] is not turn and field[coord_x][coord_y - 1] is not 3:
                elements_to_remove.append(board.create_rectangle(coord_x * size + indent,
                                                                 coord_y * size + indent,
                                                                 coord_x * size + size + indent,
                                                                 coord_y * size - size + indent,
                                                                 outline="red", width=indent // 2))
                move_list.append((coord_x, coord_y - 2, coord_x, coord_y - 1))
            else:
                move_list.append((coord_x, coord_y - 2))
    # If field does not exist pass
    except IndexError:
        pass
    try:
        if field[coord_x][coord_y + 2] == 3:
            elements_to_remove.append(board.create_rectangle(coord_x * size + indent,
                                                             coord_y * size + (2 * size) + indent,
                                                             coord_x * size + size + indent,
                                                             coord_y * size + (3 * size) + indent,
                                                             outline="green", width=indent // 2))
            # Check if player can eat
            if field[coord_x][coord_y + 1] is not turn and field[coord_x][coord_y + 1] is not 3:
                elements_to_remove.append(board.create_rectangle(coord_x * size + indent,
                                                                 coord_y * size + size + indent,
                                                                 coord_x * size + size + indent,
                                                                 coord_y * size + (2 * size) + indent,
                                                                 outline="red", width=indent // 2))
                move_list.append((coord_x, coord_y + 2, coord_x, coord_y + 1))
            else:
                move_list.append((coord_x, coord_y + 2))
    # If field does not exist pass
    except IndexError:
        pass
    try:
        if field[coord_x - 2][coord_y] == 3 and coord_x - 2 >= 0:
            elements_to_remove.append(board.create_rectangle(coord_x * size - size + indent,
                                                             coord_y * size + indent,
                                                             coord_x * size - (2 * size) + indent,
                                                             coord_y * size + size + indent,
                                                             outline="green", width=indent // 2))
            # Check if player can eat
            if field[coord_x - 1][coord_y] is not turn and field[coord_x - 1][coord_y] is not 3:
                elements_to_remove.append(board.create_rectangle(coord_x * size + indent,
                                                                 coord_y * size + indent,
                                                                 coord_x * size - size + indent,
                                                                 coord_y * size + size + indent,
                                                                 outline="red", width=indent // 2))
                move_list.append((coord_x - 2, coord_y, coord_x - 1, coord_y))
            else:
                move_list.append((coord_x - 2, coord_y))

    # If field does not exist pass
    except IndexError:
        pass
    try:
        if field[coord_x + 2][coord_y] == 3:
            elements_to_remove.append(board.create_rectangle(coord_x * size + (2 * size) + indent,
                                                             coord_y * size + indent,
                                                             coord_x * size + (3 * size) + indent,
                                                             coord_y * size + size + indent,
                                                             outline="green", width=indent // 2))
            # Check if player can eat
            if field[coord_x + 1][coord_y] is not turn and field[coord_x + 1][coord_y] is not 3:
                elements_to_remove.append(board.create_rectangle(coord_x * size + size + indent,
                                                                 coord_y * size + indent,
                                                                 coord_x * size + (2 * size) + indent,
                                                                 coord_y * size + size + indent,
                                                                 outline="red", width=indent // 2))
                move_list.append((coord_x + 2, coord_y, coord_x + 1, coord_y))
            else:
                move_list.append((coord_x + 2, coord_y))
    # If field does not exist pass
    except IndexError:
        pass
    # Find chip to move
    if len(move_list) > 0:
        for chip in chips_list:
            if chip[1][0] == coord_x + 1 and chip[1][1] == coord_y + 1:
                move_list.append(chip)
                break


def available_turns_after_eat(coords):
    global turn
    global extra_move
    extra_move = True
    coord_x, coord_y = coords
    # Check empty neighboring fields and chips to eat
    try:
        if field[coord_x][coord_y - 2] == 3 and coord_y - 2 >= 0 and \
           field[coord_x][coord_y - 1] is not turn and field[coord_x][coord_y - 1] is not 3:
            elements_to_remove.append(board.create_rectangle(coord_x * size + indent,
                                                             coord_y * size - size + indent,
                                                             coord_x * size + size + indent,
                                                             coord_y * size - (2 * size) + indent,
                                                             outline="green", width=indent // 2))
            elements_to_remove.append(board.create_rectangle(coord_x * size + indent,
                                                             coord_y * size + indent,
                                                             coord_x * size + size + indent,
                                                             coord_y * size - size + indent,
                                                             outline="red", width=indent // 2))
            move_list.append((coord_x, coord_y - 2, coord_x, coord_y - 1))
    # If field does not exist pass
    except IndexError:
        pass
    try:
        if field[coord_x][coord_y + 2] == 3 and field[coord_x][coord_y + 1] is not turn and \
           field[coord_x][coord_y + 1] is not 3:
            elements_to_remove.append(board.create_rectangle(coord_x * size + indent,
                                                             coord_y * size + (2 * size) + indent,
                                                             coord_x * size + size + indent,
                                                             coord_y * size + (3 * size) + indent,
                                                             outline="green", width=indent // 2))
            elements_to_remove.append(board.create_rectangle(coord_x * size + indent,
                                                             coord_y * size + size + indent,
                                                             coord_x * size + size + indent,
                                                             coord_y * size + (2 * size) + indent,
                                                             outline="red", width=indent // 2))
            move_list.append((coord_x, coord_y + 2, coord_x, coord_y + 1))
    # If field does not exist pass
    except IndexError:
        pass
    try:
        if field[coord_x - 2][coord_y] == 3 and coord_x - 2 >= 0 and field[coord_x - 1][coord_y] is not turn and \
           field[coord_x - 1][coord_y] is not 3:
            elements_to_remove.append(board.create_rectangle(coord_x * size - size + indent,
                                                             coord_y * size + indent,
                                                             coord_x * size - (2 * size) + indent,
                                                             coord_y * size + size + indent,
                                                             outline="green", width=indent // 2))
            elements_to_remove.append(board.create_rectangle(coord_x * size + indent,
                                                             coord_y * size + indent,
                                                             coord_x * size - size + indent,
                                                             coord_y * size + size + indent,
                                                             outline="red", width=indent // 2))
            move_list.append((coord_x - 2, coord_y, coord_x - 1, coord_y))

    # If field does not exist pass
    except IndexError:
        pass
    try:
        if field[coord_x + 2][coord_y] == 3 and field[coord_x + 1][coord_y] is not turn and \
           field[coord_x + 1][coord_y] is not 3:
            elements_to_remove.append(board.create_rectangle(coord_x * size + (2 * size) + indent,
                                                             coord_y * size + indent,
                                                             coord_x * size + (3 * size) + indent,
                                                             coord_y * size + size + indent,
                                                             outline="green", width=indent // 2))
            elements_to_remove.append(board.create_rectangle(coord_x * size + size + indent,
                                                             coord_y * size + indent,
                                                             coord_x * size + (2 * size) + indent,
                                                             coord_y * size + size + indent,
                                                             outline="red", width=indent // 2))
            move_list.append((coord_x + 2, coord_y, coord_x + 1, coord_y))
    # If field does not exist pass
    except IndexError:
        pass
    # Find chip to move
    if len(move_list) > 0:
        for chip in chips_list:
            if chip[1][0] == coord_x + 1 and chip[1][1] == coord_y + 1:
                move_list.append(chip)
                break
    # If no more extra turns
    else:
        turn = not turn
        # Tooggle turn label
        board.itemconfig(turn_display, text=f"Ход: {'белые' if turn else 'черные'}")
        # Toogle available chips
        board.itemconfig(chip_display, text=f"Шашек осталось: {counter[1] if turn else counter[0]}")
        board.unbind("<Button-1>")
        board.bind("<Button-1>", make_turn)
        make_turn(None)


def move(event):  # TODO more sensetive corner caclulation
    global turn
    global extra_move
    global counter_on_field
    chip = move_list[len(move_list) - 1]
    move_list.pop()
    coord_x, coord_y = (event.x - indent) // size, (event.y - indent) // size
    # Check if chip was eaten on this turn
    eat_check = False
    for coord_pare in move_list:
        if coord_pare[0] == coord_x and coord_pare[1] == coord_y:
            # Remove old chip position from list
            for current_chip in chips_list:
                if current_chip[0] == chip[0]:
                    chips_list.remove(current_chip)
                    break
            board.move(chip[0], ((coord_x + 1) * size) - (chip[1][0] * size),
                       ((coord_y + 1) * size) - (chip[1][1] * size))
            # Change position in field
            field[coord_x][coord_y] = turn
            field[chip[1][0] - 1][chip[1][1] - 1] = 3
            # Remove eaten chip
            try:
                for chip_eaten in chips_list:
                    if chip_eaten[1][0] == coord_pare[2] + 1 and chip_eaten[1][1] == coord_pare[3] + 1:
                        # Remove chip image
                        elements_to_remove.append(chip_eaten[0])
                        # Remove chip from field
                        field[coord_pare[2]][coord_pare[3]] = 3
                        # Remove chip info
                        chips_list.remove(chip_eaten)
                        eat_check = True
                        counter_on_field[not turn] -= 1
                        break
            # If no cheap to eat
            except IndexError:
                pass
            # List new chip position
            chips_list.append((chip[0], (coord_x + 1, coord_y + 1)))
            move_list.clear()
            # Change turn if no chips were eaten
            if not eat_check:
                turn = not turn
                # Tooggle turn label
                board.itemconfig(turn_display, text=f"Ход: {'белые' if turn else 'черные'}")
                # Toogle available chips
                board.itemconfig(chip_display, text=f"Шашек осталось: {counter[1] if turn else counter[0]}")
                board.unbind("<Button-1>")
                board.bind("<Button-1>", make_turn)
                make_turn(None)
            # Extra move if player ate chip
            else:
                # Clear garbage list
                remove_garbage()
                # Search for extra move
                available_turns_after_eat((coord_x, coord_y))
            break
    # Happens when pressed close to corner of field or outside of field
    else:
        move_list.clear()
        board.unbind("<Button-1>")
        board.bind("<Button-1>", make_turn)
        # Change turn if refuse to extra move
        if extra_move:
            turn = not turn
            # Tooggle turn label
            board.itemconfig(turn_display, text=f"Ход: {'белые' if turn else 'черные'}")
            # Toogle available chips
            board.itemconfig(chip_display, text=f"Шашек осталось: {counter[1] if turn else counter[0]}")
        make_turn(None)


def make_turn(event):
    global extra_move
    # End game check
    if (counter[turn] == 0 and counter_on_field[turn] == 0) or counter_on_field == [32, 32]:
        board.unbind_all("<Button-1>")
        board.create_rectangle(indent + (2 * size), indent + (3 * size), indent + (6 * size), indent + (5 * size),
                               fill='white', outline='gray', width=indent // 2)
        win_message = board.create_text(indent + (4 * size), indent + (3 * size) + (size // 2), text="",
                               fill="black", font=("Impact", int(window_size // 50)))
        retry_button = tkinter.Button(main_window, text='Еще раз', fg='black', bg='white',
                                      height=indent // 6, width=indent // 3, command=restart)
        board.create_window((2 * indent) + (3 * size), indent + (4 * size), anchor='nw', window=retry_button)
        menu_button = tkinter.Button(main_window, text='Меню', fg='black', bg='white',
                                      height=indent // 6, width=indent // 3, command=menu)
        board.create_window((2 * indent) + (4 * size), indent + (4 * size), anchor='nw', window=menu_button)
        main_menu_button = ''
        if counter[0] == 0 and counter_on_field[0] == 0:
            board.itemconfig(win_message, text="Победа белых!")
        elif counter[1] == 0 and counter_on_field[1] == 0:
            board.itemconfig(win_message, text="Победа черных!")
        else:
            board.itemconfig(win_message, text="Ничья!")
    # Return to basic move condition
    extra_move = False
    # Clear garbage list
    remove_garbage()
    # Check if field is empty and suitable
    try:
        coord_x, coord_y = (event.x - indent) // size, (event.y - indent) // size
        # Check if clicked in field
        if coord_x in range(0, 8) and coord_y in range(0, 8):
            if field[coord_x][coord_y] == 3 and \
                    (((coord_x + 1) % 2 == 0 and (coord_y + 1) % 2 == 0 and turn) or
                     ((coord_x + 1) % 2 != 0 and (coord_y + 1) % 2 != 0 and turn) or
                     ((coord_x + 1) % 2 == 0 and (coord_y + 1) % 2 != 0 and not turn) or
                     ((coord_x + 1) % 2 != 0 and (coord_y + 1) % 2 == 0 and not turn)):
                place_chip(event)
            elif field[coord_x][coord_y] == turn:
                board.unbind_all("<Button-1>")
                board.bind("<Button-1>", move)
                available_turns(event)
            # If player press field with enemy chip
            else:
                pass
        # Idle call from move()
    except AttributeError:
        pass


draw_field()
board.bind("<Button-1>", make_turn)
main_window.mainloop()
