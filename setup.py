import math
import random
from pyray import *
import campain
import sys
import os

# Initialisation générale
# ----------------------------------------------------------------------------------------------------------------------
init_window(1, 1, "1")  # dummy initialisation pour pouvoir détecter l'écran
device = get_current_monitor()  # device se réfère à l'écran utilisé
sWidthConst = get_monitor_width(device)  # on en prend la largeur
sHeightConst = get_monitor_height(device)  # on en prend la hauteur
sWidth, sHeight = (sWidthConst, sHeightConst)  # mettre une taille personnalisée ? - conseillée (1200, 800)
rW = sWidthConst / sWidth  # des ratios pour ajuster les intéractions
rH = sHeightConst / sHeight
init_window(sWidth, sHeight, "Doom Au Louvre")  # initialisation de la fenêtre
disable_cursor()
FPS = 60  # 60 FPS pour une expérience fluide mais peu couteuse
set_target_fps(FPS)
# ----------------------------------------------------------------------------------------------------------------------
# Initialisation des variables utilisées par le joueur
# ----------------------------------------------------------------------------------------------------------------------
gravity = 3.75  # gravité
friction = 1 + 16 / FPS  # friction / resistance de l'air
speed = 1.25  # vitesse du joueur
artificial_heigh = 2  # taille du joueur (en blocks)
distance_of_view = campain.render_distance  # = 20, les objets a plus de 20 blocks de distance disparaissent
range_view = range(-distance_of_view + 2, distance_of_view - 1)  # Liste de nombres
FoV = 90  # grand FoV (Field of View = Champ de Vision) pour une impression de grandeur de l'espace
y_player_offset = 0  # Déplacement vertical artificiel (pas, recul..)
mob_strength = 1.0  # Coefficient multiplicateur de la force des monstres
danger_mod = True


# ----------------------------------------------------------------------------------------------------------------------
# Initialisation des ressources graphiques
# ----------------------------------------------------------------------------------------------------------------------
def resize_image_to_screen(image_path, screen_width, screen_height):
    img = load_image(image_path)
    image_resize(img, screen_width, screen_height)
    texture = load_texture_from_image(img)
    return texture

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Définition des couleurs utilisées dans le jeu (RGBA)
floor_color = (225, 220, 200, 255)
fade_color = (0, 0, 0, 255)
brickwall_color = (180, 175, 160, 255)
red_wall_color = (255, 240, 220, 255)
woodenwall_color = (190, 190, 200, 255)
white_wall_color = (225, 220, 210, 255)
mob_color = (220, 190, 200, 255)
painting_color = (205, 202, 200, 255)
item_color = (205, 202, 210, 200)

# Indices de réfraction des surfaces
floor_refraction = .8
brickwall_refraction = .95
red_wall_refraction = .85
woodenwall_refraction = 1
white_wall_refraction = 0.8
mob_refraction = 1.05
painting_refraction = 0.85
item_refraction = 1.05

# Chargement des modèles 3Ds
none_model = load_model_from_mesh(gen_mesh_cube(0.0, 0.0, 0.0))
woodenwall_model = load_model_from_mesh(gen_mesh_cube(1.0, 1.0, 1.0))
red_wall_model = load_model_from_mesh(gen_mesh_cube(1.0, 1.0, 1.0))
brickwall_model = load_model_from_mesh(gen_mesh_cube(1.0, 1.0, 1.0))
white_wall_model = load_model_from_mesh(gen_mesh_cube(1.0, 1.0, 1.0))
floor_model = load_model_from_mesh(gen_mesh_cube(1.0, 1.0, 1.0))
light_ray_model = load_model_from_mesh(gen_mesh_cylinder(.05, .25, 16))

mob_model1 = load_model_from_mesh(gen_mesh_cube(1.25, 1.25, 0.0))
mob_model2 = load_model_from_mesh(gen_mesh_cube(1.25, 1.5, 0.0))
mob_model3 = load_model_from_mesh(gen_mesh_cube(1.75, 2.0, 0.0))
mob_model4 = load_model_from_mesh(gen_mesh_cube(1, 2, 0.0))
mob_model5 = load_model_from_mesh(gen_mesh_cube(1, 2, 0.0))

painting_north_model1 = load_model_from_mesh(gen_mesh_cube(1.28, 1.7, 0.15))
painting_north_model2 = load_model_from_mesh(gen_mesh_cube(1.5, 1.25, 0.15))
painting_north_model3 = load_model_from_mesh(gen_mesh_cube(1.5, 1.5, 0.15))
painting_north_model4 = load_model_from_mesh(gen_mesh_cube(2, 1.5, 0.15))
painting_north_model5 = load_model_from_mesh(gen_mesh_cube(1.7, 1.25, 0.15))
painting_north_model6 = load_model_from_mesh(gen_mesh_cube(1.5, 1.25, 0.15))

