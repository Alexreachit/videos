# Baut erd03/scene.html: Blender-Bilder (bg/NNNNN.jpg) als Hintergrund + Overlays/Untertitel. Ankerpunkte (Kopf, Erd-Schichten) per shared.py projiziert.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shared as SH
FREDDY = 6
A = {"chef": [], "blake": [], "freddy": [], "vein": [], "pin": [], "center": []}
for f in range(SH.NF):
    t = f / SH.FPS; cam, tg = SH.cam_at(t)
    pc = SH.dig_pose(t, 0., True); pg = SH.dig_pose(t, .55, True); pg = dict(pg, twist=-pg["twist"])
    pts = {"chef": SH.add(SH.head_world(SH.CHEF_ROOT, SH.CHEF_YAW, pc), [0, 0, .32]), "blake": SH.add(SH.head_world(SH.BLAKE_ROOT, SH.BLAKE_YAW, pg), [0, 0, .32]),
           "freddy": [SH.POS[FREDDY][0], SH.POS[FREDDY][1], 1.72 * SH.POS[FREDDY][3]], "vein": [0, 2.42, SH.ZB - .3]}
    pts.update({k: SH.ANCH_EARTH[k] for k in ("pin", "center")})
    for k, X in pts.items():
        p = SH.project(cam, tg, X); A[k].append([round(p[0]), round(p[1])] if p else None)
T = dict(space=SH.T_SPACE, zoomEnd=SH.T_ZOOM_END, back=SH.T_BACK, d0=SH.T_DESC0, d1=SH.T_DESC1, follow=SH.T_FOLLOW, kola=SH.T_KOLA, crust=SH.T_CRUST, vein=SH.T_VEIN, blake=SH.T_BLAKE, fps=SH.FPS, nf=SH.NF)
T['depth'] = [round(SH.depth_at(f / SH.FPS), 1) for f in range(SH.NF)]
head = open(os.path.join(HERE, "head.html")).read(); body = open(os.path.join(HERE, "overlay.js")).read()
open(os.path.join(HERE, "scene.html"), "w").write(head + "const ANCH = " + json.dumps(A, separators=(",", ":")) + ";\nconst TT = " + json.dumps(T) + ";\nconst MAP = " + json.dumps(list(range(SH.NF)), separators=(',', ':')) + ";\n" + body)
print("scene.html", SH.NF, "frames")

json.dump({"ANCH": A, "TT": T}, open(os.path.join(HERE, "anchors_tt.json"), "w"))
