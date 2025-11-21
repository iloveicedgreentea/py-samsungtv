#!/usr/bin/env python3
"""Send remote key sequences to a Samsung TV using pysamsungtv."""

from __future__ import annotations

import argparse
import asyncio
from pysamsungtv import RemoteKey, SamsungTVClient, SamsungTVError
from pysamsungtv.const import DEFAULT_PORT

# MENU -> right x5 -> ENTER replicates the "menu/settings, right 5x, ok" request.
KEY_SEQUENCE: list[RemoteKey] = [
    RemoteKey.MENU,
    # RemoteKey.CURSOR_DN,
    # RemoteKey.CURSOR_DN,
    # RemoteKey.ENTER,
    # RemoteKey.CURSOR_DN,
    # RemoteKey.CURSOR_DN,
    # RemoteKey.CURSOR_DN,
    # RemoteKey.CURSOR_DN,
    # RemoteKey.ENTER,
    # RemoteKey.ENTER,
]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Send Samsung remote keys using pysamsungtv."
    )
    parser.add_argument("--host", required=True, help="TV hostname or IP address")
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"TV HTTPS JSON-RPC port (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--token",
        help=(
            "Access token created through the Samsung pairing prompt. "
            "If omitted the script will request a token and print it."
        ),
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="Seconds to wait between key presses (default: 0.4)",
    )
    parser.add_argument(
        "--verify-ssl",
        action="store_true",
        help="Enable TLS certificate verification (off by default for self-signed certs).",
    )
    return parser


async def send_remote_sequence(args: argparse.Namespace) -> None:
    async with SamsungTVClient(
        args.host,
        port=args.port,
        verify_ssl=args.verify_ssl,
        access_token=args.token,
    ) as client:
        if client.access_token is None:
            print(
                "No access token provided, requesting one (accept the prompt on TV)..."
            )
            token = await client.create_access_token()
            print(f"Access token granted: {token}")

        total = len(KEY_SEQUENCE)
        for idx, key in enumerate(KEY_SEQUENCE, 1):
            print(f"[{idx}/{total}] Sending {key.name}")
            await client.remote_key_control(key)
            if args.delay and idx < total:
                await asyncio.sleep(args.delay)


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        asyncio.run(send_remote_sequence(args))
    except SamsungTVError as exc:
        raise SystemExit(f"Samsung TV request failed: {exc}") from exc
    except KeyboardInterrupt:
        raise SystemExit("Cancelled by user")


if __name__ == "__main__":
    main()
