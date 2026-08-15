/* ============================================================
   TRACKER ESPRITS FORTNITE – app.js
   ============================================================ */

"use strict";

// ── Données des sprites ──────────────────────────────────────

const SPRITES = [
  { id: "WATER", nom: "Eau", rarity: "Rare", slug: "water" },
  { id: "EARTH", nom: "Terre", rarity: "Rare", slug: "earth" },
  { id: "FIRE", nom: "Feu", rarity: "Rare", slug: "fire" },
  { id: "FISHY", nom: "Poiscaille", rarity: "Rare", slug: "fishy" },
  { id: "AIR", nom: "Air", rarity: "Rare", slug: "air" },
  { id: "DUCK", nom: "Canard", rarity: "Epic", slug: "duck" },
  { id: "GHOST", nom: "Fantome", rarity: "Epic", slug: "ghost" },
  { id: "DEMON", nom: "Demon", rarity: "Epic", slug: "demon" },
  { id: "KING", nom: "Roi", rarity: "Epic", slug: "king" },
  { id: "AURA", nom: "Aura", rarity: "Epic", slug: "drifter" },
  { id: "STRIKER", nom: "Buteur", rarity: "Epic", slug: "soccer" },
  { id: "DREAM", nom: "Reve", rarity: "Legendary", slug: "dream" },
  { id: "PUNK", nom: "Punk", rarity: "Legendary", slug: "punk" },
  { id: "BOSS", nom: "Boss", rarity: "Legendary", slug: "boss" },
  { id: "SEVEN", nom: "Seven", rarity: "Legendary", slug: "seven" },
  { id: "PEELY", nom: "Peeky Peely", rarity: "Legendary", slug: "peely" },
  { id: "LLAMA", nom: "Lootin' Llama", rarity: "Legendary", slug: "llama" },
  { id: "BATMAN", nom: "Batman", rarity: "Mythic", slug: "fossilmeal" },
  { id: "GRIMREAPER", nom: "Faucheuse", rarity: "Mythic", slug: "grimreaper" },
  { id: "ZEROPOINT", nom: "Point Zero", rarity: "Mythic", slug: "zeropoint" },
  {
    id: "BURNTPEANUT",
    nom: "Cacahuete Grillee",
    rarity: "Mythic",
    slug: "theburntpeanut",
  },
  { id: "VINIJR", nom: "Vini Jr.", rarity: "Mythic", slug: "cokeparmesan" },
  { id: "POLLO", nom: "Pollo", rarity: "Mythic", slug: "companystargazer" },
  { id: "JOHNWICK", nom: "John Wick", rarity: "Mythic", slug: "fillergrunt" },
  {
    id: "IRONMOUSE",
    nom: "Ironmouse",
    rarity: "Mythic",
    slug: "pedicureantacid",
  },
];

const VARIANTS_BY_ID = {
  WATER: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM", "HOLOFOIL", "QUACK"],
  EARTH: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM", "CUBE", "QUACK"],
  FIRE: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL", "CUBE", "QUACK"],
  FISHY: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "CUBE"],
  AIR: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL"],
  DUCK: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM"],
  GHOST: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL"],
  DEMON: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM"],
  KING: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL"],
  AURA: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM"],
  STRIKER: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL"],
  DREAM: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "CUBE"],
  PUNK: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "CUBE"],
  BOSS: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "CUBE"],
  SEVEN: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL"],
  PEELY: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL"],
  LLAMA: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM"],
  BATMAN: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "HOLOFOIL", "CUBE"],
  GRIMREAPER: ["NORMAL", "GOLD", "GUMMY", "GALAXY", "GEM", "HOLOFOIL", "CUBE"],
  ZEROPOINT: [
    "NORMAL",
    "GOLD",
    "GUMMY",
    "GALAXY",
    "GEM",
    "HOLOFOIL",
    "CUBE",
    "QUACK",
  ],
  BURNTPEANUT: ["NORMAL"],
  VINIJR: ["NORMAL"],
  POLLO: ["NORMAL"],
  JOHNWICK: ["NORMAL"],
  IRONMOUSE: ["NORMAL"],
};

