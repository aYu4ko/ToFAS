import asyncio
import codecs
import os
import queue
import sys
from asyncio.tasks import Task
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from time import sleep
from typing import Callable, Literal, Optional
from zoneinfo import ZoneInfo

import cv2
import numpy as np
import pandas as pd
import pyautogui
import pygetwindow as pw  # type: ignore
from dotenv import load_dotenv

from template import Template

# Check dotenv
if os.path.exists(".env"):
    load_dotenv()
    RIM_PASSWORD = os.environ.get("RIM_PASSWORD", "")

    if not RIM_PASSWORD:
        raise ValueError("Environment variable 'RIM_PASSWORD' not set!")
else:
    raise ValueError(".env file missing!")


# ============ Initial Setup ============
pyautogui.FAILSAFE = False

NORMAL_PAUSE = 0.5
FAST_PAUSE = 2 / 60

pyautogui.PAUSE = FAST_PAUSE

show_d = False
dir_path = sys.path[0]

date = datetime.now(ZoneInfo("Asia/Chongqing"))
formatted_date = date.strftime("%Y-%m-%d")
formatted_time = float(date.strftime("%H.%M"))
thresh_factor = 0.95

# CSV file paths
file_name = formatted_date + ".csv"
file_path = os.path.join(dir_path, file_name)
creds_path = os.path.join(dir_path, "accounts.csv")

# Read account data from CSV
df = pd.read_csv(creds_path)
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

# Global DataFrame for progress tracking
progress_df: Optional[pd.DataFrame] = None


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


# ============ CSV Helper Functions ============


def save_progress():
    """Save the progress DataFrame to CSV file"""
    global progress_df
    if progress_df is not None:
        progress_df.to_csv(file_path, index=False)
        print(f"Progress saved to {file_path}")


def status_update(i: int, value: str):
    global progress_df
    if progress_df is not None:
        progress_df.loc[i, "status"] = value
        save_progress()


def daily_dono_update(i: int, value: str):
    global progress_df
    if progress_df is not None:
        progress_df.loc[i, "daily dono"] = value
        save_progress()


def dimensional_trials_update(i: int, value: str):
    global progress_df
    if progress_df is not None:
        progress_df.loc[i, "dimensional trials"] = value
        save_progress()


def oldman_update(i: int, value: str):
    global progress_df
    if progress_df is not None:
        progress_df.loc[i, "oldman"] = value
        save_progress()


def supply_run_update(i: int, value: str):
    global progress_df
    if progress_df is not None:
        progress_df.loc[i, "supply run"] = value
        save_progress()


def supply_run_2_update(i: int, value: str):
    global progress_df
    if progress_df is not None:
        progress_df.loc[i, "supply run 2"] = value
        save_progress()


def debug_update(i: int, value: str):
    global progress_df
    if progress_df is not None:
        progress_df.loc[i, "debug"] = value
        save_progress()


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


def takeScreenshotDirect(window_size=(0, 0, 720, 480)):
    """Take screenshot directly and return as numpy array for OpenCV"""
    im = pyautogui.screenshot(region=window_size)
    # Convert PIL Image to numpy array (RGB format)
    img_array = np.array(im)
    # Convert RGB to BGR (OpenCV format)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    return img_bgr