painting_west_model1 = load_model_from_mesh(gen_mesh_cube(0.15, 1.7, 1.28))
painting_west_model2 = load_model_from_mesh(gen_mesh_cube(0.15, 1.25, 1.5))
painting_west_model3 = load_model_from_mesh(gen_mesh_cube(0.15, 1.5, 1.5))
painting_west_model4 = load_model_from_mesh(gen_mesh_cube(0.15, 1.5, 2))
painting_west_model5 = load_model_from_mesh(gen_mesh_cube(0.15, 1.25, 1.7))
painting_west_model6 = load_model_from_mesh(gen_mesh_cube(0.15, 1.25, 1.5))

riffle_gun_2d_model = load_model_from_mesh(gen_mesh_cube(1.5, 1.5, 0.0))
powerup_health_model = load_model_from_mesh(gen_mesh_cube(1.7, 1.7, 0.0))
powerup_speed_model = load_model_from_mesh(gen_mesh_cube(1.7, 1.7, 0.0))
powerup_damage_model = load_model_from_mesh(gen_mesh_cube(1.7, 1.7, 0.0))

# Chargement des textures des modèles
woodenwall_model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/woodenwall.png"))
red_wall_model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/redwall.png"))
brickwall_model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/brickwall.png"))
white_wall_model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/whitewall.png"))
floor_model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/floor.png"))
light_ray_model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/lightray.png"))

mob_model1.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/demon1.png"))
mob_model2.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/demon2.png"))
mob_model3.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/demon3.png"))
mob_model4.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/demon4.png"))
mob_model5.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/demon5.png"))

painting_north_model1.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/painting1.png"))
painting_north_model2.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/painting2.png"))
painting_north_model3.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/painting3.png"))
painting_north_model4.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/painting4.png"))
painting_north_model5.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/painting5.png"))
painting_north_model6.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/painting6.png"))

painting_west_model1.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/painting1.png"))
painting_west_model2.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/painting2.png"))
painting_west_model3.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/painting3.png"))
painting_west_model4.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/painting4.png"))
painting_west_model5.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/painting5.png"))
painting_west_model6.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = load_texture(resource_path("resources/painting6.png"))
# Chargement des textures UI/FX (Interface Utilisateur/Effets Spéciaux)
UI_hotbar_texture = load_texture(resource_path("resources/hotbar.png"))
UI_indicators_texture = load_texture(resource_path("resources/indicators.png"))
UI_slot_texture = load_texture(resource_path("resources/slot_highlight.png"))
UI_crossair_texture = load_texture(resource_path("resources/crossair.png"))
UI_scope_crossair_texture = load_texture(resource_path("resources/scope_crossair.png"))
UI_life_texture = load_texture(resource_path("resources/life.png"))
UI_bullets_texture = load_texture(resource_path("resources/bullets.png"))
UI_base_layer_right = load_texture(resource_path("resources/base_layer_right.png"))
FX_bullet_texture = load_texture(resource_path("resources/bullet.png"))
FX_shadow_texture = resize_image_to_screen(resource_path("resources/shadow.png"), sWidth, sHeight)
menu_background = load_texture(resource_path("resources/menubackground.png"))
menu_logo = load_texture(resource_path("resources/logo.png"))
menu_options = load_texture(resource_path("resources/options.png"))

main_gun_2d_texture = load_texture(resource_path("resources/main_gun_2d_texture.png"))
riffle_gun_2d_texture = load_texture(resource_path("resources/riffle_gun_2d_texture.png"))
riffle_gun_2d_model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = riffle_gun_2d_texture
powerup_health_texture = load_texture(resource_path("resources/powerup_health_texture.png"))
powerup_health_model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = powerup_health_texture
powerup_speed_texture = load_texture(resource_path("resources/powerup_speed_texture.png"))
powerup_speed_model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = powerup_speed_texture
powerup_damage_texture = load_texture(resource_path("resources/powerup_damage_texture.png"))
powerup_damage_model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = powerup_damage_texture

blocks_2d_texture = load_texture(resource_path("resources/blocks_2d_texture.png"))
mobs_2d_texture = load_texture(resource_path("resources/mobs_2d_texture.png"))
empty_slot_texture = load_texture(resource_path("resources/empty_slot_texture.png"))

