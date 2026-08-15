import json
import os
import tkinter as tk
import urllib.request
from tkinter import ttk, messagebox, filedialog

try:
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

if PIL_AVAILABLE:
    RESAMPLING_LANCZOS = getattr(getattr(Image, "Resampling", Image), "LANCZOS")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPIRIT_LIST_FILE = os.path.join(BASE_DIR, "esprits.txt")
STATE_FILE = os.path.join(BASE_DIR, "etat_esprits.json")
MASTERED_STATE_FILE = os.path.join(BASE_DIR, "etat_esprits_maitrise.json")
SPIRIT_IMAGES_FILE = os.path.join(BASE_DIR, "esprits_images.json")
IMAGE_CACHE_DIR = os.path.join(BASE_DIR, "cache_esprits")

VARIANT_META = {
    "NORMAL": {"label": "Normal", "suffix": "basic"},
    "GOLD": {"label": "Or", "suffix": "gold"},
    "GUMMY": {"label": "Gelifie", "suffix": "candy"},
    "GALAXY": {"label": "Galaxie", "suffix": "galaxy"},
    "GEM": {"label": "Gemme", "suffix": "gem"},
    "HOLOFOIL": {"label": "Holographique", "suffix": "holofoil"},
    "CUBE": {"label": "Cube", "suffix": "cube"},
    "QUACK": {"label": "Coin-coin", "suffix": "quack"},
}

RARITY_BY_OFFICIAL = {
    "WATER": "Rare",
    "EARTH": "Rare",
    "FIRE": "Rare",
    "FISHY": "Rare",
    "AIR": "Rare",
    "DUCK": "Epic",
    "GHOST": "Epic",
    "DEMON": "Epic",
    "KING": "Epic",
    "AURA": "Epic",
    "STRIKER": "Epic",
    "DREAM": "Legendary",
    "PUNK": "Legendary",
    "BOSS": "Legendary",
    "SEVEN": "Legendary",
    "PEELY": "Legendary",
    "LLAMA": "Legendary",
    "BATMAN": "Mythic",
    "GRIM REAPER": "Mythic",
    "ZERO POINT": "Mythic",
    "BURNT PEANUT": "Mythic",
    "VINI JR": "Mythic",
    "POLLO": "Mythic",
    "JOHN WICK": "Mythic",
    "IRONMOUSE": "Mythic",
}

RARITY_ORDER = {"Rare": 0, "Epic": 1, "Legendary": 2, "Mythic": 3}

MOBILE_COLORS = {
    "bg3": "#222222",
    "border": "#2a2a2a",
    "text2": "#aaaaaa",
    "gold": "#f4c95d",
    "gold2": "#c47d0a",
    "rare": "#3a7bd5",
    "epic": "#7c3aed",
    "legend": "#e58c18",
    "mythic": "#d946ef",
}

# Certains fichiers Holographiques ont un suffixe special dans la source.
VARIANT_SUFFIX_OVERRIDES = {
    ("AIR", "HOLOFOIL"): "holo",
    ("GHOST", "HOLOFOIL"): "holo",
    ("DUCK", "HOLOFOIL"): "holo",
}

# Liste derivee des donnees source pour obtenir exactement les entrees publiees.
SPRITE_VARIANTS_BY_OFFICIAL = {
    "WATER": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM", "HOLOFOIL", "QUACK"],
    "EARTH": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM", "CUBE", "QUACK"],
    "FIRE": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL", "CUBE", "QUACK"],
    "FISHY": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "CUBE"],
    "AIR": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL"],
    "DUCK": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM"],
    "GHOST": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL"],
    "DEMON": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM"],
    "KING": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL"],
    "AURA": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM"],
    "STRIKER": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL"],
    "DREAM": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "CUBE"],
    "PUNK": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "CUBE"],
    "BOSS": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "CUBE"],
    "SEVEN": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL"],
    "PEELY": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL"],
    "LLAMA": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM"],
    "BATMAN": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL", "CUBE"],
    "GRIM REAPER": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM", "HOLOFOIL", "CUBE"],
    "ZERO POINT": ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM", "HOLOFOIL", "CUBE", "QUACK"],
    "BURNT PEANUT": ["NORMAL"],
    "VINI JR": ["NORMAL"],
    "POLLO": ["NORMAL"],
    "JOHN WICK": ["NORMAL"],
    "IRONMOUSE": ["NORMAL"],
}

