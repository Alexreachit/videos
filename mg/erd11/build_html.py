# Baut erd03/scene.html: Blender-Bilder (bg/NNNNN.jpg) als Hintergrund + Overlays/Untertitel. Ankerpunkte (Kopf, Erd-Schichten) per shared.py projiziert.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shared as SH
FOSA = 7; KARL = SH.KARL
A = {"chef": [], "blake": [], "lena": [], "fosa": [], "karl": [], "pin": [], "center": [], "drill": [], "rmin": []}
for f in range(SH.NF):
    t = f / SH.FPS; cam, tg = SH.cam_at(t)
    pc = SH.dig_pose(t, 0., True); pg = SH.dig_pose(t, .55, True); pg = dict(pg, twist=-pg["twist"])
    pts = {"chef": SH.add(SH.head_world(SH.CHEF_ROOT, SH.CHEF_YAW, pc), [0, 0, .32]), "blake": SH.add(SH.head_world(SH.BLAKE_ROOT, SH.BLAKE_YAW, pg), [0, 0, .32]),
           "fosa": [SH.POS[FOSA][0], SH.POS[FOSA][1], 1.72 * SH.POS[FOSA][3]], "karl": [SH.POS[KARL][0] * .985, SH.POS[KARL][1] * .985, 1.3 * SH.POS[KARL][3]], "lena": SH.add(SH.head_world(SH.LENA_ROOT, SH.LENA_YAW, SH.dig_pose(t, .3, True)), [0, 0, .32])}
    pts.update({k: SH.ANCH_EARTH[k] for k in ("pin", "center")}); pts["drill"] = [SH.DRILL[0], SH.DRILL[1], 6.4]; pts["rmin"] = SH.add(SH.RMIN_ROOT, [.04, 0, 2.15])
    for k, X in pts.items():
        p = SH.project(cam, tg, X); A[k].append([round(p[0]), round(p[1])] if p else None)
T = dict(space=SH.T_SPACE, zoomEnd=SH.T_ZOOM_END, back=SH.T_BACK, d0=SH.T_DESC0, d1=SH.T_DESC1, follow=SH.T_FOLLOW, up=SH.T_UP, rmin=SH.T_RMIN, turbo=SH.T_TURBO, fps=SH.FPS, nf=SH.NF)
T['depth'] = [round(SH.depth_at(f / SH.FPS), 1) for f in range(SH.NF)]
head = open(os.path.join(HERE, "head.html")).read(); body = open(os.path.join(HERE, "overlay.js")).read()
open(os.path.join(HERE, "scene.html"), "w").write(head + "const ANCH = " + json.dumps(A, separators=(",", ":")) + ";\nconst TT = " + json.dumps(T) + ";\nconst MAP = " + json.dumps(list(range(SH.NF)), separators=(',', ':')) + ";\n" + body)
print("scene.html", SH.NF, "frames")

json.dump({"ANCH": A, "TT": T}, open(os.path.join(HERE, "anchors_tt.json"), "w"))
