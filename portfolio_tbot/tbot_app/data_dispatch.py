import aiohttp
import json

from local_settings import POSTS, TAGS, PORTFOLIO, ADMIN_USER, ADMIN_PASSWORD, CLIENT_DETAIL, POST_DETAIL, \
    SERVICE_DETAIL, SERVICES, TAG_DETAIL
from tbot_app.app import AIOHTTP_SESSION


async def post_new_post(data):
    async with AIOHTTP_SESSION.post(url=POSTS,
                                    auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                    data=json.dumps(data),
                                    headers={"Content-Type": "application/json"}) as response:
        return await response.json()


async def post_new_tag(data):
    async with AIOHTTP_SESSION.post(url=TAGS,
                                    data=json.dumps(data),
                                    auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                    headers={"Content-Type": "application/json"}) as response:
        return await response.json()


async def put_portfolio(data):
    async with AIOHTTP_SESSION.put(url=PORTFOLIO,
                                   data=json.dumps(data),
                                   auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                   headers={"Content-Type": "application/json"}) as response:
        return await response.json()


async def put_client(pk, data):
    async with AIOHTTP_SESSION.put(url=CLIENT_DETAIL + str(pk),
                                   data=json.dumps(data),
                                   auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                   headers={"Content-Type": "application/json"}) as response:
        return await response.json()


async def put_post(pk, data):
    async with AIOHTTP_SESSION.put(url=POST_DETAIL + str(pk),
                                   auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                   data=json.dumps(data),
                                   headers={"Content-Type": "application/json"}) as response:
        return await response.json()


async def delete_post(pk):
    async with AIOHTTP_SESSION.delete(url=POST_DETAIL + str(pk),
                                      auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                      headers={"Content-Type": "application/json"}) as response:
        return await response.json()


async def delete_client(pk):
    async with AIOHTTP_SESSION.delete(url=CLIENT_DETAIL + str(pk),
                                      auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                      headers={"Content-Type": "application/json"}) as response:
        return await response.json()


async def delete_service(pk):
    async with AIOHTTP_SESSION.delete(url=SERVICE_DETAIL + str(pk),
                                      auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                      headers={"Content-Type": "application/json"}) as response:
        return await response.json()


async def delete_tag(pk):
    async with AIOHTTP_SESSION.delete(url=TAG_DETAIL + str(pk),
                                      auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                      headers={"Content-Type": "application/json"}) as response:
        return await response.json()


async def post_service(data):
    async with AIOHTTP_SESSION.post(url=SERVICES,
                                    data=json.dumps(data),
                                    auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                    headers={"Content-Type": "application/json"}) as response:
        return await response.json()
