from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import pytest

from samsungtv import SamsungTVClient, SamsungTVResponseError

HOST = os.getenv("SAMSUNG_TV_HOST")
TOKEN_ENV = os.getenv("SAMSUNG_TV_TOKEN") or ""
PORT = int(os.getenv("SAMSUNG_TV_PORT", "1516"))
TOKEN_CACHE = Path(
    os.getenv("SAMSUNG_TV_TOKEN_CACHE", ".pytest_cache/samsung_tv_token")
)


def _load_cached_token() -> Optional[str]:
    if TOKEN_CACHE.exists():
        try:
            value = TOKEN_CACHE.read_text().strip()
        except OSError:
            return None
        return value or None
    return None


def _store_token(token: str) -> None:
    try:
        TOKEN_CACHE.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_CACHE.write_text(token)
    except OSError:
        pass


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_tv_states_live() -> None:
    if not HOST:
        pytest.skip("Set SAMSUNG_TV_HOST to run live tests")

    token: Optional[str] = TOKEN_ENV.strip() or _load_cached_token()

    async with SamsungTVClient(HOST, access_token=token, port=PORT) as tv:
        if token is None:
            token = await tv.create_access_token()
            _store_token(token)
        states = await tv.get_tv_states()
        video_states = await tv.get_video_states()
        try:
            usb_devices = await tv.usb_source_control()
        except SamsungTVResponseError as err:
            if "Method not found" in str(err):
                usb_devices = []
            else:
                raise
        try:
            rvu_devices = await tv.rvu_source_control()
        except SamsungTVResponseError as err:
            if "Method not found" in str(err):
                rvu_devices = []
            else:
                raise
        try:
            speakers = await tv.external_speaker_control()
        except SamsungTVResponseError as err:
            if "Method not found" in str(err):
                speakers = []
            else:
                raise

        assert len(states) != 0

        print("TV states:", states)
        print("Video states:", video_states)
        print("USB devices:", usb_devices)
        print("RVU devices:", rvu_devices)
        print("External speakers:", speakers)
