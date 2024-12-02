import aiohttp
from local_settings import POST_DETAIL, TAG_DETAIL, POSTS, TAGS, PORTFOLIO, ADMIN_USER, ADMIN_PASSWORD, CLIENTS, \
    CLIENT_DETAIL, SERVICE_DETAIL
from tbot_app.app import AIOHTTP_SESSION


async def get_posts():
    async with AIOHTTP_SESSION.get(url=POSTS,
                                   auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                   ) as response:
        return await response.json()


async def get_post(pk):
    async with AIOHTTP_SESSION.get(url=POST_DETAIL + str(pk),
                                   auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                   ) as response:
        status = response.status
        if status == 200:
            return await response.json()
        return None


async def get_tags():
    async with AIOHTTP_SESSION.get(url=TAGS,
                                   auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                   ) as response:
        return await response.json()


async def get_tag(pk):
    async with AIOHTTP_SESSION.get(url=TAG_DETAIL + str(pk),
                                   auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                   ) as response:
        status = response.status
        if status == 200:
            return await response.json()
        return None


async def get_portfolio():
    async with AIOHTTP_SESSION.get(url=PORTFOLIO,
                                   auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                   ) as response:
        status = response.status
        if status == 200:
            return await response.json()
        return None


async def get_active_clients():
    async with AIOHTTP_SESSION.get(url=CLIENTS + 'active',
                                   auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                   ) as response:
        return await response.json()


async def get_archived_clients():
    async with AIOHTTP_SESSION.get(url=CLIENTS + 'archived',
                                   auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                   ) as response:
        return await response.json()


async def get_client(pk):
    async with AIOHTTP_SESSION.get(url=CLIENT_DETAIL + str(pk),
                                   auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                   ) as response:
        return await response.json()


async def get_service(pk):
    async with AIOHTTP_SESSION.get(url=SERVICE_DETAIL + str(pk),
                                   auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                   ) as response:
        return await response.json()
