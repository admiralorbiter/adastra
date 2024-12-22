class Camera:
    def __init__(self, screen_width: int, screen_height: int):
        self.x = 0
        self.y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.panning = False
        self.pan_start_x = 0
        self.pan_start_y = 0

    def start_pan(self, mouse_x: int, mouse_y: int):
        """Start camera panning from the given mouse position"""
        self.panning = True
        self.pan_start_x = mouse_x - self.x
        self.pan_start_y = mouse_y - self.y

    def update_pan(self, mouse_x: int, mouse_y: int):
        """Update camera position during panning"""
        if self.panning:
            self.x = mouse_x - self.pan_start_x
            self.y = mouse_y - self.pan_start_y

    def stop_pan(self):
        """Stop camera panning"""
        self.panning = False

    def center_on(self, width: int, height: int):
        """Center the camera on an area of the given size"""
        self.x = (self.screen_width - width) // 2
        self.y = (self.screen_height - height) // 2

    def screen_to_world(self, screen_x: int, screen_y: int):
        """Convert screen coordinates to world coordinates"""
        world_x = (screen_x - self.x)
        world_y = (screen_y - self.y)
        return world_x, world_y

    def world_to_screen(self, world_x: int, world_y: int):
        """Convert world coordinates to screen coordinates"""
        screen_x = world_x + self.x
        screen_y = world_y + self.y
        return screen_x, screen_y 

    def move(self, dx, dy):
        """Move the camera by the given delta x and y amounts"""
        self.x += dx
        self.y += dy