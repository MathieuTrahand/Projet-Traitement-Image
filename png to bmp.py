from PIL import Image

def convert_png_to_bmp(chemin_entrée, chemin_sortie):
    # Ouvrir l'image PNG
    image = Image.open(input_image_path)
    # Convertir l'image en BMP
    image.convert("RGB").save(output_image_path)

# Chemin d'accès de l'image PNG d'entrée
input_image_path = "T:\image.png"

# Chemin d'accès de l'image BMP de sortie
output_image_path = "T:\image_bitmap.bmp"

# Convertir l'image PNG en BMP
convert_png_to_bmp(input_image_path, output_image_path)

print("Conversion terminée.")
