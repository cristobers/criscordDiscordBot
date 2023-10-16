from aiohttp import ClientSession
from io import BytesIO
from asyncio import run

# URL = 'https://cataas.com/cat/Cls8xWGi0Xm3d2EK'
async def download_cat_image(URL):
    async with ClientSession() as session:
        async with session.get(URL) as a:
            content = await a.read()
            return BytesIO(content)
            
async def main(URL):
    return await download_cat_image(URL)

if __name__ == '__main__':
    run(main(URL))
