from environment_details import ENVIRONMENT

if ENVIRONMENT == 'prod':
    from .prod import *
elif ENVIRONMENT == 'test':
    from .test import *
else:
    raise ValueError(f"Unknown environment: {ENVIRONMENT}")
