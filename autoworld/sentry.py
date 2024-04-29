import os

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


def sentry_init() -> None:
    sentry_sdk.consts.DEFAULT_MAX_VALUE_LENGTH = 10_000_000

    sentry_sdk.init(
        send_default_pii=True,
        dsn=os.environ.get("GLITCH_TIP_DSN"),
        integrations=[
            CeleryIntegration(),
            LoggingIntegration(),  # default = error
        ],
        sample_rate=0,
        traces_sample_rate=0,
        auto_session_tracking=False,
        max_request_body_size="always",
    )


if os.environ.get("GLITCH_TIP_DSN"):
    sentry_init()
    
