from Scripts.Global.var import *


def rand_range(a: float, b: float, s=10):
    a = a
    b = b

    return random.randint(a, b) / s


class Food:
    def __init__(self):
        self.size = 0.2
        self.pos: tuple[int, int] = (0, 0)
        self.col = RED
        self.value = FOOD_VALUE
        self.age = 1
        self.turns_to_grow = 20

    def update(self):
        if self.age < 1:
            self.age += 1 / self.turns_to_grow


class Food_Cluster:
    def __init__(self):
        self.food: list[Food] = []


class Entity_Stats:
    def __init__(self, size: float, vision: int, col: tuple[int, int, int, int]):
        self.size = size
        self.col = col
        self.vision = vision

        self.speed = 2 - self.size
        self.strenght = self.size * 2
        self.hunger = MAX_HUNGER

    def clone(self):
        return Entity_Stats(
            self.size,
            self.vision,
            self.col,
        )


class Default_Classes:
    assasin = Entity_Stats(rand_range(3, 5), random.randint(8, 10), GREEN)
    normal = Entity_Stats(rand_range(5, 8), random.randint(4, 7), BLUE)
    tank = Entity_Stats(rand_range(8, 10), random.randint(2, 5), RED)
    all = (assasin, normal, tank)


class Entity:
    def __init__(self):
        self.stats = random.choice(Default_Classes.all).clone()
        self.pos: tuple[int, int] = (0, 0)
        self.hunger_rate = 1 + (self.stats.size / 4)

        self.age = 1.0
        self.closest_enemy: Entity = None
        self.closest_food: Food = None
        self.food_smelt: Food = None
        self.id = 0

        self.is_dead = False

    def move_towards_a_random_direction(self):
        d_temp = random.randint(-1, 1)
        dx = 0
        dy = 0

        if random.randint(0, 1):
            dx = d_temp
        else:
            dy = d_temp

        if dx == 0 and dy == 0:
            return self.move_towards_a_random_direction()

        return dx, dy

    def move_towards(self, pos, direction=1):
        tx, ty = pos
        x, y = self.pos

        dx = 1 if x < tx else -1 if x > tx else 0
        dy = 1 if y < ty else -1 if y > ty else 0

        return dx * direction, dy * direction

    def move_away_from(self, pos):
        return self.move_towards(pos, -1)

    def clamp_movement(self, pos, max_pos: int):
        x, y = pos

        if x > max_pos:
            x = max_pos
        elif x < 0:
            x = 0

        if y > max_pos:
            y = max_pos
        elif y < 0:
            y = 0

        return x, y

    def move(self, max_pos: int):
        x, y = self.pos

        dx, dy = 0, 0
        if self.stats.hunger < 5:
            if self.closest_food:
                dx, dy = self.move_towards(self.closest_food.pos)

            else:
                if self.food_smelt:
                    dx, dy = self.move_towards(self.food_smelt.pos)

        elif self.closest_enemy:  # Either Flee or pursue enemy based on size
            if self.stats.size < self.closest_enemy.stats.size:
                dx, dy = self.move_away_from(self.closest_enemy.pos)
            else:
                dx, dy = self.move_towards(self.closest_enemy.pos)

        if dx == 0 and dy == 0:
            dx, dy = self.move_towards_a_random_direction()

        new_pos = x + dx, y + dy
        new_pos = self.clamp_movement(new_pos, max_pos)

        return new_pos

    def __repr__(self):
        return f"<id:{self.id} size:{self.stats.size}, spd:{self.stats.speed}, pos:({self.pos[0]}, {self.pos[1]})>"

    def update(self):
        self.stats.hunger -= self.hunger_rate
        self.is_dead = self.stats.hunger <= 0
