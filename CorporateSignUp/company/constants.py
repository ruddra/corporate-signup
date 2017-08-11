"""
Contains constants which can be used anywhere in the APP
Prefer keeping constant.py separate for each app directory if they need
"""


class CompanyType(object):
    """
    Company Type Constants
    """
    PUBLIC = 0
    LIMITED = 1
    LIMITED_PARTNERSHIP = 2
    UNLIMITED_PARTNERSHIP = 3
    CHARTERED = 4
    STATUTORY = 5
    HOLDING = 6
    SUBSIDIARY = 7
    ONEMAN = 8
    NGO = 9

    choices = (
        (PUBLIC, "Public Limited Company"),
        (LIMITED, "Ltd."),
        (LIMITED_PARTNERSHIP, "Limited Partnership"),
        (UNLIMITED_PARTNERSHIP, "Unlimited Partnership"),
        (CHARTERED, "Chartered Company"),
        (STATUTORY, "Statutory Company"),
        (HOLDING, "Holding Company"),
        (SUBSIDIARY, "Subsidiary Company"),
        (ONEMAN, "Sole Proprietor"),
        (NGO, "NGOs"),
    )
