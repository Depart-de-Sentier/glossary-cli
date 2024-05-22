__all__ = (
    "__version__",
    "GlossaryAPI",
    "CommonSchemes",
)

__version__ = "0.4.0"

import sentry_sdk
sentry_sdk.init(
    dsn="https://9e46eb069bb559eed2b074ee8b20d19e@o4507277389004800.ingest.de.sentry.io/4507299672883280",
    traces_sample_rate=1.0,
)

from .main import CommonSchemes, GlossaryAPI
