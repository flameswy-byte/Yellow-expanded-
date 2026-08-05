#!/usr/bin/env python3
"""Strip kanto_editor.html down to artifact-publishable content.

The Artifact host supplies <!doctype>/<html>/<head>/<body>, so the page content
must be handed over without them. Generated from the canonical editor so the
two cannot drift apart.
"""
import re, sys
src = open('/home/user/Yellow-expanded-/kanto_editor.html').read()
style = re.search(r'<style>.*?</style>', src, re.S).group(0)
body  = re.search(r'<body>(.*?)</body>', src, re.S).group(1).strip()
# the editor is a dark-canvas pixel-art tool; tell the browser so chrome matches
style = style.replace(':root{', ':root{\n  color-scheme:dark;', 1)
out = f'<title>Kanto Block Editor</title>\n{style}\n{body}\n'
open(sys.argv[1], 'w').write(out)
print(f'{len(out)} bytes -> {sys.argv[1]}')
