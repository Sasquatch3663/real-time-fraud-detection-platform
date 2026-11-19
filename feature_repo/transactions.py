from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64

transaction = Entity(name="transaction_id", join_keys=["transaction_id"])
source = FileSource(name="transactions_source", path="../data/processed/transactions.parquet", timestamp_field="event_timestamp")
transaction_features = FeatureView(name="transaction_features", entities=[transaction], ttl=timedelta(days=1), schema=[
    Field(name="amount", dtype=Float32), Field(name="step", dtype=Int64),
], source=source)
