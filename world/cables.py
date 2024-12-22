from world.modules import ReactorModule


class Cable:
    def __init__(self):
        self.powered = False
        self.network_id = None
        self.connected_modules = []  # List of connected modules

class CableSystem:
    def __init__(self):
        self.cables = {}  # (x, y) -> Cable
        self.preview_cables = set()
        self.drag_start = None
        self.drag_end = None
        self.networks = []  # List of connected cable networks
        self.ship = None  # Reference to ship will be set later
    
    def add_cable(self, x: int, y: int):
        """Add a cable at the specified coordinates"""
        if (x, y) not in self.cables:
            self.cables[(x, y)] = Cable()
            self._update_networks()
    
    def remove_cable(self, x: int, y: int):
        """Remove a cable at the specified coordinates"""
        if (x, y) in self.cables:
            del self.cables[(x, y)]
            self._update_networks()
    
    def start_drag(self, x: int, y: int):
        """Start cable dragging operation"""
        # Ensure coordinates are valid before starting drag
        if (0 <= x < self.ship.decks[0].width and 
            0 <= y < self.ship.decks[0].height):
            self.drag_start = (int(x), int(y))
            self.preview_cables.clear()
    
    def update_drag(self, x: int, y: int):
        """Update cable preview during drag"""
        if self.drag_start:
            # Clamp coordinates to deck bounds
            x = max(0, min(int(x), self.ship.decks[0].width - 1))
            y = max(0, min(int(y), self.ship.decks[0].height - 1))
            self.drag_end = (x, y)
            self._update_preview()
    
    def end_drag(self):
        """Place cables based on preview"""
        for x, y in self.preview_cables:
            self.add_cable(x, y)
        self.preview_cables.clear()
        self.drag_start = None
        self.drag_end = None
    
    def _update_preview(self):
        """Update preview cables based on drag coordinates"""
        self.preview_cables.clear()
        if not self.drag_start or not self.drag_end:
            return
            
        x1, y1 = self.drag_start
        x2, y2 = self.drag_end
        
        # Create a path of coordinates between start and end
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        n = 1 + dx + dy
        x_inc = 1 if x2 > x1 else -1
        y_inc = 1 if y2 > y1 else -1
        error = dx - dy
        dx *= 2
        dy *= 2

        for _ in range(n):
            self.preview_cables.add((x, y))
            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx
    
    def update_networks(self):
        """Public method to update cable networks and power distribution"""
        self._update_networks()
    
    def _update_networks(self):
        """Internal method to update connected cable networks and power distribution"""
        # Clear existing networks and module connections
        self.networks = []
        visited_cables = set()
        
        # Reset all module power
        if self.ship and self.ship.decks:
            for deck in self.ship.decks:
                for y in range(deck.height):
                    for x in range(deck.width):
                        if deck.tiles[y][x].module and not isinstance(deck.tiles[y][x].module, ReactorModule):
                            deck.tiles[y][x].module.power_available = 0

        # Find all connected networks
        for pos, cable in self.cables.items():
            if pos not in visited_cables:
                network = self._find_connected_network(pos, visited_cables)
                if network:
                    self.networks.append(network)
                    self._distribute_power(network)
    
    def _find_connected_network(self, start_pos, visited):
        """Find all connected cables and modules in a network"""
        network = {
            'cables': set(),
            'modules': set(),
            'total_power': 0,
            'total_required': 0
        }
        
        to_visit = [start_pos]
        while to_visit:
            pos = to_visit.pop()
            if pos in visited:
                continue
                
            visited.add(pos)
            network['cables'].add(pos)
            x, y = pos
            
            # Check adjacent tiles for modules and cables
            adjacent = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
            for adj_x, adj_y in adjacent:
                # Check for connected modules
                if (0 <= adj_x < self.ship.decks[0].width and 
                    0 <= adj_y < self.ship.decks[0].height):
                    tile = self.ship.decks[0].tiles[adj_y][adj_x]
                    if tile.module:
                        network['modules'].add(tile.module)
                        if isinstance(tile.module, ReactorModule):
                            network['total_power'] += tile.module.power_output
                        else:
                            network['total_required'] += tile.module.power_required
                
                # Check for connected cables
                adj_pos = (adj_x, adj_y)
                if adj_pos in self.cables and adj_pos not in visited:
                    to_visit.append(adj_pos)
        
        return network
    
    def _distribute_power(self, network):
        """Distribute power from reactors to modules in network"""
        if not network['modules']:
            return
        
        # Calculate available power per module
        power_per_module = min(
            network['total_power'] / max(1, len(network['modules']) - 1),  # -1 for reactor
            network['total_required']
        )
        
        # Distribute power to modules
        for module in network['modules']:
            if not isinstance(module, ReactorModule):
                module.power_available = min(power_per_module, module.power_required)