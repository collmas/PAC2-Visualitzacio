import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

df = pd.read_csv("./data/nba_field_goals_scrap.csv")
data = df[["FTM", "FG2M", "FG3M"]].values.tolist()

colors = ["#FFFFFF", "#C9082A", "#17408B"]
team_colors = pd.DataFrame({
    'team_abbreviation':['BOS', 'MIN', 'MIL', 'PHI', 'DEN', 'OKC', 'SAC', 'ORL', 'DAL',
       'LAC', 'MIA', 'NYK', 'CLE', 'NOP', 'HOU', 'LAL', 'GSW', 'IND',
       'PHX', 'BKN', 'CHI', 'ATL', 'UTA', 'TOR', 'MEM', 'CHA', 'POR',
       'WAS', 'SAS', 'DET'],
    'team_color':['#008248','#236192','#00471b','#006bb6','#0d2240','#007ac1','#5b2b82','#0b77bd','#007dc5',
                  '#1d428a','#98002e','#f58426','#6f2633','#b4975a','#ce1141','#552583','#fdb927','#002d62',
                  '#b95915','Black','#ce1141','#e03a3e','#2b5134','#a0a0a3','#5d76a9','#00788c','#cf0a2c',
                  '#002b5c','Black','#1d428a'
                  ]
})


fig, axes = plt.subplots(2, 5, figsize=(15, 10))
axes = axes.flatten()

# Paràmetres per ajustar la separació dels punts
row_length = 10  # nombre de cercles per fila
spacing_x = 0.5  # espai horitzontal entre cercles
spacing_y = 0.3  # espai vertical entre cercles

# Creació dels punts per a cada regió
for i, (team, counts) in enumerate(zip(df["TEAM_ABBREVIATION"], data)):
    ax = axes[i]
    ax.set_title(team, fontsize=10, backgroundcolor = team_colors[team_colors.team_abbreviation == team]["team_color"].values[0], color = "#FFFFFF")
    
    x = []
    y = []
    colors_list = []
    
    # Variables de posició inicial
    x_offset = 0
    y_offset = 0
    
    # Generem els punts en forma de matriu
    for color, count in zip(colors, counts):
        for _ in range(count):
            x.append(x_offset * spacing_x)  # Ajustem l'espai horitzontal
            y.append(y_offset * spacing_y)  # Ajustem l'espai vertical
            colors_list.append(color)
            
            # Increment de la posició x i canvi de fila quan arribi al límit
            x_offset += 1
            if x_offset >= row_length:
                x_offset = 0
                y_offset -= 1  # Nova fila (més avall en l'eix y)
    
    # Dibuixem els punts com a cercles
    ax.scatter(x, y, c=colors_list, s=100, edgecolor="black")

    # Fixem els límits dels eixos per mantenir la consistència entre subgràfics
    ax.set_xlim(-0.5, row_length * spacing_x)  # límit de l'eix x
    ax.set_ylim(-10 * spacing_y, spacing_y)   # límit de l'eix y, ajustat per al nombre de files

    ax.text(x=2.25, y=-2.15, s=f"{df[df.TEAM_ABBREVIATION == team]['PTS'].values[0]} PTS", horizontalalignment='center',
     verticalalignment='center', fontweight="bold", color=team_colors[team_colors.team_abbreviation == team]["team_color"].values[0])
    
    # Ocultem els eixos
    ax.axis("off")

# fig.text(0.5, 1.1, "Millors equips NBA", horizontalalignment='center',
    #  verticalalignment='center')

fig.suptitle("Distribució dels tirs dels top 5 en anotació a la NBA 2024-25", y=1.0001, fontsize=16)
fig.text(0.5, 0.53, "Distribució dels tirs dels bottom 5 en anotació a la NBA 2024-25", horizontalalignment='center',
     verticalalignment='center', fontsize=16)


ftm_cercle = mpatches.Circle((0.5, 0.5), 0.25, facecolor="green",
                    edgecolor="red", linewidth=3)


# Ajustem el layout
plt.tight_layout()

# plt.legend(handles=[red_patch, blue_patch], loc=(0.6,0.8))

# Configura la llegenda amb punts sense línia i amb vora negra
blanc_point = Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[0], markeredgecolor='black', markersize=10, linestyle='None', label="Tirs lliures (1PT)")
vermell_point = Line2D([0], [0], marker='o', color='r', markerfacecolor=colors[1], markeredgecolor='black', markersize=10, linestyle='None', label="Tirs de 2PTS")
blau_point = Line2D([0], [0], marker='o', color='b', markerfacecolor=colors[2], markeredgecolor='black', markersize=10, linestyle='None', label="Tirs de 3PTS")

# Afegeix la llegenda amb els punts en lloc de rectangles
plt.legend(handles=[blanc_point, vermell_point, blau_point], loc=(-2.5, 0.05), fontsize=10, ncol=3, frameon=False)
plt.show()
