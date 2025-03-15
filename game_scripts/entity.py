#game/entity.py
class Entity:
    numberOfEntities = 0
    def __init__(self, name=f"Entity #{len(numberOfEntities+1)}", health=100):
        self.name = name
        self.health = health
        Entity.numberOfEntities += 1
    
    def kill(self):
        Entity.numberOfEntities -= 1
        del self