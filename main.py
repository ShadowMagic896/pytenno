import asyncio
from src.client import PyTenno


async def main():
    async with PyTenno() as pytenno:
        items = await pytenno.get_droptable(
            "mirage_prime_systems", include_items=True
        )
        print(items)


asyncio.run(main())
