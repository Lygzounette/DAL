# ***README***

## ***README SUMMARY***

#### INSTALLATION
#### ENGLISH DESCRIPTION
#### DESCRIPTION FRANCAISE
#### OUR BESTEST PIECE OF CODE
---
***Installation***
---

- Last .exe version available !

1. Download .zip:

		Dowload .zip in code > download ZIP, and extract DAL-main anywhere

  	1. Or .exe:

			Download only DAL.exe in files > DAL.exe > ... > download (Ctrl + Shift + S)

2. Execute DAL:
  
   		Find DAL.exe ( \DAL-main\DAL-main\DAL.exe) and click on it to execute
  		If a warning appears click on launch anyways

  	1. Or with main.py:
	
	  		Open main.py with a python interpreter
			Make sure you have installed the packages "raylib" (not pyray) and "noise"
	  		Start program
3. Voilà !
---

Anglais / English
---


***Doom Au Louvre (DAL)***
> - Python

A retro-styled *FPS* where art meets demons in the world's most famous museum!

***🎮 Description***

*Doom Au Louvre (DAL)* is a *Python-powered* first-person shooter combining rogue-like elements with *classic Doom-inspired mechanics*. Battle demonic forces through either infinite procedurally generated mazes or hand-crafted levels, all set within a *pixel-art* reimagining of the Louvre Museum.

***✨ Features***

***Gameplay***
>	- **Two Modes**: Endless procedural maze OR designed campaign levels
>	- **Dynamic Combat**: 2 unique weapons with alt-fire modes (scope & integrated flashlight)
>	- **Movement Mastery**: Run, dash, mid-air shooting, and momentum-based jumps
>	- **Destructible Environment**: Strategic wall destruction & environmental interaction

***Enemies & Environment***
>	- 🧟 **Demonic AI**: Multiple enemy types with chase behaviors
>	- 🧱 **Interactive Maze**: Breakable walls & hidden secrets
>	- 🔦 **Light Management**: Weapon-mounted flashlight system

***Technical***
>	- 🐍 **Python Core**: Built with modern Python features
>	- 🕹️ **Retro Rendering**: Pseudo-3D raycasting engine
>	- 🧠 **Procedural Generation**: Custom maze algorithm
	
 - ⌨️ **Controls**

| Action | Key |
|----------|----------|
| Movement | WASD     |
| Run      | Ctrl     |
| Dash      | Left Shift     |
| Jump      | Space     |
| Fire      | Left Click     |
| Scope      | Right Click     |
| Weapon Switch      | Q     |
| Use PowerUps      | E     |
| Menu / Leave      | Escape     |

***Team***

	Maé Picard: Lead Programmer & Game Design & README
	Nolan Guthinger: Pixel Artist & Level Designer
	Nathan Bruyère: Systems Programmer & Technical Writer


---
---
---
Français / French
---


***Doom Au Louvre (DAL)***
> - Python

Un *FPS* rétro où l'art rencontre le chaos dans le musée le plus célèbre du monde !

***🎮 Description***

*Doom Au Louvre* (DAL) est un jeu de tir en *Python* combinant des éléments roguelike avec des mécaniques inspirées du classique *Doom premier du nom*. Affrontez des forces démoniaques dans des labyrinthes générés procéduralement ou des niveaux conçus à la main et avec amour, le tout dans une réinterprétation *pixel-art* du Louvre.

***✨ Fonctionnalités***

***Gameplay***
>	- **Deux Modes**: Labyrinthe infini généré OU niveaux conçus
>	- **Armes Dynamiques**: 2 armes uniques avec modes secondaires (visée & lampe torche)
>	- **Mouvement Avancé**: Course, dash, tir en l'air et sauts dynamiques
>	- **Environnement Destructible**: Murs destructibles & secrets cachés

***Ennemis & Environnement***
>	- 🧟 **IA Démoniaque**: Plusieurs types d'ennemis intelligents
>	- 🧱 **Labyrinthe Interactif**: Système de destruction stratégique
>	- 🔦 **Gestion Lumière**: Système de lampe torche intégrée