const VARIANT_LABEL = {
  NORMAL: "Normal",
  GOLD: "Or",
  GUMMY: "Gélifié",
  GALAXY: "Galaxie",
  GEM: "Gemme",
  HOLOFOIL: "Holographique",
  CUBE: "Cube",
  QUACK: "Coin-coin",
};

// Suffixes réels des images (certains diffèrent du nom de variante)
const VARIANT_SUFFIX = {
  NORMAL: "basic",
  GOLD: "gold",
  GUMMY: "candy",
  GALAXY: "galaxy",
  GEM: "gem",
  HOLOFOIL: "holofoil",
  CUBE: "cube",
  QUACK: "quack",
};

// Corrections spécifiques (slug+variant → suffixe réel)
const SUFFIX_OVERRIDES = {
  air_HOLOFOIL: "holo",
  ghost_HOLOFOIL: "holo",
  duck_HOLOFOIL: "holo",
};

function imgUrl(slug, variant) {
  const key = `${slug}_${variant}`;
  const suffix = SUFFIX_OVERRIDES[key] ?? VARIANT_SUFFIX[variant] ?? "basic";
  return `https://spritelocker.com/sprites/${slug}_${suffix}.webp`;
}

// ── État ─────────────────────────────────────────────────────

const STATE_KEY = "esprits-fn-v2";

function normalizeState(raw) {
  // Compatibilite v1: ancien format { "ID::VARIANT": true/false }
  if (raw && typeof raw === "object" && !Array.isArray(raw)) {
    const hasOwned = Object.prototype.hasOwnProperty.call(raw, "owned");
    const hasMastered = Object.prototype.hasOwnProperty.call(raw, "mastered");
    if (hasOwned || hasMastered) {
      const owned =
        raw.owned && typeof raw.owned === "object" ? { ...raw.owned } : {};
      const mastered =
        raw.mastered && typeof raw.mastered === "object"
          ? { ...raw.mastered }
          : {};
      return { owned, mastered };
    }
    return { owned: { ...raw }, mastered: {} };
  }
  return { owned: {}, mastered: {} };
}

function loadState() {
  try {
    return normalizeState(JSON.parse(localStorage.getItem(STATE_KEY)) || {});
  } catch {
    return { owned: {}, mastered: {} };
  }
}

function saveState(state) {
  localStorage.setItem(
    STATE_KEY,
    JSON.stringify({
      owned: state.owned || {},
      mastered: state.mastered || {},
    }),
  );
}

function entryKey(spriteId, variant) {
  return `${spriteId}::${variant}`;
}

// ── UI ───────────────────────────────────────────────────────

let state = loadState();
let activeFilter = "all";
let activeRarity = null;

const listEl = document.getElementById("sprite-list");
const emptyEl = document.getElementById("empty-msg");
const searchEl = document.getElementById("search");
const progBar = document.getElementById("progress-bar");
const progText = document.getElementById("progress-text");
const ringFill = document.getElementById("ring-fill");
const pctEl = document.getElementById("progress-pct");

// Toast
let toastTimer;
function showToast(msg) {
  let t = document.getElementById("toast");
  if (!t) {
    t = document.createElement("div");
    t.id = "toast";
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), 1800);
}

// Calcul progression
function calcProgress() {
  let total = 0,
    owned = 0,
    mastered = 0;
  for (const sp of SPRITES) {
    for (const v of VARIANTS_BY_ID[sp.id] || ["NORMAL"]) {
      const k = entryKey(sp.id, v);
      total++;
      if (state.owned[k]) owned++;
      if (state.mastered[k]) mastered++;
    }
  }
  return { total, owned, mastered };
}

function updateProgress() {
  const { total, owned, mastered } = calcProgress();
  const pct = total ? Math.round((owned / total) * 100) : 0;
  progBar.style.width = pct + "%";
  progText.textContent = `${owned} / ${total} obtenus | 👑 ${mastered}`;
  pctEl.textContent = pct + "%";
  const circ = 2 * Math.PI * 18;
  ringFill.style.strokeDashoffset = circ - (circ * pct) / 100;
}

