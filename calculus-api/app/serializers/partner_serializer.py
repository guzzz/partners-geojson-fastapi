
def partner_serializer(partner):
    return {
        "id": partner["id"],
        "tradingName": partner["tradingName"],
        "ownerName": partner["ownerName"],
        "document": partner["document"],
        "coverageArea": partner["coverageArea"],
        "address": partner["address"]
    }
