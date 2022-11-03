import sys
import constraint
import win32api
import win32con
import keyboard
from PIL import Image, ImageGrab
import allinoen
import auto


# 保存剪切板内图片
def get_pic(pic_name):
    # im = ImageGrab.grabclipboard()    # 手动截图
    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    im = ImageGrab.grab(bbox=(0, 0, width, height))
    if isinstance(im, Image.Image):
        im = im.crop((345, 190, 1035, 885))
        im.save(pic_name)
    else:
        print("clipboard is empty")
        sys.exit()


def solution(board):
    problem = constraint.Problem()

    # We're letting VARIABLES 11 through 99 have an interval of [1..9]
    for i in range(1, 10):
        problem.addVariables(range(i * 10 + 1, i * 10 + 10), range(1, 10))

    # We're adding the constraint that all values in a row must be different
    # 11 through 19 must be different, 21 through 29 must be all different,...
    for i in range(1, 10):
        problem.addConstraint(constraint.AllDifferentConstraint(), range(i * 10 + 1, i * 10 + 10))

    # Also all values in a column must be different
    # 11,21,31...91 must be different, also 12,22,32...92 must be different,...
    for i in range(1, 10):
        problem.addConstraint(constraint.AllDifferentConstraint(), range(10 + i, 100 + i, 10))

    # The last rule in a sudoku 9x9 puzzle is that those nine 3x3 squares must have all different values,
    # we start off by noting that each square"starts" at row indices 1, 4, 7
    for i in [1, 4, 7]:
        # Then we note that it's the same for columns, the squares start at indices 1, 4, 7 as well
        # basically one square starts at 11, the other at 14, another at 41, etc
        for j in [1, 4, 7]:
            square = [10*i+j, 10*i+j+1, 10*i+j+2, 10*(i+1)+j, 10*(i+1)+j+1, 10*(i+1)+j+2, 10*(i+2)+j, 10*(i+2)+j+1, 10*(i+2) + j+2]
            # As an example, for i = 1 and j = 1 (bottom left square), the cells 11,12,13,
            # 21,22,23, 31,32,33 have to be all different
            problem.addConstraint(constraint.AllDifferentConstraint(), square)

    # We're adding a constraint for each number on the board (0 is an"empty" cell),
    # Since they're already solved, we don't need to solve them
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                def c(variable_value, value_in_table=board[i][j]):
                    if variable_value == value_in_table:
                        return True

                # Basically we're making sure that our program doesn't change the values already on the board
                # By telling it that the values NEED to equal the corresponding ones at the base board
                problem.addConstraint(c, [((i+1)*10 + (j+1))])

    solutions = problem.getSolutions()

    result = []
    for s in solutions:
        print("==================")
        for i in range(1, 10):
            print("|", end='')
            for j in range(1, 10):
                result.append(str(s[i*10+j]))
                if j % 3 == 0:
                    print(str(s[i*10+j])+" |", end='')
                else:
                    print(str(s[i*10+j]), end='')
            print("")
            if i % 3 == 0 and i != 9:
                print("------------------")
        print("==================")
    if len(solutions) == 0:
        print("No solutions found.")
    return result, solutions


if __name__ == '__main__':
    image_name = 'Sudoku.png'
    auto.bringToFront("Microsoft Sudoku")   # 打开了数独界面
    while True:
        keyboard.wait('enter')
        get_pic(image_name)   # 截取图片
        list_info = allinoen.generate_list_in_one(image_name)
        print(list_info)
        over, nnn = solution(list_info)     # 解数独
        if len(nnn) != 0:
            auto.auto_1(nnn[0], list_info)      # 自动填数独
