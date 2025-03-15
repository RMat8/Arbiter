#game/entity.py
class Entity:
    numberOfEntities = 0
    def __init__(self, name="_", health=100):
        Entity.numberOfEntities += 1
        self.health = health
        if name == "_":
            self.name = "Entity" + str(Entity.numberOfEntities)
    
def kill(entity):
    Entity.numberOfEntities -= 1
    del entity
