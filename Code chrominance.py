import numpy as np
from PIL import Image
import os

def chroma_subsample(image, width=None, height=None, ratio=(4, 2, 2)):
    # Vérifiez les arguments d'entrée
    if width is None:
        width = image.width
    if height is None:
        height = image.height

    # Convertissez l'image en mode YCbCr
    image = image.convert('YCbCr')

    # Extrayez les canaux Y, Cb et Cr
    y, cb, cr = image.split()

    # Calculez les nouvelles dimensions pour les canaux Cb et Cr
    new_width = width // ratio[1]
    new_height = height // ratio[0]

    # Redimensionnez les canaux Y, Cb et Cr
    y = y.resize((new_width, new_height))
    cb = cb.resize((new_width, new_height))
    cr = cr.resize((new_width, new_height))

    # Réassemblez les canaux Y, Cb et Cr en une seule image
    image_subsampled = Image.merge('YCbCr', (y, cb, cr))

    # Convertissez l'image en mode RGB
    image_subsampled = image_subsampled.convert('RGB')

    # Enregistrer l'image compressée
    filename = 'image_sous_échantillonnée.png'
    image_subsampled.save(filename)

    #Calcul des tailles des deux images
    size_original = os.path.getsize(r"T:\Fond ecran\2233780901_preview_2.jpg")
    size_compressed = os.path.getsize(filename)
    print(f'Taille de limage originale: {size_original} bytes')
    print(f'Taille de limage sous-échantillonnée compressée: {size_compressed} bytes')
    return image_subsampled

# Chargez l'image
image = Image.open(r"T:\Fond ecran\2233780901_preview_2.jpg")

# Appelez la fonction de sous-échantillonnage de chrominance
image_subsampled = chroma_subsample(image)

# Affichez l'image sous-échantillonnée
image_subsampled.show('Image sous-échantillonnée')