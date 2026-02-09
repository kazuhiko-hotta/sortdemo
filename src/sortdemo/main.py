import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw
from .window import SortDemoWindow


class SortDemoApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id='com.example.SortDemo',
                         flags=0,
                         **kwargs)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = SortDemoWindow(application=self)
        win.present()


def main():
    app = SortDemoApp()
    return app.run(sys.argv)


if __name__ == '__main__':
    sys.exit(main())
