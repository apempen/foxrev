import random

from linebot.models import (
    TextSendMessage,
)

# じゃんけん処理に使用
DRAW = 0
USER1_WIN = 1
USER2_WIN = 2

# 1 -> グー , 2 -> チョキ, 3 -> パー
def game_janken(user1, user2):
    # IDで受け取る。
    if user1 not in [1, 2, 3] or user2 not in [1, 2, 3]:
        raise Exception("game_janken() failure: invalid params")

    if user1 == user2:
        return DRAW
    elif (
        (user1 == 1 and user2 == 2)
        or (user1 == 2 and user2 == 3)
        or (user1 == 3 and user2 == 1)
    ):
        return USER1_WIN
    else:
        return USER2_WIN


def hand_id2str(hand_id):
    if hand_id == 1:
        return "ぐー"
    elif hand_id == 2:
        return "ちょき"
    elif hand_id == 3:
        return "ぱー"

    raise Exception("handid2str() failure: 不正な入力値です")


def hand_str2id(hand_str):
    if hand_str == "ぐー":
        return 1
    elif hand_str == "ちょき":
        return 2
    elif hand_str == "ぱー":
        return 3

    raise Exception("hand_str2id() failure: 不正な入力値です")

def handle_janken(event):
    msg = event.message.text
    if msg not in ["ぐー", "ちょき", "ぱー"]:
        return TextSendMessage(text="「ぐー」, 「ちょき」, 「ぱー」のいずれかで答えてね！")

    # 勝敗を決める処理
    user_hand = hand_str2id(msg)
    bot_hand = random.randint(1, 3)  # [1, 3]
    ret_msg = f"{hand_id2str(bot_hand)} !!\n"
    res = game_janken(bot_hand, user_hand)

    if res == DRAW:
        ret_msg += "あーいこーで ..."
    elif res == USER1_WIN:
        ret_msg += "僕の勝ち！！"
    elif res == USER2_WIN:
        ret_msg += "君の勝ち！！"

    return TextSendMessage(text=ret_msg)
