import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gio
import urllib.request
import json
from multiprocessing import Pool
import subprocess as sp

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="AYAYA")

        self.main_box = Gtk.VBox(spacing=5)
        self.search_box = Gtk.HBox(spacing=5)
        self.main_box.pack_start(self.search_box, False, False, 0)
        self.add(self.main_box)

        self.entry = Gtk.Entry()
        self.entry.connect("activate", self.on_entry_activate)
        self.search_box.pack_start(self.entry, True, True, 0)

        self.button = Gtk.Button(label="AYAYA")
        self.button.connect("clicked", self.on_search_button_clicked)
        self.search_box.pack_start(self.button, True, True, 0)

        self.grid = Gtk.FlowBox()
        self.grid.set_selection_mode(Gtk.SelectionMode.NONE)
        self.grid.set_min_children_per_line(10)
        self.grid.set_max_children_per_line(10)
        self.main_box.pack_end(self.grid, True, True, 0)

    def on_entry_activate(self, uwu):
        self.on_search_button_clicked(uwu)

    def on_search_button_clicked(self, widget):
        search = self.entry.get_text()
        url = f"https://api.frankerfacez.com/v1/emotes?q={search}&sensitive=false&sort=count&high_dpi=off&page=1&per_page=60"
        request = urllib.request.urlopen(url).read().decode("utf-8")
        json_emotes = json.loads(request)["emoticons"]

        emotes = []
        for e in json_emotes:
            emotes.append((e["name"], e['id']))

        with Pool(processes=30) as p:
            owo = p.map_async(get_image, emotes).get()

        for uwu in owo:
            name, im_id, response = uwu
            input_stream = Gio.MemoryInputStream.new_from_data(response, None)
            pixbuf = Pixbuf.new_from_stream(input_stream, None)
            image = Gtk.Image()
            image.set_from_pixbuf(pixbuf)
            b = Gtk.Button(label = name[:10])
            b.set_always_show_image(True)
            b.set_image(image)
            b.set_image_position(Gtk.PositionType.TOP)
            b.connect("clicked", kopi, im_id)
            self.grid.add(b)
        self.show_all()

    #def fetch_all_emotes(self, emotes):
    #    http = urllib3.PoolManager()
    #
    #    for e in emotes:
    #        r = http.request("GET", f"https://cdn.frankerfacez.com/emoticon/{e['id']}/2", preload_content = False)
    #        input_stream = Gio.MemoryInputStream.new_from_data(r.read(), None)
    #        pixbuf = Pixbuf.new_from_stream(input_stream, None)
    #        image = Gtk.Image()
    #        image.set_from_pixbuf(pixbuf)
    #        e["image"] = image
    #
    #    return emotes

def kopi(button, im_id):
    url = f"https://cdn.frankerfacez.com/emoticon/{im_id}/2"
    sp.run(f"convert {url} -filter catrom -unsharp 2 -resize x48 png:- | xclip -selection clipboard -t image/png", shell=True)
    Gtk.main_quit()

def get_image(e):
    name, im_id = e
    url = f"https://cdn.frankerfacez.com/emoticon/{im_id}/2"
    response = urllib.request.urlopen(url)
    return name, im_id, response.read()

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

