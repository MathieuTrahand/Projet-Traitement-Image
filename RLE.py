import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def convert_image_matrice(chemin):
    image = Image.open(chemin)
    matrice = np.array(image, dtype=np.uint8)
    mat = []
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            pixel = [matrice[i][j][0], matrice[i][j][1], matrice[i][j][2]]
            mat.append(pixel)

    return mat

def codage_RLE(matrice):
    L1 = []
    p = matrice[0]
    nb = 0
    for i in range(len(matrice)):
        p1 = matrice[i]

        if tuple(p) == tuple(p1):
            nb += 1
        else:
            L1.append((nb, p))
            nb = 1
            p = p1

    L1.append((nb, p))
    return L1


def decodage_RLE(compressed_matrix):
    decompressed_matrix = []
    for elem in compressed_matrix:
        for i in range(elem[0]):
            decompressed_matrix.append(elem[1])
    return np.array(decompressed_matrix, dtype=np.int32).reshape((-1, 3))


matrice = convert_image_matrice(r"T:\image_bitmap.bmp")

# Affichage de la matrice (les valeurs des pixels)
print("Matrice de pixels:")
print(matrice)

# Encodage RLE
matrice_compresse = codage_RLE(matrice)
print("\nDonnées encodées RLE:")
print(matrice_compresse)

# Décodage RLE
matrice_decomp = decodage_RLE(matrice_compresse)
print("\nMatrice décompressée:")
print(matrice_decomp)

# On s'assure que les valeurs sont dans la plage correcte (0 à 255)
matrice_decomp = np.clip(matrice_decomp, 0, 255).astype(np.uint8)

# Afficher l'image décompressée avec Matplotlib
plt.imshow(matrice_decomp.reshape((966, 1828, 3)))
plt.title("Image Décompressée")
plt.show()

print("Taille de la matrice encodée:", len(matrice_compresse) * 3, "octets")
print("Taille de la matrice d'origine:", len(matrice) *3, "octets")
print("Taille de la matrice décompressée:", len(matrice_decomp) * 3, "octets")

