SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 20
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 2.0
PLAYER_MAX_HP = 3


SHOT_RADIUS = 5

# Elite asteroid settings
ELITE_SPAWN_CHANCE = 0.15  # 15% chance of an asteroid being elite
ELITE_MIN_WAVE = 3  # Elites start appearing from wave 3

# Wave settings
WAVE_COUNTDOWN = 3.0  # Seconds to wait before a wave starts
PERK_SELECTION_AFTER_WAVE = True  # Whether to show perk selection after wave

# Elite types
ELITE_TYPES = ['exploder', 'shielded', 'swarm_leader']

# Game state
STATE_PLAYING = 0
STATE_WAVE_TRANSITION = 1
STATE_PERK_SELECTION = 2
STATE_GAME_OVER = 3