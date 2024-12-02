from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from tbot_app.app import dp
from tbot_app.data_dispatch import put_portfolio, delete_service, post_service
from tbot_app.data_fetch import get_portfolio, get_service
from tbot_app.keyboards.inline_keyboard import make_inline_keyboard
from tbot_app.messages import PORTFOLIO_UPDATE_MESSAGE, PORTFOLIO_MESSAGE
from tbot_app.states import PortfolioUpdateStates


@dp.message_handler(state=PortfolioUpdateStates.update_name)
async def process_update_name_info(message_: types.Message, state: FSMContext):
    await state.finish()
    portfolio = await get_portfolio()
    name_portfolio_info = {'site_name': message_.text,
                           'site_description': portfolio['site_description'],
                           'about': portfolio['about'],
                           'service_list': portfolio['service_list']}
    portfolio = await put_portfolio(name_portfolio_info)
    await message_.reply(text=await format_portfolio(portfolio, portfolio['service_list']),
                         reply_markup=make_inline_keyboard({'update_portfolio': 'Редактировать'})
                         )


@dp.message_handler(state=PortfolioUpdateStates.update_description)
async def process_update_description_info(message_: types.Message, state: FSMContext):
    await state.finish()
    portfolio = await get_portfolio()
    name_portfolio_info = {'site_name': portfolio['site_name'],
                           'site_description': message_.text,
                           'about': portfolio['about'],
                           'service_list': portfolio['service_list']}
    portfolio = await put_portfolio(name_portfolio_info)
    await message_.reply(text=await format_portfolio(portfolio, portfolio['service_list']),
                         reply_markup=make_inline_keyboard({'update_portfolio': 'Редактировать'})
                         )


@dp.message_handler(state=PortfolioUpdateStates.update_about)
async def process_update_about_info(message_: types.Message, state: FSMContext):
    await state.finish()
    portfolio = await get_portfolio()
    name_portfolio_info = {'site_name': portfolio['site_name'],
                           'site_description': portfolio['site_description'],
                           'about': message_.text,
                           'service_list': portfolio['service_list']}
    portfolio = await put_portfolio(name_portfolio_info)
    await message_.reply(text=await format_portfolio(portfolio, portfolio['service_list']),
                         reply_markup=make_inline_keyboard({'update_portfolio': 'Редактировать'})
                         )


@dp.message_handler(state=PortfolioUpdateStates.update_service_list)
async def process_update_service_list_info(message_: types.Message, state: FSMContext):
    await state.finish()
    portfolio = await get_portfolio()
    parsed_list = await parse_service_list(message_.text, portfolio['service_list'])
    print(parsed_list)
    name_portfolio_info = {'site_name': portfolio['site_name'],
                           'site_description': portfolio['site_description'],
                           'about': portfolio['about'],
                           'service_list': parsed_list}
    portfolio = await put_portfolio(name_portfolio_info)
    await message_.reply(text=await format_portfolio(portfolio, portfolio['service_list']),
                         reply_markup=make_inline_keyboard({'update_portfolio': 'Редактировать'})
                         )


async def parse_service_list(text, old_list):
    new_service_list = []
    '''
    Удаляем пункты, которые пользователь убрал из списка
    Затем удаляем из текста все пункты, которые уже были в портфолио
    '''
    for pk in old_list:
        service = await get_service(pk)
        if text.find(service['value']) == -1:
            await delete_service(pk)
        else:
            new_service_list.append(pk)
        text = text.replace(service['value'], '')
    '''
    В тексте остались только новые пункты, выделим их
    '''
    for item in text.split('\n'):
        new_value = item.strip('# ')
        if new_value != '':
            new_service = await post_service({'value': new_value})
            new_service_list.append(new_service['id'])
    return new_service_list


@dp.message_handler(commands=['portfolio'])
async def process_portfolio_command(message_: types.Message):
    portfolio = await get_portfolio()
    print(portfolio)
    p = await format_portfolio(portfolio, portfolio['service_list'])
    print(p)
    await message_.reply(text=p,
                         reply_markup=make_inline_keyboard({'update_portfolio': 'Редактировать'}))


async def format_portfolio(portfolio, service_list):
    services = ''
    for service_id in service_list:
        service = await get_service(service_id)
        services += f'# {service["value"]}\n'
    print(services)
    return PORTFOLIO_MESSAGE.format(site_name=portfolio['site_name'],
                                    site_description=portfolio['site_description'],
                                    about=portfolio['about'],
                                    service_list=services)


@dp.callback_query_handler(F.data == "update_portfolio")
async def process_update_portfolio_command(callback: types.CallbackQuery):
    portfolio_fields = {'site_name': 'Название сайта', 'site_description': 'Описание сайта', 'about': 'Обо мне',
                        'service_list': 'Список услуг'}
    await callback.message.reply(
        text=PORTFOLIO_UPDATE_MESSAGE,
        reply_markup=make_inline_keyboard(portfolio_fields),
    )
    await callback.answer()


@dp.callback_query_handler(F.data == "site_name")
async def update_site_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(PortfolioUpdateStates.update_name)
    await callback.message.reply('Введите новое имя для сайта')
    await callback.answer()


@dp.callback_query_handler(F.data == "site_description")
async def update_site_description(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(PortfolioUpdateStates.update_description)
    await callback.message.reply('Введите новое описание для сайта')
    await callback.answer()


@dp.callback_query_handler(F.data == "about")
async def update_site_description(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(PortfolioUpdateStates.update_about)
    await callback.message.reply('Введите новую информацию про вас для сайта')
    await callback.answer()


@dp.callback_query_handler(F.data == "service_list")
async def update_site_description(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(PortfolioUpdateStates.update_service_list)
    await callback.message.reply('Введите новый список услуг для сайта')
    await callback.answer()
