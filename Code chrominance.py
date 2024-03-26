import numpy as np
from PIL import Image
import os

def sous_echant(image, largeur=None, hauteur=None, ratio=(4, 2, 2)):
    # Vérifiez les arguments d'entrée
    if largeur is None:
        largeur = image.width
    if hauteur is None:
        hauteur = image.height

    # Convertissez l'image en mode YCbCr
    image = image.convert('YCbCr')

    # Extrayez les canaux Y, Cb et Cr
    y, cb, cr = image.split()

    # Calculez les nouvelles dimensions pour les canaux Cb et Cr
    new_largeur = largeur // ratio[1]
    new_hauteur = hauteur // ratio[0]

    # Redimensionnez les canaux Y, Cb et Cr
    y = y.resize((new_largeur, new_hauteur))
    cb = cb.resize((new_largeur, new_hauteur))
    cr = cr.resize((new_largeur, new_hauteur))

    # Réassemblez les canaux Y, Cb et Cr en une seule image
    image_echantillonnee = Image.merge('YCbCr', (y, cb, cr))

    # Convertissez l'image en mode RGB
    image_echantillonnee = image_echantillonnee.convert('RGB')

    # Enregistrer l'image compressée
    filename = 'image_sous_échantillonnée.png'
    image_echantillonnee.save(filename)

    #Calcul des tailles des deux images
    taille_origine = os.path.getsize(r"T:\Fond ecran\2233780901_preview_2.jpg")
    taille_compressee = os.path.getsize(filename)
    print(f'Taille de limage originale: {taille_origine} bytes')
    print(f'Taille de limage sous-échantillonnée compressée: {taille_compressee} bytes')
    return image_echantillonnee

###TEST ET ANALYSES

# Chargez l'image
image = Image.open(r"T:\Fond ecran\2233780901_preview_2.jpg")

# Appel de la fonction de sous-échantillonnage de chrominance
image_echantillonnee = sous_echant(image)

# Affichage l'image sous-échantillonnée
image_echantillonnee.show('Image sous-échantillonnée')