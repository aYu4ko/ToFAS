import cv2


def readImg(img_name):
    return cv2.imread(f"images/{img_name}.png", cv2.IMREAD_COLOR)


class Template:
    __slots__ = ()

    OTHER_LOGIN = readImg("other_login")
    EMAIL_SIGNIN = readImg("email_signin")
    NEXT_STEP = readImg("next_step")
    LOGIN = readImg("login")
    SERVER_GREEN_BUTTON = readImg("server_green_button")
    SERVER_AESTRAL_NOA = readImg("server_aestral_noa")
    SERVER_ANIMUS = readImg("server_animus")
    ENTER = readImg("enter")
    ORIGIN_RESO = readImg("origin_reso")
    UID_TEXT = readImg("uid_text")
    SWORD_ICON = readImg("sword_icon")
    CASUAL_TAB = readImg("casual_tab")
    ARTIFICIAL_ISLAND_ICON = readImg("artificial_island_icon")
    OLDMAN_ICON = readImg("oldman_icon")
    BACK_BUTTON = readImg("back_button")
    ESC_BUTTON = readImg("esc_button")
    SETTINGS_BUTTON = readImg("settings_button")
    SETTINGS_BUTTON_2 = readImg("settings_button_2")
    SWITCH_ACC_BUTTON = readImg("switch_acc_button")
    SWITCH_ACC_TEXT = readImg("switch_acc_text")

    RECOMMENDED_BUTTON = readImg("recommended_button")

    DIMENSINAL_TRIALS_BUTTON = readImg("dimensinal_trials_button")
    GOLD_DRILL_BUTTON = readImg("gold_drill_button")
    GO_BUTTON = readImg("go_button")
    QUICK_BATTLE_BUTTON = readImg("quick_battle_button")
    OPERATION_SUCCESS_TEXT = readImg("operation_success_text")
    ANYWHERE_TEXT = readImg("anywhere_text")
    CROSS_BUTTON = readImg("cross_button")

    MIA_KITCHEN_ICON = readImg("mia_kitchen_icon")
    TASTE_BUTTON = readImg("taste_button")
    MIA_KITCHEN_DONE_ICON = readImg("mia_kitchen_done_icon")
    CONGRATULATIONS_TEXT = readImg("congratulations_text")

    MIA_KITCHEN_MISSION_TEXT = readImg("mia_kitchen_mission_text")
    BYGONE_MISSION_TEXT = readImg("bygone_mission_text")
    VITALITY_MISSION_TEXT = readImg("vitality_mission_text")

    CREW_ICON = readImg("crew_icon")
    CREW_ICON_2 = readImg("crew_icon_2")
    DAILY_BUTTON = readImg("daily_button")
    DONATE_BUTTON = readImg("donate_button")
    OK_BUTTON = readImg("ok_button")
    ACCEPT_BUTTON = readImg("accept_button")
    ABANDON_BUTTON = readImg("abandon_button")
    SUBMIT_BUTTON = readImg("submit_button")

    CHALLENGE_BUTTON = readImg("challenge_button")
    BYGONE_ICON = readImg("bygone_icon")
    SAME_LEVEL_BUTTON = readImg("same_level_button")
    SNEAK_LEVEL_BUTTON = readImg("sneak_level_button")
    INITIATING_TRANSMISSION = readImg("initiating_transmission")
    SKIP_BUTTON = readImg("skip_button")
    EXIT_BUTTON = readImg("exit_button")

    PASS_CANCEL = readImg("pass_cancel")

    SPECIAL_OPERATION = readImg("special_operation")
    SUPPLY_RUN = readImg("supply_run")
    SUPPLY_RUN_2 = readImg("supply_run_2")
    SUMMER_WELFARE = readImg("summer_welfare")
    SUPPLY_CLAIM = readImg("supply_claim")
    FINAL_SUPPLY_CLAIM = readImg("final_supply_claim")
    ALL_REWARDS_COLLECTED = readImg("all_rewards_collected")

    MAIL_ICON = readImg("mail_icon")
    MAIL_ICON2 = readImg("mail_icon2")
    CLAIM_ALL_BUTTON = readImg("claim_all_button")
    DELETE_ALL_BUTTON = readImg("delete_all_button")

    REWARDS_BUTTON = readImg("rewards_button")
    EXCHANGE_BUTTON = readImg("exchange_button")
    GIFT_CODE_BLOCK = readImg("gift_code_block")
    CONFIRM_BUTTON = readImg("confirm_button")
    CHAT_CLOSE_BUTTON = readImg("chat_close_button")
