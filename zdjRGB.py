import cv2 #przetwarzanie obrazów
import numpy as np #macierze (= obrazy)
import matplotlib.pyplot as plt #obrazy i wykresy
from matplotlib.colors import ListedColormap #kolory do progowania

#------WCZYTANIE ZDJĘĆ------
image_files = [
    r"projekt/images/1985.png",
    r"projekt/images/1993.png",
    r"projekt/images/2001.png",
    r"projekt/images/2011.png",
]

titles = ["1985", "1993", "2001", "2011"]

#------ANALIZA ZDJĘĆ RGB------

images_equalized = []

for path in image_files:
    image = cv2.imread(path, cv2.IMREAD_COLOR) #wczytanie obrazu w kolorze
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #onversja do HSV
    image_hsv[:,:,2] = cv2.equalizeHist(image_hsv[:,:,2]) #wyrównanie histogramu w jasności (V)
    image_eq = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR) #konwersja z powrotem do BGR

    images_equalized.append(image_eq) #dodanie przetworzonego obrazu do listy

plt.figure(1)
for i, img in enumerate(images_equalized): #iteracja po przetworzonych obrazach i ich indeksach
    plt.subplot(2, 2, i+1) #subplot: 2 wiersze, 2 kolumny, iteracja
    plt.imshow(img[:,:,::-1])  # BGR -> RGB
    plt.title(titles[i]) #tytuły
    plt.axis('off') #bez osi



#------WSKAŹNIKI ROŚLINNOŚCI------
def VARI(R, G, B): #zgodnie z githubem z instrukcji, tylko na kanałach
    return (G - R) / (G + R - B + 1e-6)

def GLI(R, G, B):
    return (2*G - R - B) / (2*G + R + B + 1e-6)

def VIGREEN(R, G, B):
    return (G - R) / (G + R + 1e-6)

images_vari = []
images_gli = []
images_vigreen = []

for path in image_files: #iteracja po ścieżkach do obrazów
    image = cv2.imread(path, cv2.IMREAD_COLOR) #wczytanie obrazu w kolorze
    
    # kanały RGB
    B = image[:, :, 0].astype(np.float32) #konwersja na float32, żeby uniknąć problemów z dzieleniem i zakresami wartości
    G = image[:, :, 1].astype(np.float32)
    R = image[:, :, 2].astype(np.float32)
    
    # wskaźniki roślinności
    images_vari.append(VARI(R, G, B)) #dodanie obliczonego wskaźnika VARI do listy
    images_gli.append(GLI(R, G, B))
    images_vigreen.append(VIGREEN(R, G, B))


plt.figure(2)
for i, idx_img in enumerate(images_vari):  # iteracja po obrazach VARI
    plt.subplot(2, 2, i+1)
    plt.imshow(idx_img, cmap='jet', vmin=-0.1, vmax=0.2)  # wyświetlamy obraz z normalizacją
    plt.title(titles[i])
    plt.axis('off')
plt.suptitle("Indeks VARI")


plt.figure(3)
for i, idx_img in enumerate(images_gli):  # iteracja po obrazach GLI
    plt.subplot(2, 2, i+1)
    plt.imshow(idx_img, cmap='jet', vmin=-0.04, vmax=0.2)  # wyświetlamy obraz z normalizacją
    plt.title(titles[i])
    plt.axis('off')
plt.suptitle("Indeks GLI")


plt.figure(4)
for i, idx_img in enumerate(images_vigreen):  # iteracja po obrazach VARI
    plt.subplot(2, 2, i+1)
    plt.imshow(idx_img, cmap='jet', vmin=-0.1, vmax=0.2)  # wyświetlamy obraz z normalizacją
    plt.title(titles[i])
    plt.axis('off')
plt.suptitle("Indeks VIGREEN")




#------PROGOWANIE------
binary_cmap = ListedColormap(['#2a003f', '#ffff00'])  # fiolet, żółty

thresholds = { #progi
    "VARI": 0.05,
    "GLI": 0.08,
    "VIGREEN": 0.04
}

plt.figure(5) #vari
for i, idx_img in enumerate(images_vari): #iteracja po obrazach VARI
    plt.subplot(2, 2, i+1) #subplot: 2 wiersze, 2 kolumny, iteracja
    binary = np.where(idx_img > thresholds["VARI"], 1, 0) #pixele powyżej progu są 1 (żółty)
    plt.imshow(binary, cmap=binary_cmap) 
    plt.title(f"{titles[i]}")
    plt.axis('off')
plt.suptitle("Progowanie VARI")


plt.figure(6) #gli
for i, idx_img in enumerate(images_gli):
    plt.subplot(2, 2, i+1)
    binary = np.where(idx_img > thresholds["GLI"], 1, 0)
    plt.imshow(binary, cmap=binary_cmap)
    plt.title(f"{titles[i]}")
    plt.axis('off')
plt.suptitle("Progowanie GLI")


plt.figure(7) #vigreen
for i, idx_img in enumerate(images_vigreen):
    plt.subplot(2, 2, i+1)
    binary = np.where(idx_img > thresholds["VIGREEN"], 1, 0)
    plt.imshow(binary, cmap=binary_cmap)
    plt.title(f"{titles[i]}")
    plt.axis('off')
plt.suptitle("Progowanie VIGREEN")


#------WYKRES POSTĘPU WYLESIANIA------

def procent_zalesienia(images_idx, threshold): #procent pikseli powyżej progu
    percentages = []
    for img in images_idx:
        total = img.size
        above = np.sum(img > threshold)
        perc = (above / total) * 100
        percentages.append(perc)
    return percentages

years = [1985, 1993, 2001, 2011] #lata

vari_pct = procent_zalesienia(images_vari, 0.05) #odpowiednie progi dla każdego wskaźnika
gli_pct = procent_zalesienia(images_gli, 0.08)
vigreen_pct = procent_zalesienia(images_vigreen, 0.04)

plt.figure(8)
plt.plot(years, vari_pct, marker='o', markersize=10, color='blue', label='VARI')
plt.plot(years, gli_pct, marker='o', markersize=10, color='orange', label='GLI')
plt.plot(years, vigreen_pct, marker='o', markersize=10, color='green', label='VIGREEN')

plt.xticks(years)
plt.ylim(0, 100)
plt.xlabel("Rok")
plt.ylabel("Procent pokrycia lasem [%]")
plt.title("Postęp wylesiania w latach")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.show()