from typing import Union, Callable, Optional
from typing_extensions import Protocol

from Crypto.PublicKey.RSA import RsaKey


class Hash(Protocol):
    def digest(self) -> bytes: ...
    def update(self, bytes) -> None: ...


class HashModule(Protocol):
    @staticmethod
    def new(data: Optional[bytes]) -> Hash: ...


MaskFunction = Callable[[bytes, int, Union[Hash, HashModule]], bytes]
RndFunction = Callable[[int], bytes]

class PSS_SigScheme:
    def __init__(self, key: RsaKey, mgfunc: MaskFunction, saltLen: int, randfunc: RndFunction) -> None: ...
    def can_sign(self) -> bool: ...
    def sign(self, msg_hash: Hash) -> bytes: ...
    def verify(self, msg_hash: Hash, signature: bytes) -> None: ...


MGF1 : MaskFunction
def _EMSA_PSS_ENCODE(mhash: Hash, emBits: int, randFunc: RndFunction, mgf:MaskFunction, sLen: int) -> str: ...
def _EMSA_PSS_VERIFY(mhash: Hash, em: str, emBits: int, mgf: MaskFunction, sLen: int) -> None: ...
def new(rsa_key: RsaKey, **kwargs: Union[MaskFunction, RndFunction, int]) -> PSS_SigScheme: ...
