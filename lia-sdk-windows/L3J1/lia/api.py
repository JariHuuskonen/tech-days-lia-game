
class Api:
    def __init__(self, uid):
        self.response = {}
        self.uid = uid
        self.current_index = 0
        self.type = "RESPONSE"
        self.speedEvents = []
        self.rotationEvents = []
        self.shootEvents = []
        self.navigationStartEvents = []
        self.navigationStopEvents = []
        self.saySomethingEvents = []
        self.spawnUnitEvents = []

    def get_index(self):
        index = self.current_index
        self.current_index += 1
        return index

    def set_speed(self, unit_id, speed):
        self.speedEvents.append({"index": self.get_index(), "unitId": unit_id, "speed": speed})

    def set_rotation(self, unit_id, rotation):
        self.rotationEvents.append({"index": self.get_index(), "unitId": unit_id, "rotation": rotation})

    def shoot(self, unit_id):
        self.shootEvents.append({"index": self.get_index(), "unitId": unit_id})

    def navigation_start(self, unit_id, x, y, move_backwards=False):
        self.navigationStartEvents.append({"index": self.get_index(), "unitId": unit_id,
                                           "x": x, "y": y, "moveBackwards": move_backwards})

    def navigation_stop(self, unit_id):
        self.navigationStopEvents.append({"index": self.get_index(), "unitId": unit_id})

    def say_something(self, unit_id, text):
        self.saySomethingEvents.append({"index": self.get_index(), "unitId": unit_id, "text": text})

    def spawn_unit(self, unit_type):
        self.spawnUnitEvents.append({"index": self.get_index(), "type": unit_type})
