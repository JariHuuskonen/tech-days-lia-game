import lia.api.*;
import lia.*;

/**
 * Initial implementation keeps picking random locations on the map
 * and sending units there. Worker units collect resources if they
 * see them while warrior units shoot if they see opponents.
 */
public class MyBot implements Bot {
    int i = 0;
    boolean right = false;
    // This method is called 10 times per game second and holds current
    // game state. Use Api object to call actions on your units.
    // - GameState reference: https://docs.liagame.com/api/#gamestate
    // - Api reference:       https://docs.liagame.com/api/#api-object
    @Override
    public void update(GameState state, Api api) {
        i++;
        // If you have enough resources to spawn a new warrior unit then spawn it.
        spawn(state, api);

        // We iterate through all of our units that are still alive.
        for (int i = 0; i < state.units.length; i++) {
            UnitData unit = state.units[i];

            // If the unit is not going anywhere, we send it
            // to a random valid location on the map.


            // If the unit is a worker and it sees at least one resource
            // then make it go to the first resource to collect it.
            if (unit.type == UnitType.WORKER && unit.resourcesInView.length > 0) {
                if (unit.resourcesInView.length > 0) {
                    ResourceInView resource = unit.resourcesInView[0];
                    api.navigationStart(unit.id, resource.x, resource.y);
                } else {
                    panic(unit, api);
                }
            }

            // If the unit is a warrior and it sees an opponent then start shooting
            if (unit.type == UnitType.WARRIOR) {
                if (unit.opponentsInView.length > 0) {
                    fight(state, api, unit);
                } else {
                    evade(api, unit);
                    communicate(state, api, unit);
                }
            }

            avoidWall(unit, api);
        }
    }

    private void avoidWall(UnitData unit, Api api) {
        if (unit.navigationPath.length == 0) {

            // Generate new x and y until you get a position on the map
            // where there is no obstacle. Then move the unit there.
            while (true) {
                int x = (int) (Math.random() * Constants.MAP_WIDTH);
                int y = (int) (Math.random() * Constants.MAP_HEIGHT);

                // Map is a 2D array of booleans. If map[x][y] equals false it means that
                // at (x,y) there is no obstacle and we can safely move our unit there.
                if (!Constants.MAP[x][y]) {
                    api.navigationStart(unit.id, x, y);
                    break;
                }
            }
        }
    }

    private void panic(UnitData unit, Api api) {
        if (unit.health < Constants.BULLET_DAMAGE_TO_WORKER * 3) {
            api.navigationStart(unit.id, Constants.SPAWN_POINT.x, Constants.SPAWN_POINT.y, true);
        } else {
            for(OpponentInView opponent : unit.opponentsInView) {
                if (opponent.type == UnitType.WARRIOR) {
                    api.navigationStart(unit.id, Constants.SPAWN_POINT.x, Constants.SPAWN_POINT.y, true);
                }
            }
        }

        if (unit.resourcesInView.length >=  0) {
            ResourceInView resource = unit.resourcesInView[0];
            api.navigationStart(unit.id, resource.x, resource.y);
        }
    }

    private void spawn(GameState state, Api api) {
        if (state.resources >= Constants.WARRIOR_PRICE) {
            // Calculate how many workers you currently have
            int numberOfWorkers = 0;
            for (UnitData unit : state.units) {
                if (unit.type == UnitType.WORKER) numberOfWorkers++;
            }
            // If from all of your units less than 60% are workers
            // and you have enough resources, then create a new worker.
            if (numberOfWorkers / (float) state.units.length < 0.6f) {
                if (state.resources >= Constants.WORKER_PRICE) {
                    api.spawnUnit(UnitType.WORKER);
                }
            }
            // Else if you can, spawn a new warrior
            else if (state.resources >= Constants.WARRIOR_PRICE) {
                api.spawnUnit(UnitType.WARRIOR);
            }
        }
    }

