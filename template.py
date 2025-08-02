from enum import Enum

import cv2


def readImg(img_name):
    return cv2.imread(f"images/{img_name}.png", cv2.IMREAD_COLOR)


class Template(Enum):
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
