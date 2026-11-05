# Calibration de caméra (TICV 2026, Rendu 1)

Script de calibration de la caméra principale d'un iPhone 15 Pro (tutoriels OpenCV calibration + pose).

## Installation
pip install -r requirements.txt

## Lancement (depuis ce dossier)
python calibration_Harena.py

## Résultats attendus
- 14 images utilisées (IMG_3280 exclue), taille 4284 x 5712
- Erreur RMS ≈ 0,85 px
- fx ≈ 4094 px, fy ≈ 4098 px
- focale ≈ 7,05 mm = 0,00705 m (fovx ≈ 55,2°, fovy ≈ 69,7°)
- distances caméra-damier : ≈ 36,1 / 31,8 / 41,3 cm
- fichiers créés dans resultats/ : calibration.npz, corrigee.jpg, pose_0.jpg, pose_7.jpg, pose_13.jpg