// Rendu
function render() {
  const query = searchEl.value.trim().toLowerCase();
  listEl.innerHTML = "";
  let shown = 0;

  for (const sp of SPRITES) {
    // Filtre rareté
    if (activeRarity && sp.rarity !== activeRarity) continue;

    const variants = VARIANTS_BY_ID[sp.id] || ["NORMAL"];
    const ownedCount = variants.filter(
      (v) => state.owned[entryKey(sp.id, v)],
    ).length;
    const masteredCount = variants.filter(
      (v) => state.mastered[entryKey(sp.id, v)],
    ).length;
    const isFullyOwned = ownedCount === variants.length;

    // Filtre possession
    if (activeFilter === "owned" && ownedCount === 0) continue;
    if (activeFilter === "missing" && isFullyOwned) continue;

    // Filtre recherche
    if (query && !sp.nom.toLowerCase().includes(query)) continue;

    shown++;

    // Groupe
    const group = document.createElement("div");
    group.className = "sprite-group";
    group.dataset.id = sp.id;

    // En-tête du groupe
    const header = document.createElement("div");
    header.className = "group-header";

    // Avatar (image Normal)
    const avatarUrl = imgUrl(sp.slug, "NORMAL");
    const avatarImg = document.createElement("img");
    avatarImg.className = "group-avatar";
    avatarImg.alt = sp.nom;
    avatarImg.loading = "lazy";
    avatarImg.src = avatarUrl;
    avatarImg.onerror = function () {
      const ph = document.createElement("div");
      ph.className = "group-avatar-placeholder";
      ph.textContent = sp.nom.slice(0, 3).toUpperCase();
      this.replaceWith(ph);
    };

    const info = document.createElement("div");
    info.className = "group-info";

    const nameEl = document.createElement("div");
    nameEl.className = "group-name";
    nameEl.textContent = sp.nom;

    const subEl = document.createElement("div");
    subEl.className = "group-sub";
    subEl.textContent = `${ownedCount}/${variants.length} obtenues • 👑 ${masteredCount}`;

    info.append(nameEl, subEl);

    const badge = document.createElement("span");
    badge.className = `rarity-badge rarity-${sp.rarity}`;
    badge.textContent =
      sp.rarity === "Mythic"
        ? "Mythique"
        : sp.rarity === "Legendary"
          ? "Légendaire"
          : sp.rarity === "Epic"
            ? "Épique"
            : "Rare";

    const chevron = document.createElement("span");
    chevron.className = "group-chevron";
    chevron.textContent = "▾";

    header.append(avatarImg, info, badge, chevron);

    // Repli/dépli
    const variantList = document.createElement("div");
    variantList.className = "variant-list";

    // Mémoriser l'état collapsed du groupe
    const collapsedKey = `collapsed_${sp.id}`;
    if (sessionStorage.getItem(collapsedKey) === "1") {
      group.classList.add("group-collapsed");
    }

    header.addEventListener("click", () => {
      group.classList.toggle("group-collapsed");
      sessionStorage.setItem(
        collapsedKey,
        group.classList.contains("group-collapsed") ? "1" : "0",
      );
    });

    // Lignes de variantes
    for (const variant of variants) {
      const key = entryKey(sp.id, variant);
      const row = document.createElement("div");
      row.className =
        "variant-row" +
        (state.owned[key] ? " owned" : "") +
        (state.mastered[key] ? " mastered" : "");

      // Mini image
      const vUrl = imgUrl(sp.slug, variant);
      const vImg = document.createElement("img");
      vImg.className = "variant-icon";
      vImg.alt = VARIANT_LABEL[variant];
      vImg.loading = "lazy";
      vImg.src = vUrl;
      vImg.onerror = function () {
        const ph = document.createElement("div");
        ph.className = "variant-icon-placeholder";
        ph.textContent = (VARIANT_LABEL[variant] || "?").slice(0, 2);
        this.replaceWith(ph);
      };

      const lbl = document.createElement("span");
      lbl.className = "variant-label";
      lbl.textContent = VARIANT_LABEL[variant] || variant;

      const dot = document.createElement("div");
      dot.className = "variant-dot";

      const crownBtn = document.createElement("button");
      crownBtn.className =
        "variant-crown" + (state.mastered[key] ? " active" : "");
      crownBtn.type = "button";
      crownBtn.title = "Marquer maîtrisé (niveau 5)";
      crownBtn.textContent = "👑";

      row.append(vImg, lbl, dot, crownBtn);

      row.addEventListener("click", () => {
        state.owned[key] = !state.owned[key];
        if (!state.owned[key]) {
          state.mastered[key] = false;
        }
        saveState(state);
        row.classList.toggle("owned", state.owned[key]);
        row.classList.toggle("mastered", state.mastered[key]);
        crownBtn.classList.toggle("active", state.mastered[key]);
        showToast(
          state.owned[key]
            ? `✓ ${sp.nom} ${VARIANT_LABEL[variant]}`
            : `✗ ${sp.nom} ${VARIANT_LABEL[variant]}`,
        );
        // Re-appliquer le filtre actif : re-render complet pour masquer
        // immédiatement les lignes désormais incompatibles avec le filtre.
        render();
      });

      crownBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        state.mastered[key] = !state.mastered[key];
        if (state.mastered[key]) {
          state.owned[key] = true;
        }
        saveState(state);
        showToast(
          state.mastered[key]
            ? `👑 ${sp.nom} ${VARIANT_LABEL[variant]} maîtrisé`
            : `👑 retiré: ${sp.nom} ${VARIANT_LABEL[variant]}`,
        );
        render();
      });

      variantList.appendChild(row);
    }

    group.append(header, variantList);
    listEl.appendChild(group);
  }

  emptyEl.hidden = shown > 0;
  updateProgress();
}

