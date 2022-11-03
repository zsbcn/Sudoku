import time

import pyautogui
import win32api
import win32gui
import win32con

# 横向步进80px, 纵向步进70px
Origin_info = [380, 230]
location_info = {'1': [380, 950], '2': [460, 950], '3': [540, 950],
                 '4': [620, 950], '5': [700, 950], '6': [780, 950],
                 '7': [860, 950], '8': [940, 950], '9': [1020, 950], }
location_info_1 = {1: [380, 950], 2: [460, 950], 3: [540, 950],
                   4: [620, 950], 5: [700, 950], 6: [780, 950],
                   7: [860, 950], 8: [940, 950], 9: [1020, 950], }


def click(x, y):
    win32api.SetCursorPos([x, y])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.02)


def windowEnumHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def bringToFront(window_name):
    top_windows = []
    win32gui.EnumWindows(windowEnumHandler, top_windows)
    for i in top_windows:
        if window_name.lower() in i[1].lower():
            win32gui.ShowWindow(i[0], win32con.SW_SHOWMAXIMIZED)
            win32gui.SetForegroundWindow(i[0])
            break


def auto(target_list):
    for num in range(81):
        print(num, target_list[num], Origin_info[0] + num % 9 * 80, Origin_info[1] + num // 9 * 70)
        pyautogui.moveTo(location_info[target_list[num]][0], location_info[target_list[num]][1])
        pyautogui.click()
        pyautogui.moveTo(Origin_info[0] + num % 9 * 77, Origin_info[1] + num // 9 * 77)
        pyautogui.click()


def auto_1(target_list, know_list):
    last_num = 0
    click(200, 200)
    for x in range(1, 10):
        for y in range(1, 10):
            if know_list[x-1][y-1] == 0:
                num = target_list[x * 10 + y]
                if last_num != num:
                    click(location_info_1[num][0], location_info_1[num][1])
                    # pyautogui.click(location_info_1[num][0], location_info_1[num][1])
                # pyautogui.click(Origin_info[0] + (y-1) * 77, Origin_info[1] + (x-1) * 77)
                click(Origin_info[0] + (y-1) * 77, Origin_info[1] + (x-1) * 77)
                last_num = num


if __name__ == "__main__":
    bringToFront("Microsoft Sudoku")
    # time.sleep(5)
    # for i in range(81):
    #     pyautogui.moveTo(385, 950)
    #     pyautogui.click()
