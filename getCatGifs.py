from aiohttp import ClientSession
from io import BytesIO
from asyncio import run

# URL = 'https://cataas.com/cat/Cls8xWGi0Xm3d2EK'

async def saveCatImageAsBytesObject(URL):
    async with ClientSession() as session:
        async with session.get(URL) as a:
            content = await a.read()
            return BytesIO(content)
            
async def main(URL):
    catFile = await saveCatImageAsBytesObject(URL)
    return catFile

if __name__ == '__main__':
    run(main(URL))
