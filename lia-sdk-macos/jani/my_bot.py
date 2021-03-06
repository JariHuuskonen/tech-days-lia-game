import asyncio
import random

from lia.enums import *
from lia.api import *
from lia import constants
from lia import math_util
from lia.bot import Bot
from lia.networking_client import connect


# Initial implementation keeps picking random locations on the map
# and sending units there. Worker units collect resources if they
# see them while warrior units shoot if they see opponents.
class MyBot(Bot):

    # This method is called 10 times per game second and holds current
    # game state. Use Api object to call actions on your units.
    # - GameState reference: https://docs.liagame.com/api/#gamestate
    # - Api reference:       https://docs.liagame.com/api/#api-object
    def update(self, state, api):
        number_of_workers = 0
        for unit in state["units"]:
            if unit["type"] == UnitType.WORKER:
                number_of_workers += 1
        # If from all of your units less than 60% are workers
        # and you have enough resources, then create a new worker.
        if number_of_workers / len(state["units"]) < 0.45 and constants.GAME_DURATION * 0.533 > state["time"]:
            if state["resources"] >= constants.WORKER_PRICE:
                api.spawn_unit(UnitType.WORKER)
        # Else if you can, spawn a new warrior
        elif state["resources"] >= constants.WARRIOR_PRICE:
            api.spawn_unit(UnitType.WARRIOR)
        # If you have enough resources to spawn a new warrior unit then spawn it.
        if state["resources"] >= constants.WARRIOR_PRICE:
            api.spawn_unit(UnitType.WARRIOR)

        # We iterate through all of our units that are still alive.
        for unit in state["units"]:
            # If the unit is not going anywhere, we send it
            # to a random valid location on the map.
            if len(unit["navigationPath"]) == 0:

                # Generate new x and y until you get a position on the map
                # where there is no obstacle.
                while True:
                    x = random.randint(0, constants.MAP_WIDTH - 1)
                    y = random.randint(0, constants.MAP_HEIGHT - 1)

                    # If map[x][y] equals false it means that at (x,y) there is no obstacle.
                    if constants.MAP[x][y] is False:
                        # Send the unit to (x, y)
                        api.navigation_start(unit["id"], x, y)
                        break

            # If the unit is a worker and it sees at least one resource
            # then make it go to the first resource to collect it.
            if unit["type"] == UnitType.WORKER:
                # Fallback if health is low
                if unit["health"] < constants.BULLET_DAMAGE_TO_WORKER * 2:
                    api.navigation_start(unit["id"], constants.SPAWN_POINT.x, constants.SPAWN_POINT.y, True)
                    break
                else:
                    # Dodge opponent warriors
                    for opponent in unit["opponentsInView"]:
                        if opponent["type"] == UnitType.WARRIOR:
                            api.navigation_start(unit["id"], constants.SPAWN_POINT.x, constants.SPAWN_POINT.y, True)
                    # Collect res
                    if len(unit["resourcesInView"]) > 0:
                        resource = unit["resourcesInView"][0]
                        api.navigation_start(unit["id"], resource["x"], resource["y"])

            # If the unit is a warrior and it sees an opponent then make it shoot.
            if unit["type"] == UnitType.WARRIOR and len(unit["opponentsInView"]) > 0:
                api.say_something(unit["id"], "TROLOLOLOLO :D :---D")
                opponent = unit["opponentsInView"][0]
                aim_angle = math_util.angle_between_unit_and_point(unit, opponent["x"], opponent["y"])
                if aim_angle < 0:
                    api.say_something(unit["id"], "NO-SCOPE 360 HEADSHOT")
                    api.set_rotation(unit["id"], Rotation.RIGHT)
                else:
                    api.say_something(unit["id"], "MAD??")
                    api.set_rotation(unit["id"], Rotation.LEFT)
                api.shoot(unit["id"])

# Connects your bot to Lia game engine, don't change it.
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect(MyBot()))
