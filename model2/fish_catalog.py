"""Last Catch: fish catalog for Model 2.

About 100 commonly caught species (with a focus on more rural areas), grouped by how they spoil.
Fish in the same group spoil in a similar way, so they share a base spoilage rate.
Within a group, fattier fish spoil faster ("fat": 0 = lean, 1 = medium, 2 = high).

BASE_HOURS_ON_ICE = rough hours a freshly caught fish of that group stays food-safe on ice.
These are PLACEHOLDER estimates for a hackathon prototype and should be checked
against food-science sources before any real use.
"""

BASE_HOURS_ON_ICE = {
    "lean_white":    216,  # white-fleshed, low fat: spoil slowest
    "freshwater":    168,
    "cartilaginous": 144,  # sharks, rays: build up ammonia if not bled/iced
    "oily_pelagic":  132,  # oily fish: fats go rancid
    "cephalopod":    120,  # squid, octopus
    "scombroid":      96,  # tuna/mackerel family: histamine risk when warm
    "gastropod":      96,  # abalone, whelks
    "crustacean":     72,  # lobster, prawns, crab: spoil fast once dead
    "bivalve":        60,  # mussels, oysters, clams: highest risk
}

FISH = [
    # --- lean_white ---
    ("Hake", "lean_white", 0), ("Kob", "lean_white", 0), ("Kabeljou", "lean_white", 0),
    ("Kingklip", "lean_white", 0), ("Cod", "lean_white", 0), ("Haddock", "lean_white", 0),
    ("Pollock", "lean_white", 0), ("Whiting", "lean_white", 0), ("Red Roman", "lean_white", 0),
    ("Carpenter", "lean_white", 0), ("Seventy-four", "lean_white", 0), ("Musselcracker", "lean_white", 0),
    ("White Steenbras", "lean_white", 0), ("Dageraad", "lean_white", 0), ("Panga", "lean_white", 0),
    ("Snapper", "lean_white", 0), ("Grouper", "lean_white", 0), ("Rockcod", "lean_white", 0),
    ("Sole", "lean_white", 0), ("Flounder", "lean_white", 0), ("Plaice", "lean_white", 0),
    ("Halibut", "lean_white", 1), ("Turbot", "lean_white", 1), ("John Dory", "lean_white", 0),
    ("Monkfish", "lean_white", 0), ("Gurnard", "lean_white", 0), ("Sea Bass", "lean_white", 1),
    ("Sea Bream", "lean_white", 0), ("Hottentot", "lean_white", 0), ("Galjoen", "lean_white", 1),
    ("Blacktail", "lean_white", 0), ("Stumpnose", "lean_white", 0), ("Grunter", "lean_white", 0),
    ("Barracuda", "lean_white", 1),
    # --- oily_pelagic ---
    ("Snoek", "oily_pelagic", 1), ("Yellowtail", "oily_pelagic", 1), ("Harders", "oily_pelagic", 1),
    ("Mullet", "oily_pelagic", 1), ("Sardine", "oily_pelagic", 2), ("Pilchard", "oily_pelagic", 2),
    ("Anchovy", "oily_pelagic", 2), ("Herring", "oily_pelagic", 2), ("Sprat", "oily_pelagic", 2),
    ("Horse Mackerel", "oily_pelagic", 1), ("Maasbanker", "oily_pelagic", 1), ("Salmon", "oily_pelagic", 2),
    ("Elf", "oily_pelagic", 1), ("Bluefish", "oily_pelagic", 1), ("Garrick", "oily_pelagic", 1),
    ("Leervis", "oily_pelagic", 1), ("Kingfish", "oily_pelagic", 1), ("Trevally", "oily_pelagic", 1),
    ("Amberjack", "oily_pelagic", 1), ("Pompano", "oily_pelagic", 1), ("Butterfish", "oily_pelagic", 2),
    ("Eel", "oily_pelagic", 2),
    # --- scombroid ---
    ("Yellowfin Tuna", "scombroid", 1), ("Bigeye Tuna", "scombroid", 1), ("Albacore", "scombroid", 1),
    ("Skipjack Tuna", "scombroid", 1), ("Bluefin Tuna", "scombroid", 2), ("Bonito", "scombroid", 1),
    ("Mackerel", "scombroid", 2), ("Chub Mackerel", "scombroid", 2), ("King Mackerel", "scombroid", 1),
    ("Couta", "scombroid", 1), ("Spanish Mackerel", "scombroid", 1), ("Wahoo", "scombroid", 0),
    ("Mahi-mahi", "scombroid", 0), ("Dorado", "scombroid", 0), ("Swordfish", "scombroid", 1),
    ("Marlin", "scombroid", 1), ("Sailfish", "scombroid", 0),
    # --- cartilaginous ---
    ("Shark", "cartilaginous", 0), ("Smoothhound", "cartilaginous", 0), ("Soupfin Shark", "cartilaginous", 0),
    ("Mako Shark", "cartilaginous", 0), ("Blue Shark", "cartilaginous", 0), ("Dogfish", "cartilaginous", 0),
    ("Skate", "cartilaginous", 0), ("Ray", "cartilaginous", 0), ("Guitarfish", "cartilaginous", 0),
    # --- freshwater ---
    ("Tilapia", "freshwater", 0), ("Catfish", "freshwater", 1), ("Carp", "freshwater", 1),
    ("Largemouth Bass", "freshwater", 0), ("Perch", "freshwater", 0), ("Trout", "freshwater", 1),
    ("Rainbow Trout", "freshwater", 1), ("Yellowfish", "freshwater", 0), ("Nile Perch", "freshwater", 1),
    ("Pike", "freshwater", 0), ("Walleye", "freshwater", 0),
    # --- crustacean ---
    ("Crayfish", "crustacean", 0), ("Rock Lobster", "crustacean", 0), ("Lobster", "crustacean", 0),
    ("Prawn", "crustacean", 0), ("Shrimp", "crustacean", 0), ("Langoustine", "crustacean", 0),
    ("Mud Crab", "crustacean", 0), ("Crab", "crustacean", 0),
    # --- bivalve ---
    ("Mussel", "bivalve", 0), ("Black Mussel", "bivalve", 0), ("White Mussel", "bivalve", 0),
    ("Oyster", "bivalve", 0), ("Clam", "bivalve", 0), ("Scallop", "bivalve", 0), ("Cockle", "bivalve", 0),
    # --- cephalopod ---
    ("Squid", "cephalopod", 0), ("Chokka", "cephalopod", 0), ("Octopus", "cephalopod", 0),
    ("Cuttlefish", "cephalopod", 0),
    # --- gastropod ---
    ("Abalone", "gastropod", 0), ("Periwinkle", "gastropod", 0), ("Whelk", "gastropod", 0),
    ("Limpet", "gastropod", 0),
]