# Chargement des textures/animations des armes
main_gun_frames = []
riffle_gun_frames = []
for i in [0, 1, 2]: main_gun_frames.append(load_texture(resource_path(f"resources/{i}.png")))
for i in [0, 1, 2, 3, 4, 5]: riffle_gun_frames.append(load_texture(resource_path(f"resources/riffle{i}.png")))
flashlight_texture = load_texture(resource_path("resources/flashlight.png"))


# ----------------------------------------------------------------------------------------------------------------------
# Classes
# ----------------------------------------------------------------------------------------------------------------------
class Player:
    def __init__(self):
        self.is_in_air = False  # Indique si le joueur est en l'air
        self.is_sprinting = False  # Indique si le joueur cours
        self.is_dashing = False  # Indique si le joueur fait un dash
        self.dash_tick = 0  # Le temps pour lequel le joueur dash
        self.block_height = 0  # Indique la hauteur du bloc sur lequel est le joueur (0 = sol)
        self.pos = [0, 0, 0]  # x, y, z : Position actuel du joueur
        self.movements = [0, 0, 0]  # x, z, y : Mouvement actuel du joueur
        self.accels = [0, 0, 0]  # x, z, y : Accélération du joueur
        self.yaw = -40  # Angle horizontal du joueur
        self.roll = 95  # Angle vertical du joueur
        self.v = (0, 0, 0)  # Vecteur normal du joueur
        self.target = (0, 0, 0)  # Position que le joueur regarde
        self.life = 26  # Vies du joueur
        self.shield = get_fps()  # Bouclier du joueur (durée)
        self.speed = 1.0  # Coefficient de vitesse
        self.resistance = 1.0  # Coefficient de resistance
        self.dmg = 0.0 # Stock le boost de dégat des armes
    
    def is_colliding(self):
        """Vérifie si le joueur est en collision avec un bloc."""
        global artificial_heigh
        x = camera.position.x
        y = camera.position.y
        z = camera.position.z
        for f1 in [-.35, .35]:
            for f2 in [-.35, .35]:
                for f3 in [-.35, .35]:
                    if (round(x + f1), round(y + f2 - .3), round(z + f3)) in blocks or \
                            (round(x + f1), round(y + f2 - 1), round(z + f3)) in blocks:
                        return True
        return False

    def update_movement(self):
        """Gère le déplacement et la gravité du joueur."""
        global friction
        friction = 1.1 + 12 / FPS * (get_fps() / FPS) + (-0.125 if player.is_dashing else 0)
        for k, i, m in [(KEY_W, 0, 1), (KEY_S, 0, -1), (KEY_D, 1, 1), (KEY_A, 1, -1)]:
            if is_key_down(k):
                self.accels[i] = (self.accels[i] + m * speed / 100) / friction
                if self.is_sprinting: self.accels[i] *= 1.2
                if self.is_in_air: self.accels[i] /= 1.1
        for i in [0, 1]:
            self.movements[i] = (self.movements[i] + self.accels[i]) / friction
            self.accels[i] /= friction

        # Gestion de la gravité et de la position verticale
        a = (self.movements[2] + self.accels[2] - gravity / 60) / friction
        if camera.position.y + a > artificial_heigh + self.block_height:
            self.is_in_air = True
            self.movements[2] = a
        else:
            self.accels[2] = 0
            self.movements[2] = artificial_heigh + self.block_height - camera.position.y
            self.is_in_air = False
        self.accels[2] /= 1 + (friction - 1) / 4

    def update(self):
        """Met à jour les entrées clavier et applique les mouvements."""
        self.update_movement()
        # gère le stockage de l'orientation de la caméra
        self.yaw += get_mouse_delta().x * 0.45 * rW
        if self.roll <= 185 and self.roll >= 5: self.roll += get_mouse_delta().y * 0.45 * rH
        if self.roll > 185: self.roll = 185
        if self.roll < 5: self.roll = 5
        self.v = (math.sin(self.yaw * DEG2RAD), math.cos(self.roll * DEG2RAD), -math.cos(self.yaw * DEG2RAD))
        camera.fovy += zoom * 70
        camera.fovy = min(160, max(60, camera.fovy))
        # gère les hitboxes et la mise à jour de la caméra
        z, x, y = self.movements
        update_camera_pro(camera, (0, 0, 0), (get_mouse_delta().x * 0.45 * rW, get_mouse_delta().y * 0.45 * rH, 0),
                          zoom / 4)
        update_camera_pro(camera, (z * self.speed, 0, 0), (0, 0, 0), 0)
        if self.is_colliding():
            update_camera_pro(camera, (-z * self.speed, 0, 0), (0, 0, 0), 0)
            self.movements[0] = 0
        update_camera_pro(camera, (0, x * self.speed, 0), (0, 0, 0), 0)
        if self.is_colliding():
            update_camera_pro(camera, (0, -x * self.speed, 0), (0, 0, 0), 0)
            self.movements[1] = 0
        update_camera_pro(camera, (0, 0, y + y_player_offset / 2), (0, 0, 0), 0)
        if self.is_colliding():
            if self.movements[2] < 0:
                self.is_in_air = False
            else:
                self.accels[2] = .02
            self.movements[2] = 0
            update_camera_pro(camera, (0, 0, -y - y_player_offset / 2), (0, 0, 0), 0)
        self.pos = [camera.position.x, camera.position.y, camera.position.z]

    def damage(self, dmg):
        global campain
        if self.life <= 0:
            campain.in_menu = True
            campain.in_world = False
        self.life -= dmg / self.resistance


