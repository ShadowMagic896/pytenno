# PyTenno
PyTenno is an asynchronous Python wrapper for the warframe.market API

[Read Documentation](https://pytenno.readthedocs.io/en/latest/index.html)

## Installation

### Git
Use your favorite spice of the following:

```bash
py -m pip install git+https://github.com/ShadowMagic896/pytenno.git
```

- [Git](https://git-scm.com/) is required for direct installation

### PyPi

```bash
py -m pip install pytenno
```

## Requirements
The project's only requiremnt is aiohttp, which is available on PyPi.
[aiohttp](https://aiohttp.readthedocs.io/en/stable/index.html) >= 3.8.1

## Examples
```python

import asyncio # To use asynchronous programming
import pytenno
from pytenno.models.enums import Platform # To specify platforms for requests

async def main(): # PyTenno is asynchronous, so it must be done in an asynchronous context
    default_language = "en" # Set default response language to English
    default_platform = Platform.pc # Set default platform to PC

    email = "email" # Your warframe.market email
    password = "password" # Your password for your warframe.market account

    # Create a context manager for PyTenno
    async with pytenno.PyTenno(
        default_language=default_language, 
        default_platform=default_platform
    ) as tenno:
        ########################################
        # Logging to a warframe.market account #
        ########################################

        # This function returns a `CurrentUser` object, which contains misc. information about the user account.
        # This can be accessed through the `Auth` attribute on the client.
        current_user = await tenno.Auth.login(
            email=email, 
            password=password
        )

        ######################################
        # Finding orders for a specific item #
        ######################################

        # This function returns a `OrderRow` object, which contains information about the order.
        orders = await tenno.Items.get_orders(
            # The full name of the item
            item_name="Mirage Prime Neuroptics", 
            # Whether to include data about the items requested, as well as the orders. If this were set to 
            # True, the method would return a tuple of (list[OrderRow], list[ItemFull]).
            # However in this case, it will just return a list[OrderRow].
            include_items=False,
            # The platform the orders must be on. If not set, it will use the default set
            # whent the client was created.
            platform=Platform.pc, 
        )
        for order in orders:
           
            user = order.user # The user who placed the order
            order_type = order.order_type # The type of the order (buy or sell)
            platinum = order.platinum # The amount of platinum in the order

            print(f"User: {user.ingame_name}\nOrder Type: {order_type}\nPlatinum: {platinum}\n")
    
if __name__ == "__main__":
    asyncio.run(main())
```