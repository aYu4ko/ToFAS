import asyncio
import codecs
import os
import queue
import random
import string
import sys
import time
from datetime import datetime
from time import sleep
from typing import Callable, Optional
from zoneinfo import ZoneInfo

import cv2
import numpy as np
import pandas as pd
import pyautogui
import pygetwindow as pw

from template import Template

# ============ Initial Setup ============
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1.0

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
OLDMAN = True
MIA_KITCHEN_MISSION = False
VITALITY_MISSION = False
BYGONE_MISSION = False
CREW_DONATIONS = False
LOGIN_REWARDS = False
REDEEM_REWARDS = False
CLAIM_MAIL = False

redeem_code = "624star"


# ============ Window Functions ============

window_title = "Tower of Fantasy  "


def get_window_geometry(title: str, width: int = 720, height: int = 480):
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


def status_update(i: int, value: str):
    sheet.Cells(i + 2, 2).Value = value


def daily_dono_update(i: int, value: str):
    sheet.Cells(i + 2, 3).Value = value


def dimensional_trials_update(i: int, value: str):
    sheet.Cells(i + 2, 4).Value = value


def oldman_update(i: int, value: str):
    sheet.Cells(i + 2, 5).Value = value


def supply_run_update(i: int, value: str):
    sheet.Cells(i + 2, 6).Value = value


def supply_run_2_update(i: int, value: str):
    sheet.Cells(i + 2, 0).Value = value


def debug_update(i: int, value: str):
    sheet.Cells(i + 2, 7).Value = value


# ============ Screenshot & Detection ============


def preassign(
    threshold: float,
    invert_threshold: bool,
) -> tuple[float, float, int]:
    threshold *= thresh_factor
    if invert_threshold:
        threshold = -threshold
    max_val = -1.0
    return threshold, max_val, 0


def takeScreenshot(window_size=(0, 0, 720, 480), image_name="temp.tmppng"):
    im = pyautogui.screenshot(region=window_size)
    im.save(image_name, format="PNG")


def takeScreenshotDirect(window_size=(0, 0, 720, 480)):
    """Take screenshot directly and return as numpy array for OpenCV"""
    im = pyautogui.screenshot(region=window_size)
    # Convert PIL Image to numpy array (RGB format)
    img_array = np.array(im)
    # Convert RGB to BGR (OpenCV format)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    return img_bgr


def findElement(
    window_size: tuple[int, int, int, int],
    img_list: list[np.ndarray] | np.ndarray,
    threshold: float = 0.85,
    invert_threshold: bool = False,
    leniency: float = 0.0,
    max_tries: int = 100,
    fallback_func: Callable[[], None] = lambda: print("Failed to find object"),
):
    if not isinstance(img_list, list):
        img_list = [img_list]

    threshold, max_val, tries = preassign(threshold, invert_threshold)

    while max_val <= threshold:
        ss_img = takeScreenshotDirect(window_size)

        n = len(img_list)
        _vals = [0.0] * n
        _locs = [0.0] * n
        for i in range(n):
            result = cv2.matchTemplate(ss_img, img_list[i], cv2.TM_CCOEFF_NORMED)
            _, _vals[i], _, _locs[i] = cv2.minMaxLoc(result)  # type: ignore

        ind = _vals.index(max(_vals))
        max_val = _vals[ind]
        max_loc = _locs[ind]

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


