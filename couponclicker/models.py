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
            offerStartDt=offer_detail["offerStartDt"],
            offerEndDt=offer_detail["offerEndDt"],
            purchaseRank=offer_detail["purchaseRank"],
            arrivalRank=offer_detail["arrivalRank"],
            expiryRank=offer_detail["expiryRank"],
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
            offerId=offer_dict["offerId"],
            offerPgm=offer_dict["offerPgm"],
            offerProvider=offer_dict["offerProvider"],
            offerTs=offer_dict["offerTs"],
            clipStatus=offer_dict["clipStatus"],
            listStatus=offer_dict["listStatus"],
            purchaseInd=offer_dict["purchaseInd"],
            offerDetail=OfferDetail.deserialize(offer_dict["offerDetail"]),
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
            offerTypes=[Label(**x) for x in offer_hierarchies["offerTypes"]],
            categories=[Label(**x) for x in offer_hierarchies["categories"]],
            events=[Label(**x) for x in offer_hierarchies["events"]],
        )


@dataclass(frozen=True)
class GetCouponsResponse:
    offers: List[Offer]
    offerHierarchies: Hierarchies

    @classmethod
    def deserialize(cls, get_coupons_response: Dict):
        return cls(
            offers=[Offer.deserialize(o) for o in get_coupons_response["offers"]],
            offerHierarchies=Hierarchies.deserialize(get_coupons_response["offerHierarchies"]),
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
            clipType=item["clipType"],
            itemId=item["itemId"],
            itemType=item["itemType"],
            vndrBannerCd=item["vndrBannerCd"],
            status=item["status"],
            clipId=item["clipId"],
            checked=item["checked"],
        )


@dataclass(frozen=True)
class ClipCouponResponse:
    items: List[ClipCouponItem]

    @classmethod
    def deserialize(cls, response: Dict):
        return cls(
            items=[ClipCouponItem.deserialize(i) for i in response["items"]]
        )
