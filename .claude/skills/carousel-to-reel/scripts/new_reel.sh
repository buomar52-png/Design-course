#!/usr/bin/env bash
# Scaffold a new reel project from the template.
#   bash new_reel.sh <slug> ["عنوان الريل"]      -> motion-graphics/<slug>/
set -euo pipefail
slug="${1:?usage: new_reel.sh <slug> [title]}"
title="${2:-$slug}"
here="$(cd "$(dirname "$0")/.." && pwd)"
repo="$(git -C "$here" rev-parse --show-toplevel 2>/dev/null || pwd)"
dest="$repo/motion-graphics/$slug"
[ -e "$dest" ] && { echo "already exists: $dest" >&2; exit 1; }
mkdir -p "$dest"/{fonts,output,lottie,reels}
cp "$here/template/index.html" "$here/template/gsap.min.js" "$dest/"
cp "$here/template/fonts/"*.ttf "$dest/fonts/"
python3 - "$dest/index.html" "$title" <<'PY'
import sys; p, t = sys.argv[1], sys.argv[2]
s = open(p, encoding="utf-8").read().replace("__TITLE__", t, 1); open(p, "w", encoding="utf-8").write(s)
PY
printf 'output/bake*.json\noutput/stills/\n' > "$dest/.gitignore"
echo "created $dest"