***Technique***
>	- 🐍 **Python Moderne**: Utilisation des meilleurs fonctionnalités
>	- 🕹️ **Rendu Rétro**: Moteur de rendu pseudo-3D avec éclairage dynamique
>	- 🧠 **Génération Procédurale**: Algorithme de labyrinthe unique
 
- ⌨️ **Contrôles**

| Action | Touche |
|----------|----------|
| Déplacement | ZQSD     |
| Course      | Ctrl     |
| Dash      | Maj Gauche     |
| Saut      | Espace     |
| Tir      | Clic Gauche     |
| Visée      | Clic Droit     |
| Changement Arme      | A     |
| Utiliser Bonus      | E     |
| Menu / Quitter      | Échape     |

***Équipe***

	Maé Picard: Développeur Principal & Game Design & README
	Nolan Guthinger: Artiste Pixel & Level Designer
	Nathan Bruyère: Développeur & Rédaction Technique
---
---
---
# Our Best Piece of Code.

This piece of code is used **everytime** the game renders (*60 times per second*).
> It has to draw any object on the screen with the **same laws** :
> - based how far away the **player's flashlight's light** is, we darken it or lighten it
> - if it is too **far**, it isn't rendered (*lost in the darkness*)
> - if it has to be rotated, it will be
> - it's colors will be modified to give a more *natural-retro-bad-camera-look*
The brightness is based on **two points** in front of the player,
a *farther one* and a *nearer one*, they are used to make a good **flashlight effect**
which's brightness is *consistant, dynamic and realistic*.

 ```python
def draw_custom(pos, model, color, r, axis = (0, 0, 0), rotation_r = 0, scale = 1):
    """Draw (or not) Any object, based on camera position, direction of looking and other time events.
    It hads light effects on any object, depending on the distance from the camera and the light effects of the gun.
    This makes a great flashlight effect using only two distance calculation and color manipulation"""

    # Initialisation of the positions
    x, y, z = player.pos
    x1, y1, z1 = pos
    vx, vy, vz = player.v # Normal vector of the player
    c = (distance_of_view >> 1) - 2 # First constant
    c2 = min(c, 6) # Second constant
    x2, y2, z2 = x1 - x - c2 * vx, y1 - y - (c2 / 2) * vy - 1 / (gun.tick_after_shoot // 6 + 0.75) + 0.5, z1 - z - c2 * vz
    # ^^^^ Calculates useful coordinates depending on position, orientation, and time events of the gun
    #      These are the coordinates of the farest away point, making the big circle of the flashlight effect
    d2 = math.sqrt(x2 ** 2 + 4 * y2 ** 2 + z2 ** 2)
    # ^^^^ Calculates a first distance far away from the player
    if d2 < c + 9 - c2: # Draw only if object is near enough
        x3, y3, z3 = x1 - x - 2.5 * vx, y1 - y - vy, z1 - z - 2.5 * vz # Other coordinates, second point, nearest
        d3 = x3 ** 2 + 2 * y3 ** 2 + z3 ** 2 # This distance is an added light to the nearer points, making a clean effect
        if d3 < 9: d2 *= d3 / 9 # If near enough, we multiply to get a smooth light
        d = max(7, d2 * 21) # We ensure that the light is never too bright by minimizing to 7, this gives a semi-realistic look
        # Some constants and variables needed to process the colors
        b = abs(1 - distance_of_view * 9 / d)
        t = d / r
        c1, c2, c3, _ = color
        bc1, bc2, bc3, _ = fade_color
        # We rotate the model by the specified amount (exemple : rotating the floating items)
        model.transform = matrix_rotate(axis, rotation_r)
        # And finally the object is drawn, with intricate color manipulation to give a less smooth more realistic look
        draw_model(model, pos, scale,
                   (min(255, int(max(bc1 * b, c1 - t ** 1.05 * 0.8))),
                    min(255, int(max(bc2 * b, c2 - t ** 1.04 * 0.85))),
                    min(255, int(max(bc3 * b, c3 - t ** 1.06 * 0.9))), 255))
        return True # The object has been drawned successfully
    else: return False # It hasn't
```
