import pytest
from gdpy.crypto import xor_cipher, xor_cipher_int, generate_gjp2, encode_base64, decode_base64
from gdpy.constants import Secrets, Salts, URLs


class TestCrypto:
    def test_xor_cipher(self):
        data = "hello"
        key = "abc"
        result = xor_cipher(data, key)
        assert result != data
        decrypted = xor_cipher(result, key)
        assert decrypted == data

    def test_xor_cipher_int(self):
        data = "hello"
        key = 11
        result = xor_cipher_int(data, key)
        assert result != data
        decrypted = xor_cipher_int(result, key)
        assert decrypted == data

    def test_generate_gjp2(self):
        password = "testpassword"
        gjp = generate_gjp2(password)
        assert len(gjp) == 40
        assert gjp.isalnum()

    def test_base64_encode_decode(self):
        data = "test data"
        encoded = encode_base64(data)
        decoded = decode_base64(encoded)
        assert decoded == data


class TestConstants:
    def test_secrets(self):
        assert Secrets.COMMON == "Wmfd2893gb7"
        assert Secrets.ACCOUNT == "Wmfv3899gc9"
        assert Secrets.LEVEL == "Wmfv2898gc9"
        assert Secrets.MODERATOR == "Wmfp3879gc3"

    def test_salts(self):
        assert Salts.GJP2 == "mI29fmAnxgTs"

    def test_urls(self):
        assert URLs.DEFAULT == URLs.BOOMLINGS
        assert URLs.BOOMLINGS.startswith("https://")
