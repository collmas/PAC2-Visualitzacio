import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as image
import matplotlib.lines as lines
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import pandas as pd
import numpy as np

df = pd.read_csv("./gaming_revenue.csv")
df["Percentatges"] = round(df["Ventes"] / sum(df["Ventes"]) * 100, 2)

# Dades de distribució de tipus de feina (exemple)
categories = df["Plataforma"].values.tolist()
percentatges = df["Percentatges"].values.tolist()
dolars = df["Ventes"].values.tolist()

# Preparem les icones 
icones_files = ["smartphone-call", "game-console", "keyboard-and-mouse", "browser"]
icones = {}
new_colors = [[0.8509803921568627, 0.37254901960784315, 0.00784313725490196, 1.0], 
              [0.10588235294117647, 0.6196078431372549, 0.4666666666666667, 1.0], 
              [0.4588235294117647, 0.4392156862745098, 0.7019607843137254, 1.0], 
              [0.9764705882352941, 0.6078431372549019, 0.7607843137254902, 1.0]]
for i, icona in enumerate(icones_files):
    file = f"./icons/{icona}.png"
    icones[icona] = image.imread(file)
    mask = (icones[icona][:, :, :3] == [0, 0, 0]).all(axis=-1) & (icones[icona][:, :, 3] > 0)
    icones[icona][mask] = new_colors[i]
    # print(icones[icona].shape)
    # print(icones[icona])


# Configuració de la mida de la figura
fig, ax = plt.subplots(figsize=(15, 15))
ax.set_xlim(-50, 150)
ax.set_ylim(0, 104)
ax.axis('off')  # Ocultem els eixos

# Colors per a cada secció
colors = ["#f5aa7b", "#85cdb0", "#b8b0e0", "#f99bc2"]
colors_foscos = ["#d95f02", "#1b9e77", "#7570b3", "#e7298a"]

# Posició inicial de la part inferior de la piràmide
bottom = 0

# Amplada inicial de la base de la piràmide
base_width = 200

# Crear les seccions de la piràmide
for i in range(len(categories)):
    # Alçada de cada secció proporcional al percentatge
    height = percentatges[i]
    
    # Amplada inferior i superior per a cada trapezi
    width_bottom = base_width - (bottom / 100) * base_width
    width_top = base_width - ((bottom + height) / 100) * base_width
    mid_width = ((50 + width_bottom / 2) + (50 + width_top / 2)) / 2
    
    if i == len(categories) - 1:
        # La part superior és un triangle per l'última categoria
        triangle = patches.Polygon(
            [[50 - width_bottom / 2, bottom], [50 + width_bottom / 2, bottom], [50, bottom + height]],
            closed=True, color=colors[i]
        )
        ax.add_patch(triangle)
        line = lines.Line2D([50, 55], [(bottom + (bottom + height))/ 2, (bottom + (bottom + height))/ 2], color=colors[i], linewidth=0.5)
        ax.add_line(line)

        # Afegim l'icona
        imagebox = OffsetImage(icones[icones_files[i]], zoom = 0.03)
        ab = AnnotationBbox(imagebox, (89, bottom + height / 2), frameon=False )
        ax.add_artist(ab)    

    else:
        # Crear un trapezi per a cada nivell
        trapezoid = patches.Polygon(
            [[50 - width_bottom / 2, bottom], [50 + width_bottom / 2, bottom], 
             [50 + width_top / 2, bottom + height], [50 - width_top / 2, bottom + height]],
            closed=True, color=colors[i]
        )
        ax.add_patch(trapezoid)

        # Afegim l'icona
        imagebox = OffsetImage(icones[icones_files[i]], zoom = 0.07*height/25)
        ab = AnnotationBbox(imagebox, (50, bottom + height / 2), frameon=False )
        ax.add_artist(ab)
    
    # Afegir el text del percentatge i la categoria
    ax.text(mid_width + 5, bottom + height / 2, f"{categories[i]} {percentatges[i]}%", ha='left', va='center', fontsize=10, color=colors[i])
    # Afegir text dels milions de dòlars
    ax.text(100-mid_width -5, bottom + height / 2, f"USD {int(dolars[i]*1000):,} m", ha='right', va='center', fontsize=10, color=colors[i])
    
    # Augmentem la posició inferior per a la següent secció
    bottom += height


# Títol
plt.suptitle("Ventes mundials en milions de dòlars del sector de videojocs al 2022", fontsize=16, y = 0.97)
plt.title("La importància dels jocs de mòbil en el sector", fontsize=12, y = 1.03)
plt.show()
