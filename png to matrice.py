from PIL import Image

# Ouvrir une image
image_path = "Capture3.png"
image = Image.open(image_path)

# Obtenir les dimensions de l'image
largeur, hauteur = image.size

# Parcourir tous les pixels de l'image
for y in range(hauteur):
    for x in range(largeur):
        # Obtenir la valeur du pixel à la position (x, y)
        pixel_value = image.getpixel((x, y))

        # Faire quelque chose avec la valeur du pixel (par exemple, l'afficher)
        print(f"Pixel à la position ({x}, {y}): {pixel_value}")

# Fermer l'image
image.close()
