# Conversion des photos HEIC de l'iPhone en JPEG (à lancer une seule fois)
import glob
from PIL import Image
import pillow_heif
pillow_heif.register_heif_opener()

for f in glob.glob("photos/*.HEIC"):
    img = Image.open(f)
    img.save(f.replace(".HEIC", ".jpg"), quality=95, exif=img.getexif().tobytes())
    print("converti :", f)
