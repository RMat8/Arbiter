#game/entity.py
class Entity:
    numberOfEntities = 0
    def __init__(self, name="_", health=100):
        Entity.numberOfEntities += 1
        self.health = health
        self.inventory = {}
        if name == "_":
            self.name = "Entity" + str(Entity.numberOfEntities)
        else:
            self.name = name

def kill(entity):
    if entity:
        Entity.numberOfEntities -= 1
        del entity
        return True
    else:
        print("Entity not found")
        return False
