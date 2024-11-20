from aiogram.dispatcher.filters.state import State, StatesGroup


class PostCreateStates(StatesGroup):
    add_text = State()
    add_tags = State()


class TagCreateStates(StatesGroup):
    add_info = State()


class PortfolioUpdateStates(StatesGroup):
    update_name = State()
    update_description = State()
    update_about = State()
    update_service_list = State()
