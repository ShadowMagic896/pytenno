from ..models.auctions import AuctionEntryExpanded
from ..utils import from_data
from .core import BackendAdapter


class AuctionEntriesBackend(BackendAdapter):
    async def _get_by_id(
        self,
        auction_id: str,
    ):
        data = await self._backend._request(f"/auctions/entry/{auction_id}")
        return from_data(AuctionEntryExpanded, data)

    async def _get_bids_by_id(self, auction_id: str):
        data = await self._backend._request(f"/auctions/entry/{auction_id}/bids")
        return from_data(AuctionEntryExpanded, data)
