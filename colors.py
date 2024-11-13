import numpy as np

def hex_to_rgba(hex_color, alpha=1.0):
    """Converteix un color hexadecimal a format RGBA per a matplotlib.
    
    Paràmetres:
    hex_color (str): Color en format hexadecimal, ex: '#FF9999'.
    alpha (float): Opacitat del color, per defecte és 1.0 (totalment opac).
    
    Retorna:
    np.array: Array numpy amb els valors RGBA normalitzats entre 0 i 1.
    """
    # Elimina el símbol '#' si està present
    hex_color = hex_color.lstrip('#')
    
    # Converteix cada parell de caràcters hexadecimals a decimal i normalitza a [0, 1]
    rgb = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    
    # Retorna el color en format np.array incloent el canal alpha
    return rgb + [alpha]

# Exemple d'ús
new_color = hex_to_rgba("#FF9999", alpha=1.0)
colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "f5aa7b"]
foscos = ["#d95f02", "#1b9e77", "#7570b3", "#e7298a"]
clars = ["#f5aa7b", "#85cdb0", "#b8b0e0", "#f99bc2"]

print([hex_to_rgba(color) for color in clars])
