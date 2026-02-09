import gi
from gi.repository import Gtk, Adw, GLib
from .canvas import SortCanvas
from .algorithms import BubbleSort, InsertionSort, QuickSort, MergeSort

class SortDemoWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("Sort Demo")
        self.set_default_size(800, 600)

        # Main content box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)

        # Header Bar
        header_bar = Adw.HeaderBar()
        main_box.append(header_bar)

        # Algorithm Selector
        self.algo_model = Gtk.StringList()
        self.algorithms = {
            "Bubble Sort": BubbleSort,
            "Insertion Sort": InsertionSort,
            "Quick Sort": QuickSort,
            "Merge Sort": MergeSort
        }
        for name in self.algorithms.keys():
            self.algo_model.append(name)

        self.algo_dropdown = Gtk.DropDown(model=self.algo_model)
        header_bar.set_title_widget(self.algo_dropdown)

        # Controls in Header
        self.start_btn = Gtk.Button(label="Start")
        self.start_btn.connect("clicked", self.on_start_clicked)
        header_bar.pack_start(self.start_btn)

        reset_btn = Gtk.Button(label="Reset")
        reset_btn.connect("clicked", self.on_reset_clicked)
        header_bar.pack_end(reset_btn)

        # Canvas Area
        self.canvas = SortCanvas()
        self.canvas.set_vexpand(True)
        self.canvas.set_hexpand(True)
        main_box.append(self.canvas)

        # Bottom Controls
        controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        controls_box.set_margin_top(10)
        controls_box.set_margin_bottom(10)
        controls_box.set_margin_start(10)
        controls_box.set_margin_end(10)
        main_box.append(controls_box)

        # Speed Slider
        controls_box.append(Gtk.Label(label="Speed:"))
        self.speed_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 100, 1)
        self.speed_scale.set_value(50)
        self.speed_scale.set_hexpand(True)
        controls_box.append(self.speed_scale)

        # Size Slider
        controls_box.append(Gtk.Label(label="Size:"))
        self.size_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 10, 1000, 10)
        self.size_scale.set_value(50)
        self.size_scale.set_hexpand(True)
        self.size_scale.connect("value-changed", self.on_size_changed)
        controls_box.append(self.size_scale)
        
        # Status Label
        self.status_label = Gtk.Label(label="Steps: 0")
        controls_box.append(self.status_label)

        # State
        self.generator = None
        self.timeout_id = None
        self.is_running = False

        # Connect map signal to ensure initial draw
        self.connect("map", self.on_map)

        # Initial data generation
        self.on_size_changed(self.size_scale)

    def on_map(self, widget):
        self.canvas.queue_draw()

    def on_size_changed(self, scale):
        size = int(scale.get_value())
        self.canvas.generate_data(size)
        # Stop sorting but don't clear generator if we want to support resizing during sort (optional)
        # For now, we reset everything on resize
        self.stop_sorting()
        self.status_label.set_label("Steps: 0")

    def on_reset_clicked(self, btn):
        self.on_size_changed(self.size_scale)

    def on_start_clicked(self, btn):
        if self.is_running:
            # Pause behavior
            self.is_running = False
            if self.timeout_id:
                GLib.source_remove(self.timeout_id)
                self.timeout_id = None
            btn.set_label("Start")
        else:
            # Start/Resume behavior
            self.start_sorting()
            btn.set_label("Pause")

    def start_sorting(self):
        if not self.generator:
            algo_name = self.algo_model.get_string(self.algo_dropdown.get_selected())
            algo_class = self.algorithms[algo_name]
            self.generator = algo_class(self.canvas.data).sort()
        
        self.is_running = True
        self.schedule_tick()

    def stop_sorting(self):
        self.is_running = False
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        
        self.generator = None
        self.start_btn.set_label("Start")

    def schedule_tick(self):
        if not self.is_running:
            return

        # Calculate interval based on current slider value
        # Value 1 (slow) -> 100ms, Value 100 (fast) -> 1ms
        interval = max(1, int(101 - self.speed_scale.get_value()))
        self.timeout_id = GLib.timeout_add(interval, self.on_tick)

    def on_tick(self):
        # Clear the timeout_id because this function was called (one-shot)
        self.timeout_id = None
        
        if not self.is_running:
            return False

        try:
            active_indices, steps = next(self.generator)
            self.canvas.update_view(active_indices)
            self.status_label.set_label(f"Steps: {steps}")
            
            # Schedule the next tick
            self.schedule_tick()
            return False # Don't repeat automatically, we manually scheduled the next one
            
        except StopIteration:
            self.stop_sorting()
            self.canvas.update_view([])
            return False
