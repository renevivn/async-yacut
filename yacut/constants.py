from string import ascii_lowercase, ascii_uppercase, digits

ALLOWED_CHARACTERS = ascii_lowercase + ascii_uppercase + digits
NUMBER = 6
RESERVED_NAMES = ('files',)
MAX_SHORT_ID_LENGTH = 16
SHORT_ID_PATTERN = rf'^[A-Za-z0-9]{{1,{MAX_SHORT_ID_LENGTH}}}$'  # noqa: E231
