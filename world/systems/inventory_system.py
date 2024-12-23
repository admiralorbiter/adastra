from world.objects import StorageContainer
from world.items import ItemType

class InventorySystem:
    def __init__(self):
        self.storage_containers = []
        self.ship = None

    def register_container(self, container):
        """Register a storage container with the system"""
        if isinstance(container, StorageContainer) and container not in self.storage_containers:
            self.storage_containers.append(container)

    def unregister_container(self, container):
        """Remove a storage container from the system"""
        if container in self.storage_containers:
            self.storage_containers.remove(container)

    def get_total_food(self) -> int:
        """Get total food across all storage containers"""
        return sum(
            container.get_item_count(ItemType.FOOD)
            for container in self.storage_containers
        )

    def find_nearest_storage(self, x: int, y: int) -> tuple[StorageContainer, tuple[int, int]] | None:
        """Find nearest storage container with food and its position"""
        nearest_distance = float('inf')
        nearest_storage = None
        nearest_pos = None
        
        for container in self.storage_containers:
            if container.get_item_count(ItemType.FOOD) > 0:
                # Find container position in ship
                container_pos = self._find_container_position(container)
                if container_pos:
                    tile_x, tile_y = container_pos
                    distance = ((tile_x - x) ** 2 + (tile_y - y) ** 2) ** 0.5
                    if distance < nearest_distance:
                        nearest_distance = distance
                        nearest_storage = container
                        nearest_pos = container_pos
        
        return (nearest_storage, nearest_pos) if nearest_storage else None

    def _find_container_position(self, container) -> tuple[int, int] | None:
        """Find the position of a container in the ship"""
        for deck in self.ship.decks:
            for y in range(deck.height):
                for x in range(deck.width):
                    tile = deck.tiles[y][x]
                    if tile.object == container:
                        return (x, y)
        return None 