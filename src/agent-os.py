import logging
import time

import boto3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

region = "insatance-region"  # Hyderabad

instance_ids = [
    "instance-id",  # inst-1
    "instance-id",  # inst-2
]

ssm = boto3.client(
    "ssm",
    region_name=region
)


while True:

    try:

        for instance_id in instance_ids:

            # ---------------------------------------
            # Check middleware status
            # ---------------------------------------

            response = ssm.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={
                    "commands": [
                        "systemctl is-active httpd"
                    ]
                }
            )

            command_id = response["Command"]["CommandId"]

            time.sleep(2)

            result = ssm.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id
            )

            status = result.get(
                "StandardOutputContent",
                ""
            ).strip()

            logging.info(
                "%s httpd status: %s",
                instance_id,
                status
            )


            # ---------------------------------------
            # Middleware stopped
            # ---------------------------------------

            if status != "active":

                logging.warning(
                    "%s: httpd is DOWN. Starting application...",
                    instance_id
                )

                ssm.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={
                        "commands": [
                            "systemctl start httpd"
                        ]
                    }
                )

                logging.warning(
                    "%s: httpd start request sent",
                    instance_id
                )


            # ---------------------------------------
            # Middleware running
            # ---------------------------------------

            else:

                logging.info(
                    "%s: Application is UP",
                    instance_id
                )


    except Exception:

        logging.exception(
            "Application monitoring check failed; retrying"
        )


    # Check application every 10 seconds

    time.sleep(10)