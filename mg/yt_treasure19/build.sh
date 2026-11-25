cd "$(dirname "$0")" && { cat p0_shell.html p1_base.js p2_intro.js p3_train.js $(ls p4_*.js p5_*.js p6_*.js p7_*.js p8_*.js 2>/dev/null) p9_draw.js; echo '</script></body></html>'; } > scene.html