class Wall:
    def __init__(self, pos, orientation, model, color, refraction, height=5, length=5):
        """Construit un mur (en blocs et tableaux) à une position donnée."""
        x, y, z = pos
        flag = True
        if campain.campain_stage == 0:
            xp, yp, zp = player.pos
            if abs(x - xp) > 32 * wall_length or abs(z - zp) > 32 * wall_length:
                flag = False
        if flag:
            if random.random() < 0.6: add_painting = True
            else: add_painting = False
            if orientation == "West": l = [1, height, length]
            else: l = [length, height, 1]

            block_list = []

            for c1 in range(l[0]):
                for c2 in range(l[1]):
                    for c3 in range(l[2]):
                        p = (x + c1, y + c2, z + c3)
                        if campain.campain_stage == 0:
                            if p in blocks:
                                add_painting = False
                                block_list = []
                                break
                        block_list.append(p)
            for p in block_list:
                Block(p, model, color, refraction)

            if campain.campain_stage >= 1: add_painting = False
            if add_painting:
                if orientation == "West":
                    side = random.choice([0, -1])
                    pos = (x + side, y + 1, z + 1)
                    paintings[pos] = random.choice([painting_west_model1, painting_west_model2, painting_west_model3,
                                                    painting_west_model4, painting_west_model5, painting_west_model6])
                else:
                    side = random.choice([0, -1])
                    pos = (x + 1, y + 1, z + side)
                    paintings[pos] = random.choice([painting_north_model1, painting_north_model2, painting_north_model3,
                                                    painting_north_model4, painting_north_model5, painting_north_model6])


class Floor:
    def __init__(self, pos, size_x, size_z, model, color, refraction):
        """Construit une platforme (en blocs) à une position donnée."""
        x, y, z = pos
        sx = size_x // 2
        sz = size_z // 2
        for c1 in range(-sx, sx + size_x % 2):
            for c2 in range(-sz, sz + size_z % 2):
                Block((x + c1, y, z + c2), model, color, refraction)


class Block:
    def __init__(self, pos, model, color, refraction):
        """Initialise un bloc à une position donnée."""
        self.pos = pos
        self.model = model
        self.color = color
        self.refraction = refraction
        self.duration = 6
        blocks[pos] = self

    def damage(self):
        """Gère les dégats faits au bloc."""
        if campain.campain_stage < 1:
            if self.model == white_wall_model: return 0
        else:
            if self.model == white_wall_model or self.model == red_wall_model or self.model == woodenwall_model: return 0
        if self.duration <= 0:
            Item((self.pos), self.model, "Block")
            del blocks[self.pos]
        self.duration -= gun.dmg / 6 * (2 + math.sqrt(mob_strength)) / 2
        c1, c2, c3, a = self.color
        self.color = (min(130 + 10 * self.duration, c1),
                      min(120 + 8 * self.duration, c2),
                      min(110 + 11 * self.duration, c2), a)