# If a seller types a fish that isn't in the list, guess the group from keywords
KEYWORD_GROUPS = [
    ("tuna", "scombroid"), ("mackerel", "scombroid"), ("shark", "cartilaginous"), ("ray", "cartilaginous"),
    ("lobster", "crustacean"), ("crab", "crustacean"), ("prawn", "crustacean"), ("shrimp", "crustacean"),
    ("mussel", "bivalve"), ("oyster", "bivalve"), ("clam", "bivalve"), ("squid", "cephalopod"),
    ("trout", "freshwater"), ("bass", "lean_white"), ("bream", "lean_white"),
]

GROUP_NAMES = list(BASE_HOURS_ON_ICE)


def lookup_fish(name):
    """Return (group, fat_level, matched_name) for a fish name. Unknown fish get a cautious guess."""
    key = name.strip().lower()
    for fish_name, group, fat in FISH:                       # 1. exact match
        if fish_name.lower() == key:
            return group, fat, fish_name
    for fish_name, group, fat in sorted(FISH, key=lambda f: -len(f[0])):   # 2. partial: "Blue Marlin" -> Marlin, "Mussels" -> Mussel
        if fish_name.lower() in key:
            return group, fat, fish_name
    for word, group in KEYWORD_GROUPS:                       # 3. keyword guess
        if word in key:
            return group, 1, name
    return "oily_pelagic", 1, name   # unknown: assume a faster-spoiling group to be safe
