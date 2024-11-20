import aiohttp
import json

from local_settings import POSTS, TAGS, PORTFOLIO, ADMIN_USER, ADMIN_PASSWORD, CLIENT_DETAIL


async def post_new_post(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=POSTS,
                                auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                data=json.dumps(data),
                                headers={"Content-Type": "application/json"}) as response:
            return await response.json()


async def post_new_tag(data):
    async with aiohttp.ClientSession() as session:
        print(data)
        async with session.post(url=TAGS,
                                data=json.dumps(data),
                                auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                                headers={"Content-Type": "application/json"}) as response:
            return await response.json()


async def put_portfolio(data):
    async with aiohttp.ClientSession() as session:
        print(data)
        async with session.put(url=PORTFOLIO,
                               data=json.dumps(data),
                               auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                               headers={"Content-Type": "application/json"}) as response:
            return await response.json()


async def put_client(pk, data):
    async with aiohttp.ClientSession() as session:
        print(data)
        async with session.put(url=CLIENT_DETAIL + '/' + str(pk),
                               data=json.dumps(data),
                               auth=aiohttp.BasicAuth(ADMIN_USER, ADMIN_PASSWORD),
                               headers={"Content-Type": "application/json"}) as response:
            return await response.json()

# async def get_post(pk):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(POST_DETAIL + '/' + str(pk)) as response:
#             status = response.status
#             if status == 200:
#                 return await response.json()
#             return None
