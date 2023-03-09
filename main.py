import os
import uuid

from google.cloud import dataflow_v1beta3


GH_REF = os.getenv("GH_REF", "master")
PROJECT_ID = "mimo-capital-1"


def launch():
    param = dataflow_v1beta3.LaunchFlexTemplateParameter(
        job_name=f"cryptio-{uuid.uuid4()}",
        container_spec_gcs_path=f"gs://mimo-capital-cryptio/dataflow/template-{GH_REF}.json",
        parameters={
            "sdk_container_image": f"us-docker.pkg.dev/{PROJECT_ID}/docker-1/mimo-capital-cryptio/container:{GH_REF}",
        },
    )

    request = dataflow_v1beta3.LaunchFlexTemplateRequest(
        project_id=PROJECT_ID,
        location="us-central1",
        launch_parameter=param,
    )

    with dataflow_v1beta3.FlexTemplatesServiceClient() as client:
        response = client.launch_flex_template(request=request)

    return response.job.name


def main(request):
    return launch()
