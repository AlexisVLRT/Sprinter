from subprocess import check_output
from pathlib import Path

import config


class Functions:
    def __init__(self):
        pass

    def deploy(self, path: Path):
        call = f"""gcloud functions deploy {config.PROCESSOR_SERVICE} \
            --region=europe-west1 \
            --allow-unauthenticated \
            --service-account={config.SERVICE_ACCOUNT} \
            --runtime=python37 \
            --trigger-http \
            --source={str(path)} \
            --entry-point=main \
            --timeout=540s
        """
        check_output([call], shell=True)
