class DigitalContent:
    def __init__(self):
        self.content = []
        self.digital_content_id = None
        self.versioned_content_id = None


# def auditing_logs():
#     pass


from google.cloud import logging

# Generic Logging function
from datetime import datetime
def auditing_logs(versioned_content_id, tool_name, tool_args,api_name,user_id,
                     severity="INFO", error="NA" ):

    log_client = logging.Client()
    logger = log_client.logger('DSH_ASSISTANT')
    log_text = "AUDIT LOG"
    tool_args.pop('API_KEY')
    logger.log_text(log_text, severity=severity,
                    labels={
                        "api_versioned_contentid": versioned_content_id,
                        "user_id": str(user_id),
                        "tool_name": str(tool_name),
                        "tool_args": str(tool_args),
                        "api_name":str(api_name),
                        "time_stamp": str(datetime.now())
                    }
                    )
