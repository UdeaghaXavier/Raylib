from Scripts.Core.GridMap import GridMap
from Scripts.Core.Entity import Entity, Food, Food_Cluster
from Scripts.Global.var import *


class Info:
    def __init__(self):
        self.entities: list[Entity] = []
        self.food = []


class Entity_Manager:
    def __init__(self, gridMap: GridMap):
        self.grid_map = gridMap
        # self.initial_enemy_count = self.grid_map.map_size
        self.initial_enemy_count = STARTING_ENTITIES
        self.info = Info()
        self.turn = 0
        self.entity_count = 0
        self.num_of_food_clusters = 4
        self.food_clusters: list[Food] = []

        self.spawn_entities()
        self.spawn_food()

    def update(self):
        if self.turn % 2 == 0:
            self.update_grid_objects()
        else:
            self.update_info()
        if self.turn % 10 == 0:
            self.update_food_clusters()

        self.turn += 1

    def update_food_clusters(self):
        clusters = self.food_clusters

        for cluster in clusters:
            for food in cluster.food:
                x, y = food.pos
                if food.age >= 1:
                    if self.grid_map.map[y][x] == None:
                        self.update_location((x, y), food)

    def spawn_food(self):
        # Food exists in clusters, like resources exist in automation games
        # Number of clusters on the map is given by this eqn

        self.food_clusters = self.get_clusters_with_food()

        for cluster in self.food_clusters:
            for food in cluster.food:
                x, y = food.pos
                self.update_location((x, y), food)

    def new_food(self, pos) -> Food:
        x, y = pos
        food = Food()
        food.pos = (x, y)

        return food

    def get_clusters_with_food(self) -> list[Food_Cluster]:
        # Get number of rows and cols enough to contain all custers
        r = int((self.num_of_food_clusters) ** 0.5)
        # Since the number is gotten the width of each cluster is determined
        w = int(self.grid_map.map_size / r)

        food_cluster: list[Food_Cluster] = []
        for y in range(r):
            for x in range(r):
                # For each row and col
                cluster = self.new_food_cluster((x * w, y * w), w)
                food_cluster.append(cluster)

        return food_cluster

    def new_food_cluster(self, pos: tuple[float, float], w: float) -> Food_Cluster:
        x1, y1 = pos  # Top left - Start Pos
        nfw = int((w**2))
        nf = random.randint(
            int(MIN_FOOD_PERCENATGE * nfw), int(nfw * MAX_FOOD_PERCENTAGE)
        )  # number of food to spawn
        food_cluster = Food_Cluster()

        for i in range(nf):
            food = self.new_food(
                self.get_valid_spawn_point_within((x1, y1), (x1 + w, y1 + w))
            )
            food_cluster.food.append(food)

        return food_cluster

    def get_valid_spawn_point_within(
        self, start_pos: tuple[int, int], end_pos: tuple[int, int]
    ):
        x1, y1 = start_pos
        x2, y2 = end_pos

        x = random.randint(x1, x2)
        y = random.randint(y1, y2)

        if self.grid_map.map[y][x] == None:
            return (x, y)
        return self.get_valid_spawn_point_within(start_pos, end_pos)

    def new_entity(self, pos) -> Entity:
        entity = Entity()
        entity.pos = pos
        entity.id = self.entity_count

        self.entity_count += 1
        return entity

    def update_location(self, pos, entity):
        x, y = pos
        self.grid_map.map[y][x] = entity

    def get_stronger_entity(self, entity1: Entity, entity2: Entity):
        # We'll let entity 1 win since it initiated the attack..
        # it more or less jumped entity2
        if entity1.stats.strenght >= entity2.stats.strenght:
            return entity1
        return entity2

    def move_entity(self, pos: tuple[int, int]):
        x, y = pos
        entity = self.grid_map.map[y][x]

        nx, ny = entity.move(self.grid_map.map_size - 1)
        other_entity = self.grid_map.map[ny][nx]
        self.update_location(pos, None)

        winner = entity

        if type(other_entity) == Entity:  # Check if this new pos is occupied
            winner = self.get_stronger_entity(entity, other_entity)
            # Weaken the winner after the fight
            if winner == entity:
                entity.stats.strenght -= other_entity.stats.strenght / 2
            else:
                other_entity.stats.strenght -= entity.stats.strenght / 2
        elif type(other_entity) == Food:
            other_entity.age = 0
            entity.stats.strenght = entity.stats.size * 2
            entity.stats.hunger = FOOD_VALUE

        self.update_location((nx, ny), winner)

    def update_info(self):
        entities = []
        for y, row in enumerate(self.grid_map.map):
            for x, entity in enumerate(row):
                if type(entity) == Entity:
                    entity.pos = (x, y)
                    entities.append(entity)

        self.info.entities = entities

    def get_closest_object_to(self, entity: Entity, _type: Entity | Food, v=None):
        cx, cy = entity.pos  # Center of search radius
        if not v:
            v = entity.stats.vision  # Radius of search

        closest_obj = None
        shortest_dist = float("inf")  # Track the shortest distance found
        sx, sy = cx - v, cy - v  # Top-left search start

        for dy in range(v * 2 + 1):  # Cover full vision range
            y = int(clamp(sy + dy, 0, self.grid_map.map_size - 1))
            for dx in range(v * 2 + 1):
                x = int(clamp(sx + dx, 0, self.grid_map.map_size - 1))
                obj = self.grid_map.map[y][x]

                if isinstance(obj, _type):  # Correct type check
                    dfx, dfy = abs(cx - x), abs(cy - y)
                    if dfx == 0 and dfy == 0:  # Skip itself
                        continue

                    distance = dfx + dfy  # Manhattan distance
                    if distance < shortest_dist:
                        shortest_dist = distance
                        closest_obj = obj

        return closest_obj

        # Im lazy so ill make it a square (row = col)

        # We do not iterate through the entire map, just the region the entity can see

    def update_grid_objects(self):
        entities: list[Entity] = []
        food: list[Food] = []

        for y, row in enumerate(self.grid_map.map):
            for x, entity in enumerate(row):

                if type(entity) == Entity:
                    entity: Entity = entity
                    entity.update()
                    self.move_entity((x, y))
                    entity.closest_enemy = self.get_closest_object_to(entity, Entity)
                    entity.closest_food = self.get_closest_object_to(entity, Food)
                    if entity.stats.hunger <= 7:
                        entity.food_smelt = self.get_closest_object_to(
                            entity, Food, entity.stats.vision
                        )
                    if entity.is_dead:
                        self.grid_map.map[y][x] = None
                    else:
                        entities.append(entity)

                if type(entity) == Food:
                    entity: Food = entity
                    entity.update()
                    food.append(entity)

        self.info.food = food
        self.info.entities = entities

    def spawn_entities(self):
        for _ in range(self.initial_enemy_count):
            x, y = self.get_valid_spawn_point()

            self.grid_map.map[y][x] = self.new_entity((x, y))

    def get_valid_spawn_point(self):
        rx = random.randint(0, self.grid_map.map_size - 1)
        ry = random.randint(0, self.grid_map.map_size - 1)

        if self.grid_map.map[ry][rx] != None:
            return self.get_valid_spawn_point()
        return (rx, ry)
