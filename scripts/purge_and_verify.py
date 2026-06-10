#!/usr/bin/env python3
"""Purge jsDelivr cache for a manifest and verify the CDN copy.

Usage examples:
  python3 scripts/purge_and_verify.py
  python3 scripts/purge_and_verify.py --owner varghese-ruben --repo boto-templates

This performs a GET against the purge endpoint, waits a few seconds,
then fetches the CDN URL and prints the first 3 lines of the manifest.
"""
import argparse
import sys
import time
import urllib.request


def http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def main():
    parser = argparse.ArgumentParser(description="Purge jsDelivr and verify manifest via CDN")
    parser.add_argument("--owner", "-o", default="varghese-ruben")
    parser.add_argument("--repo", "-r", default="boto-templates")
    parser.add_argument("--branch", "-b", default="main")
    parser.add_argument("--manifest", "-m", default="manifest.json")
    parser.add_argument("--wait", type=int, default=3, help="seconds to wait before first verify")
    parser.add_argument("--retries", type=int, default=6, help="number of verify attempts")
    parser.add_argument("--interval", type=int, default=5, help="seconds between retries")
    args = parser.parse_args()

    purge_url = f"https://purge.jsdelivr.net/gh/{args.owner}/{args.repo}@{args.branch}/{args.manifest}"
    cdn_url = f"https://cdn.jsdelivr.net/gh/{args.owner}/{args.repo}@{args.branch}/{args.manifest}"

    print(f"Purging: {purge_url}", file=sys.stderr)
    try:
        resp = http_get(purge_url)
        print(f"Purge response: {resp.strip()}", file=sys.stderr)
    except Exception as e:
        print(f"Purge request failed: {e}", file=sys.stderr)

    print(f"Waiting {args.wait} seconds before verifying...", file=sys.stderr)
    time.sleep(args.wait)

    for attempt in range(1, args.retries + 1):
        try:
            content = http_get(cdn_url)
            lines = content.splitlines()
            # Print only the first 3 lines as in the original curl | head -3
            print("\n".join(lines[:3]))
            return 0
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}", file=sys.stderr)
            if attempt < args.retries:
                time.sleep(args.interval)

    print("Failed to fetch CDN manifest after retries", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
