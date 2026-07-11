# htools/utils/crypto.py
"""基础加密原语 — AES-256-GCM 加解密、PBKDF2 密钥派生。

提供三团队通用的加密能力：
    - 密钥派生：硬件指纹 → 对称密钥
    - 对称加解密：AES-256-GCM
    - JSON 序列化加解密
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Any

# ── 常量 ──────────────────────────────────────────────────────
PBKDF2_SALT = b"quant-harvester-v1"
PBKDF2_ITERATIONS = 100_000
PBKDF2_KEY_LEN = 32  # AES-256
AES_NONCE_LEN = 12   # GCM 推荐 12 字节


# ════════════════════════════════════════════════════════════════
#  密钥派生
# ════════════════════════════════════════════════════════════════

def derive_key(fingerprint: str) -> bytes:
    """从硬件指纹派生 32 字节 AES-256 对称密钥。

    Args:
        fingerprint: 16 位十六进制硬件指纹。

    Returns:
        32 字节派生密钥。
    """
    return hashlib.pbkdf2_hmac(
        "sha256",
        fingerprint.encode(),
        PBKDF2_SALT,
        PBKDF2_ITERATIONS,
        dklen=PBKDF2_KEY_LEN,
    )


# ════════════════════════════════════════════════════════════════
#  AES-256-GCM 对称加密
# ════════════════════════════════════════════════════════════════

def encrypt(plaintext: bytes, key: bytes) -> bytes:
    """使用 AES-256-GCM 加密任意字节。

    密文格式：nonce (12) || ciphertext || tag (16)

    Args:
        plaintext: 明文字节。
        key: 32 字节密钥。

    Returns:
        密文字节。
    """
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    nonce = os.urandom(AES_NONCE_LEN)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ciphertext


def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """解密 AES-256-GCM 密文。

    Args:
        ciphertext: 密文字节，格式为 nonce (12) || ciphertext || tag (16)。
        key: 32 字节密钥。

    Returns:
        明文字节。

    Raises:
        cryptography.exceptions.InvalidTag: 密钥不匹配或数据损坏。
    """
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    nonce = ciphertext[:AES_NONCE_LEN]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext[AES_NONCE_LEN:], None)


# ════════════════════════════════════════════════════════════════
#  JSON 序列化加解密
# ════════════════════════════════════════════════════════════════

def encrypt_json(data: dict[str, Any], key: bytes) -> bytes:
    """将 dict 序列化为 JSON 后用 AES-GCM 加密。

    Args:
        data: 待加密的字典。
        key: 32 字节密钥。

    Returns:
        密文字节。
    """
    plain = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()
    return encrypt(plain, key)


def decrypt_json(ciphertext: bytes, key: bytes) -> dict[str, Any]:
    """解密 JSON 密文并反序列化为 dict。

    Args:
        ciphertext: 密文字节。
        key: 32 字节密钥。

    Returns:
        解密后的字典。
    """
    plain = decrypt(ciphertext, key)
    return json.loads(plain)
