# Constants are set on runtime from game engine, changing them has
# no effect. Find the predefined values in data/game-config.json or
# print them out in processGameEnvironment() method in your bot
# implementation.

# The duration of the game in seconds.
global GAME_DURATION
# The width of the map in world units.
global MAP_WIDTH
# The height of the map in world units.
global MAP_HEIGHT
# Map as a 2D array of booleans. If map[x][y] equals True that means that at (x,y)
# there is an obstacle. x=0, y=0 points to bottom left corner.
global MAP
# Approximate location where your team was spawned.
global SPAWN_POINT
# The diameter of the unit in world units.
global UNIT_DIAMETER
# A full health of a unit when the game starts.
global UNIT_FULL_HEALTH
# The velocity in world units per second with which the unit moves forward.
global UNIT_FORWARD_VELOCITY
# The velocity in world units per second with which the unit moves backward.
global UNIT_BACKWARD_VELOCITY
# The angle with which the unit's orientation changes per second when rotating normally.
global UNIT_ROTATION_VELOCITY
# The angle with which the unit's orientation changes per second when rotating slowly.
global UNIT_SLOW_ROTATION_VELOCITY
# Delay between shooting two pre-loaded bullets.
global DELAY_BETWEEN_SHOTS
# The time to reload one bullet.
global RELOAD_TIME
# A maximum number of bullets that a unit can hold at once.
global MAX_BULLETS
# The time after which the unit starts to regenerate health after being hit by a bullet.
global HEALTH_REGENERATION_DELAY
# The amount of health points per second that the unit receives when recovering.
global HEALTH_REGENERATION_PER_SECOND
# The length of unit's viewing area.
global VIEWING_AREA_LENGTH
# The width of unit's viewing area at the side that is the furthest away from the unit.
global VIEWING_AREA_WIDTH
# The amount by which is the start of a viewing area offset from the unit's center
# (negative means towards the back).
global VIEWING_AREA_OFFSET
# The diameter of the bullet in world units.
global BULLET_DIAMETER
# The speed in world units per second with which the bullet moves forward.
global BULLET_VELOCITY
# The damage that a warrior receives when it is hit by a bullet.
global BULLET_DAMAGE_TO_WARRIOR
# The damage that a worker receives when it is hit by a bullet.
global BULLET_DAMAGE_TO_WORKER
# The range of the bullet in world units.
global BULLET_RANGE
# Price in resources for purchasing a warrior unit.
global WARRIOR_PRICE
# Price in resources for purchasing a worker unit.
global WORKER_PRICE
# Maximum number of units on your team.
global MAX_NUMBER_OF_UNITS
# After how many seconds new resources stop spawning.
global STOP_SPAWNING_AFTER
# The maximum duration of the first update() call.
global FIRST_TICK_TIMEOUT
# The maximum duration of each update() call after the first one.
global TICK_TIMEOUT


# This method is called from networking_client.py. Do not call it again.
def load_constants(constants_json):
    global MAP_WIDTH, MAP_HEIGHT, GAME_DURATION, UNIT_DIAMETER, UNIT_FULL_HEALTH, UNIT_FORWARD_VELOCITY
    global UNIT_BACKWARD_VELOCITY, UNIT_ROTATION_VELOCITY, UNIT_SLOW_ROTATION_VELOCITY, DELAY_BETWEEN_SHOTS
    global RELOAD_TIME, MAX_BULLETS, HEALTH_REGENERATION_DELAY, HEALTH_REGENERATION_PER_SECOND, VIEWING_AREA_LENGTH
    global VIEWING_AREA_WIDTH, VIEWING_AREA_OFFSET, BULLET_DIAMETER, BULLET_VELOCITY, BULLET_DAMAGE, BULLET_RANGE
    global FIRST_TICK_TIMEOUT, TICK_TIMEOUT, STOP_SPAWNING_AFTER, MAP, SPAWN_POINT
    global BULLET_DAMAGE_TO_WARRIOR, BULLET_DAMAGE_TO_WORKER, WARRIOR_PRICE, WORKER_PRICE, MAX_NUMBER_OF_UNITS

    # Setup constants
    MAP_WIDTH = constants_json["MAP_WIDTH"]
    MAP_HEIGHT = constants_json["MAP_HEIGHT"]
    GAME_DURATION = constants_json["GAME_DURATION"]
    UNIT_DIAMETER = constants_json["UNIT_DIAMETER"]
    UNIT_FULL_HEALTH = constants_json["UNIT_FULL_HEALTH"]
    UNIT_FORWARD_VELOCITY = constants_json["UNIT_FORWARD_VELOCITY"]
    UNIT_BACKWARD_VELOCITY = constants_json["UNIT_BACKWARD_VELOCITY"]
    UNIT_ROTATION_VELOCITY = constants_json["UNIT_ROTATION_VELOCITY"]
    UNIT_SLOW_ROTATION_VELOCITY = constants_json["UNIT_SLOW_ROTATION_VELOCITY"]
    DELAY_BETWEEN_SHOTS = constants_json["DELAY_BETWEEN_SHOTS"]
    RELOAD_TIME = constants_json["RELOAD_TIME"]
    MAX_BULLETS = constants_json["MAX_BULLETS"]
    HEALTH_REGENERATION_DELAY = constants_json["HEALTH_REGENERATION_DELAY"]
    HEALTH_REGENERATION_PER_SECOND = constants_json["HEALTH_REGENERATION_PER_SECOND"]
    VIEWING_AREA_LENGTH = constants_json["VIEWING_AREA_LENGTH"]
    VIEWING_AREA_WIDTH = constants_json["VIEWING_AREA_WIDTH"]
    VIEWING_AREA_OFFSET = constants_json["VIEWING_AREA_OFFSET"]
    BULLET_DIAMETER = constants_json["BULLET_DIAMETER"]
    BULLET_VELOCITY = constants_json["BULLET_VELOCITY"]
    BULLET_RANGE = constants_json["BULLET_RANGE"]
    FIRST_TICK_TIMEOUT = constants_json["FIRST_TICK_TIMEOUT"]
    TICK_TIMEOUT = constants_json["TICK_TIMEOUT"]
    STOP_SPAWNING_AFTER = constants_json["STOP_SPAWNING_AFTER"]
    MAX_NUMBER_OF_UNITS = constants_json["MAX_NUMBER_OF_UNITS"]
    WORKER_PRICE = constants_json["WORKER_PRICE"]
    WARRIOR_PRICE = constants_json["WARRIOR_PRICE"]
    BULLET_DAMAGE_TO_WORKER = constants_json["BULLET_DAMAGE_TO_WORKER"]
    BULLET_DAMAGE_TO_WARRIOR = constants_json["BULLET_DAMAGE_TO_WARRIOR"]

    SPAWN_POINT = SpawnPoint(constants_json["SPAWN_POINT"]["x"], constants_json["SPAWN_POINT"]["y"])

    MAP = []
    for row in constants_json["MAP"]:
        row_bool = []
        for val in row:
            row_bool.append(val)
        MAP.append(row)


class SpawnPoint:

    def __init__(self, x, y):
        self.x = x
        self.y = y