class Mob:
    def __init__(self, pos, model, dmg, life, speed):
        """Initialise un ennemi à une position donnée."""
        self.pos = pos
        self.movements = [0, 0, 0]
        self.model = model
        self.color = mob_color
        self.refraction = mob_refraction
        self.yaw = 0  # Angle horizontal du sprite
        self.roll = 180  # Rotation verticale du sprite
        self.dmg = dmg
        self.life = life
        self.initial_life = life
        self.speed = speed
        if campain.campain_stage == 0:
            if len(mobs) < int(2 * mob_strength):
                mobs[pos] = self
        else: mobs[pos] = self
            

    def update_movements(self):
        global mobs
        temp_pos = (round(self.pos[0]), round(self.pos[1]), round(self.pos[2]))
        del mobs[temp_pos]
        new_pos = list(self.pos)
        for i in [0, 1, 2]:
            new_pos[i] += self.movements[i]
        int_pos = (round(new_pos[0]), round(new_pos[1]), round(new_pos[2]))
        if int_pos not in mobs:
            self.pos = tuple(new_pos)
            mobs[int_pos] = self
        else:
            mobs[temp_pos] = self

    def move_forwards(self):
        t_yaw = self.yaw + 180 * DEG2RAD
        vx, vz = (math.sin(t_yaw), math.cos(t_yaw))
        s = mob_strength ** (1 / 3) * 0.3333
        self.movements[0] = self.speed * vx / (get_fps() + 1) * (2 + self.life / self.initial_life) * s
        self.movements[2] = self.speed * vz / (get_fps() + 1) * (2 + self.life / self.initial_life) * s

    def seek_player(self):
        x, y, z = self.pos
        px, py, pz = player.pos
        t_yaw = self.yaw + 180 * DEG2RAD
        vx, vz = (math.sin(t_yaw), math.cos(t_yaw))
        for t in range(0, distance_of_view + 10):
            rx, ry, rz = (x + vx * t, y, z + vz * t)
            intrpos = (round(rx), round(py), round(rz))
            subintrpos = (round(rx), round(py - 1), round(rz))
            if intrpos in blocks or subintrpos in blocks:
                return False
            if intrpos == (round(px), round(py), round(pz)) or \
                    intrpos == (round(px + 0.3), round(py), round(pz + 0.3)) or \
                    intrpos == (round(px - 0.3), round(py), round(pz - 0.3)):
                if (x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2 > 0.5:
                    return True
                else:
                    return False
        return False

    def update(self):
        if self.seek_player():
            self.move_forwards()
        else:
            self.movements = [0, 0, 0]
        self.update_movements()

    def draw_mob(self):
        """Affiche l'ennemi à l'écran en fonction de la position de la caméra."""
        self.update()
        x, y, z = player.pos
        x1, y1, z1 = self.pos
        dx, dz = x1 - x, z1 - z
        self.yaw = vector2_angle((dx, dz), (1, 1)) + 0.75

        if draw_custom(self.pos, self.model, self.color, self.refraction, (0, 1, 0), self.yaw):
            if player.shield == 0 and (x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2 < 0.6:
                player.life -= self.dmg * mob_strength ** 2
                player.shield = get_fps() // 2
            draw_shadow_entity(self.pos, 1)

    def damage(self):
        """Gère les dégats infligés au monstre."""
        x, y, z = self.pos
        if self.life <= 0:
            # Drop d'un item aléatoire
            if random.choice([0, 1]) != 0:
                Item((self.pos), self.model, "Mob")
            elif not gun_hotbar[0]:
                if random.choice([0, 1, 2, 3]) != 0:
                    model, tag = random.choice([(powerup_health_model, "Health"),
                                                (powerup_speed_model, "Speed"),
                                                (powerup_damage_model, "Damage")])
                    Item((self.pos), model, tag)  # PowerUps
                else:
                    Item((self.pos), riffle_gun_2d_model, "Riffle")
            else:
                model, tag = random.choice([(powerup_health_model, "Health"),
                                            (powerup_speed_model, "Speed"),
                                            (powerup_damage_model, "Damage")])
                Item((self.pos), model, tag)  # PowerUps
            del mobs[round(x), round(y), round(z)]

        self.life -= gun.dmg / 8 * (1 + 3 * math.sqrt(mob_strength)) / mob_strength
        c1, c2, c3, a = self.color
        self.color = (min(150 + 10 * self.life, c1),
                      min(140 + 8 * self.life, c2),
                      min(140 + 9 * self.life, c2), a)


class Gun:
    def __init__(self, frames, dmg, speed, offset, type):
        self.frames = frames
        self.nb_frames = len(frames)
        self.dmg = dmg + player.dmg
        self.knockback = dmg ** (1 / 3)
        self.speed = speed
        self.offset = offset
        self.type = type
        self.bullets = 14 if type == "main" else 26
        self.tick_after_shoot = 0

    def switch(self):
        """Passe d'une arme à l'autre."""
        global gun
        if gun_hotbar[0]:
            if self.type == "riffle":
                gun = Gun(main_gun_frames, 12, 7, -100, "main")
            elif self.type == "main":
                gun = Gun(riffle_gun_frames, 9, 19, -250, "riffle")
            gun.tick_after_shoot = 1


class Bullet:
    def __init__(self, type, again=1):
        player.target = find_target(player.pos, DEG2RAD * player.yaw, DEG2RAD * player.roll)
        gun.tick_after_shoot = 1
        self.type = type
        self.tick = 0
        self.again = again
        self.c = random.random()  # Constante aléatoire par balle
        self.playerpos = (player.pos[0] + player.movements[0],  # Position du joueur au moment du tire
                          player.pos[1] + player.movements[1], player.pos[2] + player.movements[2])
        # Vecteur de vision du joueur au moment du tire
        self.playerv = (player.v[0], player.v[1] + 0.02, player.v[2])  # 0.02 > 0.0174... = pi/180
        light_ray_model.transform = matrix_rotate_xyz((DEG2RAD * player.roll, 0, DEG2RAD * player.yaw))
        self.model = light_ray_model  # Model transformé en fonction de la caméra du joueur
        bullets.append(self)
        gun.bullets -= 1

    def draw_bullet(self):
        """Animation de la balle tirée."""
        vx, vy, vz = self.playerv
        if (vx, vy, vz) == (0, 0, 0): return 0  # si on tire sur place on ne fait rien
        x, y, z = self.playerpos
        m = 2.25 if self.type == "main" else 1  # Modifications légères en fonction de l'arme
        r = 50 if self.type == "riffle" else 0
        t = (self.tick + m - .75) * math.sqrt(m) / 2
        rx, ry, rz = (x + (vx + (self.c - .5) * r / 400) * t,
                      y - .5 - (self.c / 5 - 0.2) + vy * t + t / 30,
                      z + (vz + (self.c - .5) * r / 400) * t)
        r_pos = (round(rx), round(ry), round(rz))
        if r_pos == player.target:  # Détection si la cible est atteinte
            if r_pos in paintings:
                del paintings[r_pos]
            elif r_pos in blocks:
                blocks[r_pos].damage()
            elif r_pos in mobs:
                mobs[r_pos].damage()

            self.model = none_model  # N'affiche plus la balle une fois la cible atteinte

        draw_model(self.model, (rx, ry, rz), 0.8 * m, (255, 255, 255, 150))
        draw_model(self.model, (rx, ry, rz), 1.0 * m, (200, 170, 150, 100))

    def animate(self):
        """Gère les animations des balles vides."""
        global fade_color
        self.tick += 1
        if self.tick <= get_fps() // 3:
            if self.type == "main": self.draw_main_empty()
            if self.type == "riffle":
                self.draw_riffle_empty()
                if self.tick >= get_fps() // 7 and self.again != 0:
                    _ = Bullet("riffle", self.again - 1)
                    fade_color = (200, 175, 150, 0)
                    player.movements[2] += gun.knockback / 10
                    self.again = 0
        else:
            bullets.remove(self)

    def draw_main_empty(self):
        t = ((self.tick >> 2) << 2) - 3
        y_offset = -300 - 120 * self.c + abs(16 * (t / (get_fps() / 30) - 1))
        x_offset = 70 + int(14 * t) - int(6 * get_mouse_delta().x)
        draw_texture_ex(FX_bullet_texture, (sWidth // 2 + x_offset, sHeight + y_offset), (5 - 3 * self.c) * t, 1.3,
                        (200, 210, 150, 255))

    def draw_riffle_empty(self):
        t = ((self.tick // 3) * 3) + 2
        y_offset = -300 - 50 * self.c + abs((10 + 20 * self.c) * (t / (get_fps() / 60) - (2 + 2 * self.c)) + t)
        x_offset = int(200 + (20 + 10 * self.c) * t) - int(6 * get_mouse_delta().x)
        draw_texture_ex(FX_bullet_texture, (sWidth // 2 + x_offset, sHeight + y_offset), 10 * t + 90, 1.0,
                        (200, 210, 150, 255))


class Item:
    def __init__(self, pos, model, type):
        self.pos = pos
        self.model = model
        self.color = item_color
        self.refraction = item_refraction
        self.tick = random.random()
        self.type = type
        items[pos] = [self]

    def pickup(self):
        global gun_hotbar, pickable_hotbar
        if self.type == "Block":
            pickable_hotbar[0] += 1
        elif self.type == "Mob":
            pickable_hotbar[1] += 1
        elif self.type == "Riffle":
            gun_hotbar[0] = True
        elif self.type == "Health":
            powerups_hotbar[0] = True
        elif self.type == "Speed":
            powerups_hotbar[1] = True
        elif self.type == "Damage":
            powerups_hotbar[2] = True
        else:
            print("unrecognized type")

    def update(self):
        x, y, z = self.pos
        x1, y1, z1 = player.pos
        if (x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2 < 3:
            self.pickup()
            i = items[self.pos].index(self)
            del items[self.pos][i]

        elif y > 1 + 3 / (get_fps() + 1) and (x, round(y - 1), z) not in blocks:
            del items[self.pos]
            new_pos = (x, y - 3 / (get_fps() + 1), z)
            self.pos = new_pos
            if new_pos in items:
                items[new_pos].append(self)
            else:
                items[new_pos] = [self]

    def draw_item(self):
        self.update()
        self.tick += 1 / (get_fps() + 1)
        if self.tick > 3.141592653589 * 2.0: self.tick = 0.0
        pos = (self.pos[0], self.pos[1] + math.sin(self.tick) / 20, self.pos[2])
        draw_custom(pos, self.model, self.color, self.refraction, (0, 1, 0), self.tick, 0.4)


# ----------------------------------------------------------------------------------------------------------------------
# Fonctions utilitaires
# ----------------------------------------------------------------------------------------------------------------------
def draw_custom(pos, model, color, r, axis=(0, 0, 0), rotation_r=0, scale=1):
    """Dessine un objet en tenant compte de la distance à la caméra."""
    x, y, z = player.pos
    x1, y1, z1 = pos
    vx, vy, vz = player.v
    c = (distance_of_view >> 1) - 2
    c2 = min(c, 6)
    x2, y2, z2 = x1 - x - c2 * vx, y1 - y - (c2 / 2) * vy - 1 / (
                gun.tick_after_shoot // 6 + 0.75) + 0.5, z1 - z - c2 * vz
    d2 = math.sqrt(x2 ** 2 + 4 * y2 ** 2 + z2 ** 2)
    if d2 < c + 9 - c2:
        x3, y3, z3 = x1 - x - 2.5 * vx, y1 - y - vy, z1 - z - 2.5 * vz
        d3 = x3 ** 2 + 2 * y3 ** 2 + z3 ** 2
        if d3 < 9: d2 *= d3 / 9
        d = max(3, d2 * 21)
        b = abs(1 - distance_of_view * 9 / d)
        t = d / r
        c1, c2, c3, _ = color
        bc1, bc2, bc3, _ = fade_color
        model.transform = matrix_rotate(axis, rotation_r)
        draw_model(model, pos, scale,
                   (min(255, int(max(bc1 * b, c1 - t ** 1.05 * 0.8))),
                    min(255, int(max(bc2 * b, c2 - t ** 1.04 * 0.85))),
                    min(255, int(max(bc3 * b, c3 - t ** 1.06 * 0.9))), 255))
        return True  # l'objet a été dessiné
    else:
        return False  # l'objet n'a pas été dessiné


def build_map():
    """Construit et affiche la carte du jeu."""
    x, y, z = camera.position.x, camera.position.y, camera.position.z
    for c1 in range_view:
        for c2 in range_view:
            draw_custom((int(x) + c1, 0, int(z) + c2), floor_model, floor_color, floor_refraction)

    for pos in blocks:
        x1, y1, z1 = pos
        if abs(x - x1) < distance_of_view and \
                abs(y - y1) < distance_of_view and \
                abs(z - z1) < distance_of_view:  # Si l'objet est suffisemment proche du joueur
            b = blocks[pos]
            draw_custom(pos, b.model, b.color, b.refraction)

    if danger_mod:
        mobs_copy = mobs.copy()  # Copy pour éviter les erreurs de pointeurs (del ..)
        for pos in mobs_copy:
            x1, y1, z1 = pos
            if abs(x - x1) < distance_of_view and \
                    abs(y - y1) < distance_of_view and \
                    abs(z - z1) < distance_of_view:  # Si l'objet est suffisemment proche du joueur
                mobs_copy[pos].draw_mob()

    items_copy = items.copy()  # Copy pour éviter les erreurs de pointeurs (del ..)
    for pos in items_copy:
        x1, y1, z1 = pos
        if abs(x - x1) < distance_of_view and \
                abs(y - y1) < distance_of_view and \
                abs(z - z1) < distance_of_view:  # Si l'objet est suffisemment proche du joueur
            for item in items_copy[pos]:
                item.draw_item()

    for pos in paintings:
        new_pos = list(map(lambda x: x + 0.475, pos))  # Ajuste la position pour coller le tableau contre le mur
        draw_custom(new_pos, paintings[pos], painting_color, painting_refraction)


def draw_shadow_entity(pos, radius):
    x, y, z = player.pos
    x1, y1, z1 = pos
    vx = (vector3_angle((x - x1, y - y1, z - z1), (1, 0, 0)) - 1.5707963268) / 2
    vy = (vector3_angle((x - x1, y - y1, z - z1), (0, 1, 0)) - 1.5707963268) / 2
    vz = (vector3_angle((x - x1, y - y1, z - z1), (0, 0, 1)) - 1.5707963268) / 2
    draw_cylinder_ex((x1 + y1 * vx, 0.51, z1 + y1 * vz), (x1 + y1 * vx, 1 + vy, z1 + y1 * vz), radius, 0, 10,
                     (0, 0, 0, 173))


def find_target(pos, yaw_rad, roll_rad):
    x, y, z = pos
    vx, vy, vz = (math.sin(yaw_rad), math.cos(roll_rad), -math.cos(yaw_rad))
    rangex = [-2.25, -1.5, -0.75, 0, 0.75, 1.5, 2.25]
    rangey = [-0.75, 0, 0.75]
    for t in range(-1, 2 * distance_of_view + 2):
        rx, ry, rz = (x + vx * t / 2, y + vy * t / 2, z + vz * t / 2)
        intrpos = (round(rx), round(ry), round(rz))
        if intrpos in mobs or intrpos in blocks:
            return intrpos
    for t in range(1, 2 * distance_of_view):
        rx, ry, rz = (x + vx * t / 2, y + vy * t / 2, z + vz * t / 2)
        vx2 = (vx + 1) / 2
        vz2 = (vz + 1) / 2
        for i in rangex:
            for j in rangey:
                if i != 0 or j != 0:
                    intrpos = (round(rx + i * vz2), round(ry + j), round(rz + i * vx2))
                    if intrpos in mobs:
                        return (round(rx), round(ry), round(rz))
    return intrpos


def reset_map():
    blocks.clear()
    mobs.clear()
    mob_sizes.clear()
    paintings.clear()
    items.clear()
    bullets.clear()
    player.pos = [0, 0, 0]
    camera.position = (1.0, 2.0, 1.0)
    camera.target = (0.0, 2.0, 0.0)
    camera.up = (0.0, 1.0, 0.0)
    player.yaw = -40
    player.roll = 90
    player.v = [0, 0, 0]

def resume():
    set_mouse_position(0, 0)
    campain.in_menu = not campain.in_menu
    campain.in_world = not campain.in_world
    campain.first_time = False


def switch_stage(new_stage):
    reset_map()
    campain.switching_stage = True
    campain.campain_stage = new_stage
    resume()
# ----------------------------------------------------------------------------------------------------------------------
# Initialisation de la caméra
# ----------------------------------------------------------------------------------------------------------------------
camera = Camera3D()  # Création de la caméra
camera.position = (1.0, 2.0, 1.0)
camera.target = (0.0, 2.0, 0.0)
camera.up = (0.0, 1.0, 0.0)
camera.fovy = FoV
camera.projection = CameraProjection.CAMERA_PERSPECTIVE
cameraMode = CameraMode.CAMERA_CUSTOM
zoom = .2  # Variable active qui reste à 0 si aucun zoom n'est appliqué ou varie de -1 à 1 suivant l'intensité
player = Player()
# ----------------------------------------------------------------------------------------------------------------------
# Initialisation du monde et des dictionnaires
# ----------------------------------------------------------------------------------------------------------------------
blocks = {}  # Dictionnaire des blocs
mobs = {}  # Dictionnaire des ennemis
mob_sizes = []  # Liste des tailles des monstres du jeu pour leur hitbox
paintings = {}  # Dictionnaire des tableaux
items = {}  # Dictionnaire des items présents en jeu
bullets = []  # Liste éphémère des balles vides
wall_length = 5  # Longueur des murs
wall_height = 5  # Hauteur des murs
gun = Gun(main_gun_frames, 12, 7, -100, "main")  # Initialisation de larmes sinon ca marche pas je pleure des LARMES
gun_hotbar = [False, True]  # Etat par défaut des armes
pickable_hotbar = [0, 0]  # Etat par défaut du nombres de blocs et monstres collectés
powerups_hotbar = [False, False, False]  # Etat par défaut des PowerUps
# ----------------------------------------------------------------------------------------------------------------------