# Tu peux modifier cette liste dans esprits.txt (un nom par ligne).
DEFAULT_SPIRITS = [
    "Eau",
    "Terre",
    "Feu",
    "Poiscaille",
    "Air",
    "Canard",
    "Fantome",
    "Demon",
    "Roi",
    "Aura",
    "Buteur",
    "Reve",
    "Punk",
    "Boss",
    "Seven",
    "Peeky Peely",
    "Lootin' Llama",
    "Batman",
    "Faucheuse",
    "Point Zero",
    "Cacahuete Grillee",
    "Vini Jr.",
    "Pollo",
    "John Wick",
    "Ironmouse",
]


def ensure_spirit_list_file():
    if not os.path.exists(SPIRIT_LIST_FILE):
        with open(SPIRIT_LIST_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(DEFAULT_SPIRITS) + "\n")


def load_spirit_names():
    ensure_spirit_list_file()
    names = []
    with open(SPIRIT_LIST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            name = line.strip()
            if name:
                names.append(name)

    deduped = []
    seen = set()
    for name in names:
        key = name.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(name)
    return deduped


def load_state(spirit_names):
    if not os.path.exists(STATE_FILE):
        return {name: False for name in spirit_names}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {name: False for name in spirit_names}

    state = {}
    for name in spirit_names:
        direct_value = data.get(name, None)
        if direct_value is not None:
            state[name] = bool(direct_value)
            continue

        # Compatibilite: un ancien etat pouvait stocker uniquement "NomEsprit".
        if " - Normal" in name:
            legacy_name = name.split(" - Normal", 1)[0].strip()
            state[name] = bool(data.get(legacy_name, False))
        else:
            state[name] = False
    return state


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def load_mastered_state(spirit_names):
    if not os.path.exists(MASTERED_STATE_FILE):
        return {name: False for name in spirit_names}

    try:
        with open(MASTERED_STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {name: False for name in spirit_names}

    state = {}
    for name in spirit_names:
        state[name] = bool(data.get(name, False))
    return state


def save_mastered_state(state):
    with open(MASTERED_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def load_spirit_images_map():
    if not os.path.exists(SPIRIT_IMAGES_FILE):
        return {}

    try:
        with open(SPIRIT_IMAGES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

    if not isinstance(data, list):
        return {}

    result = {}
    for item in data:
        if not isinstance(item, dict):
            continue
        name = str(item.get("nom", "")).strip()
        image_url = str(item.get("image", "")).strip()
        if name and image_url:
            result[name] = item
    return result


def build_spirit_entries(images_map):
    entries = []

    for site_index, (_, item) in enumerate(images_map.items()):
        if not bool(item.get("released", True)):
            continue

        base_name = str(item.get("nom", "")).strip()
        official = str(item.get("nom_officiel", "")).strip().upper()
        image_url = str(item.get("image", "")).strip()
        slug = str(item.get("slug_source", "")).strip()
        if not base_name or not official or not image_url:
            continue

        variants = SPRITE_VARIANTS_BY_OFFICIAL.get(official, ["NORMAL"])
        for variant in variants:
            meta = VARIANT_META.get(variant)
            if meta is None:
                continue

            label = f"{base_name} - {meta['label']}"
            variant_suffix = VARIANT_SUFFIX_OVERRIDES.get((official, variant), meta["suffix"])
            variant_image = image_url.replace("_basic.webp", f"_{variant_suffix}.webp")
            entries.append(
                {
                    "key": label,
                    "base_name": base_name,
                    "official": official,
                    "rarity": RARITY_BY_OFFICIAL.get(official, "Rare"),
                    "site_index": site_index,
                    "variant": variant,
                    "variant_label": meta["label"],
                    "variant_suffix": variant_suffix,
                    "image": variant_image,
                    "slug": slug,
                }
            )

    # Tri stable: ordre du site puis ordre de variante.
    variant_order = {key: idx for idx, key in enumerate(VARIANT_META.keys())}
    entries.sort(key=lambda e: (e.get("site_index", 10_000), variant_order.get(e["variant"], 99)))
    return entries


class SpiritOverlayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tracker Esprits Fortnite")
        self.root.geometry("420x620+20+20")
        self.root.configure(bg="#141414")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.92)

        self.drag_data = {"x": 0, "y": 0}

        self.spirit_images = load_spirit_images_map()
        self.spirit_entries = build_spirit_entries(self.spirit_images)

        if self.spirit_entries:
            self.spirit_names = [entry["key"] for entry in self.spirit_entries]
            self.entry_by_name = {entry["key"]: entry for entry in self.spirit_entries}
        else:
            # Fallback si le JSON n'est pas disponible.
            self.spirit_names = load_spirit_names()
            self.entry_by_name = {
                name: {
                    "key": name,
                    "base_name": name,
                    "official": name.upper(),
                    "rarity": "Rare",
                    "site_index": idx,
                    "variant": "NORMAL",
                    "variant_label": "Normal",
                    "variant_suffix": "basic",
                    "image": str(self.spirit_images.get(name, {}).get("image", "")).strip(),
                    "slug": str(self.spirit_images.get(name, {}).get("slug_source", "")).strip(),
                }
                for idx, name in enumerate(self.spirit_names)
            }

        self.state = load_state(self.spirit_names)
        self.mastered_state = load_mastered_state(self.spirit_names)
        self.vars = {}
        self.row_frames = {}
        self.crown_buttons = {}
        self.tk_images = {}
        self.group_widgets = {}
        self.entry_to_group = {}
        self.collapsed_groups = set()
        self._pillow_warning_shown = False

        self.active_filter = "all"
        self.active_rarity = ""
        self.sort_mode = tk.StringVar(value="Site")

        self._build_ui()
        self._render_spirits()
        self._update_progress()

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        header = tk.Frame(self.root, bg="#111111", height=40)
        header.pack(fill="x")
        header.bind("<ButtonPress-1>", self._start_drag)
        header.bind("<B1-Motion>", self._on_drag)

        title = tk.Label(
            header,
            text="FORTNITE - TRACKER ESPRITS",
            fg="#f6f6f6",
            bg="#111111",
            font=("Segoe UI", 10, "bold"),
        )
        title.pack(side="left", padx=10)
        title.bind("<ButtonPress-1>", self._start_drag)
        title.bind("<B1-Motion>", self._on_drag)

        close_btn = tk.Button(
            header,
            text="X",
            command=self.root.destroy,
            fg="#ffffff",
            bg="#8f1d1d",
            relief="flat",
            width=3,
            activebackground="#b32121",
            activeforeground="#ffffff",
        )
        close_btn.pack(side="right", padx=6, pady=6)

        controls = tk.Frame(self.root, bg="#141414")
        controls.pack(fill="x", padx=10, pady=10)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._apply_filters())

        search_entry = tk.Entry(
            controls,
            textvariable=self.search_var,
            bg="#222222",
            fg="#f6f6f6",
            insertbackground="#f6f6f6",
            relief="flat",
            font=("Segoe UI", 10),
        )
        search_entry.pack(fill="x", pady=(0, 8), ipady=6)
        search_entry.insert(0, "")

        filter_line = tk.Frame(controls, bg="#141414")
        filter_line.pack(fill="x", pady=(0, 6))

        self.filter_buttons = {}

        for key, label in (("all", "Tous"), ("owned", "Obtenus"), ("missing", "Manquants")):
            btn = tk.Button(
                filter_line,
                text=label,
                command=lambda k=key: self._set_filter(k),
                relief="flat",
                bg=MOBILE_COLORS["bg3"],
                fg=MOBILE_COLORS["text2"],
                activebackground="#3a3a3a",
                activeforeground="#ffffff",
                font=("Segoe UI", 8, "bold"),
                padx=8,
                pady=3,
            )
            btn.pack(side="left", padx=(0, 6))
            self.filter_buttons[key] = btn

        rarity_line = tk.Frame(controls, bg="#141414")
        rarity_line.pack(fill="x", pady=(0, 6))

        tk.Label(
            rarity_line,
            text="Rareté:",
            bg="#141414",
            fg="#d6d6d6",
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=(0, 6))

        self.rarity_buttons = {}
        for key, label in (("", "Toutes"), ("Rare", "Rare"), ("Epic", "Epic"), ("Legendary", "Legendaire"), ("Mythic", "Mythique")):
            btn = tk.Button(
                rarity_line,
                text=label,
                command=lambda k=key: self._set_rarity(k),
                relief="flat",
                bg=MOBILE_COLORS["bg3"],
                fg=MOBILE_COLORS["text2"],
                activebackground="#3a3a3a",
                activeforeground="#ffffff",
                font=("Segoe UI", 8),
                padx=6,
                pady=2,
            )
            btn.pack(side="left", padx=(0, 4))
            self.rarity_buttons[key] = btn

        order_line = tk.Frame(controls, bg="#141414")
        order_line.pack(fill="x")

        tk.Label(
            order_line,
            text="Ordre:",
            bg="#141414",
            fg="#d6d6d6",
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=(0, 6))

        order_menu = tk.OptionMenu(
            order_line,
            self.sort_mode,
            "Site",
            "Rareté",
            "Nom (A-Z)",
            "Progression",
            command=lambda _v: self._apply_filters(),
        )
        order_menu.config(
            bg="#222222",
            fg="#f0f0f0",
            activebackground="#333333",
            activeforeground="#ffffff",
            relief="flat",
            highlightthickness=0,
            font=("Segoe UI", 9),
        )
        order_menu["menu"].config(bg="#222222", fg="#f0f0f0", activebackground="#333333")
        order_menu.pack(side="left")

        self._refresh_filter_button_states()

        button_line = tk.Frame(self.root, bg="#141414")
        button_line.pack(fill="x", padx=10)

        refresh_btn = tk.Button(
            button_line,
            text="Recharger la liste",
            command=self._reload_from_file,
            bg="#1f6f5d",
            fg="#ffffff",
            relief="flat",
            activebackground="#288d75",
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=5,
        )
        refresh_btn.pack(side="left")

        reset_btn = tk.Button(
            button_line,
            text="Tout decocher",
            command=self._reset_all,
            bg="#444444",
            fg="#ffffff",
            relief="flat",
            activebackground="#666666",
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=5,
        )
        reset_btn.pack(side="right")

        sync_line = tk.Frame(self.root, bg="#141414")
        sync_line.pack(fill="x", padx=10, pady=(6, 0))

        import_btn = tk.Button(
            sync_line,
            text="\u2b06 Importer depuis mobile",
            command=self._import_from_mobile,
            bg="#2a3a6a",
            fg="#ffffff",
            relief="flat",
            activebackground="#3a4e8a",
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=5,
        )
        import_btn.pack(side="left", fill="x", expand=True)

        export_btn = tk.Button(
            sync_line,
            text="\u2b07 Exporter vers mobile",
            command=self._export_for_mobile,
            bg="#1f4a3a",
            fg="#ffffff",
            relief="flat",
            activebackground="#2a6050",
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=5,
        )
        export_btn.pack(side="right", fill="x", expand=True)

        self.progress_label = tk.Label(
            self.root,
            text="Progression: 0/0",
            bg="#141414",
            fg="#f4c95d",
            font=("Segoe UI", 10, "bold"),
        )
        self.progress_label.pack(anchor="w", padx=10, pady=(10, 6))

        list_container = tk.Frame(self.root, bg="#141414")
        list_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.canvas = tk.Canvas(
            list_container,
            bg="#1a1a1a",
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.list_frame = tk.Frame(self.canvas, bg="#1a1a1a")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.list_frame.bind("<Configure>", self._on_list_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        footer = tk.Label(
            self.root,
            text="Mode variantes actif: total auto depuis le JSON. Clique Recharger apres modif.",
            bg="#141414",
            fg="#a9a9a9",
            font=("Segoe UI", 8),
        )
        footer.pack(anchor="w", padx=10, pady=(0, 8))

    def _on_list_configure(self, _event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def _on_drag(self, event):
        x = self.root.winfo_x() + event.x - self.drag_data["x"]
        y = self.root.winfo_y() + event.y - self.drag_data["y"]
        self.root.geometry(f"+{x}+{y}")

    def _render_spirits(self):
        for child in self.list_frame.winfo_children():
            child.destroy()

        self.vars.clear()
        self.row_frames.clear()
        self.crown_buttons.clear()
        self.tk_images.clear()
        self.group_widgets.clear()
        self.entry_to_group.clear()

        grouped = {}
        for name in self.spirit_names:
            entry = self.entry_by_name.get(name, {})
            base_name = str(entry.get("base_name", "")).strip() or name
            grouped.setdefault(base_name, []).append(name)
            self.entry_to_group[name] = base_name

        for base_name, names in grouped.items():
            group_frame = tk.Frame(self.list_frame, bg="#1f1f1f", bd=1, relief="flat")
            group_frame.pack(fill="x", padx=4, pady=4)

            header = tk.Frame(group_frame, bg="#252525")
            header.pack(fill="x")

            # Avatar: utilise la variante Normal si disponible.
            avatar_name = names[0]
            for candidate in names:
                candidate_entry = self.entry_by_name.get(candidate, {})
                if str(candidate_entry.get("variant", "")).upper() == "NORMAL":
                    avatar_name = candidate
                    break

            avatar = tk.Label(
                header,
                width=44,
                height=44,
                bg="#252525",
                fg="#d8d8d8",
                text="IMG",
                font=("Segoe UI", 7, "bold"),
            )
            avatar.pack(side="left", padx=(6, 4), pady=6)

            photo = self._get_spirit_photo(avatar_name, size=40)
            if photo is not None:
                avatar.config(image=photo, text="")
                self.tk_images[f"group::{base_name}"] = photo

            info = tk.Frame(header, bg="#252525")
            info.pack(side="left", fill="x", expand=True)

            title = tk.Label(
                info,
                text=base_name,
                bg="#252525",
                fg="#f2f2f2",
                font=("Segoe UI", 10, "bold"),
                anchor="w",
            )
            title.pack(fill="x", padx=(2, 0), pady=(7, 0))

            subtitle = tk.Label(
                info,
                text="",
                bg="#252525",
                fg="#c8c8c8",
                font=("Segoe UI", 9),
                anchor="w",
            )
            subtitle.pack(fill="x", padx=(2, 0), pady=(0, 7))

            chevron = tk.Label(
                header,
                text="▾",
                bg="#252525",
                fg="#d0d0d0",
                font=("Segoe UI", 11, "bold"),
                width=2,
            )
            chevron.pack(side="right", padx=(0, 8))

            variants_container = tk.Frame(group_frame, bg="#1f1f1f")
            variants_container.pack(fill="x")

            self.group_widgets[base_name] = {
                "frame": group_frame,
                "variants": variants_container,
                "subtitle": subtitle,
                "chevron": chevron,
                "entries": list(names),
                "rarity": str(self.entry_by_name.get(avatar_name, {}).get("rarity", "Rare")),
                "site_index": min(
                    int(self.entry_by_name.get(n, {}).get("site_index", 10_000))
                    for n in names
                ),
            }

            def toggle_group(group_name=base_name):
                if group_name in self.collapsed_groups:
                    self.collapsed_groups.remove(group_name)
                else:
                    self.collapsed_groups.add(group_name)
                self._apply_filters()

            for widget in (header, avatar, info, title, subtitle, chevron):
                widget.bind("<Button-1>", lambda _e, g=base_name: toggle_group(g))

            for name in names:
                row = tk.Frame(variants_container, bg="#1f1f1f")
                row.pack(fill="x", padx=4, pady=2)

                image_label = tk.Label(
                    row,
                    width=30,
                    height=30,
                    bg="#1f1f1f",
                    fg="#d8d8d8",
                    text="",
                    font=("Segoe UI", 6, "bold"),
                )
                image_label.pack(side="left", padx=(6, 4), pady=4)

                photo = self._get_spirit_photo(name, size=26)
                if photo is not None:
                    image_label.config(image=photo)
                    self.tk_images[name] = photo

                entry = self.entry_by_name.get(name, {})
                variant_label = str(entry.get("variant_label", "Normal")).strip() or "Normal"

                var = tk.BooleanVar(value=self.state.get(name, False))
                chk = tk.Checkbutton(
                    row,
                    text=variant_label,
                    variable=var,
                    command=lambda n=name: self._toggle_spirit(n),
                    bg="#1f1f1f",
                    fg="#f0f0f0",
                    activebackground="#1f1f1f",
                    activeforeground="#ffffff",
                    selectcolor="#1f1f1f",
                    anchor="w",
                    justify="left",
                    font=("Segoe UI", 9),
                )
                chk.pack(side="left", fill="x", expand=True, padx=(6, 2), pady=4)

                crown_btn = tk.Button(
                    row,
                    text="👑",
                    command=lambda n=name: self._toggle_mastered(n),
                    relief="flat",
                    font=("Segoe UI", 9, "bold"),
                    width=3,
                )
                crown_btn.pack(side="right", padx=(2, 8), pady=4)
                self.crown_buttons[name] = crown_btn
                self._update_crown_button(name)

                self.vars[name] = var
                self.row_frames[name] = row

            self._update_group_header(base_name)

        self._apply_filters()

    def _update_group_header(self, group_name):
        group = self.group_widgets.get(group_name)
        if not group:
            return

        names = group["entries"]
        total = len(names)
        owned = sum(1 for n in names if self.state.get(n, False))
        mastered = sum(1 for n in names if self.mastered_state.get(n, False))
        group["subtitle"].config(text=f"{owned}/{total} obtenues • 👑 {mastered}")

        collapsed = group_name in self.collapsed_groups
        group["chevron"].config(text="▸" if collapsed else "▾")

    def _set_filter(self, mode):
        self.active_filter = mode
        self._refresh_filter_button_states()
        self._apply_filters()

    def _set_rarity(self, rarity):
        self.active_rarity = rarity
        self._refresh_filter_button_states()
        self._apply_filters()

    def _refresh_filter_button_states(self):
        for key, btn in self.filter_buttons.items():
            active = key == self.active_filter
            btn.config(
                bg=MOBILE_COLORS["gold2"] if active else MOBILE_COLORS["bg3"],
                fg="#111111" if active else MOBILE_COLORS["text2"],
                activebackground=MOBILE_COLORS["gold2"] if active else "#333333",
                activeforeground="#111111" if active else "#ffffff",
            )

        for key, btn in self.rarity_buttons.items():
            active = key == self.active_rarity

            if active:
                if key == "Rare":
                    active_bg = MOBILE_COLORS["rare"]
                    active_fg = "#ffffff"
                elif key == "Epic":
                    active_bg = MOBILE_COLORS["epic"]
                    active_fg = "#ffffff"
                elif key == "Legendary":
                    active_bg = MOBILE_COLORS["legend"]
                    active_fg = "#111111"
                elif key == "Mythic":
                    active_bg = MOBILE_COLORS["mythic"]
                    active_fg = "#ffffff"
                else:
                    active_bg = MOBILE_COLORS["gold2"]
                    active_fg = "#111111"
            else:
                active_bg = MOBILE_COLORS["bg3"]
                active_fg = MOBILE_COLORS["text2"]

            btn.config(
                bg=active_bg,
                fg=active_fg,
                activebackground=active_bg if active else "#333333",
                activeforeground=active_fg if active else "#ffffff",
            )

    def _get_sorted_group_names(self):
        names = list(self.group_widgets.keys())
        mode = self.sort_mode.get()

        if mode == "Site":
            names.sort(key=lambda n: (self.group_widgets[n].get("site_index", 10_000), n.lower()))
            return names

        if mode == "Nom (A-Z)":
            names.sort(key=lambda n: n.lower())
            return names

        if mode == "Progression":
            def progress_key(group_name):
                entries = self.group_widgets[group_name]["entries"]
                total = len(entries) or 1
                owned = sum(1 for n in entries if self.state.get(n, False))
                ratio = owned / total
                return (-ratio, -owned, group_name.lower())

            names.sort(key=progress_key)
            return names

        # Defaut: ordre par rarete puis nom.
        names.sort(
            key=lambda n: (
                RARITY_ORDER.get(self.group_widgets[n].get("rarity", "Rare"), 99),
                n.lower(),
            )
        )
        return names

    def _toggle_spirit(self, name):
        self.state[name] = self.vars[name].get()
        if not self.state[name]:
            self.mastered_state[name] = False
        save_state(self.state)
        save_mastered_state(self.mastered_state)
        self._update_crown_button(name)
        group_name = self.entry_to_group.get(name)
        if group_name:
            self._update_group_header(group_name)
        self._update_progress()
        self._apply_filters()

    def _toggle_mastered(self, name):
        new_value = not bool(self.mastered_state.get(name, False))
        self.mastered_state[name] = new_value

        # Un esprit maîtrise doit toujours être obtenu.
        if new_value and not self.state.get(name, False):
            self.state[name] = True
            if name in self.vars:
                self.vars[name].set(True)

        save_state(self.state)
        save_mastered_state(self.mastered_state)
        self._update_crown_button(name)
        group_name = self.entry_to_group.get(name)
        if group_name:
            self._update_group_header(group_name)
        self._update_progress()
        self._apply_filters()

    def _update_crown_button(self, name):
        btn = self.crown_buttons.get(name)
        if not btn:
            return
        if self.mastered_state.get(name, False):
            btn.config(bg="#3b2d09", fg="#f4c95d", activebackground="#5a4511", activeforeground="#f4c95d")
        else:
            btn.config(bg="#2a2a2a", fg="#8e8e8e", activebackground="#3a3a3a", activeforeground="#c0c0c0")

    def _update_progress(self):
        total = len(self.spirit_names)
        owned = sum(1 for n in self.spirit_names if self.state.get(n, False))
        mastered = sum(1 for n in self.spirit_names if self.mastered_state.get(n, False))
        percent = int((owned / total) * 100) if total else 0
        self.progress_label.config(text=f"Progression: {owned}/{total} ({percent}%) | 👑 {mastered}")

    def _apply_filters(self):
        query = self.search_var.get().strip().lower()
        sorted_groups = self._get_sorted_group_names()
        visible_groups = []

        for group_name in sorted_groups:
            group = self.group_widgets[group_name]
            visible_in_group = 0
            collapsed = group_name in self.collapsed_groups

            group_rarity = str(group.get("rarity", "Rare"))
            rarity_ok = (not self.active_rarity) or (group_rarity == self.active_rarity)

            for name in group["entries"]:
                is_owned = self.state.get(name, False)
                entry = self.entry_by_name.get(name, {})
                variant_label = str(entry.get("variant_label", "")).lower()
                is_match = True
                if query:
                    is_match = (query in group_name.lower()) or (query in variant_label) or (query in name.lower())

                filter_ok = True
                if self.active_filter == "owned":
                    filter_ok = is_owned
                elif self.active_filter == "missing":
                    filter_ok = not is_owned

                is_visible = is_match and filter_ok and rarity_ok

                frame = self.row_frames[name]
                if is_visible:
                    visible_in_group += 1
                    if (not collapsed) and (not frame.winfo_ismapped()):
                        frame.pack(fill="x", padx=4, pady=2)
                    if collapsed and frame.winfo_ismapped():
                        frame.pack_forget()
                else:
                    if frame.winfo_ismapped():
                        frame.pack_forget()

            if visible_in_group > 0:
                visible_groups.append(group_name)
                if not group["frame"].winfo_ismapped():
                    group["frame"].pack(fill="x", padx=4, pady=4)
            else:
                if group["frame"].winfo_ismapped():
                    group["frame"].pack_forget()

            self._update_group_header(group_name)

            if collapsed or visible_in_group == 0:
                if group["variants"].winfo_ismapped():
                    group["variants"].pack_forget()
            else:
                if not group["variants"].winfo_ismapped():
                    group["variants"].pack(fill="x")

        # Re-ordonner les groupes visibles selon le tri choisi.
        for group_name in visible_groups:
            self.group_widgets[group_name]["frame"].pack_forget()
            self.group_widgets[group_name]["frame"].pack(fill="x", padx=4, pady=4)

    def _reload_from_file(self):
        self.spirit_images = load_spirit_images_map()
        self.spirit_entries = build_spirit_entries(self.spirit_images)

        if self.spirit_entries:
            new_names = [entry["key"] for entry in self.spirit_entries]
            self.entry_by_name = {entry["key"]: entry for entry in self.spirit_entries}
        else:
            new_names = load_spirit_names()
            self.entry_by_name = {
                name: {
                    "key": name,
                    "base_name": name,
                    "official": name.upper(),
                    "rarity": "Rare",
                    "site_index": idx,
                    "variant": "NORMAL",
                    "variant_label": "Normal",
                    "variant_suffix": "basic",
                    "image": str(self.spirit_images.get(name, {}).get("image", "")).strip(),
                    "slug": str(self.spirit_images.get(name, {}).get("slug_source", "")).strip(),
                }
                for idx, name in enumerate(new_names)
            }

        if not new_names:
            messagebox.showwarning("Liste vide", "esprits.txt est vide. Ajoute au moins un esprit.")
            return

        self.spirit_names = new_names

        # Garde l'etat connu et initialise le reste a False.
        new_state = {}
        new_mastered_state = {}
        for name in self.spirit_names:
            new_state[name] = bool(self.state.get(name, False))
            new_mastered_state[name] = bool(self.mastered_state.get(name, False)) and bool(new_state[name])
        self.state = new_state
        self.mastered_state = new_mastered_state

        save_state(self.state)
        save_mastered_state(self.mastered_state)
        self._render_spirits()
        self._update_progress()

    def _get_spirit_photo(self, spirit_name, size=40):
        if not PIL_AVAILABLE:
            if not self._pillow_warning_shown:
                self._pillow_warning_shown = True
                messagebox.showinfo(
                    "Miniatures desactivees",
                    "Pour afficher les images, installe Pillow avec: pip install pillow",
                )
            return None

        meta = self.entry_by_name.get(spirit_name, {})
        image_url = str(meta.get("image", "")).strip()
        if not image_url:
            return None

        os.makedirs(IMAGE_CACHE_DIR, exist_ok=True)

        slug = str(meta.get("slug", "")).strip().lower() or spirit_name.lower().replace(" ", "_")
        variant_suffix = str(meta.get("variant_suffix", "basic")).strip().lower() or "basic"
        filename = "".join(ch for ch in slug if ch.isalnum() or ch in ("_", "-"))
        filename += f"_{variant_suffix}.webp"
        local_path = os.path.join(IMAGE_CACHE_DIR, filename)

        if not os.path.exists(local_path):
            try:
                request = urllib.request.Request(
                    image_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                        "Referer": "https://spritelocker.com/fr/",
                    },
                )
                with urllib.request.urlopen(request, timeout=8) as response:
                    data = response.read()
                with open(local_path, "wb") as f:
                    f.write(data)
            except Exception:
                return None

        try:
            with Image.open(local_path) as img:
                img = img.convert("RGBA")
                img.thumbnail((size, size), RESAMPLING_LANCZOS)
                # Centrer dans un petit canevas carre pour un rendu stable.
                canvas_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
                x = (size - img.width) // 2
                y = (size - img.height) // 2
                canvas_img.paste(img, (x, y), img)
                return ImageTk.PhotoImage(canvas_img)
        except OSError:
            return None

    def _import_from_mobile(self):
        path = filedialog.askopenfilename(
            title="Selectionner le fichier JSON exporte depuis le mobile",
            filetypes=[("Fichier JSON", "*.json"), ("Tous les fichiers", "*.*")],
        )
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier:\n{e}")
            return

        # Le format mobile stocke typiquement:
        # { "collection": { "ID::VARIANT": true/false }, "mastered": { ... } }
        # et anciennement un simple objet { "ID::VARIANT": true/false }.
        collection = data.get("collection", data) if isinstance(data, dict) else {}
        mastered_collection = data.get("mastered", {}) if isinstance(data, dict) else {}

        if not isinstance(collection, dict):
            messagebox.showerror("Erreur", "Format de fichier non reconnu.")
            return
        if not isinstance(mastered_collection, dict):
            mastered_collection = {}

        # Correspondance format mobile (ID::VARIANT) → format PC (Nom - Variante)
        # Construire un index inverse: (official_id, variant) → pc_key
        mobile_to_pc = {}
        for entry in self.spirit_entries:
            mobile_key = f"{entry['official'].replace(' ', '')}::{entry['variant']}"
            mobile_to_pc[mobile_key] = entry["key"]
            # Variante avec espaces aussi (ex: "GRIM REAPER" → "GRIMREAPER")
            mobile_key2 = f"{entry['official'].replace(' ', '')[:20]}::{entry['variant']}"
            mobile_to_pc[mobile_key2] = entry["key"]

        imported = 0
        imported_mastered = 0
        for mobile_key, value in collection.items():
            if not isinstance(mobile_key, str) or "::" not in mobile_key:
                continue
            pc_key = mobile_to_pc.get(mobile_key)
            if pc_key and pc_key in self.state:
                self.state[pc_key] = bool(value)
                imported += 1

        for mobile_key, value in mastered_collection.items():
            if not isinstance(mobile_key, str) or "::" not in mobile_key:
                continue
            pc_key = mobile_to_pc.get(mobile_key)
            if pc_key and pc_key in self.mastered_state:
                self.mastered_state[pc_key] = bool(value)
                imported_mastered += 1

        # Un esprit maîtrisé doit toujours être obtenu.
        for name in self.spirit_names:
            if self.mastered_state.get(name, False):
                self.state[name] = True

        if imported == 0:
            messagebox.showwarning(
                "Aucune correspondance",
                "Aucune entree du fichier n'a pu etre importee.\n"
                "Verifie que le fichier vient bien de l'app mobile Esprits Fortnite.",
            )
            return

        save_state(self.state)
        save_mastered_state(self.mastered_state)
        for name, var in self.vars.items():
            var.set(self.state.get(name, False))
            self._update_crown_button(name)
        self._update_progress()
        self._apply_filters()
        messagebox.showinfo(
            "Import reussi",
            f"{imported} entrees obtenues importees\n"
            f"{imported_mastered} entrees maitrisees importees.",
        )

    def _export_for_mobile(self):
        from datetime import date
        default_name = f"esprits-fortnite-{date.today()}.json"
        path = filedialog.asksaveasfilename(
            title="Enregistrer la progression pour le mobile",
            defaultextension=".json",
            initialfile=default_name,
            filetypes=[("Fichier JSON", "*.json")],
        )
        if not path:
            return

        # Convertir format PC → format mobile (ID::VARIANT)
        mobile_collection = {}
        mobile_mastered = {}
        for entry in self.spirit_entries:
            mobile_key = f"{entry['official'].replace(' ', '')}::{entry['variant']}"
            pc_key = entry["key"]
            mobile_collection[mobile_key] = bool(self.state.get(pc_key, False))
            mobile_mastered[mobile_key] = bool(self.mastered_state.get(pc_key, False))

        total = len(mobile_collection)
        owned = sum(1 for v in mobile_collection.values() if v)
        mastered = sum(1 for v in mobile_mastered.values() if v)

        payload = {
            "version": 2,
            "source": "overlay-pc",
            "progression": f"{owned}/{total}",
            "collection": mobile_collection,
            "mastered": mobile_mastered,
            "crowns": mastered,
        }

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            messagebox.showinfo(
                "Export reussi",
                f"Progression exportee ({owned}/{total}).\n"
                f"Maitrises exportees: 👑 {mastered}.\n"
                f"Envoie ce fichier sur ton telephone puis utilise\n"
                f"'Importer' dans l'app mobile.",
            )
        except OSError as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer le fichier:\n{e}")

    def _reset_all(self):
        if not messagebox.askyesno(
            "Confirmation",
            "Tout passer en non recupere ?",
        ):
            return

        for name in self.spirit_names:
            self.state[name] = False
            self.mastered_state[name] = False
            if name in self.vars:
                self.vars[name].set(False)
            self._update_crown_button(name)

        save_state(self.state)
        save_mastered_state(self.mastered_state)
        self._update_progress()
        self._apply_filters()


def main():
    root = tk.Tk()
    app = SpiritOverlayApp(root)
    root.minsize(320, 420)
    root.mainloop()


if __name__ == "__main__":
    main()