    private void shoot(GameState state, Api api, UnitData unit) {
        OpponentInView opponent = unit.opponentsInView[0];
        float opponentDistance = MathUtil.distance(opponent.x, opponent.y, unit.x, unit.y);
        for (UnitData teammate : state.units) {
            float friendDistance = MathUtil.distance(teammate.x, teammate.y, unit.x, unit.y);
            float friendAngle = MathUtil.angleBetweenUnitAndPoint(unit, teammate.x, teammate.y);
            if (Math.abs(friendAngle) <= 10 && friendDistance < opponentDistance) {
                api.saySomething(unit.id, "CAN\'T SHOOT!");
            } else {
                api.shoot(unit.id);
            }
        }


    }

    private void evade(Api api, UnitData unit) {
        /*api.setSpeed(unit.id, Speed.FORWARD);
        if (i % 30 == 0) {
            right = !right;
        }

        if (right) {
            api.saySomething(unit.id, "Too fast!");
            api.setRotation(unit.id, Rotation.RIGHT);
        } else {
            api.saySomething(unit.id, "Can\'t catch me!");
            api.setRotation(unit.id, Rotation.LEFT);
        }*/
    }

    private void fight(GameState state, Api api, UnitData unit) {
        // Get the first opponent that the unit sees.
        OpponentInView opponent = unit.opponentsInView[0];

        float aimAngle = MathUtil.angleBetweenUnitAndPoint(unit, opponent.x, opponent.y);
        float distance = MathUtil.distance(opponent.x, opponent.y, unit.x, unit.y);

        api.saySomething(unit.id, "Distance: " + distance);
        // Stop the unit.
        //api.setSpeed(unit.id, Speed.NONE);

        // Based on the aiming angle turn towards the opponent.

        if (distance < 5) {
            if (distance < 3) {
                api.setSpeed(unit.id, Speed.NONE);
            } else {
                api.setSpeed(unit.id, Speed.FORWARD);
            }
            if (aimAngle < 0) {
                api.setRotation(unit.id, Rotation.RIGHT);
            } else {
                api.setRotation(unit.id, Rotation.LEFT);
            }
            if (aimAngle <= 10 && aimAngle >= -10) {
                shoot(state, api, unit);
            }
        } else if (aimAngle <= 10 && aimAngle >= -10) {
            api.setSpeed(unit.id, Speed.FORWARD);
            if (aimAngle < 0) {
                api.setRotation(unit.id, Rotation.SLOW_RIGHT);
            } else {
                api.setRotation(unit.id, Rotation.SLOW_LEFT);
            }
            shoot(state, api, unit);
        } else if (aimAngle <= 15 && aimAngle >= -15) {
            api.setSpeed(unit.id, Speed.FORWARD);
            if (aimAngle < 0) {
                api.setRotation(unit.id, Rotation.SLOW_RIGHT);
            } else {
                api.setRotation(unit.id, Rotation.SLOW_LEFT);
            }
        } else {
            api.setSpeed(unit.id, Speed.NONE);
            if (aimAngle < 0) {
                api.setRotation(unit.id, Rotation.RIGHT);
            } else {
                api.setRotation(unit.id, Rotation.LEFT);
            }
        }

        //api.saySomething(unit.id, "All your base are belong to us!");
    }

    private void communicate(GameState state, Api api, UnitData unit) {
        // Check if some teammate detected an opponent near the unit. If
        // it did then send the unit to the location of the opponent.
        for (UnitData teammate : state.units) {
            boolean found = false;

            for (OpponentInView opponent : teammate.opponentsInView) {
                // Calculate the distance between the unit and opponent.
                float dst = MathUtil.distance(unit.x, unit.y, opponent.x, opponent.y);

                if (dst < Constants.VIEWING_AREA_LENGTH) {
                    // We have detected an opponent that is very close!
                    api.navigationStart(unit.id, opponent.x, opponent.y);
                    found = true;
                    break;
                }
            }
            if (found) break;
        }
    }

    // Connects your bot to Lia game engine, don't change it.
    public static void main(String[] args) throws Exception {
        NetworkingClient.connectNew(args, new MyBot());
    }

}
