"""Module holding the AuctionEntries interface class."""

from .._backends.auction_entries import AuctionEntriesBackend
from ..models.auctions import AuctionEntryExpanded


class AuctionEntries(AuctionEntriesBackend):
    """A class for getting information about auction entries by ID."""

    async def get_by_id(self, auction_id: str) -> AuctionEntryExpanded:
        """Gets a specific auction entry by ID.

        Parameters
        ----------
        auction_id : str
            The ID of the auction entry to get.

        Returns
        -------
        AuctionEntryExpanded

        Example
        -------
        >>> async with PyTenno() as tenno:
        >>>     auction = await tenno.AuctionEntries.get_by_id("...")
        >>>     print(auction.owner.ingame_name, auction.platinum)
        """
        return await self._get_by_id(auction_id)

    async def get_bids_by_id(self, auction_id: str) -> AuctionEntryExpanded:
        """Gets all bids for a specific auction entry by ID.

        Parameters
        ----------
        auction_id : str
            The ID of the auction entry to get bids for.

        Returns
        -------
        AuctionEntryExpanded

        Example
        -------
        >>> async with PyTenno() as tenno:
        >>>     auction = await tenno.AuctionEntries.get_bids_by_id("...")
        >>>     print(auction.owner.ingame_name, auction.platinum)
        """
        return await self._get_bids_by_id(auction_id)
