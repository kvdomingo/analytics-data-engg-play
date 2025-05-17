from datetime import timedelta
from json import JSONDecodeError

import dagster as dg

from src.partitions import election_returns_batch_partitions_def
from src.resources.gma_api import GmaApi


@dg.sensor(minimum_interval_seconds=int(timedelta(minutes=5).total_seconds()))
def latest_er_batch_sensor(context: dg.SensorEvaluationContext, gma_data_api: GmaApi):
    with gma_data_api.get_client() as client:
        res = client.get("/batch/latest_batch.json")
        res.raise_for_status()

        try:
            data = res.json()
        except JSONDecodeError:
            context.log.error(f"Invalid JSON:\n{res.text}")
            raise

        latest_batch = data.get("latest_batch")

        if latest_batch is None:
            raise ValueError(f"Invalid {latest_batch=}")

    context.log.info(f"{latest_batch=}")
    new_batches = [str(b) for b in range(1, latest_batch + 1)]
    return dg.SensorResult(
        dynamic_partitions_requests=[
            election_returns_batch_partitions_def.build_add_request(new_batches)
        ],
    )
