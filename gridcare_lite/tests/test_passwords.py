"""Tests for GridCare-Lite password helpers."""

from __future__ import annotations

from gridcare_lite.app.security.passwords import hash_password, verify_password


def test_hash_and_verify_password() -> None:
    hashed = hash_password("sample-password")
    assert hashed != "sample-password"
    assert verify_password("sample-password", hashed)
    assert not verify_password("wrong-password", hashed)
