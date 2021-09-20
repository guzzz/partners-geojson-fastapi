
def partner_serializer(partner):
    return {
        "id": partner["id"],
        "tradingName": partner["tradingName"],
        "ownerName": partner["ownerName"],
        "document": partner["document"],
        "coverageArea": partner["coverageArea"],
        "address": partner["address"]
    }


def partners_serializer(partners_list):
    return [partner_serializer(partner) for partner in partners_list]
