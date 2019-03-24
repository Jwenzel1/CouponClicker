from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class OfferDetail:
    offerStartDt: str
    offerEndDt: str
    purchaseRank: int
    arrivalRank: int
    expiryRank: int

    @classmethod
    def deserialize(cls, offer_detail: Dict):
        return cls(
            offerStartDt=offer_detail.get("offerStartDt", ""),
            offerEndDt=offer_detail.get("offerEndDt", ""),
            purchaseRank=offer_detail.get("purchaseRank", 0),
            arrivalRank=offer_detail.get("arrivalRank", 0),
            expiryRank=offer_detail.get("expiryRank", 0),
        )


@dataclass(frozen=True)
class Offer:
    """This is not all the attributes."""
    offerId: int
    offerPgm: str
    offerProvider: str
    offerTs: int
    clipStatus: str
    listStatus: str
    purchaseInd: str
    offerDetail: OfferDetail
    offerSubPgm: Optional[str] = None

    @classmethod
    def deserialize(cls, offer_dict: Dict):
        return cls(
            offerId=offer_dict.get("offerId", 0),
            offerPgm=offer_dict.get("offerPgm", ""),
            offerProvider=offer_dict.get("offerProvider", ""),
            offerTs=offer_dict.get("offerTs", 0),
            clipStatus=offer_dict.get("clipStatus", ""),
            listStatus=offer_dict.get("listStatus", ""),
            purchaseInd=offer_dict.get("purchaseInd", ""),
            offerDetail=OfferDetail.deserialize(offer_dict.get("offerDetail", {})),
            offerSubPgm=offer_dict.get("offerSubPgm"),
        )


@dataclass(frozen=True)
class Label:
    code: str
    name: str
    count: int


@dataclass(frozen=True)
class Hierarchies:
    offerTypes: List[Label]
    categories: List[Label]
    events: List[Label]

    @classmethod
    def deserialize(cls, offer_hierarchies: Dict):
        return cls(
            offerTypes=[Label(**x) for x in offer_hierarchies.get("offerTypes", [])],
            categories=[Label(**x) for x in offer_hierarchies.get("categories", [])],
            events=[Label(**x) for x in offer_hierarchies.get("events", [])],
        )


@dataclass(frozen=True)
class GetCouponsResponse:
    offers: List[Offer]
    offerHierarchies: Hierarchies

    @classmethod
    def deserialize(cls, get_coupons_response: Dict):
        return cls(
            offers=[Offer.deserialize(o) for o in get_coupons_response.get("offers", [])],
            offerHierarchies=Hierarchies.deserialize(get_coupons_response.get("offerHierarchies", {})),
        )


@dataclass(frozen=True)
class ClipCouponItem:
    clipType: str
    itemId: str
    itemType: str
    vndrBannerCd: str
    status: int
    clipId: str
    checked: bool

    @classmethod
    def deserialize(cls, item: Dict):
        return cls(
            clipType=item.get("clipType", ""),
            itemId=item.get("itemId", ""),
            itemType=item.get("itemType", ""),
            vndrBannerCd=item.get("vndrBannerCd", ""),
            status=item.get("status", 0),
            clipId=item.get("clipId", ""),
            checked=item.get("checked", False),
        )


@dataclass(frozen=True)
class ClipCouponResponse:
    items: List[ClipCouponItem]

    @classmethod
    def deserialize(cls, response: Dict):
        return cls(
            items=[ClipCouponItem.deserialize(i) for i in response.get("items", [])]
        )
