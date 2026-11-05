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

- 14 images utilisées (IMG_3280 exclue), taille 4284 x 5712
- Erreur RMS ≈ 0,85 px
- fx ≈ 4094 px, fy ≈ 4098 px
- focale ≈ 7,05 mm = 0,00705 m (fovx ≈ 55,2°, fovy ≈ 69,7°)
- distances caméra-damier : ≈ 36,1 / 31,8 / 41,3 cm
- fichiers créés dans `resultats/` : calibration.npz, corrigee.jpg, pose_0.jpg, pose_7.jpg, pose_13.jpg

Les dernières décimales peuvent varier un peu selon la version d'OpenCV (testé avec OpenCV 5.0 et Python 3.14).
