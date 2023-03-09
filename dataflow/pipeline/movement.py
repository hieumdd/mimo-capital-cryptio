from pipeline.interface import CryptioTable


movement = CryptioTable(
    table="Movement",
    endpoint="movement",
    transform_fn=lambda rows: [
        {
            "id": row.get("id"),
            "transaction_id": row.get("transaction_id"),
            "transaction_hash": row.get("transaction_hash"),
            "transaction_date": row.get("transaction_date"),
            "source_id": row.get("source_id"),
            "other_party": {
                "address": row["other_party"].get("address"),
                "blockchain": row["other_party"].get("blockchain"),
            }
            if row.get("other_party")
            else {},
            "volume": row.get("volume"),
            "direction": row.get("direction"),
            "asset": row.get("asset"),
        }
        for row in rows
    ],
    schema=[
        {"name": "id", "type": "STRING"},
        {"name": "transaction_id", "type": "STRING"},
        {"name": "transaction_hash", "type": "STRING"},
        {"name": "transaction_date", "type": "INTEGER"},
        {"name": "source_id", "type": "STRING"},
        {
            "name": "other_party",
            "type": "record",
            "fields": [
                {"name": "address", "type": "STRING"},
                {"name": "blockchain", "type": "STRING"},
            ],
        },
        {"name": "volume", "type": "STRING"},
        {"name": "direction", "type": "STRING"},
        {"name": "asset", "type": "STRING"},
    ],
)
