from pipeline.interface import CryptioTable


asset = CryptioTable(
    table="Asset",
    endpoint="asset",
    transform_fn=lambda row: {
        "id": row.get("id"),
        "name": row.get("name"),
        "symbol": row.get("symbol"),
        "addresses": [
            {
                "address": address.get("address"),
                "blockchain": address.get("blockchain"),
            }
            for address in row["addresses"]
        ]
        if row.get("addresses")
        else [],
    },
    schema=[
        {"name": "id", "type": "STRING"},
        {"name": "name", "type": "STRING"},
        {"name": "symbol", "type": "STRING"},
        {
            "name": "addresses",
            "type": "RECORD",
            "mode": "REPEATED",
            "fields": [
                {"name": "address", "type": "STRING"},
                {"name": "blockchain", "type": "STRING"},
            ],
        },
        {"name": "api_key", "type": "STRING"},
    ],
)
