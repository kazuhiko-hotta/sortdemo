import gi
import random
from gi.repository import Gtk, Gdk

class SortCanvas(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        # Pass None as user_data explicitly
        self.set_draw_func(self.draw_func, None)
        
        # Request a minimum size
        self.set_content_width(600)
        self.set_content_height(400)
        
        self.data = []
        self.active_indices = []

    def generate_data(self, size):
        print(f"Generating data with size: {size}") # Debug
        self.data = list(range(1, size + 1))
        random.shuffle(self.data)
        self.active_indices = []
        self.queue_draw()

    def update_view(self, active_indices):
        self.active_indices = active_indices
        self.queue_draw()

    def draw_func(self, area, cr, width, height, user_data):
        # Debug output to check if drawing happens
        # print(f"Draw func called: w={width}, h={height}, data_len={len(self.data)}")

        # Fill background with white explicitly
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        if not self.data:
            return

        n = len(self.data)
        if n == 0:
            return

        bar_width = width / n
        max_val = max(self.data) if self.data else 1
        
        # If bars are too thin, skip drawing borders
        draw_border = bar_width > 3

        for i, value in enumerate(self.data):
            bar_height = (value / max_val) * height
            
            # Default color: Blue
            r, g, b = 0.2, 0.4, 0.8
            
            # Highlight active elements: Red
            if i in self.active_indices:
                r, g, b = 0.9, 0.2, 0.2

            cr.set_source_rgb(r, g, b)
            cr.rectangle(i * bar_width, height - bar_height, bar_width, bar_height)
            cr.fill()
            
            if draw_border:
                # Border
                cr.set_source_rgb(0, 0, 0)
                cr.set_line_width(1)
                cr.rectangle(i * bar_width, height - bar_height, bar_width, bar_height)
                cr.stroke()