# ============ Input Scheduler ============
class InputScheduler:
    def __init__(self):
        self.input_queue = asyncio.Queue()
        self.priority_queue = asyncio.Queue()  # High priority queue
        self.current_window: Optional[int] = None
        self.scheduler_task: Optional[asyncio.Task] = None
        self._running = False
        self._priority_mode = False  # Track if we're in priority mode
        self._priority_window: Optional[int] = None  # Window that has priority

    async def start(self):
        """Start the input scheduler"""
        print(f"[INPUT_SCHEDULER] Starting input scheduler...")
        self._running = True
        print(f"[INPUT_SCHEDULER] Running flag set to: {self._running}")
        self.scheduler_task = asyncio.create_task(self._process_input_queue())
        print(f"[INPUT_SCHEDULER] Scheduler task created: {self.scheduler_task}")
        print("Input scheduler started")

    async def stop(self):
        """Stop the input scheduler"""
        print(f"[INPUT_SCHEDULER] Stopping input scheduler...")
        self._running = False
        print(f"[INPUT_SCHEDULER] Running flag set to: {self._running}")
        if self.scheduler_task:
            print(f"[INPUT_SCHEDULER] Cancelling scheduler task: {self.scheduler_task}")
            self.scheduler_task.cancel()
            try:
                await self.scheduler_task
                print(f"[INPUT_SCHEDULER] Scheduler task cancelled successfully")
            except asyncio.CancelledError:
                print(
                    f"[INPUT_SCHEDULER] Scheduler task cancelled with CancelledError (expected)"
                )
                pass
        else:
            print(f"[INPUT_SCHEDULER] No scheduler task to cancel")
        print("Input scheduler stopped")

    async def _process_input_queue(self):
        """Process input queue with priority support"""
        print("[INPUT_SCHEDULER] Starting input queue processor")
        loop_count = 0

        while self._running:
            loop_count += 1
            print(f"[INPUT_SCHEDULER] Loop #{loop_count} - Running: {self._running}")

            try:
                # Check priority queue first
                priority_queue_size = self.priority_queue.qsize()
                print(f"[INPUT_SCHEDULER] Priority queue size: {priority_queue_size}")

                if not self.priority_queue.empty():
                    print(f"[INPUT_SCHEDULER] Processing priority queue item")
                    input_request = await self.priority_queue.get()
                    print(
                        f"[INPUT_SCHEDULER] Got priority input request: {input_request}"
                    )
                    await self._execute_input(input_request)
                    self.priority_queue.task_done()
                    print(
                        f"[INPUT_SCHEDULER] Priority input completed, task_done() called"
                    )
                    continue

                # If not in priority mode, process regular queue
                regular_queue_size = self.input_queue.qsize()
                print(f"[INPUT_SCHEDULER] Regular queue size: {regular_queue_size}")
                print(f"[INPUT_SCHEDULER] Priority mode: {self._priority_mode}")

                if not self._priority_mode and not self.input_queue.empty():
                    print(f"[INPUT_SCHEDULER] Processing regular queue item")
                    input_request = await self.input_queue.get()
                    print(
                        f"[INPUT_SCHEDULER] Got regular input request: {input_request}"
                    )
                    await self._execute_input(input_request)
                    self.input_queue.task_done()
                    print(
                        f"[INPUT_SCHEDULER] Regular input completed, task_done() called"
                    )
                else:
                    # No inputs to process, sleep briefly
                    if self._priority_mode:
                        print(
                            f"[INPUT_SCHEDULER] In priority mode, skipping regular queue"
                        )
                    else:
                        print(
                            f"[INPUT_SCHEDULER] No inputs to process, sleeping for 0.1s"
                        )
                    await asyncio.sleep(0.1)

            except asyncio.CancelledError:
                print(f"[INPUT_SCHEDULER] CancelledError caught, breaking loop")
                break
            except Exception as e:
                print(f"[INPUT_SCHEDULER] Unexpected error in loop: {e}")
                import traceback

                traceback.print_exc()
                await asyncio.sleep(0.1)  # Brief pause before retrying

        print(
            f"[INPUT_SCHEDULER] Input queue processor stopped after {loop_count} loops"
        )

    async def _execute_input(self, input_request):
        """Execute a single input request"""
        print(f"[INPUT_SCHEDULER] Executing input request: {input_request}")
        window_id, input_type, *args = input_request
        print(
            f"[INPUT_SCHEDULER] Parsed: window_id={window_id}, input_type={input_type}, args={args}"
        )

        # Activate window if different from current
        print(
            f"[INPUT_SCHEDULER] Current window: {self.current_window}, target window: {window_id}"
        )
        if self.current_window != window_id:
            print(
                f"[INPUT_SCHEDULER] Window change needed, activating window {window_id}"
            )
            await self._activate_window(window_id)
            self.current_window = window_id
            print(
                f"[INPUT_SCHEDULER] Window {window_id} activated, current_window updated"
            )
        else:
            print(f"[INPUT_SCHEDULER] No window change needed")

        # Execute the input
        print(f"[INPUT_SCHEDULER] Executing {input_type} input...")
        if input_type == "click":
            x, y = args
            print(f"[INPUT_SCHEDULER] About to click at ({x}, {y})")
            pyautogui.click(x, y)
            print(f"Window {window_id + 1}: Clicked at ({x}, {y})")
        elif input_type == "type":
            text = args[0]
            print(f"[INPUT_SCHEDULER] About to type: '{text}'")
            pyautogui.write(text)
            print(f"Window {window_id + 1}: Typed '{text}'")
        elif input_type == "key":
            key = args[0]
            print(f"[INPUT_SCHEDULER] About to press key: '{key}'")
            pyautogui.press(key)
            print(f"Window {window_id + 1}: Pressed key '{key}'")
        elif input_type == "hotkey":
            keys = args
            print(f"[INPUT_SCHEDULER] About to press hotkey: {'+'.join(keys)}")
            pyautogui.hotkey(*keys)
            print(f"Window {window_id + 1}: Pressed hotkey {'+'.join(keys)}")
        else:
            print(f"[INPUT_SCHEDULER] Unknown input type: {input_type}")

        print(f"[INPUT_SCHEDULER] Input execution completed")

    async def _activate_window(self, window_id):
        """Activate a specific window"""
        # Find the window instance and activate it
        for inst in win_instances:
            if inst.id == window_id:
                inst.activate()
                print(f"Activated Window {window_id + 1}")
                await asyncio.sleep(0.1)  # Small delay for window activation
                break

    async def schedule_click(self, window_id: int, x: int, y: int):
        """Schedule a click operation"""
        print(
            f"[INPUT_SCHEDULER] Scheduling click for window {window_id} at ({x}, {y})"
        )
        await self.input_queue.put((window_id, "click", x, y))
        print(
            f"[INPUT_SCHEDULER] Click scheduled, queue size: {self.input_queue.qsize()}"
        )

    async def schedule_type(self, window_id: int, text: str):
        """Schedule a typing operation"""
        print(f"[INPUT_SCHEDULER] Scheduling type for window {window_id}: '{text}'")
        await self.input_queue.put((window_id, "type", text))
        print(
            f"[INPUT_SCHEDULER] Type scheduled, queue size: {self.input_queue.qsize()}"
        )

    async def schedule_key(self, window_id: int, key: str):
        """Schedule a key press"""
        print(f"[INPUT_SCHEDULER] Scheduling key press for window {window_id}: '{key}'")
        await self.input_queue.put((window_id, "key", key))
        print(
            f"[INPUT_SCHEDULER] Key press scheduled, queue size: {self.input_queue.qsize()}"
        )

    async def schedule_hotkey(self, window_id: int, *keys):
        """Schedule a hotkey combination"""
        print(
            f"[INPUT_SCHEDULER] Scheduling hotkey for window {window_id}: {'+'.join(keys)}"
        )
        await self.input_queue.put((window_id, "hotkey", *keys))
        print(
            f"[INPUT_SCHEDULER] Hotkey scheduled, queue size: {self.input_queue.qsize()}"
        )

    # Priority scheduling methods
    async def schedule_priority_click(self, window_id: int, x: int, y: int):
        """Schedule a high-priority click operation"""
        print(
            f"[INPUT_SCHEDULER] Scheduling PRIORITY click for window {window_id} at ({x}, {y})"
        )
        await self.priority_queue.put((window_id, "click", x, y))
        print(
            f"[INPUT_SCHEDULER] Priority click scheduled, priority queue size: {self.priority_queue.qsize()}"
        )

    async def schedule_priority_type(self, window_id: int, text: str):
        """Schedule a high-priority typing operation"""
        print(
            f"[INPUT_SCHEDULER] Scheduling PRIORITY type for window {window_id}: '{text}'"
        )
        await self.priority_queue.put((window_id, "type", text))
        print(
            f"[INPUT_SCHEDULER] Priority type scheduled, priority queue size: {self.priority_queue.qsize()}"
        )

    async def schedule_priority_key(self, window_id: int, key: str):
        """Schedule a high-priority key press"""
        print(
            f"[INPUT_SCHEDULER] Scheduling PRIORITY key press for window {window_id}: '{key}'"
        )
        await self.priority_queue.put((window_id, "key", key))
        print(
            f"[INPUT_SCHEDULER] Priority key press scheduled, priority queue size: {self.priority_queue.qsize()}"
        )

    async def schedule_priority_hotkey(self, window_id: int, *keys):
        """Schedule a high-priority hotkey combination"""
        print(
            f"[INPUT_SCHEDULER] Scheduling PRIORITY hotkey for window {window_id}: {'+'.join(keys)}"
        )
        await self.priority_queue.put((window_id, "hotkey", *keys))
        print(
            f"[INPUT_SCHEDULER] Priority hotkey scheduled, priority queue size: {self.priority_queue.qsize()}"
        )

    async def enter_priority_mode(self, window_id: int):
        """Enter priority mode for a specific window"""
        print(f"[INPUT_SCHEDULER] Entering priority mode for Window {window_id + 1}")
        self._priority_mode = True
        self._priority_window = window_id
        print(
            f"[INPUT_SCHEDULER] Priority mode enabled: {self._priority_mode}, priority window: {self._priority_window}"
        )

    async def exit_priority_mode(self):
        """Exit priority mode"""
        print(f"[INPUT_SCHEDULER] Exiting priority mode")
        self._priority_mode = False
        self._priority_window = None
        print(
            f"[INPUT_SCHEDULER] Priority mode disabled: {self._priority_mode}, priority window: {self._priority_window}"
        )

    async def wait_for_completion(self):
        """Wait for all queued inputs to complete"""
        await self.input_queue.join()
        await self.priority_queue.join()


