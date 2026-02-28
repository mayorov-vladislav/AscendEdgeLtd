from enum import Enum


class LeadSource(str, Enum):
    scanner = "scanner"
    partner = "partner"
    manual = "manual"


class BusinessDomain(str, Enum):
    first = "first"
    second = "second"
    third = "third"


class ColdStage(str, Enum):
    new = "new"
    contacted = "contacted"
    qualified = "qualified"
    transferred = "transferred"
    lost = "lost"


class SalesStage(str, Enum):
    new = "new"
    kyc = "kyc"
    agreement = "agreement"
    paid = "paid"
    lost = "lost"


class AIRecommendation(str, Enum):
    transfer_to_sales = "transfer_to_sales"
    keep_nurturing = "keep_nurturing"
    mark_as_lost = "mark_as_lost"