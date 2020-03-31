"""User Registration Configuration"""

import datetime

REST_REGISTRATION_AVAILABLE = {
    "local": {
        'REGISTER_VERIFICATION_ENABLED':
            False,
        'RESET_PASSWORD_VERIFICATION_ENABLED':
            False,
        'REGISTER_EMAIL_VERIFICATION_ENABLED':
            False,
        'REGISTER_VERIFICATION_URL':
            'https://frontend-host/verify-user/',
        'RESET_PASSWORD_VERIFICATION_URL':
            'https://frontend-host/reset-password/',
        'REGISTER_EMAIL_VERIFICATION_URL':
            'https://frontend-host/verify-email/',
        'VERIFICATION_FROM_EMAIL':
            'no-reply@example.com',
        'REGISTER_VERIFICATION_PERIOD':
            datetime.timedelta(days=7)
    }
}