async def findElement(
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
            await asyncio.sleep(1.5)

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

# # Global input scheduler instance
# input_scheduler = InputScheduler()


class RequestType(Enum):
    CLICK = 0
    KEY = 1
    TYPE = 2
    SHORTCUT = 3
    PRIORITY_START = 4
    PRIORITY_END = 5


@dataclass(slots=True)
class InputRequest:
    request_type: RequestType
    args: tuple
    window: "Window"
    event: asyncio.Event = field(init=False, default_factory=asyncio.Event)

    def execute(self, current_window: int):
        if current_window != self.window.id:
            pyautogui.keyDown("alt")
            pyautogui.click(self.window.size0[0] + 15, self.window.size0[1] + 1)
            pyautogui.keyUp("alt")

        match self.request_type:
            case RequestType.CLICK:
                pyautogui.click(*self.args)
            case RequestType.KEY:
                pyautogui.press(*self.args)
            case RequestType.TYPE:
                pyautogui.write(*self.args)
            case RequestType.SHORTCUT:
                # pyautogui.shortcut(*self.args)
                pyautogui.keyDown(self.args[0])
                sleep(FAST_PAUSE)
                pyautogui.press(self.args[1])
                sleep(FAST_PAUSE)
                pyautogui.keyUp(self.args[0])

                # pyautogui.hotkey(*self.args)
            case _:
                raise ValueError(f"Invalid request type {self.request_type}")

        self.event.set()


@dataclass(slots=True)
class RimInputScheduler:
    main_queue: asyncio.Queue[InputRequest] = field(
        init=False, default_factory=asyncio.Queue
    )
    incoming_queue: asyncio.Queue[InputRequest] = field(
        init=False, default_factory=asyncio.Queue
    )

    running: bool = field(init=False, default=False)
    current_window: int = field(init=False, default=-1)

    priority_window: Optional[int] = field(init=False, default=None)
    _task: Task = field(init=False)

    _acc_queue: Optional[queue.Queue] = field(init=False, default=None)

    def set_queue(self, queue: queue.Queue):
        self._acc_queue = queue

    async def start(self):
        self.running = True
        self._task = asyncio.create_task(self._processor())

    async def stop(self):
        self.running = False
        if self._task:
            self._task.cancel()
            await self._task

    async def _processor(self):
        move_back_count = 0
        while self.running and not self._acc_queue.empty():
            # Process main queue
            if not self.main_queue.empty():
                req = await self.main_queue.get()
                req.execute(self.current_window)
                self.current_window = req.window.id
                continue

            # Process incoming queue
            # Note that this is only processed when main queue is empty
            if not self.incoming_queue.empty():
                if move_back_count >= 2000:
                    raise ValueError("Move back loop detected!")
                else:
                    await asyncio.sleep(0.1)

                req = await self.incoming_queue.get()

                # In priority mode
                if self.priority_window is not None:
                    if (req.request_type == RequestType.PRIORITY_END) and (
                        self.priority_window == self.current_window
                    ):
                        # End priority
                        self.priority_window = None
                        req.event.set()
                        print("[PROCESSOR] Ending Priority Request")

                        move_back_count = 0
                        continue
                    elif self.priority_window == req.window.id:
                        # executing on priority window
                        await self.main_queue.put(req)
                        print("[PROCESSOR] Executing priority task")

                        move_back_count = 0
                        continue
                    else:
                        # move back non-priority window task
                        await self.incoming_queue.put(req)
                        # print(
                        #     f"[PROCESSOR] Moving back non-priority task with id {req.window.id}"
                        # )

                        move_back_count += 1
                        continue

                else:
                    # No-priority mode

                    if req.request_type == RequestType.PRIORITY_START:
                        # Start priority mode
                        self.priority_window = req.window.id
                        req.event.set()
                        print(f"[PROCESSOR] Starting priority for {req.window.id}")

                        move_back_count = 0
                        continue
                    else:
                        # Execute normal stuff
                        await self.main_queue.put(req)
                        print(
                            f"[PROCESSOR] Executing task: {req.request_type} {req.args}"
                        )

                        move_back_count = 0
                        continue

            await asyncio.sleep(0.5)

    async def schedule(self, request: InputRequest):
        await self.incoming_queue.put(request)


input_scheduler = RimInputScheduler()

# ============ Main ============
if not sys.platform.startswith("win"):
    raise ValueError("Cannot run on Linux!")

checkTime()

# SETUP CSV
os.chdir(dir_path)

if os.path.exists(file_path):
    print("The CSV already exists")
    progress_df = pd.read_csv(file_path)
    ITER_RANGE = list(progress_df.loc[progress_df["status"] == "not checked"].index)
else:
    print("New CSV")
    # Create progress DataFrame with all required columns
    progress_df = creds.copy()
    progress_df["status"] = "not checked"
    progress_df["daily dono"] = ""
    progress_df["dimensional trials"] = ""
    progress_df["oldman"] = ""
    progress_df["supply run"] = ""
    # progress_df["supply run 2"] = ""
    progress_df["debug"] = ""

    # Save initial CSV
    progress_df.to_csv(file_path, index=False)
    ITER_RANGE = range(n)

print(df)
print(f"Progress tracking initialized with {len(ITER_RANGE)} accounts to process")
# SETUP CSV END


class Window:
    _w = 720
    _h = 480
    prev_server = None
    running = False

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

    async def _click(self, x: int, y: int):
        req = InputRequest(RequestType.CLICK, (x, y), self)

        await input_scheduler.schedule(req)
        await req.event.wait()
        await asyncio.sleep(NORMAL_PAUSE)

    async def _type(self, text: str):
        req = InputRequest(RequestType.TYPE, (text,), self)

        await input_scheduler.schedule(req)
        await req.event.wait()
        await asyncio.sleep(NORMAL_PAUSE)

    async def _press(self, key: str):
        req = InputRequest(RequestType.KEY, (key,), self)

        await input_scheduler.schedule(req)
        await req.event.wait()
        await asyncio.sleep(NORMAL_PAUSE)

    async def _shortcut(self, *args):
        req = InputRequest(RequestType.SHORTCUT, args, self)

        await input_scheduler.schedule(req)
        await req.event.wait()
        await asyncio.sleep(NORMAL_PAUSE)

    async def _enter_priority(self):
        req = InputRequest(RequestType.PRIORITY_START, (None,), self)

        await input_scheduler.schedule(req)
        await req.event.wait()

    async def _exit_priority(self):
        req = InputRequest(RequestType.PRIORITY_END, (None,), self)

        await input_scheduler.schedule(req)
        await req.event.wait()

    async def findClick(
        self,
        img_list: list[np.ndarray] | np.ndarray,
        threshold: float = 0.85,
        invert_threshold: bool = False,
        leniency: float = 0,
        max_tries: int = 999,
    ) -> bool:
        loc, val = await findElement(
            self.size,
            img_list,
            threshold=threshold,
            invert_threshold=invert_threshold,
            leniency=leniency,
            max_tries=max_tries,
        )
        if val == "FOUND":
            click_x, click_y = self.size0 + loc
            await self._click(click_x, click_y)
            return True
        return False

    async def findWait(
        self,
        img_list: list[np.ndarray] | np.ndarray,
        threshold: float = 0.85,
        invert_threshold: bool = False,
        max_tries: int = 999,
    ):
        _, val = await findElement(
            self.size,
            img_list,
            threshold=threshold,
            invert_threshold=invert_threshold,
            max_tries=max_tries,
        )
        return val

    async def run_for_account(self, acc_ind: int):
        await self._enter_priority()

        print("Clicking other_login")
        await self.findClick(Template.OTHER_LOGIN)

        print("Clicking email_signin")

        # Click email signin with priority
        await self.findClick(Template.EMAIL_SIGNIN)

        debug_update(acc_ind, "Logging")
        print(f"Typing email for index {acc_ind}")
        # Type email with priority (ensures it goes to the right textbox)
        await self._type(df.email[acc_ind])

        print("Clicking next_step")
        await self.findClick(Template.NEXT_STEP)
        # while (
        #     await self.findWait(Template.NEXT_STEP, threshold=0.9, max_tries=2)
        #     == "FOUND"
        # ):
        #     print("Clicking next_step again")
        #     await self.findClick(Template.NEXT_STEP, threshold=0.9, max_tries=2)
        #     sleep(1)
        # sleep(2)

        print(f"Typing password for index {acc_ind}")
        await self._type(df.password[acc_ind])

        print("Clicking login")
        await self.findClick(Template.LOGIN)
        await asyncio.sleep(1.0)

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

        await self._exit_priority()

        debug_update(acc_ind, "Entering Game")
        print("Waiting for origin_reso to appear")
        await self.findWait(Template.ORIGIN_RESO, max_tries=5)

        print("Waiting for origin_reso to disappear")
        await self.findWait(Template.ORIGIN_RESO, invert_threshold=True, max_tries=50)
        await asyncio.sleep(7)

        debug_update(acc_ind, "Entered Game")

        # await self._enter_priority()

        print("Clicking uid_text")
        if not await self.findClick(Template.UID_TEXT, max_tries=10):
            await self._click(self.x + int(0.5 * self.w), self.y + int(0.9 * self.h))

        await asyncio.sleep(0.5)

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
            if (
                await self.findWait(Template.ALL_REWARDS_COLLECTED, max_tries=2)
                == "FOUND"
            ):
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

            await self._shortcut("alt", "3")
            # pyautogui.hotkey('alt', '3')
            # main_win.findClick(Template.SWORD_ICON,threshold=0.75)

            sword_icon_tries = 0

            while (
                not await self.findClick(Template.CASUAL_TAB, max_tries=1)
                and sword_icon_tries <= 3
            ):
                print("Clicking casual_tab recursively")
                await self._shortcut("alt", "3")
                sword_icon_tries += 1

            # await self.findClick(Template.CASUAL_TAB)

            print("Clicking artificial_island_icon")
            await self.findClick(Template.ARTIFICIAL_ISLAND_ICON)

            # await self._exit_priority()

            print("Waiting for oldman_icon")
            await self.findWait(Template.OLDMAN_ICON, max_tries=3)

            print("Waiting for oldman_icon (status check)")
            oldman_status_ = await self.findWait(Template.OLDMAN_ICON, max_tries=2)

            # await self._enter_priority()

            print("DEBUG: oldman", oldman_status_)
            oldman_update(acc_ind, oldman_status_)

            print("Clicking back_button")
            await self.findClick(Template.BACK_BUTTON, threshold=0.75)

            print("Clicking back_button again")
            await self.findClick(Template.BACK_BUTTON, threshold=0.75)
            await asyncio.sleep(1)

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
            await self.findWait(Template.INITIATING_TRANSMISSION)

            print("Waiting for initiating_transmission to disappear")
            await self.findWait(
                Template.INITIATING_TRANSMISSION,
                invert_threshold=True,
                max_tries=50,
            )

            print("Waiting for origin_reso to appear")
            await self.findWait(Template.ORIGIN_RESO, max_tries=5)

            print("Waiting for origin_reso to disappear")
            await self.findWait(
                Template.ORIGIN_RESO, invert_threshold=True, max_tries=50
            )

            print("Clicking skip_button")
            await self.findClick(Template.SKIP_BUTTON, max_tries=10)

            print("Waiting for exit_button to appear")
            await self.findWait(Template.EXIT_BUTTON)

            print("Pressing ESC key")
            await input_scheduler.schedule_key(self.id, "esc")

            print("Clicking exit_button")
            await self.findClick(Template.EXIT_BUTTON)

            print("Clicking ok_button")
            await self.findClick(Template.OK_BUTTON)

            print("Sleeping for 7 seconds")
            await asyncio.sleep(7)

            await self.findWait(Template.UID_TEXT)
            await asyncio.sleep(1)

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
            while (
                await self.findWait(Template.MIA_KITCHEN_ICON, max_tries=2) == "FOUND"
            ):
                print("mia_kitchen_done_icon not found, retrying...")
                print("Clicking mia_kitchen_icon")
                await self.findClick(Template.MIA_KITCHEN_ICON)

                print("Clicking taste_button")
                await self.findClick(Template.TASTE_BUTTON)

                print("Clicking back_button")
                await self.findClick(Template.BACK_BUTTON, threshold=0.75)
                sleep(2)

                await self.findWait(Template.CONGRATULATIONS_TEXT)
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
            if (
                await self.findWait(Template.QUICK_BATTLE_BUTTON, max_tries=2)
                == "FOUND"
            ):
                print("Clicking quick_battle_button")
                await self.findClick(Template.QUICK_BATTLE_BUTTON)

            print("Checking for operation_success_text")
            if (
                await self.findWait(Template.OPERATION_SUCCESS_TEXT, max_tries=2)
                == "FOUND"
            ):
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

            if await self.findWait(Template.OK_BUTTON, max_tries=2) == "FOUND":
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
        await self._press("esc")

        print("Clicking settings_button")
        await self.findClick([Template.SETTINGS_BUTTON, Template.SETTINGS_BUTTON_2])

        print("Clicking switch_acc_button")
        await self.findClick(Template.SWITCH_ACC_BUTTON)

        await asyncio.sleep(1)

        print("Clicking switch_acc_text")
        await self.findClick(Template.SWITCH_ACC_TEXT)

        status_update(acc_ind, "checked")
        debug_update(acc_ind, "")

        # await self._exit_priority()

        print("Waiting for origin_reso to appear")
        await self.findWait(Template.ORIGIN_RESO, max_tries=5)

        print("Waiting for origin_reso to disappear")
        await self.findWait(Template.ORIGIN_RESO, invert_threshold=True, max_tries=100)
        await asyncio.sleep(2)

    async def process_queue(self, account_queue: queue.Queue):
        self.running = True
        while not account_queue.empty():
            try:
                # Get next account from queue (non-blocking)
                acc_ind = account_queue.get_nowait()
                print(f"Window {self.id + 1} processing account {acc_ind}")
                await self.run_for_account(acc_ind)
                print(f"Window {self.id + 1} completed account {acc_ind}")
            except queue.Empty:
                # Queue is empty, we're done
                print(f"Window {self.id + 1} finished - no more accounts in queue")
                break
        self.running = False


win_instances = [
    Window(win, i) for i, win in enumerate(pw.getWindowsWithTitle(window_title))
]


async def main():
    print("\nGo to login screen where you will input the email and password")
    input("Press any key to continue after 3 seconds...\n")

    sleep(3)

    try:
        account_queue = queue.Queue()
        # Start the input scheduler
        input_scheduler.set_queue(account_queue)

        await input_scheduler.start()

        # Create a shared queue with all accounts
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
        all_tasks = tasks + [input_scheduler._task]
        await asyncio.gather(*all_tasks)

        print("[MAIN] All tasks completed")

    except KeyboardInterrupt:
        print("Interrupt signal detected!")
        save_progress()
    finally:
        # Stop the input scheduler
        await input_scheduler.stop()

    save_progress()


if __name__ == "__main__":
    asyncio.run(main())
