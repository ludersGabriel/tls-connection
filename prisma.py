import json
import asyncio

from prisma_cleanup import cleanup

cleanup()
# from prisma import Prisma

# async def main() -> None:
#     # Conecta com o banco
#     p = Prisma()
#     await p.connect()

#     # Abre o json com os pokémons
#     with open("treated.txt", "r") as j:
#         data = json.load(j)

#     for i in data:
#         await p.user.create(i)

#     await p.disconnect()

# if __name__ == '__main__':
#     asyncio.run(main())