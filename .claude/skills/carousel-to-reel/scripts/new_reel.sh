#!/usr/bin/env bash
# Scaffold a new reel project from one of the five approved templates.
#
#   bash new_reel.sh <slug> ["عنوان الريل"] [--style night|day|night-grid|day-grid|dual]
#
#   ١ day-grid    القالب النهاري بالمربعات
#   ٢ night-grid  القالب الليلي بالمربعات
#   ٣ day         القالب النهاري بدون مربعات
#   ٤ night       القالب الليلي بدون مربعات      (default)
#   ٥ dual        القالب المزدوج (ليل ونهار) بدون مربعات
#
# -> motion-graphics/<slug>/
set -euo pipefail
slug="${1:?usage: new_reel.sh <slug> [title] [--style night|day|night-grid|day-grid|dual]}"; shift
title="$slug"; style="night"
while [ $# -gt 0 ]; do
  case "$1" in
    --style) style="${2:?}"; shift 2 ;;
    *) title="$1"; shift ;;
  esac
done
here="$(cd "$(dirname "$0")/.." && pwd)"
repo="$(git -C "$here" rev-parse --show-toplevel 2>/dev/null || pwd)"
dest="$repo/motion-graphics/$slug"
[ -e "$dest" ] && { echo "already exists: $dest" >&2; exit 1; }

case "$style" in
  night)      tpl=template;      theme=dark;  grid=off ;;
  day)        tpl=template;      theme=light; grid=off ;;
  night-grid) tpl=template;      theme=dark;  grid=on ;;
  day-grid)   tpl=template;      theme=light; grid=on ;;
  dual)       tpl=template-dual; theme=;      grid= ;;
  *) echo "unknown style: $style (night|day|night-grid|day-grid|dual)" >&2; exit 1 ;;
esac

mkdir -p "$dest"/{fonts,output,lottie,reels,audio}
cp "$here/$tpl/index.html" "$dest/"
cp "$here/template/gsap.min.js" "$dest/"
cp "$here/template/fonts/"*.ttf "$dest/fonts/"
python3 - "$dest/index.html" "$title" "$theme" "$grid" <<'PY'
import sys, re
p, title, theme, grid = sys.argv[1:5]
s = open(p, encoding="utf-8").read().replace("__TITLE__", title, 1)
if theme:   # bake the chosen look in as this project's default (?theme= / ?grid= still override)
    s, n = re.subn(r"const DEFAULTS = \{ theme: '\w+', grid: '\w+' \};",
                   f"const DEFAULTS = {{ theme: '{theme}', grid: '{grid}' }};", s)
    assert n == 1, "DEFAULTS line not found in template"
open(p, "w", encoding="utf-8").write(s)
PY
printf 'output/bake*.json\noutput/stills/\n' > "$dest/.gitignore"
echo "created $dest  (style: $style)"
