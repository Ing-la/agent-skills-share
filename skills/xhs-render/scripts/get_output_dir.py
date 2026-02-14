#!/usr/bin/env python3
"""Return the next output dir for xhs-render: xhs-render/from-{source}-v{N}."""

import argparse
import re
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("post_dir", help="Post directory (e.g. Agent-skills-share/daily-posts/2026-02-13-xxx)")
    parser.add_argument("--source", default="final", choices=["final", "draft", "custom"], help="Source doc: final, draft, or custom")
    args = parser.parse_args()

    post_dir = Path(args.post_dir)
    xhs_render = post_dir / "xhs-render"
    xhs_render.mkdir(parents=True, exist_ok=True)

    pattern = re.compile(r"^from-(?:final|draft|custom)-v(\d+)$")
    versions = []
    for d in xhs_render.iterdir():
        if d.is_dir() and (m := pattern.match(d.name)):
            versions.append(int(m.group(1)))
    next_v = max(versions) + 1 if versions else 1
    out_name = f"from-{args.source}-v{next_v}"
    full_path = xhs_render / out_name
    full_path.mkdir(parents=True, exist_ok=True)
    # Output relative to post_dir for Agent to use
    print(str(post_dir / "xhs-render" / out_name))


if __name__ == "__main__":
    main()
