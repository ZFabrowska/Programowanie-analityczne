import cv2 #przetwarzanie obrazów
import numpy as np #macierze (= obrazy)
import matplotlib.pyplot as plt #obrazy i wykresy
import rasterio #wczytywanie geotiffów
from matplotlib.colors import ListedColormap #kolory do progowania

#------WCZYTANIE ZDJĘĆ------
image_files = [
    r"projekt/images_geotiff/1985api.tif",
    r"projekt/images_geotiff/1993api.tif",
    r"projekt/images_geotiff/2001api.tif",
    r"projekt/images_geotiff/2011api.tif",
]

titles = ["1985", "1993", "2001", "2011"]



#------MAPY INDEKSU NDVI------

images_ndvi = []

for path in image_files: #iteracja po ścieżkach do obrazów
    with rasterio.open(path) as src: #otwarcie geotiffu
        red = src.read(1).astype(np.float32) #kanał czerwony
        nir = src.read(4).astype(np.float32) #kanał bliskiej podczerwieni
        ndvi = (nir - red) / (nir + red + 1e-6) #obliczenie NDVI
        images_ndvi.append(ndvi) #dodanie mapy NDVI do listy
    
plt.figure(1)
for i, idx_img in enumerate(images_ndvi):  # iteracja po obrazach NDVI
    plt.subplot(2, 2, i+1)
    plt.imshow(idx_img, cmap='RdYlGn', vmin=-0.1, vmax=1)  # wyświetlamy obraz z normalizacją
    plt.title(titles[i])
    plt.axis('off')
plt.suptitle("Indeks NDVI")


#------PROGOWANIE------
binary_cmap = ListedColormap(['#2a003f', '#ffff00'])  # fiolet, żółty

ndvi_threshold = 0.6

plt.figure(2)
for i, idx_img in enumerate(images_ndvi): #iteracja po obrazach NDVI
    plt.subplot(2, 2, i+1) #subplot: 2 wiersze, 2 kolumny, iteracja
    binary = np.where(idx_img > ndvi_threshold, 1, 0) #pixele powyżej progu są 1 (żółty)
    plt.imshow(binary, cmap=binary_cmap) 
    plt.title(f"{titles[i]}")
    plt.axis('off')
plt.suptitle("Progowanie NDVI")



# #------WYKRES ZMIANA ROŚLINNOŚCI------

def procent_zalesienia(images_idx, ndvi_threshold): #procent pikseli powyżej progu
    percentages = []
    for img in images_idx:
        total = img.size
        above = np.sum(img > ndvi_threshold)
        perc = (above / total) * 100
        percentages.append(perc)
    return percentages

years = [1985, 1993, 2001, 2011] #lata

ndvi_pct = procent_zalesienia(images_ndvi, 0.6) #odpowiednie progi dla każdego wskaźnika

plt.figure(3)
plt.plot(years, ndvi_pct, marker='o', markersize=10, color='blue', label='NDVI')
plt.xticks(years)
plt.ylim(0, 100)
plt.xlabel("Rok")
plt.ylabel("Procent pokrycia lasem [%]")
plt.title("Postęp wylesiania w latach")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.show()