// ── Filtres ──────────────────────────────────────────────────

document.querySelectorAll(".filter-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const filter = btn.dataset.filter;
    const rarity = btn.dataset.rarity;

    document
      .querySelectorAll(".filter-btn")
      .forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");

    if (filter) {
      activeFilter = filter;
      activeRarity = null;
    } else if (rarity) {
      // Toggle rarity
      if (activeRarity === rarity) {
        activeRarity = null;
        // Revenir au filtre "tous"
        document.querySelector('[data-filter="all"]').classList.add("active");
      } else {
        activeRarity = rarity;
      }
      activeFilter = "all";
    }

    render();
  });
});

searchEl.addEventListener("input", render);

// ── Export ──────────────────────────────────────────────────

document.getElementById("btn-export").addEventListener("click", () => {
  const { total, owned, mastered } = calcProgress();
  const payload = {
    version: 2,
    date: new Date().toISOString(),
    progression: `${owned}/${total}`,
    collection: state.owned,
    mastered: state.mastered,
    crowns: mastered,
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `esprits-fortnite-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
  showToast("✅ Progression exportée");
});

// ── Import ──────────────────────────────────────────────────

document.getElementById("btn-import").addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    try {
      const parsed = JSON.parse(ev.target.result);
      const importedOwned = parsed.collection ?? parsed.owned ?? parsed;
      const importedMastered = parsed.mastered ?? {};
      if (typeof importedOwned !== "object" || Array.isArray(importedOwned))
        throw new Error();
      if (
        typeof importedMastered !== "object" ||
        Array.isArray(importedMastered)
      )
        throw new Error();
      // Valider que les clés correspondent au format attendu
      const validKeys = Object.keys(importedOwned).filter((k) =>
        k.includes("::"),
      );
      if (validKeys.length === 0 && Object.keys(importedOwned).length > 0)
        throw new Error("format invalide");
      state = {
        owned: { ...importedOwned },
        mastered: { ...importedMastered },
      };
      // Un maîtrisé doit toujours être obtenu.
      for (const k of Object.keys(state.mastered)) {
        if (state.mastered[k]) state.owned[k] = true;
      }
      saveState(state);
      render();
      showToast(`✅ ${validKeys.length} entrées importées`);
    } catch {
      showToast("❌ Fichier invalide");
    }
    // Reset l'input pour permettre de réimporter le même fichier
    e.target.value = "";
  };
  reader.readAsText(file);
});

// ── Reset ────────────────────────────────────────────────────

document.getElementById("fab-reset").addEventListener("click", () => {
  if (!confirm("Remettre toute la collection à zéro ?")) return;
  state = { owned: {}, mastered: {} };
  saveState(state);
  render();
  showToast("Collection remise à zéro");
});

// ── Service Worker ───────────────────────────────────────────

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("./sw.js").catch(() => {});
}

// ── Lancement ────────────────────────────────────────────────

render();
