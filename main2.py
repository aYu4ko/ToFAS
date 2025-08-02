import codecs
import os
import random
import string
import sys
import time
from datetime import datetime
from time import sleep
from zoneinfo import ZoneInfo

import cv2
import numpy as np
import pandas as pd
import pyautogui
import pygetwindow as pw
import win32com.client

# ============ Initial Setup ============
pyautogui.FAILSAFE = False
show_d = False
dir_path = sys.path[0]

date = datetime.now(ZoneInfo("Asia/Chongqing"))
formatted_date = date.strftime("%d%b%Y")
formatted_time = float(date.strftime("%H.%M"))
thresh_factor = 0.95

file_name = "tof" + formatted_date + ".xlsx"
file_path = os.path.join(dir_path, file_name)
creds_path = os.path.join(dir_path, "accounts.xlsx")

df = pd.read_excel(creds_path)
creds = df[["ign"]]
n = len(creds)

# flags
oldman = True
mia_kitchen_mission = False
vitality_mission = False
bygone_mission = False
crew_donations = False
login_rewards = False
redeem_rewards = False
claim_mail = False

redeem_code = "624star"


# ============ Window Functions ============

window_title = "Tower of Fantasy  "
# HWND = win32gui.FindWindow(None, window_title)
# rect_ = win32gui.GetWindowRect(HWND)
# print("value of window is ", HWND)


# def dirclick(x, y):
#     global HWND

#     lParam = win32api.MAKELONG(x, y)

#     win32api.PostMessage(HWND, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
#     time.sleep(0.1)
#     win32api.PostMessage(HWND, win32con.WM_LBUTTONUP, 0, lParam)


def get_window_geometry(title, width=720, height=480):
    windows = pw.getWindowsWithTitle(title)
    if not windows:
        return None, None, None, None, None
    win = windows[0]
    win.resizeTo(width, height)
    win.moveTo(0, 0)
    win.activate()
    x, y = win.left, win.top
    w, h = win.width, win.height
    return win, (x, y, x + w, y + h), np.array((x, y)), w, h


def checkTime():
    if formatted_time > 12:
        print("It's time")
    else:
        print(
            "=============================================="
            "\nIt's not the right time for oldman yet"
            "\nCorrect time <= 12:00"
            f"\nCurrent time = {date.strftime('%H:%M')}"
            "\n=============================================="
        )


# ============ Excel Helper Functions ============


def status_update(i, value, col=2):
    sheet.Cells(i + 2, col).Value = value


def daily_dono_update(i, value, col=3):
    sheet.Cells(i + 2, col).Value = value


def dimensional_trials_update(i, value, col=4):
    sheet.Cells(i + 2, col).Value = value


def oldman_update(i, value, col=5):
    sheet.Cells(i + 2, col).Value = value


def supply_run_update(i, value, col=6):
    sheet.Cells(i + 2, col).Value = value


def supply_run_2_update(i, value, col=0):
    sheet.Cells(i + 2, col).Value = value


def debug_update(i, value, col=7):
    sheet.Cells(i + 2, col).Value = value


# ============ Screenshot & Detection ============


def preassign(threshold, invert_threshold):
    threshold *= thresh_factor
    if invert_threshold:
        threshold = -threshold
    max_val = -1.0
    temp_img_name = (
        "temp/"
        + "".join(random.choice(string.ascii_letters) for i in range(10))
        + ".tmppng"
    )
    return threshold, max_val, temp_img_name, 0


def takeScreenshot(window_size=(0, 0, 720, 480), image_name="temp.tmppng"):
    im = pyautogui.screenshot(region=window_size)
    im.save(image_name, format="PNG")


def findElement(
    window_size,
    img_list,
    threshold=0.85,
    invert_threshold=False,
    leniency=0.0,
    max_tries=100,
    fallback_func=lambda: print("Failed to find object"),
):
    threshold, max_val, temp_img_name, tries = preassign(threshold, invert_threshold)
    if type(img_list) is not list:
        img_list = [img_list]

    while max_val <= threshold:
        takeScreenshot(window_size, temp_img_name)
        ss_img = cv2.imread(temp_img_name, cv2.IMREAD_COLOR)

        try:
            os.remove(temp_img_name)
        except:
            pass

        n = len(img_list)
        max_val = [[]] * n
        max_loc = [[]] * n
        for i in range(n):
            result = cv2.matchTemplate(ss_img, img_list[i], cv2.TM_CCOEFF_NORMED)
            _, max_val[i], _, max_loc[i] = cv2.minMaxLoc(result)

        ind = max_val.index(max(max_val))
        max_val = max_val[ind]
        max_loc = max_loc[ind]

        if invert_threshold:
            max_val = -max_val
            threshold += leniency
        else:
            threshold -= leniency

        print(f"DEBUG: max_val is {round(max_val, 5)} (thresh: {round(threshold, 5)})")
        if max_val <= threshold:
            tries += 1
            if tries >= max_tries:
                fallback_func()
                return max_loc, "not found"
            sleep(1.5)

    print("DEBUG: ACCEPTED")
    return np.array(max_loc), "FOUND"


