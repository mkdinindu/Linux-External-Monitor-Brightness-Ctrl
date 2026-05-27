import gi
import subprocess
from gi.repository import GLib
gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')

from gi.repository import Gtk, AyatanaAppIndicator3


def set_brightness(display, value):
    subprocess.Popen([
        "ddcutil",
        "--display", str(display),
        "setvcp",
        "10",
        str(int(value))
    ])


def get_monitors():
    try:
        output = subprocess.check_output(
            ["ddcutil", "detect"]
        ).decode()

        monitors = []

        current_display = None
        current_name = None

        for line in output.splitlines():

            line = line.strip()

            # Detect display number
            if line.startswith("Display "):
                parts = line.split()

                if len(parts) >= 2:
                    current_display = parts[1]

            # Detect monitor model
            if line.startswith("Model:"):
                current_name = line.split("Model:")[1].strip()

                # Only add valid external displays
                if current_display and current_name:
                    monitors.append({
                        "display": current_display,
                        "name": current_name
                    })

        return monitors

    except Exception as e:
        print("DDC detect failed:", e)
        return []


class BrightnessWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="Monitor Brightness")

        self.set_default_size(300, 200)
        self.set_border_width(10)

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )

        self.add(box)

        monitors = get_monitors()

        if not monitors:
            label = Gtk.Label(label="No DDC monitors detected")
            box.pack_start(label, False, False, 0)

        for monitor in monitors:

            name = monitor["name"]
            display = monitor["display"]

            label = Gtk.Label(label=name)
            box.pack_start(label, False, False, 0)

            slider = Gtk.Scale.new_with_range(
                Gtk.Orientation.HORIZONTAL,
                0,
                100,
                1
            )

            slider.set_value(70)

            slider.connect(
                "value-changed",
                self.on_slider_changed,
                display
            )

            box.pack_start(slider, False, False, 0)

        self.show_all()

    def on_slider_changed(self, slider, display):

        value = int(slider.get_value())

        # Cancel previous timer
        if hasattr(self, "timers") is False:
            self.timers = {}

        if display in self.timers:
            GLib.source_remove(self.timers[display])

        # Start new debounce timer
        timer_id = GLib.timeout_add(
            120,
            self.apply_brightness,
            display,
            value
        )

        self.timers[display] = timer_id
        
    def apply_brightness(self, display, value):

        set_brightness(display, value)

    # Remove timer reference
        if display in self.timers:
            del self.timers[display]

        return False


class TrayApp:

    def __init__(self):

        self.window = None

        self.indicator = AyatanaAppIndicator3.Indicator.new(
            "brightness-controller",
            "display-brightness-symbolic",
            AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )

        self.indicator.set_status(
            AyatanaAppIndicator3.IndicatorStatus.ACTIVE
        )

        menu = Gtk.Menu()

        open_item = Gtk.MenuItem(label="Brightness Control")
        open_item.connect("activate", self.open_window)
        menu.append(open_item)

        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit)
        menu.append(quit_item)

        menu.show_all()

        self.indicator.set_menu(menu)

    def open_window(self, source):

        if self.window is None:
            self.window = BrightnessWindow()

            self.window.connect(
                "destroy",
                self.on_window_destroy
            )

        self.window.show_all()
        self.window.present()

    def on_window_destroy(self, widget):
        self.window = None

    def quit(self, source):
        Gtk.main_quit()


TrayApp()
Gtk.main()