# Global input scheduler instance
input_scheduler = InputScheduler()


# ============ Main ============
if not sys.platform.startswith("win"):
    raise ValueError("Cannot run on Linux!")

checkTime()

# SETUP EXCEL
import win32com.client  # type: ignore  # noqa: E402

os.chdir(dir_path)
excel = win32com.client.Dispatch("Excel.Application")

if os.path.exists(file_path):
    print("The xl already exist")
    WORKBOOK = excel.Workbooks.Open(file_path)
    sheet = WORKBOOK.Sheets(1)
    WORKBOOK.Save()
    esheet = pd.read_excel(file_path)
    ITER_RANGE = list(esheet.loc[esheet["status"] == "not checked"].index)
else:
    print("New xl")
    WORKBOOK = excel.Workbooks.Add()
    sheet = WORKBOOK.Sheets(1)
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
    WORKBOOK.SaveAs(file_path)

    ITER_RANGE = range(n)

print(df)

excel.Visible = True
win2 = pw.getWindowsWithTitle(file_name + " - Excel")
excel_win = win2[0]
excel_win.moveTo(0, 490)
# SETUP EXCEL END


class Window:
    _w = 720
    _h = 480
    prev_server = None

    win: pw.Win32Window

    def __init__(self, win: pw.Win32Window, ind: int = 0):
        # windows = pw.getWindowsWithTitle(title)
        # if not windows:
        #     raise ValueError("Window not found!")
        # win: pw.Win32Window = windows[0]
        win.resizeTo(self._w, self._h)

        # TODO: set ind to move window to diff location

        win.moveTo(self._w * (ind), 0)
        x, y = win.left, win.top
        w, h = win.width, win.height

        self.win = win
        self.size = (x, y, x + w, y + h)
        self.size0 = np.array((x, y))
        self.w = w
        self.h = h
        self.id = ind

    async def findClick(
        self,
        img_list: list[np.ndarray] | np.ndarray,
        threshold: float = 0.85,
        invert_threshold: bool = False,
        leniency: float = 0,
        max_tries: int = 999,
    ):
        loc, val = findElement(
            self.size,
            img_list,
            threshold=threshold,
            invert_threshold=invert_threshold,
            leniency=leniency,
            max_tries=max_tries,
        )
        if val == "FOUND":
            click_x, click_y = self.size0 + loc
            await input_scheduler.schedule_click(self.id, click_x, click_y)

    async def findClickPriority(
        self,
        img_list: list[np.ndarray] | np.ndarray,
        threshold: float = 0.85,
        invert_threshold: bool = False,
        leniency: float = 0,
        max_tries: int = 999,
    ):
        """Find and click with priority (for multi-step actions)"""
        loc, val = findElement(
            self.size,
            img_list,
            threshold=threshold,
            invert_threshold=invert_threshold,
            leniency=leniency,
            max_tries=max_tries,
        )
        if val == "FOUND":
            click_x, click_y = self.size0 + loc
            await input_scheduler.schedule_priority_click(self.id, click_x, click_y)

    async def typePriority(self, text: str):
        """Type text with priority (for multi-step actions)"""
        await input_scheduler.schedule_priority_type(self.id, text)

    async def keyPriority(self, key: str):
        """Press key with priority (for multi-step actions)"""
        await input_scheduler.schedule_priority_key(self.id, key)

    async def hotkeyPriority(self, *keys):
        """Press hotkey with priority (for multi-step actions)"""
        await input_scheduler.schedule_priority_hotkey(self.id, *keys)

    def findWait(
        self,
        img_list: list[np.ndarray] | np.ndarray,
        threshold: float = 0.85,
        invert_threshold: bool = False,
        max_tries: int = 999,
    ):
        _, val = findElement(
            self.size,
            img_list,
            threshold=threshold,
            invert_threshold=invert_threshold,
            max_tries=max_tries,
        )
        return val

    def activate(self):
        if not self.win.isActive:
            pyautogui.click(self.size0[0] + 15, self.size0[1] + 1)

    async def run_for_account(self, acc_ind: int):
        print("Clicking other_login")
        await self.findClick(Template.OTHER_LOGIN)

        if self.findWait(Template.OTHER_LOGIN, threshold=0.9, max_tries=2) == "FOUND":
            await self.findClick(Template.OTHER_LOGIN, threshold=0.9, max_tries=2)

        print("Clicking email_signin")
        # Enter priority mode for multi-step action
        await input_scheduler.enter_priority_mode(self.id)

        # Click email signin with priority
        await self.findClickPriority(Template.EMAIL_SIGNIN)

        debug_update(acc_ind, "Logging")
        print(f"Typing email for index {acc_ind}")
        # Type email with priority (ensures it goes to the right textbox)
        await self.typePriority(df.email[acc_ind])

        # Exit priority mode after multi-step action

        print("Clicking next_step")
        await self.findClickPriority(Template.NEXT_STEP)
        while self.findWait(Template.NEXT_STEP, threshold=0.9, max_tries=2) == "FOUND":
            print("Clicking next_step again")
            await self.findClickPriority(Template.NEXT_STEP, threshold=0.9, max_tries=2)
            sleep(1)
        sleep(2)

        print(f"Typing password for index {acc_ind}")
        await self.typePriority(df.password[acc_ind])

        await input_scheduler.exit_priority_mode()

        print("Clicking login")
        await self.findClick(Template.LOGIN)
        sleep(1.0)

        await self.findClick(Template.ENTER)

        # Check server of the account
        srv = df.server[acc_ind]
        if srv != self.prev_server:
            # Switch server only if diff server compared to previous
            self.prev_server = srv

            debug_update(acc_ind, "Server Selection")
            print("Clicking server_green_button")
            await self.findClick(Template.SERVER_GREEN_BUTTON)

            print("Clicking server")
            match srv:
                case "aestral_noa":
                    srv_template = Template.SERVER_AESTRAL_NOA
                case "animus":
                    srv_template = Template.SERVER_ANIMUS
                case _:
                    raise ValueError("")
            await self.findClick(
                srv_template,
                threshold=0.9,
                max_tries=5,
            )

        print("Clicking enter")
        await self.findClick(Template.ENTER)

        debug_update(acc_ind, "Entering Game")
        print("Waiting for origin_reso to appear")
        self.findWait(Template.ORIGIN_RESO, max_tries=5)

        print("Waiting for origin_reso to disappear")
        self.findWait(Template.ORIGIN_RESO, invert_threshold=True, max_tries=50)
        sleep(7)

        debug_update(acc_ind, "Entered Game")
        print("Clicking uid_text")
        await self.findClick(Template.UID_TEXT, max_tries=10)
        sleep(0.5)

        print("Cancelling pass window, if exists")
        await self.findClick(Template.PASS_CANCEL, max_tries=2)

        print("Clicking anywhere text")
        await self.findClick(Template.ANYWHERE_TEXT, max_tries=2)

        # pyautogui.press('tab') #Secret

        if LOGIN_REWARDS:
            print("Objective: Supply Run")
            debug_update(acc_ind, "Supply Run")

            print("Clicking Gift Box Icon")
            await input_scheduler.schedule_hotkey(self.id, "alt", "1")

            print("Clicking special_operation")
            await self.findClick(Template.SPECIAL_OPERATION)

            print("Clicking summer_welfare")
            await self.findClick(Template.SUMMER_WELFARE)

            # print("Clicking supply_run")
            # main_win.findClick(Template.SUPPLY_RUN)

            print("Clicking supply_claim")
            await self.findClick(Template.SUPPLY_CLAIM, max_tries=2)
            await self.findClick(Template.FINAL_SUPPLY_CLAIM, max_tries=2)

            print("Waiting for all_rewards_collected")
            if self.findWait(Template.ALL_REWARDS_COLLECTED, max_tries=2) == "FOUND":
                print("All rewards collected")
                supply_run_update(acc_ind, "Completed")
            else:
                print("Not all rewards collected")
                supply_run_update(acc_ind, "Not Completed")

            # print("Clicking supply_run_2")
            # main_win.findClick(supply_run_2)

            # print("Clicking supply_claim")
            # main_win.findClick(supply_claim, max_tries=5)
            # main_win.findClick(final_supply_claim,max_tries=2)

            # print("Waiting for all_rewards_collected")
            # if main_win.findWait(all_rewards_collected, max_tries=5) == 'FOUND':
            #     print("All rewards collected")
            #     supply_run_2_update(i, 'Completed')
            # else:
            #     print("Not all rewards collected")
            #     supply_run_2_update(i, 'Not Completed')

            print("Clicking back_button")
            await self.findClick(Template.BACK_BUTTON, max_tries=2, threshold=0.75)

        if OLDMAN:
            print("Objective: Oldman")
            debug_update(acc_ind, "Checking Oldman")

            print("Clicking sword_icon")

            await input_scheduler.enter_priority_mode(self.id)

            await input_scheduler.schedule_priority_hotkey(self.id, "alt", "3")
            # pyautogui.hotkey('alt', '3')
            # main_win.findClick(Template.SWORD_ICON,threshold=0.75)

            await input_scheduler.exit_priority_mode()

            print("Clicking casual_tab")
            await self.findClick(Template.CASUAL_TAB)

            print("Clicking artificial_island_icon")
            await self.findClick(Template.ARTIFICIAL_ISLAND_ICON)

            print("Waiting for oldman_icon")
            self.findWait(Template.OLDMAN_ICON, max_tries=3)

            print("Waiting for oldman_icon (status check)")
            oldman_status_ = self.findWait(Template.OLDMAN_ICON, max_tries=2)
            print("DEBUG: oldman", oldman_status_)
            oldman_update(acc_ind, oldman_status_)

            print("Clicking back_button")
            await self.findClick(Template.BACK_BUTTON, threshold=0.75)

            print("Clicking back_button again")
            await self.findClick(Template.BACK_BUTTON, threshold=0.75)
            sleep(1)

        if BYGONE_MISSION:
            print("Objective: Bygone Phantasm")
            debug_update(acc_ind, "Bygone Mission")
            print("Pressing Enter")
            await input_scheduler.schedule_key(self.id, "enter")
            print("Clicking sword_icon")
            await input_scheduler.schedule_hotkey(self.id, "alt", "3")
            # pyautogui.hotkey('alt', '3')
            # main_win.findClick(Template.SWORD_ICON,threshold=0.75)

            print("Clicking challenge_button")
            await self.findClick(Template.CHALLENGE_BUTTON)

            print("Clicking bygone_icon")
            await self.findClick(Template.BYGONE_ICON)

            print("Clicking sneak level_button")
            await self.findClick(Template.SNEAK_LEVEL_BUTTON, threshold=0.7)

            print("Waiting for initiating_transmission to appear")
            self.findWait(Template.INITIATING_TRANSMISSION)

            print("Waiting for initiating_transmission to disappear")
            self.findWait(
                Template.INITIATING_TRANSMISSION,
                invert_threshold=True,
                max_tries=50,
            )

            print("Waiting for origin_reso to appear")
            self.findWait(Template.ORIGIN_RESO, max_tries=5)

            print("Waiting for origin_reso to disappear")
            self.findWait(Template.ORIGIN_RESO, invert_threshold=True, max_tries=50)

            print("Clicking skip_button")
            await self.findClick(Template.SKIP_BUTTON, max_tries=10)

            print("Waiting for exit_button to appear")
            self.findWait(Template.EXIT_BUTTON)

            print("Pressing ESC key")
            await input_scheduler.schedule_key(self.id, "esc")

            print("Clicking exit_button")
            await self.findClick(Template.EXIT_BUTTON)

            print("Clicking ok_button")
            await self.findClick(Template.OK_BUTTON)

            print("Sleeping for 7 seconds")
            sleep(7)

            self.findWait(Template.UID_TEXT)
            sleep(1)

        # main_win.findWait(sword_icon,threshold=0.75)
        # print("Clicking recommended_button")
        # main_win.findClick(recommended_button,threshold=0.75)

        if REDEEM_REWARDS:
            print("Clicking gift box icon")
            await input_scheduler.schedule_hotkey(self.id, "alt", "1")

            print("Clicking rewards button")
            await self.findClick(Template.REWARDS_BUTTON)

            print("Clicking exchange button")
            await self.findClick(Template.EXCHANGE_BUTTON)

            print("Clicking gift code block")
            await self.findClick(Template.GIFT_CODE_BLOCK)

            print("Writing redeem code")
            await input_scheduler.schedule_type(self.id, redeem_code)

            print("Clicking confirm button")
            await self.findClick(Template.CONFIRM_BUTTON)

            print("Clicking back button")
            await self.findClick(Template.BACK_BUTTON)

        if MIA_KITCHEN_MISSION:
            print("Objective: Mia's Kitchen")
            debug_update(acc_ind, "Mia Kitchen Mission")

            print("Clicking sword_icon")
            await input_scheduler.schedule_hotkey(self.id, "alt", "3")

            print("Clicking recommended button")
            await self.findClick(Template.RECOMMENDED_BUTTON)

            print("Waiting for mia_kitchen_done_icon")
            while self.findWait(Template.MIA_KITCHEN_ICON, max_tries=2) == "FOUND":
                print("mia_kitchen_done_icon not found, retrying...")
                print("Clicking mia_kitchen_icon")
                await self.findClick(Template.MIA_KITCHEN_ICON)

                print("Clicking taste_button")
                await self.findClick(Template.TASTE_BUTTON)

                print("Clicking back_button")
                await self.findClick(Template.BACK_BUTTON, threshold=0.75)
                sleep(2)

                self.findWait(Template.CONGRATULATIONS_TEXT)
                await self.findClick(Template.ANYWHERE_TEXT)

            print("Clicking back_button")
            await self.findClick(Template.BACK_BUTTON, threshold=0.75)

        if CLAIM_MAIL:
            debug_update(acc_ind, "claim mail")

            print("Closing chat")
            await self.findClick(Template.CHAT_CLOSE_BUTTON, max_tries=2)
            sleep(0.5)

            print("Press Escape key")
            await input_scheduler.schedule_key(self.id, "esc")

            print("Clicking mail icon")
            await self.findClick(
                [Template.MAIL_ICON, Template.MAIL_ICON2],
                threshold=0.75,
            )

            print("Clicking claim all button")
            await self.findClick(Template.CLAIM_ALL_BUTTON)

            sleep(1.0)  # safer with delay

            print("Click anywhere text")
            await self.findClick(Template.ANYWHERE_TEXT, max_tries=2)

            print("Clicking delete all button")
            await self.findClick(Template.DELETE_ALL_BUTTON)

            print("Clicking OK button")
            await self.findClick(Template.OK_BUTTON, max_tries=2)

            print("Clicking back button")
            await self.findClick(Template.BACK_BUTTON)

        if VITALITY_MISSION:
            print("Vitality mission active")
            debug_update(acc_ind, "Vitality Mission")

            print("Clicking sword_icon")
            await input_scheduler.schedule_hotkey(self.id, "alt", "3")

            print("Clicking recommended button")
            await self.findClick(Template.RECOMMENDED_BUTTON)

            print("Clicking dimensinal_trials_button")
            await self.findClick(Template.DIMENSINAL_TRIALS_BUTTON, threshold=0.75)

            print("Clicking gold_drill_button")
            await self.findClick(Template.GOLD_DRILL_BUTTON)

            print("Clicking go_button")
            await self.findClick(Template.GO_BUTTON)

            print("Waiting for quick_battle_button")
            if self.findWait(Template.QUICK_BATTLE_BUTTON, max_tries=2) == "FOUND":
                print("Clicking quick_battle_button")
                await self.findClick(Template.QUICK_BATTLE_BUTTON)

            print("Checking for operation_success_text")
            if self.findWait(Template.OPERATION_SUCCESS_TEXT, max_tries=2) == "FOUND":
                print("Operation success found — marking as completed")
                dimensional_trials_update(acc_ind, "Completed")
            else:
                print("Operation success not found — still marking as completed")
                dimensional_trials_update(acc_ind, "Not Completed")

            print("Clicking anywhere_text")
            await self.findClick(Template.ANYWHERE_TEXT)

            print("Clicking cross_button")
            await self.findClick(Template.CROSS_BUTTON, threshold=0.8)

            print("Clicking back_button")
            await self.findClick(Template.BACK_BUTTON, threshold=0.75)

            print("Clicking back_button")
            await self.findClick(Template.BACK_BUTTON, max_tries=2, threshold=0.75)

        if CREW_DONATIONS:
            debug_update(acc_ind, "crew donations")

            print("Pressing Enter")
            await input_scheduler.schedule_key(self.id, "enter")

            print("Clicking esc_button")
            await self.findClick(Template.ESC_BUTTON, max_tries=2, threshold=0.75)

            print("Clicking crew_icon")
            await self.findClick(
                [Template.CREW_ICON, Template.CREW_ICON_2], max_tries=2
            )

            debug_update(acc_ind, "Daily Donation")
            print("Clicking daily button")
            await self.findClick(Template.DAILY_BUTTON)

            print("Clicking donate button")
            await self.findClick(Template.DONATE_BUTTON)

            if self.findWait(Template.OK_BUTTON, max_tries=2) == "FOUND":
                daily_dono_update(acc_ind, "Donated")
            else:
                daily_dono_update(acc_ind, "Not Donated")
            print("Clicking donation ok button")
            await self.findClick(Template.OK_BUTTON, max_tries=2)

            print("Clicking back button")
            await self.findClick(Template.BACK_BUTTON, threshold=0.75)

            print("Press Escape key")
            await input_scheduler.schedule_key(self.id, "esc")

        print("Clicking esc_button")
        await input_scheduler.schedule_key(self.id, "esc")

        print("Clicking settings_button")
        await self.findClick([Template.SETTINGS_BUTTON, Template.SETTINGS_BUTTON_2])

        print("Clicking switch_acc_button")
        await self.findClick(Template.SWITCH_ACC_BUTTON)
        sleep(2)

        print("Clicking switch_acc_text")
        await self.findClick(Template.SWITCH_ACC_TEXT)

        status_update(acc_ind, "checked")
        debug_update(acc_ind, "")

        print("Waiting for origin_reso to appear")
        self.findWait(Template.ORIGIN_RESO, max_tries=5)

        print("Waiting for origin_reso to disappear")
        self.findWait(Template.ORIGIN_RESO, invert_threshold=True, max_tries=50)
        sleep(2)

    async def process_queue(self, account_queue: queue.Queue):
        while not account_queue.empty():
            try:
                # Get next account from queue (non-blocking)
                acc_ind = account_queue.get_nowait()
                print(f"Window {self.id + 1} processing account {acc_ind}")
                await self.run_for_account(acc_ind)
                WORKBOOK.Save()
                print(f"Window {self.id + 1} completed account {acc_ind}")
            except queue.Empty:
                # Queue is empty, we're done
                print(f"Window {self.id + 1} finished - no more accounts in queue")
                break


