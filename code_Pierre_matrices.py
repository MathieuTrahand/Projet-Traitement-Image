import numpy as np
from math import floor
from PIL import Image
from random import randint

global R
global G
global B

global RIGHT
global LEFT
global UP
global DOWN

#Trois constantes permettant d'accéder à la valeur de Rouge (R), Vert (G) ou Bleu (B) d'une pixel
R = 0
G = 1
B = 2

#Quatre constantes permettant de savoir dans quelle direction s'effectue le recadrage
#RIGHT: depuis la droite
#LEFT: depuis la gauche
#UP: depuis le haut
#DOWN: depuis le bas

RIGHT = 1
LEFT = -1
UP = -1
DOWN = 1

#Objet Image
class Picture():
    #Constructeur de la classe Image
    def __init__(self, path_to_file:str) -> None:
        self.path = path_to_file

        #Tableau contenant le type du fichier, la taille de l'image et sa valeur maximum
        header = []
        #Ouverture et lecture du document en mode 'ascii'
        #On ignore les erreurs car on ne veut récuperer que l'en-tête du document
        with open(self.path, 'r', encoding='ascii', errors='ignore') as im:
            i = 0
            while i < 3:
                line = im.readline()
                #On ignore les possibles commentaires présents dans le document
                if not line[0] == '#':
                    data = line.split()
                    for d in data:
                        if not d == '\n':
                            header.append(d)
                    i += 1

        self.file_type = header[0]
        self.width = int(header[1])
        self.height = int(header[2])
        self.max_value = int(header[3])

        #Si le fichier a pour en-tête P6, on l'ouvre on mode binaire
        if self.file_type[1] == '6':
            with open(self.path, 'rb') as im:

                #On passe les données d'en-tête déjà récupérée
                i = 0
                while i < 3:
                    line = im.readline()
                    #On ignore les possibles commentaires présents dans le document
                    #35 correspond au '#' en byte et donc à la présence d'un commentaire
                    if not line[0] == 35:
                        i += 1

                #Lecture du reste du document contenant les pixels
                data = im.read()

                #Tableau 3D contenant pour une ligne et une colonne le tableau [R,G,B]
                self.pixmap = np.array([[[0,0,0] for j in range(self.width)] for i in range(self.height)], ndmin=3, dtype=np.uint8)
                self.pixmap_copy = np.array([[[0,0,0] for j in range(self.width)] for i in range(self.height)], ndmin=3, dtype=np.uint8)
                for i in range(self.height):
                    for j in range(self.width):
                        for k in range(3):
                            self.pixmap[i][j][k] = data[self.width*3*i + 3*j + k]
                            self.pixmap_copy[i][j][k] = data[self.width*3*i + 3*j + k]

        #Si le fichier a pour en-tête P3, on l'ouvre en mode ascii
        if self.file_type[1] == '3':
            with open(self.path, 'r') as im:

                #On passe les données d'en-tête déjà récupérée
                i = 0
                while i < 3:
                    line = im.readline()
                    #On ignore les possibles commentaires présents dans le document
                    #35 correspond au '#' en byte et donc à la présence d'un commentaire
                    if not line[0] == '#':
                        i += 1

                #Lecture du reste du document contenant les pixels
                data = im.read()
                split_data = data.split('\n')

                #Tableau 3D contenant pour une ligne et une colonne le tableau [R,G,B]
                self.pixmap = np.array([[[0,0,0] for j in range(self.width)] for i in range(self.height)], ndmin=3, dtype=np.uint8)
                self.pixmap_copy = np.array([[[0,0,0] for j in range(self.width)] for i in range(self.height)], ndmin=3, dtype=np.uint8)
                for i in range(self.height):
                    for j in range(self.width):
                        for k in range(3):
                            self.pixmap[i][j][k] = split_data[self.width*3*i + 3*j + k]
                            self.pixmap_copy[i][j][k] = split_data[self.width*3*i + 3*j + k]

        self.veins = []
        self.energy = np.array([[0 for j in range(self.width)] for i in range(self.height)], ndmin=2, dtype=int)
        self.delete_calc = np.array([[False for j in range(self.width)] for i in range(self.height)], ndmin=2, dtype=bool)

    #Sauvegarde l'image sous le format PPM P6
    def save(self) -> None:
        split_path = self.path.split('.')
        with open(split_path[0] + "-copy." + split_path[1], "wb") as im:
            #On commence par écrire  l'en-tête directement en bytes
            #Retour à la ligne : \x0a
            #Espacement : \x20

            im.write("P6".encode("ascii"))
            im.write(b'\x0a')
            im.write(str(self.width).encode("ascii"))
            im.write(b'\x20')
            im.write(str(self.height).encode("ascii"))
            im.write(b'\x0a')
            im.write(str(self.max_value).encode("ascii"))
            im.write(b'\x0a')

            for i in range(self.height):
                for j in range(self.width):
                    for k in range(3):
                        im.write(self.pixmap[i][j][k])

    #Recadre l'image
    def crop(self, crop_x:int, dir_x:int, crop_y:int, dir_y:int) -> None:
        #On ne peut pas enlever plus de pixel que la taille de l'image
        if crop_x >= self.width or crop_y >= self.height:
            return

        #On commence par supprimer les lignes
        #########################################################

        #On crée une nouvelle image avec les bonnes dimensions
        new_pixmap = np.array([[[0,0,0] for j in range(self.width)] for i in range(self.height - crop_y)], ndmin=3, dtype=np.uint8)
        
        #On copie dans la nouvelle image la partie de l'image qui nous intéresse
        if dir_y == DOWN:
            #Si on veut recadrer depuis le haut vers le bas
            new_pixmap = self.pixmap[crop_y:self.height:]
        elif dir_y == UP:
            #Si on veut recadrer depuis le bas vers le haut
            new_pixmap = self.pixmap[0:self.height-crop_y:]

        self.pixmap = new_pixmap

        #Ensuite on supprime les colonnes
        #########################################################
        
        #On crée une nouvelle image avec les bonnes dimensions
        new_pixmap = np.array([[[0,0,0] for j in range(self.width - crop_x)] for i in range(self.height - crop_y)], ndmin=3, dtype=np.uint8)
       
        for i in range(self.height - crop_y):
            #Pour chaque ligne, on copie seulement les pixels qui nous intéressent
            if dir_x == RIGHT:
                #Si on veut recadrer depuis la gauche vers la droite
                new_pixmap[i] = self.pixmap[i][0:self.width-crop_x:]
            elif dir_x == LEFT:
                #Si on veut recadrer depuis la droite vers la gauche
                new_pixmap[i] = self.pixmap[i][crop_x:self.width:]
        
        self.pixmap = new_pixmap

        #On change les dimensions de l'image
        #########################################################

        self.width -= crop_x
        self.height -= crop_y

        self.pixmap_copy = self.pixmap
        self.delete_calc = np.array([[False for j in range(self.width)] for i in range(self.height)], ndmin=2, dtype=bool)

    #Redimenssionne l'image en la tassant
    def rescale(self, scale_x:int, scale_y:int) -> None:
        #On ne peut pas enlever plus de pixel que la taille de l'image
        if scale_x >= self.width or scale_y >= self.height:
            return
        
        self.pixmap_copy = self.pixmap

        #On commence par supprimer les lignes
        #########################################################

        if scale_y != 0: #Pour éviter une division par 0
            n_y = (self.height//scale_y) + 1
            k = 0

            #On crée une nouvelle image avec les bonnes dimensions
            new_pixmap = np.array([[[0,0,0] for j in range(self.width)] for i in range(self.height - scale_y)], ndmin=3, dtype=np.uint8)
            
            #On enlève une ligne toutes les n_y lignes
            for i in range(self.height - scale_y):
                if i % n_y == 0:
                    k += 1
                new_pixmap[i] = self.pixmap[i + k]

            self.pixmap = new_pixmap

        #Ensuite on supprime les colonnes
        #########################################################

        if scale_x != 0: #Pour éviter une division par 0
            n_x = (self.width//scale_x) + 1

            #On crée une nouvelle image avec les bonnes dimensions
            new_pixmap = np.array([[[0,0,0] for j in range(self.width - scale_x)] for i in range(self.height - scale_y)], ndmin=3, dtype=np.uint8)
            for i in range(self.height - scale_y):
                k = 0

                #Pour chaque ligne, on enlève un pixel tous les n_x pixels
                for j in range(self.width - scale_x):
                    if j % n_x == 0:
                        k += 1
                    new_pixmap[i][j] = self.pixmap[i][j + k]

            self.pixmap = new_pixmap

        #On change les dimensions de l'image
        #########################################################

        self.width -= scale_x
        self.height -= scale_y

        self.pixmap_copy = self.pixmap
        self.delete_calc = np.array([[False for j in range(self.width)] for i in range(self.height)], ndmin=2, dtype=bool)

    #Calcul l'énergie du pixel à la ligne i et à la colonne j
    def calc_energy(self, i:int, j:int) -> int:

        #Si un pixel fait partie d'une zone à supprimer, alors on met son énergie très basse
        #pour forcer les veines à passer par ce pixel
        if self.delete_calc[i][j] == True:
            return -100000
        
        Rx=int(self.pixmap[(i+1)%self.height][j][R])-int(self.pixmap[i-1][j][R])
        Gx=int(self.pixmap[(i+1)%self.height][j][G])-int(self.pixmap[i-1][j][G])
        Bx=int(self.pixmap[(i+1)%self.height][j][B])-int(self.pixmap[i-1][j][B])

        Ry=int(self.pixmap[i][(j+1)%self.width][R])-int(self.pixmap[i][j-1][R])
        Gy=int(self.pixmap[i][(j+1)%self.width][G])-int(self.pixmap[i][j-1][G])
        By=int(self.pixmap[i][(j+1)%self.width][B])-int(self.pixmap[i][j-1][B])

        deltx = Rx*Rx + Gx*Gx + Bx*Bx
        delty = Ry*Ry + Gy*Gy + By*By

        e = deltx + delty

        return e

    #Initialise le tableau des énergie de l'image
    def tab_energy(self) -> None:
        for i in range(self.height):
            for j in range(self.width):
                self.energy[i][j] = self.calc_energy(i, j)

    #Calcul une veine verticale de plus basse énergie
    def vertical_vein(self) -> np.array:
        #Tableau qui conserve les positions des pixels faisant partie de la veine
        vein = np.array([0 for i in range(self.height)], ndmin=1)

        #Tableau d'énergie intermédiaire pour retrouver la veine de plus basse énergie
        energy_sum = np.array([[0 for j in range(self.width)] for i in range(self.height)], ndmin=2, dtype=int)

        #Vraie copie du tableau des énergies
        for i in range(self.height):
            for j in range(self.width):
                energy_sum[i][j] = self.energy[i][j]

        #Pour chaque pixel, on regarde lequel parmi les trois pixels au dessus de lui
        #possède la plus basse énergie. L'energie de ce pixel dans le tableau intermédiaire
        #est la somme de la plus basse énergie parmi les trois pixels au dessus et de l'énergie du pixel
        for i in range(1, self.height):
            for j in range(self.width):
                proximity = []
                proximity.append(energy_sum[i-1][j])
                if j != 0:
                    proximity.append(energy_sum[i-1][j - 1])
                if j + 1 != self.width:
                    proximity.append(energy_sum[i-1][j + 1])
                energy_sum[i][j] = min(proximity) + self.energy[i][j]

        #On recherche le pixel en bas avec la plus basse énergie
        start = randint(0, self.width-1)
        index_min = start
        energy_min = energy_sum[self.height-1][start]
        for j in range(self.width):
            if energy_sum[self.height-1][(start + j)%self.width] < energy_min:
                index_min = (start + j)%self.width
                energy_min = energy_sum[self.height-1][(start + j)%self.width]

        #On construit la veine en trouvant le pixel au dessus qui a permis d'arriver à celui du dessous
        vein[self.height-1] = index_min
        for i in range(self.height-1):
            for j in range(-1, 2):
                if energy_sum[self.height-1-i][index_min] == self.energy[self.height-1-i][index_min] + energy_sum[self.height-2-i][(index_min + j)%self.width]:
                    vein[self.height-2-i] = (index_min + j)%self.width
                    index_min = (index_min + j)%self.width
                    break
        
        return vein
    
    #Pour effectuer un découpage de veines verticales
    def seam_carving_vertical(self, scale_x:int, show_v:bool=False):
        #On ne peut pas enlever plus de pixel que la taille de l'image
        if scale_x >= self.width:
            return

        #Tableau contenant toutes veines calculées
        self.veins = []
        for k in range(scale_x):
            #On initialise l'énergie
            self.tab_energy()

            #On calcule une veine
            vein = self.vertical_vein()
            self.veins.append([])

            #On décale tous les pixels à droite de la veine vers la gauche
            for i in range(self.height):
                for j in range(vein[i], self.width-1):
                    self.pixmap[i][j][R] = self.pixmap[i][j+1][R]
                    self.pixmap[i][j][G] = self.pixmap[i][j+1][G]
                    self.pixmap[i][j][B] = self.pixmap[i][j+1][B]

                    self.delete_calc[i][j] = self.delete_calc[i][j+1]
                
                offset = 0
                #On retrouve les positions des pixels de la veine dans l'image originales
                for v in self.veins:
                    if len(v) > i:
                        if v[i] < vein[i] + offset + 1:
                            offset += 1
                self.veins[-1].append(vein[i] + offset)

            self.width -= 1
            np.resize(self.pixmap, (self.height, self.width, 3))
            self.delete_calc = np.array([[self.delete_calc[i][j] for j in range(self.width)] for i in range(self.height)], ndmin=2, dtype=bool)
        self.delete_calc = np.array([[False for j in range(self.width)] for i in range(self.height)], ndmin=2, dtype=bool)

        if show_v == True:
            self.show_veins()

    #Pour afficher les valeurs en énergie de l'image
    def show_energy(self):
        #On initialise l'énergie
        self.tab_energy()

        T=[max(self.energy[i]) for i in range(self.height)]
        maximum=max(T)

        for i in range(self.height):
            for j in range(self.width):
                self.pixmap[i][j][R] = np.array(floor((self.energy[i][j]/maximum)*255)).astype(np.uint8)
                self.pixmap[i][j][G] = np.array(floor((self.energy[i][j]/maximum)*255)).astype(np.uint8)
                self.pixmap[i][j][B] = np.array(floor((self.energy[i][j]/maximum)*255)).astype(np.uint8)

    #Pour dessiner une veine
    def show_vein(self):
        self.tab_energy()
        vein = self.vertical_vein()

        for i in range(self.height):
            self.pixmap[i][vein[i]][R] = 255
            self.pixmap[i][vein[i]][G] = 0
            self.pixmap[i][vein[i]][B] = 0

    #Pour dessiner les veines après un seam carving
    def show_veins(self):
        for v in self.veins:
            for i in range(self.height):
                self.pixmap_copy[i][v[i]][R] = 255
                self.pixmap_copy[i][v[i]][G] = 0
                self.pixmap_copy[i][v[i]][B] = 0
        
        self.pixmap = self.pixmap_copy
        self.width = len(self.pixmap_copy[0])

        self.pixmap_copy = np.array([[[0,0,0] for j in range(self.width)] for i in range(self.height)], ndmin=3, dtype=np.uint8)
        for i in range(self.height):
            for j in range(self.width):
                self.pixmap_copy[i][j][R]=self.pixmap[i][j][R]
                self.pixmap_copy[i][j][G]=self.pixmap[i][j][G]
                self.pixmap_copy[i][j][B]=self.pixmap[i][j][B]

        self.delete_calc = np.array([[False for j in range(self.width)] for i in range(self.height)], ndmin=2, dtype=bool)

    #Pour tourner l'image
    def rotate(self):
        tab = np.array([[[0,0,0] for j in range(self.height)] for i in range(self.width)], ndmin=3, dtype=np.uint8)
        delete_tab = np.array([[False for j in range(self.height)] for i in range(self.width)], ndmin=2, dtype=bool)
        self.energy = np.array([[0 for j in range(self.height)] for i in range(self.width)], ndmin=2, dtype=int)
        for i in range(self.width):
            for j in range(self.height):
                tab[i][j]= self.pixmap[self.height-j-1][i]
                delete_tab[i][j] = self.delete_calc[self.height-j-1][i]
        self.pixmap= tab
        self.delete_calc = delete_tab

        self.pixmap_copy = np.array([[[0,0,0] for j in range(self.height)] for i in range(self.width)], ndmin=3, dtype=np.uint8)
        for i in range(self.width):
            for j in range(self.height):
                self.pixmap_copy[i][j][R]=self.pixmap[i][j][R]
                self.pixmap_copy[i][j][G]=self.pixmap[i][j][G]
                self.pixmap_copy[i][j][B]=self.pixmap[i][j][B]

        self.width, self.height = self.height, self.width

    #Pour effectuer un découpage de veines horizontales
    def seam_carving_horizontal(self, scale_x:int, show_v:bool=False):
        self.rotate()
        self.seam_carving_vertical(scale_x)
        
        if show_v == True:
            self.show_veins()

        self.rotate()
        self.rotate()
        self.rotate()
    
    #Renvoie la largeur de l'image
    def get_width(self) -> int:
        return self.width
    
    #Renvoie la hauteur de l'image
    def get_height(self) -> int:
        return self.height
    
    #Pour modifier les pixels à supprimer après un seam carving
    def modify_delete_calc(self, i, j, width):
        for l in range(-width, width + 1):
            for c in range(-width, width + 1):
                self.delete_calc[(i+l)%self.height][(j+c)%self.width] = True