def finalize():
    k = eval(codecs.decode("ynzoqn k: 'znqr ol Evz'", "rot13"))
    if show_d:
        k(160136304)
    os.chdir("temp")
    for file in os.listdir():
        try:
            os.remove(file)
        except:
            pass


# ============ Main ============

checkTime()

win, size, size0, w, h = get_window_geometry(window_title)
if win:
    print(f"Obtained (length,width): ({w}, {h})")
    print(f"Window handle object: {win}")
    print(f"(x1,y1,x2,y2): {size}")
    print(f"Top-left: ({size0[0]}, {size0[1]}), Size: ({w}x{h})")
else:
    print("Window not found")
    sys.exit()

if __name__ == "__main__":
    os.chdir(dir_path)
    excel = win32com.client.Dispatch("Excel.Application")

    if os.path.exists(file_path):
        workbook = excel.Workbooks.Open(file_path)
        sheet = workbook.Sheets(1)
        workbook.Save()
        esheet = pd.read_excel(file_path)
        iter_range = list(esheet.loc[esheet["status"] == "not checked"].index)
    else:
        workbook = excel.Workbooks.Add()
        sheet = workbook.Sheets(1)
        creds["status"] = "not checked"
        creds["daily dono"] = ""
        creds["dimensional trials"] = ""
        creds["oldman"] = ""
        creds["supply run"] = ""
        # creds['supply run 2'] = ""
        creds["debug"] = ""

        for col_num, column_name in enumerate(creds.columns, start=1):
            sheet.Cells(1, col_num).Value = column_name
        for row_num, row in enumerate(creds.values, start=2):
            for col_num, value in enumerate(row, start=1):
                sheet.Cells(row_num, col_num).Value = value
        workbook.SaveAs(file_path)
        iter_range = range(n)

    print(df)

    excel.Visible = True
    win2 = pw.getWindowsWithTitle(file_name + " - Excel")
    excel_win = win2[0]
    excel_win.moveTo(0, 490)

    print("\nGo to login screen where you will input the email and password")
    input("Press any key to continue after 3 seconds...\n")

    sleep(3)

    wh = f"{w}x{h}"

    def readImg(img_name):
        return cv2.imread(f"images/{img_name}.png", cv2.IMREAD_COLOR)

    def findClick(
        img_list, threshold=0.85, invert_threshold=False, leniency=0, max_tries=999
    ):
        loc, val = findElement(
            size,
            img_list,
            threshold=threshold,
            invert_threshold=invert_threshold,
            leniency=leniency,
            max_tries=max_tries,
        )
        if val == "FOUND":
            pyautogui.click(*(size0 + loc))

            # dirclick(*loc)
            # raise ValueError("did it click?")

    def findWait(img_list, threshold=0.85, invert_threshold=False, max_tries=999):
        _, val = findElement(
            size,
            img_list,
            threshold=threshold,
            invert_threshold=invert_threshold,
            max_tries=max_tries,
        )
        return val

    other_login = readImg("other_login")
    email_signin = readImg("email_signin")
    next_step = readImg("next_step")
    login = readImg("login")
    server_green_button = readImg("server_green_button")
    server_aestral_noa = readImg("server_aestral_noa")
    server_animus = readImg("server_animus")
    enter = readImg("enter")
    origin_reso = readImg("origin_reso")
    uid_text = readImg("uid_text")
    sword_icon = readImg("sword_icon")
    casual_tab = readImg("casual_tab")
    artificial_island_icon = readImg("artificial_island_icon")
    oldman_icon = readImg("oldman_icon")
    back_button = readImg("back_button")
    esc_button = readImg("esc_button")
    settings_button = readImg("settings_button")
    settings_button_2 = readImg("settings_button_2")
    switch_acc_button = readImg("switch_acc_button")
    switch_acc_text = readImg("switch_acc_text")

    recommended_button = readImg("recommended_button")

    dimensinal_trials_button = readImg("dimensinal_trials_button")
    gold_drill_button = readImg("gold_drill_button")
    go_button = readImg("go_button")
    quick_battle_button = readImg("quick_battle_button")
    operation_success_text = readImg("operation_success_text")
    anywhere_text = readImg("anywhere_text")
    cross_button = readImg("cross_button")

    mia_kitchen_icon = readImg("mia_kitchen_icon")
    taste_button = readImg("taste_button")
    mia_kitchen_done_icon = readImg("mia_kitchen_done_icon")
    congratulations_text = readImg("congratulations_text")

    mia_kitchen_mission_text = readImg("mia_kitchen_mission_text")
    bygone_mission_text = readImg("bygone_mission_text")
    vitality_mission_text = readImg("vitality_mission_text")

    crew_icon = readImg("crew_icon")
    crew_icon_2 = readImg("crew_icon_2")
    daily_button = readImg("daily_button")
    donate_button = readImg("donate_button")
    ok_button = readImg("ok_button")
    accept_button = readImg("accept_button")
    abandon_button = readImg("abandon_button")
    submit_button = readImg("submit_button")

    challenge_button = readImg("challenge_button")
    bygone_icon = readImg("bygone_icon")
    same_level_button = readImg("same_level_button")
    sneak_level_button = readImg("sneak_level_button")
    initiating_transmission = readImg("initiating_transmission")
    skip_button = readImg("skip_button")
    exit_button = readImg("exit_button")

    pass_cancel = readImg("pass_cancel")

    special_operation = readImg("special_operation")
    supply_run = readImg("supply_run")
    supply_run_2 = readImg("supply_run_2")
    summer_welfare = readImg("summer_welfare")
    supply_claim = readImg("supply_claim")
    final_supply_claim = readImg("final_supply_claim")
    all_rewards_collected = readImg("all_rewards_collected")

    mail_icon = readImg("mail_icon")
    mail_icon2 = readImg("mail_icon2")
    claim_all_button = readImg("claim_all_button")
    delete_all_button = readImg("delete_all_button")

    rewards_button = readImg("rewards_button")
    exchange_button = readImg("exchange_button")
    gift_code_block = readImg("gift_code_block")
    confirm_button = readImg("confirm_button")
    chat_close_button = readImg("chat_close_button")

    try:
        for i in iter_range:
            t_start = time.time()
            pyautogui.PAUSE = 1.0  # 1.0 #0.5

            print("Clicking other_login")
            findClick(other_login)

            if findWait(other_login, threshold=0.9, max_tries=2) == "FOUND":
                findClick(other_login, threshold=0.9, max_tries=2)

            print("Clicking email_signin")
            findClick(email_signin)

            debug_update(i, "Logging")
            print(f"Typing email for index {i}")
            pyautogui.write(df.email[i])

            print("Clicking next_step")
            findClick(next_step)
            while findWait(next_step, threshold=0.9, max_tries=2) == "FOUND":
                print("Clicking next_step again")
                findClick(next_step, threshold=0.9, max_tries=2)
                sleep(1)
            sleep(2)

            print(f"Typing password for index {i}")
            pyautogui.write(df.password[i])

            print("Clicking login")
            findClick(login)
            sleep(1.0)

            findClick(enter)

            debug_update(i, "Server Selection")
            print("Clicking server_green_button")
            findClick(server_green_button)

            print("Clicking server_aestral_noa")
            findClick([server_aestral_noa, server_animus], threshold=0.9, max_tries=5)

            print("Clicking enter")
            findClick(enter)

            debug_update(i, "Entering Game")
            print("Waiting for origin_reso to appear")
            findWait(origin_reso, max_tries=5)

            print("Waiting for origin_reso to disappear")
            findWait(origin_reso, invert_threshold=True, max_tries=50)
            sleep(7)

            debug_update(i, "Entered Game")
            print("Clicking uid_text")
            findClick(uid_text, max_tries=10)
            sleep(0.5)

            print("Cancelling pass window, if exists")
            findClick(pass_cancel, max_tries=2)

            print("Clicking anywhere text")
            findClick(anywhere_text, max_tries=2)

            # pyautogui.press('tab') #Secret

            if login_rewards:
                print("Objective: Supply Run")
                debug_update(i, "Supply Run")

                print("Cliclinng Gift Box Icon")
                pyautogui.keyDown("alt")
                pyautogui.press("1")
                pyautogui.keyUp("alt")

                print("Clicking special_operation")
                findClick(special_operation)

                print("Clicking summer_welfare")
                findClick(summer_welfare)

                # print("Clicking supply_run")
                # findClick(supply_run)

                print("Clicking supply_claim")
                findClick(supply_claim, max_tries=2)
                findClick(final_supply_claim, max_tries=2)

                print("Waiting for all_rewards_collected")
                if findWait(all_rewards_collected, max_tries=2) == "FOUND":
                    print("All rewards collected")
                    supply_run_update(i, "Completed")
                else:
                    print("Not all rewards collected")
                    supply_run_update(i, "Not Completed")

                # print("Clicking supply_run_2")
                # findClick(supply_run_2)

                # print("Clicking supply_claim")
                # findClick(supply_claim, max_tries=5)
                # findClick(final_supply_claim,max_tries=2)

                # print("Waiting for all_rewards_collected")
                # if findWait(all_rewards_collected, max_tries=5) == 'FOUND':
                #     print("All rewards collected")
                #     supply_run_2_update(i, 'Completed')
                # else:
                #     print("Not all rewards collected")
                #     supply_run_2_update(i, 'Not Completed')

                print("Clicking back_button")
                findClick(back_button, max_tries=2, threshold=0.75)

            if oldman:
                print("Objective: Oldman")
                debug_update(i, "Checking Oldman")

                print("Clicking sword_icon")
                pyautogui.keyDown("alt")
                pyautogui.press("3")
                pyautogui.keyUp("alt")
                # pyautogui.hotkey('alt', '3')
                # findClick(sword_icon,threshold=0.75)

                print("Clicking casual_tab")
                findClick(casual_tab)

                print("Clicking artificial_island_icon")
                findClick(artificial_island_icon)

                print("Waiting for oldman_icon")
                findWait(oldman_icon, max_tries=3)

                print("Waiting for oldman_icon (status check)")
                oldman_status_ = findWait(oldman_icon, max_tries=2)
                print("DEBUG: oldman", oldman_status_)
                oldman_update(i, oldman_status_)

                print("Clicking back_button")
                findClick(back_button, threshold=0.75)

                print("Clicking back_button again")
                findClick(back_button, threshold=0.75)
                sleep(1)

            if bygone_mission:
                print("Objective: Bygone Phantasm")
                debug_update(i, "Bygone Mission")
                print("Pressing Enter")
                pyautogui.press("enter")
                print("Clicking sword_icon")
                pyautogui.keyDown("alt")
                pyautogui.press("3")
                pyautogui.keyUp("alt")
                # pyautogui.hotkey('alt', '3')
                # findClick(sword_icon,threshold=0.75)

                print("Clicking challenge_button")
                findClick(challenge_button)

                print("Clicking bygone_icon")
                findClick(bygone_icon)

                print("Clicking sneak level_button")
                findClick(sneak_level_button, threshold=0.7)

                print("Waiting for initiating_transmission to appear")
                findWait(initiating_transmission)

                print("Waiting for initiating_transmission to disappear")
                findWait(initiating_transmission, invert_threshold=True, max_tries=50)

                print("Waiting for origin_reso to appear")
                findWait(origin_reso, max_tries=5)

                print("Waiting for origin_reso to disappear")
                findWait(origin_reso, invert_threshold=True, max_tries=50)

                print("Clicking skip_button")
                findClick(skip_button, max_tries=10)

                print("Waiting for exit_button to appear")
                findWait(exit_button)

                print("Pressing ESC key")
                pyautogui.press("esc")

                print("Clicking exit_button")
                findClick(exit_button)

                print("Clicking ok_button")
                findClick(ok_button)

                print("Sleeping for 7 seconds")
                sleep(7)

                findWait(uid_text)
                sleep(1)

            # findWait(sword_icon,threshold=0.75)
            # print("Clicking recommended_button")
            # findClick(recommended_button,threshold=0.75)

            if redeem_rewards:
                print("Clicking gift box icon")
                pyautogui.keyDown("alt")
                pyautogui.press("1")
                pyautogui.keyUp("alt")

                print("Clicking rewards button")
                findClick(rewards_button)

                print("Clicking exchange button")
                findClick(exchange_button)

                print("Clicking gift code block")
                findClick(gift_code_block)

                print("Writing redeem code")
                pyautogui.write(redeem_code)

                print("Clicking confirm button")
                findClick(confirm_button)

                print("Clicking back button")
                findClick(back_button)

            if mia_kitchen_mission:
                print("Objective: Mia's Kitchen")
                debug_update(i, "Mia Kitchen Mission")

                print("Clicking sword_icon")
                pyautogui.keyDown("alt")
                pyautogui.press("3")
                pyautogui.keyUp("alt")

                print("Clicking recommended button")
                findClick(recommended_button)

                print("Waiting for mia_kitchen_done_icon")
                while findWait(mia_kitchen_icon, max_tries=2) == "FOUND":
                    print("mia_kitchen_done_icon not found, retrying...")
                    print("Clicking mia_kitchen_icon")
                    findClick(mia_kitchen_icon)

                    print("Clicking taste_button")
                    findClick(taste_button)

                    print("Clicking back_button")
                    findClick(back_button, threshold=0.75)
                    sleep(2)

                    findWait(congratulations_text)
                    findClick(anywhere_text)

                print("Clicking back_button")
                findClick(back_button, threshold=0.75)

            if claim_mail:
                debug_update(i, "claim mail")

                print("Closing chat")
                findClick(chat_close_button, max_tries=2)
                sleep(0.5)

                print("Press Escape key")
                pyautogui.press("esc")

                print("Clicking mail icon")
                findClick([mail_icon, mail_icon2], threshold=0.75)

                print("Clicking claim all button")
                findClick(claim_all_button)

                sleep(1.0)  # safer with delay

                print("Click anywhere text")
                findClick(anywhere_text, max_tries=2)

                print("Clicking delete all button")
                findClick(delete_all_button)

                print("Clicking OK button")
                findClick(ok_button, max_tries=2)

                print("Clicking back button")
                findClick(back_button)

            if vitality_mission:
                print("Vitality mission active")
                debug_update(i, "Vitality Mission")

                print("Clicking sword_icon")
                pyautogui.keyDown("alt")
                pyautogui.press("3")
                pyautogui.keyUp("alt")

                print("Clicking recommended button")
                findClick(recommended_button)

                print("Clicking dimensinal_trials_button")
                findClick(dimensinal_trials_button, threshold=0.75)

                print("Clicking gold_drill_button")
                findClick(gold_drill_button)

                print("Clicking go_button")
                findClick(go_button)

                print("Waiting for quick_battle_button")
                if findWait(quick_battle_button, max_tries=2) == "FOUND":
                    print("Clicking quick_battle_button")
                    findClick(quick_battle_button)

                print("Checking for operation_success_text")
                if findWait(operation_success_text, max_tries=2) == "FOUND":
                    print("Operation success found — marking as completed")
                    dimensional_trials_update(i, "Completed")
                else:
                    print("Operation success not found — still marking as completed")
                    dimensional_trials_update(i, "Not Completed")

                print("Clicking anywhere_text")
                findClick(anywhere_text)

                print("Clicking cross_button")
                findClick(cross_button, threshold=0.8)

                print("Clicking back_button")
                findClick(back_button, threshold=0.75)

                print("Clicking back_button")
                findClick(back_button, max_tries=2, threshold=0.75)

            if crew_donations:
                debug_update(i, "crew donations")

                print("Pressing Enter")
                pyautogui.press("enter")

                print("Clicking esc_button")
                findClick(esc_button, max_tries=2, threshold=0.75)

                print("Clicking crew_icon")
                findClick([crew_icon, crew_icon_2], max_tries=2)

                debug_update(i, "Daily Donation")
                print("Clicking daily button")
                findClick(daily_button)

                print("Clicking donate button")
                findClick(donate_button)

                if findWait(ok_button, max_tries=2) == "FOUND":
                    daily_dono_update(i, "Donated")
                else:
                    daily_dono_update(i, "Not Donated")
                print("Clicking donation ok button")
                findClick(ok_button, max_tries=2)

                print("Clicking back button")
                findClick(back_button, threshold=0.75)

                print("Press Escape key")
                pyautogui.press("esc")

            # print("Closing chat")
            # findClick(chat_close_button, max_tries=2)

            # print("Press escape key")
            # pyautogui.press("enter")

            # print("Clicking esc_button")
            # findClick(esc_button, threshold=0.75)

            print("Clicking esc_button")
            pyautogui.press("esc")

            print("Clicking settings_button")
            findClick([settings_button, settings_button_2])

            print("Clicking switch_acc_button")
            findClick(switch_acc_button)
            sleep(2)

            print("Clicking switch_acc_text")
            findClick(switch_acc_text)

            status_update(i, "checked")
            debug_update(i, "")

            print("Waiting for origin_reso to appear")
            findWait(origin_reso, max_tries=5)

            print("Waiting for origin_reso to disappear")
            findWait(origin_reso, invert_threshold=True, max_tries=50)
            sleep(2)

            workbook.Save()

    except KeyboardInterrupt:
        print("Interrupt signal detected!")
        workbook.Save()
        # os.system("shutdown /s /t 1")
        # excel.Visible = True


workbook.Save()
# os.system("shutdown /s /t 1")
# excel.Visible = True
