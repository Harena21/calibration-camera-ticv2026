# Calibration de la caméra principale de mon iPhone 15 Pro
# Basé sur les tutoriels OpenCV "Camera Calibration" et "Pose Estimation"
# Lucka Harena - M2 VMI - TICV 2026 Rendu 1

import glob
import os
import numpy as np
import cv2

# ---------------- Paramètres ----------------
COLS, ROWS = 9, 6          # coins internes du damier
CASE = 19.0                # taille d'une case en mm (mesurée à la règle sur l'écran)
# capteur iPhone 15 Pro principal : 1/1.28", 8064 x 6048 pixels de 1.22 um
# en portrait (images 4284 x 5712) : largeur 6048*1.22 um, hauteur 8064*1.22 um
CAPTEUR_L, CAPTEUR_H = 7.379, 9.838   # mm

# dossier où sont enregistrés les résultats
RESULTATS = "resultats"
os.makedirs(RESULTATS, exist_ok=True)

critere = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# points 3D du damier : (0,0,0), (19,0,0), ... dans le plan Z = 0
objp = np.zeros((COLS * ROWS, 3), np.float32)
objp[:, :2] = np.mgrid[0:COLS, 0:ROWS].T.reshape(-1, 2) * CASE

points3D = []   # points dans le repère du damier
points2D = []   # points détectés dans les images
noms = []

# ---------------- 1. Détection des coins ----------------
for fichier in sorted(glob.glob("photos/*.jpg")):
    img = cv2.imread(fichier)
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # les photos font 24 Mpx : je cherche le damier sur une image réduite (plus rapide)
    echelle = 0.25
    petit = cv2.resize(gris, None, fx=echelle, fy=echelle)
    trouve, coins = cv2.findChessboardCorners(petit, (COLS, ROWS), None)

    if trouve:
        coins = coins / echelle   # retour à la taille réelle
        # affinage sous-pixel sur l'image complète
        coins = cv2.cornerSubPix(gris, coins, (21, 21), (-1, -1), critere)
        points3D.append(objp)
        points2D.append(coins)
        noms.append(fichier)
        print("damier trouvé :", fichier)
    else:
        print("damier NON trouvé :", fichier)

h, w = gris.shape
print("\nimages utilisées :", len(noms), " taille :", w, "x", h)

# ---------------- 2. Calibration ----------------
rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(points3D, points2D, (w, h), None, None)
print("\nErreur RMS :", rms)
print("Matrice K :\n", K)
print("Distorsion (k1, k2, p1, p2, k3) :", dist.ravel())

# erreur de reprojection image par image (pour repérer une mauvaise photo)
for i in range(len(noms)):
    proj, _ = cv2.projectPoints(points3D[i], rvecs[i], tvecs[i], K, dist)
    err = np.sqrt(np.mean(np.sum((points2D[i].reshape(-1, 2) - proj.reshape(-1, 2)) ** 2, axis=1)))
    print(noms[i], "erreur = %.2f px" % err)

np.savez(RESULTATS + "/calibration.npz", K=K, dist=dist)

# ---------------- 3. Focale en mètres ----------------
fovx, fovy, focale_mm, pp, ratio = cv2.calibrationMatrixValues(K, (w, h), CAPTEUR_L, CAPTEUR_H)
print("\nfovx = %.1f deg, fovy = %.1f deg" % (fovx, fovy))
print("focale = %.2f mm = %.5f m" % (focale_mm, focale_mm / 1000))
print("point principal (mm) :", pp, " aspect ratio :", ratio)

# ---------------- 4. Correction de la distorsion ----------------
img = cv2.imread(noms[1])
newK, roi = cv2.getOptimalNewCameraMatrix(K, dist, (w, h), 1, (w, h))
corrigee = cv2.undistort(img, K, dist, None, newK)
cv2.imwrite(RESULTATS + "/corrigee.jpg", corrigee)

# ---------------- 5. Pose : axes et cube ----------------
axes = np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]) * CASE
cube = np.float32([[0, 0, 0], [0, 3, 0], [3, 3, 0], [3, 0, 0],
                   [0, 0, -3], [0, 3, -3], [3, 3, -3], [3, 0, -3]]) * CASE

for i in [0, 7, len(noms) - 1]:
    img = cv2.imread(noms[i])
    ok, rvec, tvec, inliers = cv2.solvePnPRansac(objp, points2D[i], K, dist)
    print(noms[i], "distance caméra-damier = %.1f cm" % (np.linalg.norm(tvec) / 10))

    # cube
    pts, _ = cv2.projectPoints(cube, rvec, tvec, K, dist)
    pts = np.int32(pts).reshape(-1, 2)
    cv2.drawContours(img, [pts[:4]], -1, (0, 255, 0), -3)            # base
    for a, b in zip(range(4), range(4, 8)):
        cv2.line(img, tuple(pts[a]), tuple(pts[b]), (255, 0, 0), 12)  # arêtes
    cv2.drawContours(img, [pts[4:]], -1, (0, 0, 255), 12)             # dessus

    # axes X (bleu), Y (vert), Z (rouge)
    o = tuple(np.int32(points2D[i][0].ravel()))
    pa, _ = cv2.projectPoints(axes, rvec, tvec, K, dist)
    pa = np.int32(pa).reshape(-1, 2)
    for p, couleur in zip(pa, [(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
        cv2.line(img, o, tuple(p), couleur, 15)

    cv2.imwrite(RESULTATS + "/pose_%d.jpg" % i, img)
