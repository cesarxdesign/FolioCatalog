#!/bin/zsh
cd /private/tmp/claude-501/-Users-cgair-Claude/a92997a1-610b-4dee-9a2e-79d3d6d097d6/scratchpad/audiences-sqsp-build
rm -f source/render.png
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size=2048,${1:-4720} --user-data-dir=/private/tmp/claude-501/-Users-cgair-Claude/a92997a1-610b-4dee-9a2e-79d3d6d097d6/scratchpad/aud-chrome --screenshot=source/render.png "file://$PWD/site/index.html" >/dev/null 2>&1 &
for i in {1..60}; do sleep 1; [ -s source/render.png ] && break; done
sleep 1; pkill -f aud-chrome
python3 -c "from PIL import Image; print(Image.open('source/render.png').size)"
