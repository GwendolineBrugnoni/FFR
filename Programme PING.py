# %% Importation des bibliotheques necessaires
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import copy
import cv2
import imutils
import sys

# %% Algo de traitement d'image thermique
img2 = mpimg.imread('C:\\Users\\gwenb\\OneDrive\\Images\\photo-de-groupe-0320.jpg')

img = copy.deepcopy(img2)
img_largeur = img.shape[0]
img_hauteur = img.shape[1]

for i in range(img_largeur):
    for j in range(img_hauteur):
        if (img[i][j][0] > 150):
            img[i][j][0], img[i][j][1], img[i][j][2] = 0, 0, 0
# %% Algo Reconnaissance Faciale
imagePath = r'C:\\Users\\gwenb\\OneDrive\\Images\\photo-de-groupe-0320.jpg'
cascadefile = "haarcascade_frontalface_alt.xml"
classCascade = cv2.CascadeClassifier(cascadefile)
image = cv2.imread(imagePath)
# Echelle de gris
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Reconnaissance faciale
faces = classCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                      flags=cv2.CASCADE_SCALE_IMAGE)
# Dessine des rectangles autour des visages trouvés
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
# %% Algo Reconnaissance de Personne
# Initializing the HOG person
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Reading the Image
image1 = cv2.imread('C:\\Users\\gwenb\\OneDrive\\Images\\photo-de-groupe-0320.jpg')

# Resizing the Image
image1 = imutils.resize(image1,
                        width=min(500, image1.shape[1]))

# Detecting all humans
(humans, _) = hog.detectMultiScale(image1,
                                   winStride=(5, 5),
                                   padding=(3, 3),
                                   scale=1.21)

# Drawing the rectangle regions
for (x, y, w, h) in humans:
    cv2.rectangle(image1, (x, y),
                  (x + w, y + h),
                  (0, 0, 255), 2)
# %% Switch
rep = True
while (rep == True):
    print("1-Traitement de l'image thermique")
    print("2-Reconnaissance de visage(s)")
    print("3-Reconnaissance de personne(s)")
    print("4-Quitter")
    n = int(input("Faites votre choix !!!"))
    if (n == 1):
        imgplot = plt.imshow(img2)
        plt.show()
        plt.figure()
        imgplot1 = plt.imshow(img)
        plt.show()
    if (n == 2):
        print("Il y a {0} visage(s).".format(len(faces)))
        plt.imshow(gray)
        plt.imshow(image)
    if (n == 3):
        print('Human Detected : ', len(humans))
        cv2.imshow("Image", image1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    if (n == 4):
        print("Au revoir !!!")
        rep = False