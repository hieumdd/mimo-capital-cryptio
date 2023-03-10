import argparse

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from repository import GetCryptioApi
from secret_manager import get_secret
from pipeline import asset, movement

PROJECT_ID = "mimo-capital-1"
TEMP_LOCATION = "gs://mimo-capital-cryptio/dataflow/temp"
REGION = "us-central1"

DATASET = "Cryptio"


def main(args: argparse.Namespace, beam_args: list[str]):
    options = PipelineOptions(
        beam_args,
        runner=args.runner,
        project=args.project,
        temp_location=args.temp_location,
        region=args.region,
        sdk_container_image=args.sdk_container_image,
        num_workers=2,
        number_of_worker_harness_threads=8,
        sdk_location=args.sdk_location,
        experiments=["use_runner_v2", "upload_graph"],
        save_main_session=True,
    )

    with beam.Pipeline(options=options) as p:
        asset_api_keys = [
            get_secret("cryptio-MCAG"),
        ]

        (
            p
            | f"{asset.table}/initialize" >> beam.Create(asset_api_keys)
            | f"{asset.table}/get" >> beam.ParDo(GetCryptioApi(asset.endpoint))
            | f"{asset.table}/flatten" >> beam.FlatMap(asset.transform_fn)
            | f"{asset.table}/load"
            >> beam.io.WriteToBigQuery(
                asset.table,
                DATASET,
                schema={"fields": asset.schema},
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )

        movement_api_keys = [
            get_secret("cryptio-MCAG"),
            get_secret("cryptio-TPL"),
            get_secret("cryptio-DAO"),
        ]

        (
            p
            | f"{movement.table}/initialize" >> beam.Create(movement_api_keys)
            | f"{movement.table}/get" >> beam.ParDo(GetCryptioApi(movement.endpoint))
            | f"{movement.table}/flatten" >> beam.FlatMap(asset.transform_fn)
            | f"{movement.table}/load"
            >> beam.io.WriteToBigQuery(
                movement.table,
                DATASET,
                schema={"fields": movement.schema},
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--sdk_container_image", type=str)
    parser.add_argument("--runner", type=str, default="DataflowRunner")
    parser.add_argument("--sdk_location", type=str, default="container")
    parser.add_argument("--project", type=str, default=PROJECT_ID)
    parser.add_argument("--temp_location", type=str, default=TEMP_LOCATION)
    parser.add_argument("--region", type=str, default=REGION)

    args, beam_args = parser.parse_known_args()

    main(args, beam_args)
