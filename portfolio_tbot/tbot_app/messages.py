WELCOME_MESSAGE = '''
Привет! Я помогу тебе работать с контентом твоего сайта)
Ты можешь использовать команды: \n
/portfolio -  \n
/view_posts -  \n
/create_post -  \n
/active_clients - для получения списка твоих клиентов \n
/archive_clients - для получения списка твоих клиентов \n
/tags - для получения списка твоих клиентов \n
'''

PORTFOLIO_MESSAGE = '''
Ниже представлена информация из вашего портфолио.\n
Название сайта: {site_name}\n
Описание сайта: {site_description}\n
Обо мне: {about}\n
Список услуг: \n
{service_list}
'''
PORTFOLIO_UPDATE_MESSAGE = '''
Выберите поле, которое хотите изменить
'''
POST_VIEW_MESSAGE = '''
<u>{key_phrase}</u>\n
{tags}
<i>{datetime}</i> \n\n
{text} \n
'''
POST_CREATION_MESSAGE = '''
i don't know nothing
'''
POST_CREATION_KEY_PHRASE_MESSAGE = '''
key phrase
'''
POST_CREATION_TAGS_MESSAGE = '''
give me tags
'''

POST_CREATED_MESSAGE = '''
Спасибо! Переданные вами значения сохранены.
'''
POST_UPDATE_MESSAGE = '''
Круто! Чтобы изменить текст поста на сайте, введите новый текст
'''
POST_DELETE_MESSAGE = '''
Пост был успешно удален.
'''
TAGS_LIST_MESSAGE = '''
Спасибо)\n
Список добавленных Вами тэгов:
'''
TAG_VIEW_MESSAGE = '''
{name}: {description}\n
'''
TAGS_LIST_UPDATE_MESSAGE = '''
Введите измененный список тэгов
'''
CLIENT_ARCHIVED_MESSAGE = '''
Тэг был успешно удален
'''
CLIENT_SKIPPED_MESSAGE = '''
Клиент был оставлен в активных
'''
CLIENT_VIEW_MESSAGE = '''
<u>Имя:</u> {name}\n
<u>Компания:</u> {company}\n
<u>Telegram:</u> {telegram}\n
<u>Email:</u> {email}\n
<i>Дополнительная информация:</i>\n
{additional_info}\n
'''
CLIENT_DELETE_MESSAGE = '''
Клиент был успешно удален из архива
'''
