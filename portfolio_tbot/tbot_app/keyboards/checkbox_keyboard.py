from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

CHECK_CHAR = '✅'
UNCHECK_CHAR = '⬜'


def make_checkbox_keyboard(items: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for item in items:
        row = []
        if 'check' not in item:
            row.append(
                InlineKeyboardButton(
                    text=item['text'],
                    callback_data=item['callback']))
        elif item['check'] is True:
            row.append(
                InlineKeyboardButton(
                    text=f"{CHECK_CHAR}{item['text']}",
                    callback_data=f"post_tag_checkbox__{item['callback']}"))
        elif item['check'] is False:
            row.append(
                InlineKeyboardButton(
                    text=f"{UNCHECK_CHAR}{item['text']}",
                    callback_data=f"post_tag_checkbox__{item['callback']}"))
        rows.append(row)
    markup = InlineKeyboardMarkup(inline_keyboard=rows, resize_keyboard=True)
    return markup
