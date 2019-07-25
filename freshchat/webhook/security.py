import re
from base64 import b64decode

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class SecurityManager:
    def __init__(self, public_key: str) -> None:
        self.public_key = public_key

    def key_parse(self) -> str:
        x = re.match(
            "^-----BEGIN RSA PUBLIC KEY-----((.+)|\n(.+)\n)-----END RSA PUBLIC KEY-----\n?$",
            self.public_key,
        )
        if x:
            return x.group(1).strip()
        return None

    @property
    def rsa_key(self) -> RSA:
        data = b64decode(self.key_parse())
        return RSA.importKey(data)

    def verify_signature(self, signature: str, data: str) -> bool:
        rsa_key = self.rsa_key
        digest = SHA256.new(data)
        signer = PKCS1_v1_5.new(rsa_key)
        return signer.verify(digest, b64decode(signature))
