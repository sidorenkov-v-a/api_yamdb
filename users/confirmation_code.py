from api_yamdb.settings import SECRET_KEY
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 100_000


def _derive_key(secret_key: bytes, salt: bytes,
                iterations: int = ITERATIONS) -> bytes:
    """Derive a secret key from a given secret_key and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return b64e(kdf.derive(secret_key))


def confirmation_code_encrypt(message: bytes, secret_key: str = SECRET_KEY,
                              iterations: int = ITERATIONS) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(secret_key.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )


def confirmation_code_decrypt(token: bytes,
                              secret_key: str = SECRET_KEY) -> bytes:
    decoded = b64d(token)
    salt, iterate, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iterate, 'big')
    key = _derive_key(secret_key.encode(), salt, iterations)
    return Fernet(key).decrypt(token)
