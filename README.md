# Calibration de caméra (TICV 2026, Rendu 1)

Calibration de la caméra principale d'un iPhone 15 Pro avec OpenCV, à partir des tutoriels « Camera Calibration » et « Pose Estimation ».
Lucka Harena, M2 VMI, Université Paris Cité.

Le rapport est dans [rapport/calibrationHarenaVMI2026.pdf](rapport/calibrationHarenaVMI2026.pdf).

## Contenu

- `calibration_Harena.py` : détection du damier, calibration, focale en mètres (`calibrationMatrixValues`), correction de la distorsion, pose (axes et cube)
- `convertir.py` : conversion des photos HEIC de l'iPhone en JPEG (à lancer une seule fois)
- `photos/` : les 15 photos du damier (JPEG, 4284 x 5712)
- `resultats/` : dossier où le script enregistre ses sorties
- `rapport/` : le rapport en PDF

Mire : damier de 9 x 6 coins internes affiché sur un écran, case de 19 mm.

## Installation

```
pip install -r requirements.txt
```

## Lancement (depuis ce dossier)

```
python calibration_Harena.py
```

## Résultats attendus

- 15 images utilisées, taille 4284 x 5712
- Erreur RMS ≈ 1,16 px
- fx ≈ 4108 px, fy ≈ 4113 px
- focale ≈ 7,08 mm = 0,00708 m (fovx ≈ 55,1°, fovy ≈ 69,6°)
- distances caméra-damier : ≈ 36,2 / 31,9 / 41,4 cm
- fichiers créés dans `resultats/` : calibration.npz, corrigee.jpg, pose_0.jpg, pose_7.jpg, pose_14.jpg

IMG_3280, la vue la plus rasante, a une erreur de reprojection de 3,14 px alors que les autres restent sous 1,25 px. Sans elle, l'erreur RMS descend à 0,85 px et la focale passe à 7,05 mm (voir le rapport).

Les dernières décimales peuvent varier un peu selon la version d'OpenCV (testé avec OpenCV 5.0 et Python 3.14).