win_instances = [
    Window(win, i) for i, win in enumerate(pw.getWindowsWithTitle(window_title))
]


async def main():
    print("\nGo to login screen where you will input the email and password")
    input("Press any key to continue after 3 seconds...\n")

    sleep(3)

    ITER_RANGE = range(n)

    try:
        # Start the input scheduler
        print("[MAIN] Starting input scheduler...")
        await input_scheduler.start()
        print("[MAIN] Input scheduler started successfully")

        # Create a shared queue with all accounts
        account_queue = queue.Queue()
        total_accounts = len(ITER_RANGE)
        num_windows = len(win_instances)

        # Add all accounts to the queue
        for acc_ind in ITER_RANGE:
            account_queue.put(acc_ind)

        print(f"Total accounts: {total_accounts}")
        print(f"Number of windows: {num_windows}")
        print("All accounts added to shared queue")
        print(
            "Windows will process accounts as they become available (dynamic load balancing)"
        )

        # Create tasks for all windows to process the queue concurrently
        tasks = []
        for inst in win_instances:
            task = asyncio.create_task(inst.process_queue(account_queue))
            tasks.append(task)

        print(f"[MAIN] Created {len(tasks)} window tasks")
        print("[MAIN] Running window tasks and input scheduler concurrently...")

        # Run both window tasks and input scheduler task concurrently
        all_tasks = tasks + [input_scheduler.scheduler_task]
        await asyncio.gather(*all_tasks)

        print("[MAIN] All tasks completed")

    except KeyboardInterrupt:
        print("Interrupt signal detected!")
        WORKBOOK.Save()
    finally:
        # Stop the input scheduler
        await input_scheduler.stop()

    WORKBOOK.Save()  # type: ignore


if __name__ == "__main__":
    asyncio.run(main())
