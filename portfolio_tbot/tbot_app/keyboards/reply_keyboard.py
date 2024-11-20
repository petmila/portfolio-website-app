# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# CHECK_CHAR = '✅'
# UNCHECK_CHAR = '⬜'


# def make_checkbox_keyboard(items: list[str]) -> InlineKeyboardMarkup:
#     # rows = []
#     # i = 0
#     # row = []
#     # for item in items:
#     #     i += 1
#     #     row.append(KeyboardButton(text=item))
#     #     if i % 3 == 0:
#     #         row = []
#     #
#     # return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)
#
#
#
#     # lines = msg.split('\n')
#     keyboard = []
#
#     index = 0
#     for item in items:
#         keyboard.append([InlineKeyboardButton(
#             f"{UNCHECK_CHAR} {item}",
#             callback_data=f"toggle__{index}"
#         )])
#         index += 1
#
    # return InlineKeyboardMarkup(keyboard)