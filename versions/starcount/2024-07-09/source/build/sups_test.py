import sys, subprocess, re
fs, top = sys.argv[1], sys.argv[2]
s=open('build_html.py').read()
s=re.sub(r"^\.sups\{.*\}$", f".sups{{font-size:{fs}px;position:relative;top:{top}px}}", s, flags=re.M)
open('build_html.py','w').write(s)
