"""
Prototype compliance-rule configuration store.

The configuration is based on publicly available Jamaica regulatory
information and is used only with synthetic capstone data.

This module does not verify permits against live government systems
and does not replace the judgement of an authorized reviewer.
"""


HS_REFERENCE = {
    "8711.60": [
        "electric bicycle",
        "electric bike",
    ],
}


BASE_RULES = [
    {
        "rule_id": "DOC-001",
        "category": "document_completeness",
        "description": "Required prototype fields must be present.",
    },
    {
        "rule_id": "VAL-001",
        "category": "value_validation",
        "description": "Declared value must be a positive numeric value.",
    },
    {
        "rule_id": "HS-001",
        "category": "hs_consistency",
        "description": (
            "Product description must be consistent with the "
            "prototype HS reference table."
        ),
    },
]


RESTRICTED_GOODS_RULES = [
    {
        "rule_id": "RES-001",
        "category": "restricted_goods",
        "name": "Meat and meat products",
        "keywords": [
            "meat",
            "beef",
            "pork",
            "chicken",
            "mutton",
            "sausage",
            "ham",
        ],
        "authority": "Ministry of Agriculture and Fisheries",
        "permit_required": True,
    },
    {
        "rule_id": "RES-002",
        "category": "restricted_goods",
        "name": "Agricultural and plant products",
        "keywords": [
            "fresh fruit",
            "fresh fruits",
            "fresh vegetable",
            "fresh vegetables",
            "plant",
            "plants",
            "plant product",
            "ground provision",
            "red peas",
        ],
        "authority": "Ministry of Agriculture and Fisheries",
        "permit_required": True,
    },
    {
        "rule_id": "RES-003",
        "category": "restricted_goods",
        "name": "Human remains",
        "keywords": [
            "human remains",
            "cremated remains",
            "cremated ashes",
            "human ashes",
        ],
        "authority": "Ministry of Health and Wellness",
        "permit_required": True,
    },
    {
        "rule_id": "RES-004",
        "category": "restricted_goods",
        "name": "Pharmaceuticals",
        "keywords": [
            "pharmaceutical",
            "pharmaceuticals",
            "prescription medicine",
            "prescription medication",
        ],
        "authority": "Ministry of Health and Wellness",
        "permit_required": True,
    },
    {
        "rule_id": "RES-005",
        "category": "restricted_goods",
        "name": "Pesticides",
        "keywords": [
            "pesticide",
            "pesticides",
            "insecticide",
            "herbicide",
            "fungicide",
        ],
        "authority": "Pesticides Control Authority",
        "permit_required": True,
    },
    {
        "rule_id": "RES-006",
        "category": "restricted_goods",
        "name": "Firearms and ammunition",
        "keywords": [
            "firearm",
            "firearms",
            "ammunition",
            "gun parts",
        ],
        "authority": "Ministry of National Security",
        "permit_required": True,
    },
    {
        "rule_id": "RES-007",
        "category": "restricted_goods",
        "name": "Toy guns and imitation firearms",
        "keywords": [
            "toy gun",
            "toy guns",
            "imitation firearm",
            "imitation firearms",
        ],
        "authority": "Ministry of National Security",
        "permit_required": True,
    },
    {
        "rule_id": "RES-008",
        "category": "restricted_goods",
        "name": "Camouflage clothing and materials",
        "keywords": [
            "camouflage clothing",
            "camouflage material",
            "camouflage jacket",
            "camouflage uniform",
        ],
        "authority": "Ministry of National Security",
        "permit_required": True,
    },
    {
        "rule_id": "RES-009",
        "category": "restricted_goods",
        "name": "Motor vehicles",
        "keywords": [
            "motor vehicle",
            "motor car",
            "sedan",
            "suv",
            "motorcycle",
            "pickup truck",
            "panel van",
        ],
        "authority": "Trade Board Limited",
        "permit_required": True,
    },
]


PROHIBITED_GOODS_RULES = [
    {
        "rule_id": "PRO-001",
        "category": "prohibited_goods",
        "name": "Honey",
        "keywords": [
            "honey",
        ],
        "authority": "Jamaica Customs Agency",
    },
    {
        "rule_id": "PRO-002",
        "category": "prohibited_goods",
        "name": "Counterfeit coin",
        "keywords": [
            "counterfeit coin",
            "counterfeit coins",
            "coin-base coin",
        ],
        "authority": "Jamaica Customs Agency",
    },
    {
        "rule_id": "PRO-003",
        "category": "prohibited_goods",
        "name": "Indecent or obscene imported material",
        "keywords": [
            "obscene material",
            "indecent material",
            "obscene publication",
            "indecent publication",
        ],
        "authority": "Jamaica Customs Agency",
    },
]


RULE_CATALOG = (
    BASE_RULES
    + RESTRICTED_GOODS_RULES
    + PROHIBITED_GOODS_RULES
)


def get_rule_ids():
    """Return all configured prototype rule identifiers."""
    return [rule["rule_id"] for rule in RULE_CATALOG]


def validate_rule_configuration():
    """
    Validate the Unit 6 prototype rule configuration.

    Returns True when exactly 15 unique rule IDs are configured.
    """
    rule_ids = get_rule_ids()

    return (
        len(rule_ids) == 15
        and len(set(rule_ids)) == 15
    )