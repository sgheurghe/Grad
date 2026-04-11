import time
import pgzrun
import random
import math
import pygame

WIDTH = 1400
HEIGHT = 750
mode = 'menu'

TITLE = "Blocky Adventures"
FPS = 90

def draw():
    screen.fill((135, 206, 235))
    DIMENSIONTIME.draw()

    Character.draw()

    for fireball in fireballs:
        fireball.draw()

    for enemy_fireball in enemy_fireballs:
        enemy_fireball.draw()

    for enemy in enemies:
        enemy.actor.draw()
        enemy.draw_health_bar()
        enemy.draw_name()
    
    for mud in mud_splashes:
        mud.draw()
    
    for husker_fireball in husker_fireballs:
        husker_fireball.draw()
    
    for chain in specter_chains:
        chain.draw()

    for magma_bullet in magma_bullets:
        magma_bullet.draw()

    for magma_meteor in magma_meteors:
        magma_meteor.draw()

    for magma_puddle in magma_puddles:
        magma_puddle.draw()

    for burn_trace in burn_traces:
        burn_trace.draw()

    for weaver_puddle in weaver_puddles:
        weaver_puddle.draw()

    for stalker_fist in stalker_fists:
        stalker_fist.draw()

    for stalker_echo in stalker_echoes:
        stalker_echo.draw()

    for bullet in entropy_bullets:
        bullet.draw()

    if message:
        screen.draw.text(message, center=(WIDTH//2, 30), color="white", fontsize=40)

    if mode == 'game':
        mouse_pos = pygame.mouse.get_pos()
        if fireball_button_rect.collidepoint(mouse_pos):
            screen.draw.filled_rect(fireball_button_rect, fireball_button_hover_color)
        else:
            screen.draw.filled_rect(fireball_button_rect, fireball_button_color)
        screen.draw.text(fireball_button_text, center=fireball_button_rect.center, fontsize=25, color="white")
        
        if jump_ability_button_rect.collidepoint(mouse_pos):
            screen.draw.filled_rect(jump_ability_button_rect, jump_ability_button_hover_color)
        else:
            screen.draw.filled_rect(jump_ability_button_rect, jump_ability_button_color)
        screen.draw.text(jump_ability_button_text, center=jump_ability_button_rect.center, fontsize=25, color="white")
        
        screen.draw.text(f"Health: {Character.health}", (WIDTH // 2, 50), color="green", fontsize=25)

    
    if entropy_blur_timer > 0:
        
        line_spacing = 8
        for offset in range(0, WIDTH + HEIGHT, line_spacing):
            screen.draw.line((offset, 0), (offset - HEIGHT, HEIGHT), (150, 150, 150))
            screen.draw.line((offset + line_spacing//2, 0), (offset + line_spacing//2 - HEIGHT, HEIGHT), (100, 100, 100))
    if entropy_flash_timer > 0:
        screen.draw.filled_rect(pygame.Rect(0, 0, WIDTH, HEIGHT), (150, 150, 150))

    
    if game_completed:
        screen.draw.text("GAME COMPLETED!", center=(WIDTH//2, HEIGHT//2), color="green", fontsize=60)

    if mode == 'menu':
        screen.draw.text("Space to Start", center=(WIDTH//2, HEIGHT//2), fontsize=50)


def on_key_down(key):
    global DIMENSION, DIMENSIONTIME, current_bg_index, boost_timer, boost_cooldown_timer
    if key == keys.K_1:
        DIMENSION = 'Grasslands'
        current_bg_index = 0
        DIMENSIONTIME.image = f"{DIMENSION.lower()}{current_bg_index + 1}"
    elif key == keys.K_2:
        DIMENSION = 'Underworld'
        current_bg_index = 0
        DIMENSIONTIME.image = f"{DIMENSION.lower()}{current_bg_index + 1}"
    elif key == keys.K_3:
        DIMENSION = 'Inverse'
        current_bg_index = 0
        DIMENSIONTIME.image = f"{DIMENSION.lower()}{current_bg_index + 1}"
    elif key == keys.K.G:
        DIMENSION = 'Grasslands'
        current_bg_index = 0
        DIMENSIONTIME.image = f"{DIMENSION.lower()}{current_bg_index + 1}"
        spawn_x, spawn_y = find_spawn_position(DIMENSION, current_bg_index)
        Character.x = spawn_x
        Character.y = spawn_y
        Character.vx = 0
        Character.vy = 0
        Character.on_ground = True
        enemies.clear()
        weaver_puddles.clear()
        stalker_fists.clear()
        stalker_echoes.clear()
        entropy_bullets.clear()
        if hasattr(update, 'level_spawned'):
            delattr(update, 'level_spawned')
    elif key == keys.K.U:
        DIMENSION = 'Underworld'
        current_bg_index = 0
        DIMENSIONTIME.image = f"{DIMENSION.lower()}{current_bg_index + 1}"
        spawn_x, spawn_y = find_spawn_position(DIMENSION, current_bg_index)
        Character.x = spawn_x
        Character.y = spawn_y
        Character.vx = 0
        Character.vy = 0
        Character.on_ground = True
        enemies.clear()
        weaver_puddles.clear()
        stalker_fists.clear()
        stalker_echoes.clear()
        entropy_bullets.clear()
        if hasattr(update, 'level_spawned'):
            delattr(update, 'level_spawned')
    elif key == keys.K.I:
        DIMENSION = 'Inverse'
        current_bg_index = 0
        DIMENSIONTIME.image = f"{DIMENSION.lower()}{current_bg_index + 1}"
        spawn_x, spawn_y = find_spawn_position(DIMENSION, current_bg_index)
        Character.x = spawn_x
        Character.y = spawn_y
        Character.vx = 0
        Character.vy = 0
        Character.on_ground = True
        enemies.clear()
        weaver_puddles.clear()
        stalker_fists.clear()
        stalker_echoes.clear()
        entropy_bullets.clear()
        if hasattr(update, 'level_spawned'):
            delattr(update, 'level_spawned')
    elif key == keys.K:
        progress_to_previous_level()
    elif key == keys.L:
        progress_to_next_level()
    elif key == keys.E:
        
        if Character.on_ground and boost_cooldown_timer <= 0:
            Character.vy = -15  
            Character.on_ground = False
            Character.image = "jumpadventurer"
            boost_timer = 0.3  
            boost_cooldown_timer = 2.0  
    elif key == keys.F:
        shoot_fireball()

    if key in (keys.LEFT, keys.RIGHT, keys.UP, keys.DOWN, keys.A, keys.D, keys.W, keys.S, keys.SPACE):
        teleport_stalker_on_move(key)

Character = Actor("adventurer")
Character.pos = (WIDTH // 2, HEIGHT // 2)
Character.vx = 0 
Character.vy = 0  
Character.on_ground = False
Character.facing = 1
Character.health = 100
Character.max_health = 100
Character.burn_timer = 0
Character.burn_tick_timer = 0
Character.freeze_timer = 0  

backgrounds = {
    "Grasslands": [Actor("grasslands1"),
                   Actor("grasslands2"),
                   Actor("grasslands3")],

    "Underworld": [Actor("underworld1"),
                    Actor("underworld2"),
                    Actor("underworld3")],

    "Inverse":  [Actor("inverse1"),
                Actor("inverse2"),
                Actor("inverse3")]
}

collisions = {
    "Grasslands": [
        [  
            pygame.Rect(0, HEIGHT - 50, WIDTH - 300, 100),
            pygame.Rect(0, HEIGHT - 20, WIDTH, 100),
            pygame.Rect(1335, HEIGHT - 50, WIDTH - 300, 100)
        ],
        [  
            pygame.Rect(0, HEIGHT - 58, WIDTH, 100),
            pygame.Rect(1320, HEIGHT - 70, WIDTH - 300, 100),
            pygame.Rect(1335, HEIGHT - 80, WIDTH - 300, 100),
            pygame.Rect(1340, HEIGHT - 90, WIDTH - 300, 100)
        ],
        [  
            pygame.Rect(0, HEIGHT - 50, WIDTH, 100),
            pygame.Rect(70, HEIGHT - 70, 300, 100),
            pygame.Rect(0, HEIGHT - 150, 235, 100),
            pygame.Rect(WIDTH - 320, HEIGHT - 70, 300, 100),
            pygame.Rect(WIDTH - 200, HEIGHT - 150, 235, 100),
        ]
    ],
    "Underworld": [
        [  
            pygame.Rect(0, HEIGHT - 50, WIDTH - 300, 100),
            pygame.Rect(0, HEIGHT - 20, WIDTH, 100),
            pygame.Rect(1335, HEIGHT - 50, WIDTH - 300, 100)
        ],
         [  
            pygame.Rect(4, 361, 332, 22),
            pygame.Rect(348, 404, 66, 19),
            pygame.Rect(387, 438, 319, 22),
            pygame.Rect(625, 460, 33, 196),
            pygame.Rect(710, 400, 73, 26),
            pygame.Rect(714, 431, 34, 238),
            pygame.Rect(793, 400, 34, 268),
            pygame.Rect(1016, 437, 36, 238),
            pygame.Rect(675, 300, 234, 17),
            pygame.Rect(917, 280, 59, 10),
            pygame.Rect(1203, 358, 194, 17),
            pygame.Rect(439, 232, 249, 9),
            pygame.Rect(751, 146, 243, 10),
            pygame.Rect(1020, 149, 60, 11),
            pygame.Rect(1070, 225, 308, 19),
            pygame.Rect(0, 662, 1401, 89),
    

        ],
        [  
            pygame.Rect(1, 354, 277, 34),
            pygame.Rect(282, 372, 53, 30),
            pygame.Rect(342, 393, 35, 27),
            pygame.Rect(384, 421, 318, 41),
            pygame.Rect(794, 501, 186, 28),
            pygame.Rect(985, 467, 36, 31),
            pygame.Rect(1027, 438, 39, 32),
            pygame.Rect(1067, 412, 50, 25),
            pygame.Rect(1123, 388, 35, 28),
            pygame.Rect(1162, 376, 27, 20),
            pygame.Rect(1198, 358, 203, 24),
            pygame.Rect(443, 227, 529, 28),
            pygame.Rect(1059, 227, 313, 28),
            pygame.Rect(23, 651, 48, 8),
            pygame.Rect(118, 656, 38, 56), 
            pygame.Rect(184, 661, 398, 86), 
            pygame.Rect(753, 652, 138, 94), 
            pygame.Rect(1037, 666, 202, 81), 
            pygame.Rect(1237, 663, 115, 18), 
            pygame.Rect(1387, 661, 15, 15), 
            pygame.Rect(92, 612, 24, 140),
            pygame.Rect(162, 639, 24, 111),
            pygame.Rect(1, 631, 19, 118),
            pygame.Rect(653, 633, 21, 36),
            pygame.Rect(675, 645, 21, 23),
            pygame.Rect(708, 642, 9, 38),
            pygame.Rect(724, 668, 10, 29),
            pygame.Rect(736, 668, 21, 14),
            pygame.Rect(757, 666, 11, 26),
            pygame.Rect(608, 653, 27, 40),
            pygame.Rect(636, 652, 18, 7),
            pygame.Rect(946, 598, 33, 146),
            pygame.Rect(1246, 691, 22, 55),
            pygame.Rect(1357, 642, 25, 108),
            pygame.Rect(1314, 710, 17, 35),
        ]
    ],
    "Inverse": [
        [  
            pygame.Rect(23, 669, 1379, 14),
            pygame.Rect(2, 361, 272, 13),
            pygame.Rect(286, 363, 36, 7),
            pygame.Rect(314, 381, 50, 9),
            pygame.Rect(362, 408, 27, 7),
            pygame.Rect(396, 418, 21, 9),
            pygame.Rect(423, 430, 230, 10),
            pygame.Rect(667, 416, 26, 7),
            pygame.Rect(697, 407, 19, 6),
            pygame.Rect(721, 391, 28, 10),
            pygame.Rect(751, 380, 19, 8),
            pygame.Rect(799, 386, 24, 10),
            pygame.Rect(808, 511, 122, 10),
            pygame.Rect(944, 508, 26, 8),
            pygame.Rect(978, 495, 20, 7),
            pygame.Rect(1003, 481, 30, 8),
            pygame.Rect(1039, 460, 35, 10),
            pygame.Rect(454, 228, 239, 14),
            pygame.Rect(765, 146, 235, 13),
            pygame.Rect(1028, 147, 63, 24),
            pygame.Rect(1070, 227, 159, 12),
            pygame.Rect(929, 275, 47, 11),
            pygame.Rect(1217, 355, 182, 13),
        ],
        [
            
            pygame.Rect(127, 620, 1275, 37),
            pygame.Rect(-3, 619, 131, 39),
        ],
        [
            
            pygame.Rect(583, 511, 9, 67),
            pygame.Rect(799, 599, 11, 33),
            pygame.Rect(944, 612, 21, 76),
            pygame.Rect(943, 686, 22, 64),
            pygame.Rect(801, 630, 9, 120),
            pygame.Rect(584, 577, 12, 168),
            pygame.Rect(1112, 632, 285, 20),
            pygame.Rect(133, 632, 349, 25),
            pygame.Rect(525, 736, 593, 52) 
        ]
    ]
}

lava_collisions = {
    "Grasslands": [
        [],  
        [],  
        []   
    ],
    "Underworld": [
        [],  
        [    
            pygame.Rect(0, 662, 1401, 89)
        ],
        [    
            pygame.Rect(118, 656, 38, 56),
            pygame.Rect(184, 661, 398, 86),
            pygame.Rect(753, 652, 138, 94),
            pygame.Rect(1037, 666, 202, 81),
            pygame.Rect(1237, 663, 115, 18),
            pygame.Rect(1387, 661, 15, 15)
        ]
    ],
    "Inverse": [
        [],  
        [],  
        [    
            pygame.Rect(525, 736, 593, 52)
        ]
    ]
}

mobs = {}
bosses = {}

fireballs = []
enemy_fireballs = []
husker_fireballs = []
specter_chains = []
burn_traces = []
magma_bullets = []
magma_meteors = []
magma_puddles = []
weaver_puddles = []
stalker_fists = []
stalker_echoes = []
player_position_history = []
enemies = []
mud_splashes = []
entropy_bullets = []

cooldown_timer = 0.0
shooting_timer = 0.0
boost_timer = 0.0
boost_cooldown_timer = 4.0
elapsed_time = 0.0

entropy_blur_timer = 0.0
entropy_flash_timer = 0.0
controls_reversed = False
game_completed = False

PLAYER_FIREBALL_DAMAGE = 25
ENEMY_FIREBALL_DAMAGE = 15
CRAWLER_FIREBALL_DAMAGE = 2

HUSKER_FIREBALL_DAMAGE = 8
HUSKER_FIREBALL_COOLDOWN = 2.5
HUSKER_BURN_DAMAGE = 2
HUSKER_BURN_DURATION = 4.0
HUSKER_BURN_TICK_RATE = 0.5  

SPECTER_DASH_DAMAGE = 12
SPECTER_CHAIN_DAMAGE = 10
SPECTER_DASH_WARNING = 0.5
SPECTER_DASH_SPEED = 12.0
SPECTER_ACTION_MIN = 2.0
SPECTER_ACTION_MAX = 3.0
SPECTER_CHAIN_FRAME_TIME = 0.08

MAGMA_COLOSSUS_BULLET_DAMAGE = 15
MAGMA_COLOSSUS_METEOR_DAMAGE = 20
MAGMA_COLOSSUS_METEOR_COUNT = 8
MAGMA_COLOSSUS_METEOR_FALL_SPEED = 8.0
MAGMA_COLOSSUS_METEOR_IMPACT_TIME = 0.3
MAGMA_COLOSSUS_PUDDLE_DAMAGE = 3
MAGMA_COLOSSUS_PUDDLE_DURATION = 6.0
MAGMA_COLOSSUS_PUDDLE_SLOWDOWN = 0.4
MAGMA_COLOSSUS_PUDDLE_JUMP_LIMIT = -4
MAGMA_COLOSSUS_METEOR_COOLDOWN = 8.0
MAGMA_COLOSSUS_BULLET_COOLDOWN = 4.0

WEAVER_BULLET_DAMAGE = 18
WEAVER_ATTACK_COOLDOWN = 4.0
WEAVER_PUDDLE_DELAY = 0.7
WEAVER_PUDDLE_DURATION = 1.2
WEAVER_PUDDLE_DAMAGE = 3
WEAVER_PUDDLE_SLOWDOWN = 0.6
WEAVER_PUDDLE_RADIUS = 70

STALKER_HEALTH = 80
STALKER_MAX_SPAWN = 1
STALKER_FIREBALL_DAMAGE = 0
STALKER_FIST_COOLDOWN = 4.0
STALKER_FREEZE_DURATION = 1.0
STALKER_TELEPORT_OFFSET = 120
STALKER_ECHO_HEALTH = 60
STALKER_PAST_POSITION_RADIUS = 50
STALKER_ECHO_RADIUS = 60

LEVEL_SPAWN_CONFIG = {
    "Grasslands": {
        0: {"crawler": 6},
        1: {"crawler": 6, "stone_golem": 2},
        2: {"crawler": 6, "stone_golem": 3, "crimsonpulse": 1}
    },
    "Underworld": {
        0: {"husker": 6},
        1: {"husker": 3, "specter": 2},
        2: {"husker": 4, "specter": 3, "magma_colossus": 1}
    },
    "Inverse": {
        0: {"weaver": 3}, 
        1: {"weaver": 2, "stalker": 2},
        2: {"weaver": 2, "stalker": 3, "entropy": 1}
    }
}

DIMENSION_ORDER = ["Grasslands", "Underworld", "Inverse"]
ENEMY_SPAWN_CONFIG = {
    "crawler": {
        "name": "Crawler",
        "image": "crawler",
        "health": 30,
        "max_spawn": 6,
        "spawn_weight": 6,
        "fireball_image": "crawlerball",
        "fire_rate": 3.0,
        "walk_speed": 2.0,
        "fireball_damage": 10,
        "health_reward": 5
    },
    "stone_golem": {
        "name": "Stone Golem",
        "image": "stonegolem", 
        "health": 100,
        "max_spawn": 3,
        "spawn_weight": 3,
        "fireball_image": "stonegolemrock",
        "fire_rate": 5.0,
        "walk_speed": 1.0,
        "fireball_damage": 20,
        "health_reward": 15
    },
    "crimsonpulse": {
        "name": "The Crimson Pulse",
        "image": "thecrimsonpulse",
        "health": 250,
        "max_spawn": 1,
        "spawn_weight": 1,
        "fireball_image": "crimsonwave",
        "fire_rate": 8.0,
        "walk_speed": 1.0,
        "fireball_damage": 40,
        "health_reward": 100
    },
    "entropy": {
        "name": "Entropy",
        "image": "entropy",
        "health": 300,
        "max_spawn": 1,
        "spawn_weight": 1,
        "fireball_image": "entropybullet",
        "fire_rate": 3.0,
        "walk_speed": 1.0,
        "fireball_damage": 50,
        "health_reward": 200
    },
    "husker": {
        "name": "Husker",
        "image": "huskeridle",
        "health": 50,
        "max_spawn": 10,
        "spawn_weight": 5,
        "fireball_image": "huskerfireball",
        "fire_rate": HUSKER_FIREBALL_COOLDOWN,
        "walk_speed": 0.0,
        "fireball_damage": HUSKER_FIREBALL_DAMAGE,
        "health_reward": 10
    },
    "specter": {
        "name": "Specter",
        "image": "specter",
        "health": 80,
        "max_spawn": 6,
        "spawn_weight": 4,
        "fireball_image": "specterchainright",
        "fire_rate": 0,
        "walk_speed": 0.0,
        "fireball_damage": SPECTER_CHAIN_DAMAGE,
        "health_reward": 15
    },
    "weaver": {
        "name": "Weaver",
        "image": "weaver",
        "health": 60,
        "max_spawn": 3,
        "spawn_weight": 4,
        "fireball_image": "weaverbullet",
        "fire_rate": WEAVER_ATTACK_COOLDOWN,
        "walk_speed": 2.5,
        "fireball_damage": WEAVER_BULLET_DAMAGE,
        "health_reward": 10
    },
    "stalker": {
        "name": "Stalker",
        "image": "stalker",
        "health": STALKER_HEALTH,
        "max_spawn": STALKER_MAX_SPAWN,
        "spawn_weight": 1,
        "fireball_image": "",
        "fire_rate": 0,
        "walk_speed": 0.0,
        "fireball_damage": 0,
        "health_reward": 100
    },
    "magma_colossus": {
        "name": "Magma Colossus",
        "image": "magmacolossus",
        "health": 250,
        "max_spawn": 1,
        "spawn_weight": 1,
        "fireball_image": "magmacolossusbullet",
        "fire_rate": 1.5,
        "walk_speed": 0.0,
        "fireball_damage": 25,
        "health_reward": 100
    }
}

def count_enemies_of_type(enemy_type):
    return sum(1 for enemy in enemies if enemy.enemy_type == enemy_type)


def choose_spawn_type():
    available = [etype for etype, cfg in ENEMY_SPAWN_CONFIG.items() if count_enemies_of_type(etype) < cfg["max_spawn"]]
    if not available:
        return None
    total_weight = sum(ENEMY_SPAWN_CONFIG[etype]["spawn_weight"] for etype in available)
    choice = random.uniform(0, total_weight)
    current = 0
    for etype in available:
        current += ENEMY_SPAWN_CONFIG[etype]["spawn_weight"]
        if choice <= current:
            return etype
    return available[-1]

class Enemy:
    def __init__(self, x, y, enemy_type="crawler"):
        config = ENEMY_SPAWN_CONFIG.get(enemy_type, ENEMY_SPAWN_CONFIG["crawler"])
        self.enemy_type = enemy_type
        self.actor = Actor(config["image"])
        self.actor.pos = (x, y)
        self.health = config["health"]
        self.max_health = config["health"]
        self.shoot_timer = 0
        self.shoot_cooldown = 0
        self.fire_rate = config["fire_rate"]
        self.fireball_image = config["fireball_image"]
        self.fireball_damage = config["fireball_damage"]
        self.strafe_timer = random.uniform(1.0, 3.0)
        self.strafe_direction = random.choice([-1, 1])
        self.strafe_speed = config["walk_speed"]
        self.jump_timer = random.uniform(2.0, 5.0)
        self.vx = 0
        self.vy = 0
        self.on_ground = False  
        self.facing = 1
        self.float_offset_timer = 0  

        if enemy_type == "crimsonpulse":
            self.actor.x = WIDTH // 2
            self.strafe_speed = 0
            self.strafe_timer = float('inf')
            self.jump_timer = float('inf')
            self.vx = 0
            self.vy = 0
            self.on_ground = True
            self.strafe_direction = 0
        elif enemy_type == "entropy":
            self.actor.x = WIDTH // 2
            self.strafe_speed = 0
            self.strafe_timer = float('inf')
            self.jump_timer = float('inf')
            self.vx = 0
            self.vy = 0
            self.on_ground = True
            self.strafe_direction = 0
            self.blur_timer = random.uniform(2.0, 5.0)
            self.teleport_timer = random.uniform(3.0, 5.0)
            self.flash_timer = random.uniform(4.0, 7.0)
        elif enemy_type == "husker":
            self.strafe_speed = 0  
            self.strafe_timer = float('inf')
            self.jump_timer = float('inf')
            self.vx = 0
            self.vy = 0
            self.on_ground = False  
            self.strafe_direction = 0
            self.shoot_cooldown = random.uniform(2.0, 5.0)  
        elif enemy_type == "specter":
            self.strafe_speed = 0
            self.strafe_timer = float('inf')
            self.jump_timer = float('inf')
            self.vx = 0
            self.vy = 0
            self.on_ground = False
            self.strafe_direction = 0
            self.shoot_timer = 0  
            self.action_state = "idle"
            self.current_action = None
            self.action_timer = random.uniform(SPECTER_ACTION_MIN, SPECTER_ACTION_MAX)
            self.warning_timer = 0
            self.dash_timer = 0
            self.dash_direction = 1
            self.throw_frame_index = 0
            self.throw_frame_timer = 0
            self.dash_hit = False
            self.shoot_cooldown = 0
        elif enemy_type == "weaver":
            self.strafe_speed = config["walk_speed"]
            self.strafe_timer = float('inf')
            self.jump_timer = float('inf')
            self.vx = 0
            self.vy = 0
            self.on_ground = False
            self.strafe_direction = 0
            self.shoot_cooldown = random.uniform(1.0, 2.0)
            self.weaver_state = "ready"
            self.weaver_puddle_timer = 0
            self.weaver_puddle_image = "weaverpuddle"
            self.weaver_puddle_duration = WEAVER_PUDDLE_DURATION
        elif enemy_type == "stalker":
            self.strafe_speed = 0
            self.strafe_timer = float('inf')
            self.jump_timer = float('inf')
            self.vx = 0
            self.vy = 0
            self.on_ground = False
            self.strafe_direction = 0
            self.shoot_cooldown = 0
            self.fist_cooldown = STALKER_FIST_COOLDOWN
            self.teleport_count = 0
            self.teleport_history = []
        elif enemy_type == "magma_colossus":
            self.strafe_speed = 0
            self.strafe_timer = float('inf')
            self.jump_timer = float('inf')
            self.vx = 0
            self.vy = 0
            self.on_ground = False
            self.strafe_direction = 0
            self.shoot_timer = 0
            self.meteor_timer = 0
            self.meteor_cooldown = MAGMA_COLOSSUS_METEOR_COOLDOWN
            self.bullet_cooldown = MAGMA_COLOSSUS_BULLET_COOLDOWN
            self.float_offset_timer = 0  
    
    def shoot(self):
        if self.shoot_cooldown <= 0:
            if self.enemy_type == "husker":
                
                husker_fireball = HuskerFireball(self.actor.x, self.actor.y - 20)
                
                
                dx = Character.x - self.actor.x
                dy = Character.y - self.actor.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance > 0:
                    husker_fireball.vx = (dx / distance) * 4
                    husker_fireball.vy = (dy / distance) * 4  
                else:
                    husker_fireball.vx = 4 * self.facing
                    husker_fireball.vy = 0
                
                husker_fireballs.append(husker_fireball)
                
                
            elif self.enemy_type == "specter":
                
                return
            elif self.enemy_type == "weaver":
                if self.weaver_state == "ready" and self.shoot_cooldown <= 0:
                    weaver_puddles.append(WeaverPuddle(Character.x, Character.y))
                    self.weaver_state = "puddle"
                    self.weaver_puddle_timer = 0
                    self.shoot_cooldown = self.fire_rate
                return
            elif self.enemy_type == "stalker":
                return
            elif self.enemy_type == "entropy":
                entropy_bullets.append(EntropyBullet(self.actor.x, self.actor.y))
                self.shoot_cooldown = self.fire_rate
                return
            else:
                
                enemy_fireball = Actor(self.fireball_image)
                enemy_fireball.pos = self.actor.pos
                
                dx = Character.x - self.actor.x
                distance = abs(dx)
                if distance > 0:
                    enemy_fireball.vx = (dx / distance) * 6
                else:
                    enemy_fireball.vx = 6 * self.facing
                enemy_fireballs.append(enemy_fireball)
                self.shoot_cooldown = self.fire_rate

    def throw_fist(self):
        stalker_fists.append(StalkerFist(self.actor.x, self.actor.y, elapsed_time))
        self.fist_cooldown = STALKER_FIST_COOLDOWN

    def update(self, dt):
        if self.enemy_type == "crimsonpulse":
            self.actor.x = WIDTH // 2
            self.vx = 0
            self.vy = 0
            self.on_ground = True
            self.strafe_timer = float('inf')
            self.jump_timer = float('inf')
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= dt
            return

        if self.enemy_type == "entropy":
            self.actor.x = WIDTH // 2
            self.vx = 0
            self.vy = 0
            self.on_ground = True
            self.strafe_timer = float('inf')
            self.jump_timer = float('inf')
            
            self.blur_timer -= dt
            if self.blur_timer <= 0:
                global entropy_blur_timer
                entropy_blur_timer = 2.0
                self.blur_timer = random.uniform(2.0, 5.0)
            
            self.teleport_timer -= dt
            if self.teleport_timer <= 0:
                past_pos = get_player_position_at_time(elapsed_time - 2.0)
                if past_pos:
                    self.actor.x = past_pos[0]
                    self.actor.y = past_pos[1]
                self.teleport_timer = random.uniform(3.0, 5.0)
            
            self.flash_timer -= dt
            if self.flash_timer <= 0:
                global entropy_flash_timer, controls_reversed
                entropy_flash_timer = 0.5
                controls_reversed = not controls_reversed
                self.flash_timer = random.uniform(4.0, 7.0)
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= dt
            return
        
        if self.enemy_type == "husker":
            
            self.vx = 0
            
            
            
            if self.shoot_timer > 0:
                self.shoot_timer -= dt
                if self.shoot_timer <= 0:
                    self.actor.image = "huskeridle"
            
            
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= dt
            
            
            time_scale = TIME_SCALE.get(DIMENSION, 1.0)
            self.vy += GRAVITY * time_scale
            
            
            old_y = self.actor.y
            self.actor.y += self.vy * time_scale
            self.on_ground = False
            for rect in collisions[DIMENSION][current_bg_index]:
                if self.actor.colliderect(rect):
                    if self.vy > 0 and self.actor.bottom > rect.top:  
                        land_on_rect(self.actor, rect)
                        self.vy = 0
                        self.on_ground = True
                    elif self.vy < 0:  
                        self.actor.y = old_y
                        self.vy = 0
                    break
            
            
            if self.actor.y >= GROUND_Y:
                self.actor.y = GROUND_Y
                self.vy = 0
                self.on_ground = True
            return

        if self.enemy_type == "stalker":
            
            self.actor.x = max(0, min(WIDTH, Character.x - Character.facing * STALKER_TELEPORT_OFFSET))
            self.actor.y = max(50, min(HEIGHT - 50, Character.y))
            self.fist_cooldown -= dt
            if self.fist_cooldown <= 0:
                self.throw_fist()
            return

        if self.enemy_type == "specter":
            time_scale = TIME_SCALE.get(DIMENSION, 1.0)
            self.facing = 1 if Character.x >= self.actor.x else -1
            self.dash_direction = self.facing
            
            if self.action_state == "idle":
                self.action_timer -= dt
                if self.action_timer <= 0:
                    self.current_action = random.choice(["dash", "chain"])
                    if self.current_action == "dash":
                        self.action_state = "warning"
                        self.warning_timer = SPECTER_DASH_WARNING
                        self.actor.image = "specterwarning"
                    else:
                        self.action_state = "throwing"
                        self.throw_frame_index = 0
                        self.throw_frame_timer = 0
                        self.actor.image = "specterthrow1"

            elif self.action_state == "warning":
                self.warning_timer -= dt
                if self.warning_timer <= 0:
                    self.action_state = "dashing"
                    self.dash_timer = 0
                    self.vx = self.dash_direction * SPECTER_DASH_SPEED
                    self.actor.image = "specterdash"
                    self.dash_hit = False

            elif self.action_state == "dashing":
                old_x = self.actor.x
                self.actor.x += self.vx * time_scale
                collided = False
                for rect in collisions[DIMENSION][current_bg_index]:
                    if self.actor.colliderect(rect):
                        self.actor.x = old_x
                        collided = True
                        break

                if Character.colliderect(self.actor) and not self.dash_hit:
                    Character.health -= SPECTER_DASH_DAMAGE
                    self.dash_hit = True

                self.dash_timer += dt
                if self.dash_timer >= 0.35 or collided:
                    self.action_state = "throwing"
                    self.throw_frame_index = 0
                    self.throw_frame_timer = 0
                    self.actor.image = "specterthrow1"
                    self.vx = 0

            elif self.action_state == "throwing":
                self.throw_frame_timer += dt
                if self.throw_frame_timer >= SPECTER_CHAIN_FRAME_TIME:
                    self.throw_frame_timer -= SPECTER_CHAIN_FRAME_TIME
                    self.throw_frame_index += 1
                    if self.throw_frame_index < 4:
                        self.actor.image = f"specterthrow{self.throw_frame_index + 1}"
                    else:
                        self.actor.image = "specter"
                        specter_chains.append(SpecterChain(self.actor.x, self.actor.y, self.facing))
                        self.action_state = "idle"
                        self.action_timer = random.uniform(SPECTER_ACTION_MIN, SPECTER_ACTION_MAX)

            
            
            self.float_offset_timer += dt
            
            
            bob_amount = math.sin(self.float_offset_timer * 2) * 15
            self.actor.y = self.actor.y + (bob_amount - (self.vy or 0)) * 0.1
            self.vy = 0  
            self.on_ground = False
            
            
            for hazard_rect in lava_collisions[DIMENSION][current_bg_index]:
                if self.actor.colliderect(hazard_rect):
                    self.actor.y = hazard_rect.top - self.actor.height - 10
                    break
            return

        if self.enemy_type == "weaver":
            time_scale = TIME_SCALE.get(DIMENSION, 1.0)
            self.facing = 1 if Character.x >= self.actor.x else -1

            
            dx = Character.x - self.actor.x
            dy = Character.y - self.actor.y
            distance = math.hypot(dx, dy)
            if distance > 0:
                self.vx = (dx / distance) * self.strafe_speed * time_scale
                self.vy = (dy / distance) * self.strafe_speed * time_scale
            else:
                self.vx = 0
                self.vy = 0

            self.actor.x += self.vx
            self.actor.y += self.vy
            self.actor.x = max(0, min(WIDTH, self.actor.x))
            self.actor.y = max(50, min(HEIGHT - 50, self.actor.y))

            if self.weaver_state == "ready":
                if self.shoot_cooldown <= 0:
                    self.shoot()
            elif self.weaver_state == "puddle":
                self.weaver_puddle_timer += dt
                if self.weaver_puddle_timer >= WEAVER_PUDDLE_DELAY:
                    enemy_fireball = Actor(self.fireball_image)
                    enemy_fireball.pos = self.actor.pos
                    dx = Character.x - self.actor.x
                    dy = Character.y - self.actor.y
                    distance = math.hypot(dx, dy)
                    if distance > 0:
                        enemy_fireball.vx = (dx / distance) * 8
                        enemy_fireball.vy = (dy / distance) * 8
                    else:
                        enemy_fireball.vx = 8 * self.facing
                        enemy_fireball.vy = 0
                    enemy_fireballs.append(enemy_fireball)
                    self.weaver_state = "cooldown"
                    self.weaver_puddle_timer = 0
            elif self.weaver_state == "cooldown":
                if self.shoot_cooldown <= 0:
                    self.weaver_state = "ready"

            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= dt
            return

        if self.enemy_type == "stalker":
            if self.fist_cooldown <= 0:
                self.throw_fist()
            else:
                self.fist_cooldown -= dt
            return

        if self.enemy_type == "magma_colossus":
            time_scale = TIME_SCALE.get(DIMENSION, 1.0)
            
            
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= dt
            if self.meteor_cooldown > 0:
                self.meteor_cooldown -= dt
            
            
            if self.shoot_cooldown <= 0:
                magma_bullets.append(MagmaBullet(self.actor.x, self.actor.y, Character.x, Character.y))
                self.shoot_cooldown = self.bullet_cooldown
            
            
            if self.meteor_cooldown <= 0:
                
                for i in range(MAGMA_COLOSSUS_METEOR_COUNT):
                    meteor_x = random.randint(50, WIDTH - 50)
                    meteor_y = -50  
                    magma_meteors.append(MagmaMeteor(meteor_x, meteor_y))
                self.meteor_cooldown = MAGMA_COLOSSUS_METEOR_COOLDOWN
            
            
            self.vy += GRAVITY * time_scale
            old_y = self.actor.y
            self.actor.y += self.vy * time_scale
            self.on_ground = False
            for rect in collisions[DIMENSION][current_bg_index]:
                if self.actor.colliderect(rect):
                    if self.vy > 0 and self.actor.bottom > rect.top:
                        land_on_rect(self.actor, rect)
                        self.vy = 0
                        self.on_ground = True
                    elif self.vy < 0:
                        self.actor.y = old_y
                        self.vy = 0
                    break
            if self.actor.y >= GROUND_Y:
                self.actor.y = GROUND_Y
                self.vy = 0
                self.on_ground = True
            return

        
        self.strafe_timer -= dt
        if self.strafe_timer <= 0:
            self.strafe_direction = random.choice([-1, 1])
            self.strafe_timer = random.uniform(1.0, 3.0)
        
        self.vx = self.strafe_direction * self.strafe_speed
        
        
        self.jump_timer -= dt
        if self.jump_timer <= 0 and self.on_ground:
            self.vy = JUMP_STRENGTH
            self.on_ground = False
            self.jump_timer = random.uniform(2.0, 5.0)
        
        
        time_scale = TIME_SCALE.get(DIMENSION, 1.0)
        self.vy += GRAVITY * time_scale
        
        
        old_x = self.actor.x
        self.actor.x += self.vx * time_scale
        for rect in collisions[DIMENSION][current_bg_index]:
            if self.actor.colliderect(rect):
                if self.actor.bottom <= rect.top + 5:
                    continue
                self.actor.x = old_x
                self.vx = 0
                break
        
        
        old_y = self.actor.y
        self.actor.y += self.vy * time_scale
        self.on_ground = False
        for rect in collisions[DIMENSION][current_bg_index]:
            if self.actor.colliderect(rect):
                if self.vy > 0 and self.actor.bottom > rect.top:  
                    land_on_rect(self.actor, rect)
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:  
                    self.actor.y = old_y
                    self.vy = 0
                break
        
        
        if self.actor.x < 0:
            self.actor.x = 0
            self.strafe_direction = 1
        elif self.actor.x > WIDTH:
            self.actor.x = WIDTH
            self.strafe_direction = -1
        
        if self.actor.y >= GROUND_Y:
            self.actor.y = GROUND_Y
            self.vy = 0
            self.on_ground = True
        
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
    
    def draw_health_bar(self):
        bar_width = 40
        bar_height = 5
        bar_x = self.actor.x - bar_width // 2
        bar_y = self.actor.y + self.actor.height // 2 + 10
        
        
        pygame.draw.rect(screen.surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen.surface, (0, 255, 0), (bar_x, bar_y, bar_width * health_percentage, bar_height))
        
        
        pygame.draw.rect(screen.surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)
    
    def draw_name(self):
        config = ENEMY_SPAWN_CONFIG.get(self.enemy_type, ENEMY_SPAWN_CONFIG["crawler"])
        name = config["name"]
        name_x = self.actor.x - len(name) * 3  
        name_y = self.actor.y - self.actor.height // 2 - 25
        screen.draw.text(name, center=(self.actor.x, name_y), color="white", fontsize=16)

class MudSplash:
    def __init__(self, x, y):
        self.actor = Actor("crawlermud")
        self.actor.pos = (x, y)
        self.duration = 3.0
        self.timer = 0
        self.radius = 30
    
    def update(self, dt):
        self.timer += dt
    
    def draw(self):
        
        alpha = 1.0 - (self.timer / self.duration)
        self.actor.draw()
    
    def is_active(self):
        return self.timer < self.duration

class HuskerFireball:
    def __init__(self, x, y):
        self.actor = Actor("huskerfireball")
        self.actor.pos = (x, y)
        self.vx = 0  
        self.vy = 0  
        self.timer = 0
        self.max_lifetime = 8.0  
        self.plop_timer = -1  
    
    def update(self, dt):
        
        if self.plop_timer >= 0:
            self.plop_timer += dt
            if self.plop_timer >= 0.2:  
                return True  
            return False  
        
        
        self.vy += GRAVITY * dt
        
        
        self.actor.x += self.vx
        self.actor.y += self.vy
        
        self.timer += dt
        
        
        for rect in collisions[DIMENSION][current_bg_index]:
            if self.actor.colliderect(rect):
                
                self.actor.image = "huskerfireballplop"
                self.plop_timer = 0  
                return False  
        
        
        if self.actor.x < 0 or self.actor.x > WIDTH or self.timer > self.max_lifetime:
            return True  
        
        return False  
    
    def draw(self):
        self.actor.draw()


class SpecterChain:
    def __init__(self, x, y, direction):
        sprite = "specterchainright" if direction >= 0 else "specterchainleft"
        self.actor = Actor(sprite)
        self.actor.pos = (x + (20 * direction), y)
        self.vx = 14 * direction
        self.damage = SPECTER_CHAIN_DAMAGE
        self.travel_distance = 0
        self.max_distance = WIDTH * 1.5

    def update(self, dt):
        self.actor.x += self.vx
        self.travel_distance += abs(self.vx)
        if self.actor.x < 0 or self.actor.x > WIDTH or self.travel_distance >= self.max_distance:
            return True
        return False

    def draw(self):
        self.actor.draw()


class BurnTrace:
    def __init__(self, x, y):
        self.actor = Actor("huskertrace")
        self.actor.pos = (x, y)
        self.duration = HUSKER_BURN_DURATION
        self.timer = 0
        self.tick_timer = 0
        self.radius = 50  
        self.active = True
    
    def update(self, dt):
        self.timer += dt
        self.tick_timer += dt
        
        if self.timer >= self.duration:
            self.active = False
            return False
        
        return True  
    
    def should_tick(self):
        """Check if it's time to apply burn damage"""
        if self.tick_timer >= HUSKER_BURN_TICK_RATE:
            self.tick_timer = 0
            return True
        return False
    
    def draw(self):
        if self.active:
            self.actor.draw()


class MagmaBullet:
    def __init__(self, x, y, target_x, target_y):
        self.actor = Actor("magmacolossusbullet")
        self.actor.pos = (x, y)
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.vx = (dx / distance) * 15  
            self.vy = (dy / distance) * 15
        else:
            self.vx = 15
            self.vy = 0
        self.damage = MAGMA_COLOSSUS_BULLET_DAMAGE

    def update(self, dt):
        self.actor.x += self.vx
        self.actor.y += self.vy
        
        if self.actor.x < 0 or self.actor.x > WIDTH or self.actor.y < 0 or self.actor.y > HEIGHT:
            return True
        return False

    def draw(self):
        self.actor.draw()


class MagmaMeteor:
    def __init__(self, x, y):
        self.actor = Actor("magmacolossusmeteor")
        self.actor.pos = (x, y)
        self.vy = MAGMA_COLOSSUS_METEOR_FALL_SPEED
        self.damage = MAGMA_COLOSSUS_METEOR_DAMAGE
        self.impact_timer = 0
        self.state = "falling"  

    def update(self, dt):
        if self.state == "falling":
            self.actor.y += self.vy
            if self.actor.y >= GROUND_Y - 50:  
                self.state = "impacting"
                self.actor.image = "magmacolossusmeteorimpact"
                self.impact_timer = MAGMA_COLOSSUS_METEOR_IMPACT_TIME
        elif self.state == "impacting":
            self.impact_timer -= dt
            if self.impact_timer <= 0:
                self.state = "done"
                
                magma_puddles.append(MagmaPuddle(self.actor.x, self.actor.y))
                return True
        return False

    def draw(self):
        if self.state != "done":
            self.actor.draw()


class MagmaPuddle:
    def __init__(self, x, y):
        self.actor = Actor("magmacolossusmeteorpuddle")
        self.actor.pos = (x, y)
        self.duration = MAGMA_COLOSSUS_PUDDLE_DURATION
        self.timer = 0
        self.tick_timer = 0
        self.radius = 60  
        self.active = True

    def update(self, dt):
        self.timer += dt
        self.tick_timer += dt
        
        if self.timer >= self.duration:
            self.active = False
            return False
        
        return True  

    def should_tick(self):
        """Check if it's time to apply damage"""
        if self.tick_timer >= 0.5:  
            self.tick_timer = 0
            return True
        return False

    def draw(self):
        if self.active:
            self.actor.draw()


class WeaverPuddle:
    def __init__(self, x, y):
        self.actor = Actor("weaverpuddle")
        self.actor.pos = (x, y)
        self.duration = WEAVER_PUDDLE_DURATION
        self.timer = 0
        self.tick_timer = 0
        self.radius = WEAVER_PUDDLE_RADIUS
        self.active = True

    def update(self, dt):
        self.timer += dt
        self.tick_timer += dt
        if self.timer >= self.duration:
            self.active = False
            return False
        return True

    def should_tick(self):
        if self.tick_timer >= 0.5:
            self.tick_timer = 0
            return True
        return False

    def draw(self):
        if self.active:
            self.actor.draw()


def get_player_position_at_time(target_time):
    closest = None
    closest_diff = float('inf')
    for x, y, t in player_position_history:
        diff = abs(t - target_time)
        if diff < closest_diff:
            closest = (x, y, t)
            closest_diff = diff
    return closest if closest_diff <= 0.5 else None


class StalkerFist:
    def __init__(self, x, y, created_time):
        self.actor = Actor("stalkerfist")
        self.actor.pos = (x, y)
        angle = random.uniform(0, math.pi * 2)
        self.target_x = x + math.cos(angle) * 20
        self.target_y = y + math.sin(angle) * 20
        self.speed = 200
        self.duration = 0.5
        self.timer = 0
        self.target_time = created_time - 1.0
        self.active = True

    def update(self, dt):
        self.timer += dt
        
        dx = self.target_x - self.actor.x
        dy = self.target_y - self.actor.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.actor.x += (dx / dist) * self.speed * dt
            self.actor.y += (dy / dist) * self.speed * dt
        
        past_pos = get_player_position_at_time(self.target_time)
        if past_pos:
            dx = past_pos[0] - self.actor.x
            dy = past_pos[1] - self.actor.y
            if math.hypot(dx, dy) <= STALKER_PAST_POSITION_RADIUS:
                Character.freeze_timer = STALKER_FREEZE_DURATION
        if self.timer >= self.duration:
            self.active = False
            return False
        return True

    def draw(self):
        if self.active:
            self.actor.draw()


class StalkerEcho:
    def __init__(self, x, y, parent):
        self.actor = Actor("stalkerecho")
        self.actor.pos = (x, y)
        self.parent = parent
        self.active = True

    def update(self, dt):
        if not self.active or self.parent not in enemies:
            return False
        return True

    def hit(self, damage):
        if not self.active or self.parent not in enemies:
            self.active = False
            return
        self.parent.health -= damage
        self.active = False
        if self.parent.health <= 0:
            if self.parent in enemies:
                enemies.remove(self.parent)

    def draw(self):
        if self.active:
            self.actor.draw()


class EntropyBullet:
    def __init__(self, boss_x, boss_y):
        self.actor = Actor("entropybullet")
        
        side = random.choice(['left', 'right', 'top', 'bottom'])
        if side == 'left':
            self.actor.x = 0
            self.actor.y = random.randint(0, HEIGHT)
        elif side == 'right':
            self.actor.x = WIDTH
            self.actor.y = random.randint(0, HEIGHT)
        elif side == 'top':
            self.actor.x = random.randint(0, WIDTH)
            self.actor.y = 0
        else:
            self.actor.x = random.randint(0, WIDTH)
            self.actor.y = HEIGHT
        self.target_x = Character.x
        self.target_y = Character.y
        self.phase = 1  
        self.speed = 300
        self.boss_x = boss_x
        self.boss_y = boss_y
        self.active = True

    def update(self, dt):
        if self.phase == 1:
            target_x, target_y = self.target_x, self.target_y
        else:
            target_x, target_y = self.boss_x, self.boss_y
        dx = target_x - self.actor.x
        dy = target_y - self.actor.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.actor.x += (dx / dist) * self.speed * dt
            self.actor.y += (dy / dist) * self.speed * dt
        if dist < 10:  
            if self.phase == 1:
                self.phase = 2
            else:
                self.active = False
                return False
        return True

    def draw(self):
        if self.active:
            self.actor.draw()


current_bg_index = 0
DIMENSION = "Grasslands"
DIMENSIONTIME = Actor("grasslands1")

TIME_SCALE = {
    "Grasslands": 1.0,
    "Underworld": 0.5,
    "Inverse": 1.0
}

message = ""
message_timer = 0.0

fireball_button_rect = pygame.Rect(WIDTH - 1375, 50, 200, 50)
fireball_button_text = "Fireball (F)"
fireball_button_color = (255, 100, 100)
fireball_button_hover_color = (200, 50, 50)

jump_ability_button_rect = pygame.Rect(WIDTH - 1375, 120, 200, 50)
jump_ability_button_text = "Jump Boost (E)"
jump_ability_button_color = (100, 255, 100)
jump_ability_button_hover_color = (50, 200, 50)

def find_spawn_position(dimension, level_index):
    level_rects = collisions[dimension][level_index]
    
    if not level_rects:
        return WIDTH // 2, HEIGHT // 2  
    
    
    
    best_rect = None
    best_score = float('inf')
    
    for rect in level_rects:
        
        if rect in lava_collisions[dimension][level_index]:
            continue
            
        
        
        height_score = rect.top  
        horizontal_score = rect.left / WIDTH  
        score = height_score + (horizontal_score * 100)  
        
        if score < best_score:
            best_score = score
            best_rect = rect
    
    if best_rect:
        
        spawn_x = best_rect.centerx
        spawn_y = best_rect.top - Character.height // 2 - 5  
        return spawn_x, spawn_y
    else:
        return WIDTH // 2, HEIGHT // 2  

def set_dimension(new_dimension, background_number):
    global DIMENSION, DIMENSIONTIME, current_bg_index
    normalized_dimension = None
    for dim in backgrounds:
        if dim.lower() == str(new_dimension).lower():
            normalized_dimension = dim
            break

    if normalized_dimension and 1 <= background_number <= len(backgrounds[normalized_dimension]):
        DIMENSION = normalized_dimension
        current_bg_index = background_number - 1
        DIMENSIONTIME.image = f"{normalized_dimension.lower()}{current_bg_index + 1}"
    else:
        print(f"Invalid dimension or background number: {new_dimension}, {background_number}")
        current_bg_index = 0
        DIMENSIONTIME.image = f"{DIMENSION.lower()}{current_bg_index + 1}"


def teleport_stalker_on_move(key):
    if mode != 'game' or DIMENSION != 'Inverse':
        return
    for enemy in enemies:
        if enemy.enemy_type == "stalker":
            if key in (keys.LEFT, keys.A):
                offset_x, offset_y = STALKER_TELEPORT_OFFSET, 0
            elif key in (keys.RIGHT, keys.D):
                offset_x, offset_y = -STALKER_TELEPORT_OFFSET, 0
            elif key in (keys.UP, keys.W):
                offset_x, offset_y = 0, STALKER_TELEPORT_OFFSET
            elif key in (keys.DOWN, keys.S):
                offset_x, offset_y = 0, -STALKER_TELEPORT_OFFSET
            else:
                offset_x, offset_y = -Character.facing * STALKER_TELEPORT_OFFSET, 0
            enemy.teleport_count += 1
            enemy.teleport_history.append((enemy.actor.x, enemy.actor.y))
            if len(enemy.teleport_history) > 5:
                enemy.teleport_history = enemy.teleport_history[-5:]
            enemy.actor.x = max(0, min(WIDTH, Character.x + offset_x))
            enemy.actor.y = max(50, min(HEIGHT - 50, Character.y + offset_y))
            if enemy.teleport_count >= 1 and len(enemy.teleport_history) >= 1:
                stalker_echoes[:] = [echo for echo in stalker_echoes if echo.parent is not enemy]
                tx, ty = enemy.teleport_history[-1]
                stalker_echoes.append(StalkerEcho(tx, ty, enemy))
            break

def shoot_fireball():
    global cooldown_timer, shooting_timer
    if cooldown_timer <= 0:
        fireball = Actor("fireball")
        fireball.pos = Character.pos
        direction = Character.facing
        if DIMENSION == 'Inverse':
            direction = -direction
        fireball.vx = 10 * direction
        fireballs.append(fireball)
        cooldown_timer = 0.5
        shooting_timer = 0.2 
        
        if Character.facing == 1:
            Character.image = "rightfireballadventurer"
        else:
            Character.image = "leftfireballadventurer"

GRAVITY = 0.5
JUMP_STRENGTH = -7
SPEED = 3.5
GROUND_Y = HEIGHT - 50

def land_on_rect(actor, rect, reference_height=None):
    """Position actor so it lands on rect with consistent positioning."""
    if reference_height is None:
        reference_height = actor.height // 2
    actor.y = rect.top - reference_height

def spawn_enemies_for_level():
    """Spawn enemies based on current dimension and background index"""
    if DIMENSION not in LEVEL_SPAWN_CONFIG:
        return
    
    level_config = LEVEL_SPAWN_CONFIG[DIMENSION].get(current_bg_index, {})
    
    spawn_positions = [200, 400, 600, 800, 1000, 1200]  
    
    
    platform_rects = [rect for rect in collisions[DIMENSION][current_bg_index] 
                      if rect not in lava_collisions[DIMENSION][current_bg_index]]
    
    enemy_index = 0
    for enemy_type, count in level_config.items():
        for i in range(count):
            if enemy_type == "crimsonpulse":
                spawn_x = WIDTH // 2 + 20
                spawn_y = GROUND_Y - 150
            elif enemy_type == "entropy":
                spawn_x = WIDTH // 2 + 20
                spawn_y = GROUND_Y - 150
            elif enemy_type == "magma_colossus":
                spawn_x = WIDTH // 2
                spawn_y = GROUND_Y - 200  
            elif enemy_index < len(spawn_positions):
                spawn_x = spawn_positions[enemy_index]
                enemy_index += 1
                
                spawn_y = 300
                for rect in platform_rects:
                    if rect.left <= spawn_x <= rect.right:
                        if enemy_type == "specter":
                            spawn_y = rect.top - 120  
                        else:
                            spawn_y = rect.top - 40   
                        break
            else:
                spawn_x = random.choice([100, WIDTH - 100])
                spawn_y = 300
                for rect in platform_rects:
                    if rect.left <= spawn_x <= rect.right:
                        if enemy_type == "specter":
                            spawn_y = rect.top - 120
                        else:
                            spawn_y = rect.top - 40
                        break
            
            new_enemy = Enemy(spawn_x, spawn_y, enemy_type)
            enemies.append(new_enemy)

def progress_to_next_level():
    global DIMENSION, current_bg_index, mode, DIMENSIONTIME
    
    
    if DIMENSION in LEVEL_SPAWN_CONFIG:
        max_level = max(LEVEL_SPAWN_CONFIG[DIMENSION].keys())
        if current_bg_index >= max_level:
            
            current_dim_index = DIMENSION_ORDER.index(DIMENSION)
            if current_dim_index + 1 < len(DIMENSION_ORDER):
                DIMENSION = DIMENSION_ORDER[current_dim_index + 1]
                current_bg_index = 0
                message_text = f"ENTERING {DIMENSION.upper()}"
            else:
                
                global game_completed
                game_completed = True
                message_text = "GAME COMPLETED!"
                mode = 'menu'  
        else:
            
            current_bg_index += 1
            message_text = f"{DIMENSION.upper()} {current_bg_index + 1} - HEALTH RESTORED!"
    else:
        message_text = "LEVEL COMPLETE"
    
    DIMENSIONTIME.image = f"{DIMENSION.lower()}{current_bg_index + 1}"
    enemies.clear()
    fireballs.clear()
    enemy_fireballs.clear()
    husker_fireballs.clear()
    specter_chains.clear()
    magma_bullets.clear()
    magma_meteors.clear()
    magma_puddles.clear()
    weaver_puddles.clear()
    stalker_fists.clear()
    stalker_echoes.clear()
    mud_splashes.clear()
    burn_traces.clear()
    if hasattr(update, 'level_spawned'):
        delattr(update, 'level_spawned')

    
    spawn_x, spawn_y = find_spawn_position(DIMENSION, current_bg_index)
    Character.x = spawn_x
    Character.y = spawn_y
    Character.vx = 0
    Character.vy = 0
    Character.on_ground = True

    
    Character.health = Character.max_health
    Character.burn_timer = 0  

    spawn_enemies_for_level()
    update.level_spawned = True
    
    
    global message, message_timer
    message = message_text
    message_timer = 3.0


def progress_to_previous_level():
    global DIMENSION, current_bg_index, mode, DIMENSIONTIME

    if DIMENSION in LEVEL_SPAWN_CONFIG:
        if current_bg_index <= 0:
            current_dim_index = DIMENSION_ORDER.index(DIMENSION)
            if current_dim_index > 0:
                DIMENSION = DIMENSION_ORDER[current_dim_index - 1]
                current_bg_index = max(LEVEL_SPAWN_CONFIG[DIMENSION].keys())
                message_text = f"RETURNING TO {DIMENSION.upper()} {current_bg_index + 1}"
            else:
                message_text = "ALREADY AT FIRST LEVEL"
        else:
            current_bg_index -= 1
            message_text = f"{DIMENSION.upper()} {current_bg_index + 1} - HEALTH RESTORED!"
    else:
        message_text = "LEVEL COMPLETE"

    DIMENSIONTIME.image = f"{DIMENSION.lower()}{current_bg_index + 1}"
    enemies.clear()
    fireballs.clear()
    enemy_fireballs.clear()
    husker_fireballs.clear()
    specter_chains.clear()
    magma_bullets.clear()
    magma_meteors.clear()
    magma_puddles.clear()
    weaver_puddles.clear()
    stalker_fists.clear()
    stalker_echoes.clear()
    mud_splashes.clear()
    burn_traces.clear()
    if hasattr(update, 'level_spawned'):
        delattr(update, 'level_spawned')

    spawn_x, spawn_y = find_spawn_position(DIMENSION, current_bg_index)
    Character.x = spawn_x
    Character.y = spawn_y
    Character.vx = 0
    Character.vy = 0
    Character.on_ground = True

    Character.health = Character.max_health
    Character.burn_timer = 0

    spawn_enemies_for_level()
    update.level_spawned = True

    global message, message_timer
    message = message_text
    message_timer = 3.0


def update(dt):
    global mode, cooldown_timer, shooting_timer, boost_timer, boost_cooldown_timer, current_bg_index, DIMENSIONTIME, DIMENSION, elapsed_time

    
    DIMENSIONTIME.image = f"{DIMENSION.lower()}{current_bg_index + 1}"
    
    
    for rect in collisions[DIMENSION][current_bg_index]:
        if Character.colliderect(rect):
            
            Character.y = rect.top - Character.height // 2 - 5
            Character.vy = 0
            Character.on_ground = True
            break
    
    
    for enemy in enemies[:]:
        for hazard_rect in lava_collisions[DIMENSION][current_bg_index]:
            if enemy.actor.colliderect(hazard_rect):
                
                if enemy.enemy_type != "entropy":
                    if enemy in enemies:
                        enemies.remove(enemy)
                break
    
    
    for enemy_fireball in enemy_fireballs[:]:
        for hazard_rect in lava_collisions[DIMENSION][current_bg_index]:
            if enemy_fireball.colliderect(hazard_rect):
                if enemy_fireball in enemy_fireballs:
                    enemy_fireballs.remove(enemy_fireball)
                break
    
    
    for fireball in fireballs[:]:
        for hazard_rect in lava_collisions[DIMENSION][current_bg_index]:
            if fireball.colliderect(hazard_rect):
                if fireball in fireballs:
                    fireballs.remove(fireball)
                break
    
    
    for magma_bullet in magma_bullets[:]:
        for hazard_rect in lava_collisions[DIMENSION][current_bg_index]:
            if magma_bullet.actor.colliderect(hazard_rect):
                if magma_bullet in magma_bullets:
                    magma_bullets.remove(magma_bullet)
                break
    
    
    for magma_meteor in magma_meteors[:]:
        if magma_meteor.state == "falling":
            for hazard_rect in lava_collisions[DIMENSION][current_bg_index]:
                if magma_meteor.actor.colliderect(hazard_rect):
                    if magma_meteor in magma_meteors:
                        magma_meteors.remove(magma_meteor)
                    break
    
    
    if Character.health <= 0:
        mode = 'menu'
    
    if cooldown_timer > 0:
        cooldown_timer -= dt
    if shooting_timer > 0:
        shooting_timer -= dt
        if shooting_timer <= 0:
            if Character.facing == 1:
                Character.image = "adventurer"
            else:
                Character.image = "leftadventurer"
    if boost_timer > 0:
        boost_timer -= dt
        if boost_timer <= 0:
            if Character.facing == 1:
                Character.image = "adventurer"
            else:
                Character.image = "leftadventurer"
    if boost_cooldown_timer > 0:
        boost_cooldown_timer -= dt

    for rect in collisions[DIMENSION][current_bg_index]:
        screen.draw.rect(rect, (255, 0, 0))  

    global message, message_timer

    if mode == 'menu':
        
        if keyboard.space:
            mode = 'game'
            
            DIMENSION = "Grasslands"
            current_bg_index = 0
            DIMENSIONTIME.image = f"{DIMENSION.lower()}{current_bg_index + 1}"
            message = "GRASSLANDS 1"
            message_timer = 1.0
            Character.health = Character.max_health  
            
            spawn_x, spawn_y = find_spawn_position(DIMENSION, current_bg_index)
            Character.x = spawn_x
            Character.y = spawn_y
            Character.vx = 0
            Character.vy = 0
            Character.on_ground = True
            enemies.clear()  
            mud_splashes.clear()  
            husker_fireballs.clear()  
            specter_chains.clear()  
            magma_bullets.clear()  
            magma_meteors.clear()  
            magma_puddles.clear()  
            weaver_puddles.clear()  
            stalker_fists.clear()  
            stalker_echoes.clear()  
            burn_traces.clear()  
            Character.burn_timer = 0  
            
            if hasattr(update, 'level_spawned'):
                delattr(update, 'level_spawned')
        return

    if message_timer > 0:
        message_timer -= dt
        if message_timer <= 0:
            message = ""
            message_timer = 0.0

    Character.vx = 0
    move_left = False
    move_right = False
    if Character.freeze_timer <= 0:
        move_left = keyboard.left or keyboard.a
        move_right = keyboard.right or keyboard.d
        if DIMENSION == 'Inverse':
            move_left, move_right = move_right, move_left

        if controls_reversed:
            move_left, move_right = move_right, move_left

        if move_left:
            Character.vx = -SPEED
            Character.facing = -1
        if move_right:
            Character.vx = SPEED
            Character.facing = 1
    else:
        
        Character.vx = 0
        Character.vy = 0

    
    for mud in mud_splashes:
        if mud.is_active():
            dist = math.sqrt((Character.x - mud.actor.x)**2 + (Character.y - mud.actor.y)**2)
            if dist < mud.radius + 50:  
                Character.vx *= 0.5  

    if (keyboard.up or keyboard.w or keyboard.space) and Character.on_ground:
        Character.vy = JUMP_STRENGTH
        Character.on_ground = False

    time_scale = TIME_SCALE.get(DIMENSION, 1.0)

    Character.vy += GRAVITY * time_scale

    old_x = Character.x
    Character.x += Character.vx * time_scale
    for rect in collisions[DIMENSION][current_bg_index]:
        if Character.colliderect(rect):
            if Character.bottom <= rect.top + 5:
                continue
            Character.x = old_x
            Character.vx = 0
            break

    old_y = Character.y
    Character.y += Character.vy * time_scale
    
    
    for hazard_rect in lava_collisions[DIMENSION][current_bg_index]:
        char_rect = pygame.Rect(Character.x - Character.width//2, Character.y - Character.height//2, Character.width, Character.height)
        if char_rect.colliderect(hazard_rect):
            Character.health = 0
            break
    
    for rect in collisions[DIMENSION][current_bg_index]:
        if Character.colliderect(rect):
            if Character.vy > 0:
                land_on_rect(Character, rect)
                Character.vy = 0
                Character.on_ground = True
            elif Character.vy < 0:
                Character.y = old_y
                Character.vy = 0
            break

    if Character.y >= GROUND_Y:
        Character.y = GROUND_Y
        Character.vy = 0
        Character.on_ground = True

    elapsed_time += dt
    player_position_history.append((Character.x, Character.y, elapsed_time))
    while player_position_history and elapsed_time - player_position_history[0][2] > 5.0:
        player_position_history.pop(0)

    if Character.on_ground and shooting_timer <= 0:
        if move_left:
            Character.image = "leftadventurer"
        elif move_right:
            Character.image = "adventurer"
        else:
            Character.image = "adventurer"
    else:
        if shooting_timer <= 0:
            Character.image = "jumpadventurer"

    if Character.x < 0:
        Character.x = 0
    elif Character.x > WIDTH:
        Character.x = WIDTH

    
    if len(enemies) == 0 and not hasattr(update, 'level_spawned'):
        spawn_enemies_for_level()
        update.level_spawned = True

    for enemy in enemies[:]:
        enemy.update(dt)
        if random.random() < 0.005:
            enemy.shoot()
    
    
    global entropy_blur_timer, entropy_flash_timer
    entropy_blur_timer = max(0, entropy_blur_timer - dt)
    entropy_flash_timer = max(0, entropy_flash_timer - dt)
    
    
    for bullet in entropy_bullets[:]:
        if not bullet.update(dt):
            entropy_bullets.remove(bullet)
    
    
    if len(enemies) == 0 and hasattr(update, 'level_spawned'):
        progress_to_next_level()
    
    for mud in mud_splashes[:]:
        mud.update(dt)
        if not mud.is_active():
            mud_splashes.remove(mud)
    
    
    for husker_fb in husker_fireballs[:]:
        if husker_fb.update(dt):  
            
            burn_trace = BurnTrace(husker_fb.actor.x, husker_fb.actor.y)
            burn_traces.append(burn_trace)
            husker_fireballs.remove(husker_fb)
    
    
    for husker_fb in husker_fireballs[:]:
        for hazard_rect in lava_collisions[DIMENSION][current_bg_index]:
            if husker_fb.actor.colliderect(hazard_rect):
                if husker_fb in husker_fireballs:
                    husker_fireballs.remove(husker_fb)
                break

    
    for chain in specter_chains[:]:
        if Character.colliderect(chain.actor):
            Character.health -= chain.damage
            specter_chains.remove(chain)
            if Character.health <= 0:
                mode = 'menu'
            break

    for chain in specter_chains[:]:
        if chain.update(dt):
            specter_chains.remove(chain)
            continue
        for hazard_rect in lava_collisions[DIMENSION][current_bg_index]:
            if chain.actor.colliderect(hazard_rect):
                if chain in specter_chains:
                    specter_chains.remove(chain)
                break

    
    for burn_trace in burn_traces[:]:
        if not burn_trace.update(dt):
            burn_traces.remove(burn_trace)
    
    
    for magma_bullet in magma_bullets[:]:
        if magma_bullet.update(dt):
            magma_bullets.remove(magma_bullet)
    
    
    for magma_meteor in magma_meteors[:]:
        if magma_meteor.update(dt):
            magma_meteors.remove(magma_meteor)
    
    
    for magma_puddle in magma_puddles[:]:
        if not magma_puddle.update(dt):
            magma_puddles.remove(magma_puddle)

    
    for weaver_puddle in weaver_puddles[:]:
        if not weaver_puddle.update(dt):
            weaver_puddles.remove(weaver_puddle)

    
    for stalker_fist in stalker_fists[:]:
        if not stalker_fist.update(dt):
            stalker_fists.remove(stalker_fist)

    
    for stalker_echo in stalker_echoes[:]:
        if not stalker_echo.update(dt):
            stalker_echoes.remove(stalker_echo)

    
    for burn_trace in burn_traces:
        dist = math.sqrt((Character.x - burn_trace.actor.x)**2 + (Character.y - burn_trace.actor.y)**2)
        if dist < burn_trace.radius:
            
            if Character.burn_timer <= 0:
                Character.burn_timer = HUSKER_BURN_DURATION
                Character.burn_tick_timer = 0
            else:
                
                if burn_trace.should_tick():
                    Character.health -= HUSKER_BURN_DAMAGE
            Character.burn_timer = max(Character.burn_timer, HUSKER_BURN_DURATION)  
    
    
    if Character.burn_timer > 0:
        Character.burn_timer -= dt
        Character.burn_tick_timer += dt
        if Character.burn_tick_timer >= HUSKER_BURN_TICK_RATE:
            Character.burn_tick_timer = 0
            if Character.burn_timer > 0:
                Character.health -= HUSKER_BURN_DAMAGE

    if Character.freeze_timer > 0:
        Character.freeze_timer -= dt

    
    for magma_bullet in magma_bullets[:]:
        if Character.colliderect(magma_bullet.actor):
            Character.health -= magma_bullet.damage
            if magma_bullet in magma_bullets:
                magma_bullets.remove(magma_bullet)
            if Character.health <= 0:
                mode = 'menu'
            break
    
    
    for magma_meteor in magma_meteors[:]:
        if magma_meteor.state == "falling" and Character.colliderect(magma_meteor.actor):
            Character.health -= magma_meteor.damage
            if magma_meteor in magma_meteors:
                magma_meteors.remove(magma_meteor)
            if Character.health <= 0:
                mode = 'menu'
            break
    
    
    for magma_puddle in magma_puddles:
        dist = math.sqrt((Character.x - magma_puddle.actor.x)**2 + (Character.y - magma_puddle.actor.y)**2)
        if dist < magma_puddle.radius:
            
            Character.vx *= MAGMA_COLOSSUS_PUDDLE_SLOWDOWN  
            if Character.vy < MAGMA_COLOSSUS_PUDDLE_JUMP_LIMIT:  
                Character.vy = MAGMA_COLOSSUS_PUDDLE_JUMP_LIMIT
            if magma_puddle.should_tick():
                Character.health -= MAGMA_COLOSSUS_PUDDLE_DAMAGE

    
    for weaver_puddle in weaver_puddles:
        dist = math.sqrt((Character.x - weaver_puddle.actor.x)**2 + (Character.y - weaver_puddle.actor.y)**2)
        if dist < weaver_puddle.radius:
            Character.vx *= WEAVER_PUDDLE_SLOWDOWN
            if weaver_puddle.should_tick():
                Character.health -= WEAVER_PUDDLE_DAMAGE

    for fireball in fireballs[:]:
        hit_echo = False
        for echo in stalker_echoes[:]:
            if fireball.colliderect(echo.actor):
                echo.hit(PLAYER_FIREBALL_DAMAGE)
                if fireball in fireballs:
                    fireballs.remove(fireball)
                if not echo.active and echo in stalker_echoes:
                    stalker_echoes.remove(echo)
                hit_echo = True
                break
        if hit_echo:
            continue

        for enemy in enemies[:]:
            if fireball.colliderect(enemy.actor):
                if enemy.enemy_type == "stalker":
                    if fireball in fireballs:
                        fireballs.remove(fireball)
                    break
                enemy.health -= PLAYER_FIREBALL_DAMAGE
                if enemy.health <= 0:
                    if enemy.enemy_type == "crawler":
                        mud_splashes.append(MudSplash(enemy.actor.x, enemy.actor.y))
                    config = ENEMY_SPAWN_CONFIG.get(enemy.enemy_type, {})
                    health_reward = config.get("health_reward", 5)
                    Character.health = min(Character.health + health_reward, Character.max_health)
                    enemies.remove(enemy)
                if fireball in fireballs:
                    fireballs.remove(fireball)
                break
    
    
    for enemy_fireball in enemy_fireballs[:]:
        if Character.colliderect(enemy_fireball):
            
            damage = ENEMY_FIREBALL_DAMAGE  
            for enemy in enemies:
                if enemy.fireball_image == enemy_fireball.image:
                    damage = enemy.fireball_damage
                    break
            Character.health -= damage
            if enemy_fireball in enemy_fireballs:
                enemy_fireballs.remove(enemy_fireball)
            if Character.health <= 0:
                mode = 'menu'
            break
    
    
    for bullet in entropy_bullets[:]:
        if Character.colliderect(bullet.actor):
            Character.health -= 50  
            if bullet in entropy_bullets:
                entropy_bullets.remove(bullet)
            if Character.health <= 0:
                mode = 'menu'
            break

    
    for husker_fb in husker_fireballs[:]:
        if Character.colliderect(husker_fb.actor):
            Character.health -= HUSKER_FIREBALL_DAMAGE
            if husker_fb in husker_fireballs:
                husker_fireballs.remove(husker_fb)
            if Character.health <= 0:
                mode = 'menu'
            break

    
    for enemy_fireball in enemy_fireballs[:]:
        enemy_fireball.x += enemy_fireball.vx
        if enemy_fireball.x < 0 or enemy_fireball.x > WIDTH:
            if enemy_fireball in enemy_fireballs:
                enemy_fireballs.remove(enemy_fireball)

    for fireball in fireballs[:]:
        fireball.x += fireball.vx * time_scale
        if fireball.x > WIDTH or fireball.x < 0:
            fireballs.remove(fireball)


def on_mouse_down(pos):
    if mode == 'game' and fireball_button_rect.collidepoint(pos):
        shoot_fireball()



pgzrun.go()
