class Cable:
    def __init__(self):
        self.powered = False
        self.network_id = None  # For tracking connected cables

class CableSystem:
    def __init__(self):
        self.cables = {}  # (x, y) -> Cable
        self.preview_cables = set()  # Stores coordinates for cable preview
        self.drag_start = None
        self.drag_end = None
    
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
        self.drag_start = (x, y)
        self.preview_cables.clear()
    
    def update_drag(self, x: int, y: int):
        """Update cable preview during drag"""
        if self.drag_start:
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
    
    def _update_networks(self):
        """Update connected cable networks"""
        # Implement network connectivity logic here
        pass 