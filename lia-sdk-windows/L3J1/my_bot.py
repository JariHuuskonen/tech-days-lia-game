import asyncio
import random
import math

from lia.enums import *
from lia.api import *
from lia import constants
from lia import math_util
from lia.bot import Bot
from lia.networking_client import connect

campers = []
corners = []

def banter():
    banter = ["Rush b", "Reporting in", "Tikka Masala", "U wot m8?", "Xaxaxa", str(2 ** 2 ** -1)]
    return banter[random.randint(0, len(banter)-1)]

def get_enemy_spawnpoint(offset=0):
    offset = offset if constants.SPAWN_POINT.x < 0.5 * constants.MAP_WIDTH else -offset
    enemy_spawn_x = constants.MAP_WIDTH - constants.SPAWN_POINT.x + offset
    enemy_spawn_y =  constants.MAP_HEIGHT - constants.SPAWN_POINT.y + offset
    return {"x": round(enemy_spawn_x), "y": round(enemy_spawn_y)}

# Initial implementation keeps picking random locations on the map
# and sending units there. Worker units collect resources if they
# see them while warrior units shoot if they see opponents.
class MyBot(Bot):

    # This method is called 10 times per game second and holds current
    # game state. Use Api object to call actions on your units.
    # - GameState reference: https://docs.liagame.com/api/#gamestate
    # - Api reference:       https://docs.liagame.com/api/#api-object
    def update(self, state, api):

        id_list = []
        resources_list = []
        number_of_workers = 0
        number_of_warriors = 0
        dang_x = 0
        dang_y = 0

        
        if state["time"] % 10: 
            api.say_something(state["units"][random.randint(0, len(state["units"])-1)]["id"], banter())

        for unit in state["units"]:
            id_list.append(unit["id"])
            if unit["type"] == UnitType.WORKER: number_of_workers += 1
            else: number_of_warriors += 1

        # Populate resources table used to coordinate nearby workers 
            if len(unit["resourcesInView"]) > 0:
                for resource in unit["resourcesInView"]:
                    if {'x': resource["x"], 'y': resource["y"]} not in resources_list:
                        resources_list.append({'x': resource["x"], 'y': resource["y"]})

        # If from all of your units less than 60% are workers
        # and you have enough resources, then create a new worker.
        if number_of_workers / len(state["units"]) < 0.55 and constants.GAME_DURATION * 0.420 > state["time"]:
            if state["resources"] >= constants.WORKER_PRICE:
                api.spawn_unit(UnitType.WORKER)
        # Else if you can, spawn a new warrior
        elif state["resources"] >= constants.WARRIOR_PRICE:
            api.spawn_unit(UnitType.WARRIOR)
        

        # We iterate through all of our units that are still alive.
        for unit in state["units"]:
            # If the unit is not going anywhere, we send it
            # to a random valid location on the map.
            
            # If worker doesn't have path, send it to nearby target from resource list
            if unit["type"] == UnitType.WORKER and len(unit["resourcesInView"]) == 0 and len(resources_list) > 0 and len(unit["navigationPath"]) == 0:
                destination = {"x": 0, "y": 0, "dist": math_util.distance(0,0,constants.MAP_WIDTH,constants.MAP_HEIGHT), "index": -1 }
                for i, resource in enumerate(resources_list):
                    res_distance = math_util.distance(unit["x"], unit["y"], resource["x"], resource["y"])
                    if not res_distance > constants.VIEWING_AREA_LENGTH * 2.333:
                        if res_distance < destination["dist"]:
                            destination = {'x': resource["x"], 'y': resource["y"], 'dist': res_distance, 'index': i}

                resources_list.pop(destination["index"])
                api.navigation_start(unit["id"], destination["x"], destination["y"])

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
            if not any(item in campers for item in id_list) and unit["type"] == UnitType.WARRIOR and number_of_warriors >= 4 and state["time"] > 10:
                campers.append(unit["id"])

            if unit["id"] in campers and 140 > state["time"] :
                if abs(unit["x"] - get_enemy_spawnpoint(6)["x"]) < 3 and abs(unit["y"] - get_enemy_spawnpoint(6)["y"]) < 3:
                    api.navigation_stop(unit["id"])
                    aim_angle = math_util.angle_between_unit_and_point(unit, get_enemy_spawnpoint()["x"], get_enemy_spawnpoint()["y"])
                    if len(unit["opponentsInView"]) > 0:
                        api.shoot(unit["id"])
                    if aim_angle < 15:
                        api.set_rotation(unit["id"], Rotation.RIGHT)
                    elif aim_angle > 15:
                        api.set_rotation(unit["id"], Rotation.LEFT)
                    if len(unit["opponentsInView"]) > 0:
                        api.shoot(unit["id"])
                else:
                    api.navigation_start(unit["id"], get_enemy_spawnpoint(6)["x"], get_enemy_spawnpoint(6)["y"], False)

            if unit["type"] == UnitType.WORKER:
                # Call for backup
                if len(unit["opponentsInView"]) > 1:
                    dang_x = unit["x"]
                    dang_y = unit["y"]
                # Fallback if health is low
                if unit["health"] < constants.BULLET_DAMAGE_TO_WORKER * 3:
                    if math_util.distance(unit["x"],unit["y"], constants.SPAWN_POINT.x, constants.SPAWN_POINT.y) > (math_util.distance(0,0,constants.MAP_WIDTH,constants.MAP_HEIGHT) / 4):
                        api.set_speed(unit["id"], Speed.FORWARD)
                        api.set_rotation(unit["id"], Rotation.LEFT)
                    else:
                        api.set_speed(unit["id"], Speed.FORWARD)
                        api.set_rotation(unit["id"], Rotation.SLOW_LEFT)

                else:
                    # Collect res
                    if len(unit["resourcesInView"]) > 0:
                        resource = unit["resourcesInView"][0]
                        api.navigation_start(unit["id"], resource["x"], resource["y"])

                    # Dodge opponent warriors
                    for opponent in unit["opponentsInView"]:
                        if opponent["type"] == UnitType.WARRIOR:
                            
                            dist_unit_opponent = math_util.distance(unit["x"],unit["y"],opponent["x"],opponent["y"])

                            if dist_unit_opponent > constants.VIEWING_AREA_LENGTH/2:
                                api.set_speed(unit["id"], Speed.BACKWARD)
                            else:
                                api.set_speed(unit["id"], Speed.FORWARD)

            # If the unit is a warrior and it sees an opponent then make it shoot.
            if unit["type"] == UnitType.WARRIOR:
                if not dang_x == 0 and not dang_y == 0 and len(unit["opponentsInView"]) == 0 and not unit["id"] in campers:
                    api.navigation_start(unit["id"], dang_x, dang_y, False)
                    dang_x = 0
                    dang_y = 0
                if len(unit["opponentsInView"]) > 0:
                    opponent = unit["opponentsInView"][0]
                    aim_angle = math_util.angle_between_unit_and_point(unit, opponent["x"], opponent["y"])
                    if aim_angle < 0:
                        api.set_rotation(unit["id"], Rotation.RIGHT)
                    else:
                        api.set_rotation(unit["id"], Rotation.LEFT)
                    api.shoot(unit["id"])

                if len(unit["opponentsInView"]) == 0 and not unit["id"] in campers:
                    for teammate in state["units"]:
                        found = False

                        for opponent in teammate["opponentsInView"]:
                            distance = math_util.distance(unit["x"], unit["y"], opponent["x"], opponent["y"])

                            if distance < constants.VIEWING_AREA_LENGTH * 2 ** 2 ** -1:
                                api.navigation_start(unit["id"], opponent["x"], opponent["y"], False)
                                found = True
                                break

                        if found:
                            break


# Connects your bot to Lia game engine, don't change it.
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(connect(MyBot()))
