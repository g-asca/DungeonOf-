import random
from enemy import Enemy
from items import make_item

ROOM_TEXT = {
    "forest":   "Twisted trees. Glowing eyes watch from the dark.",
    "ruins":    "Crumbling stone walls. Ancient banners hang in tatters.",
    "crypt":    "Cold air rises from cracked sarcophagi.",
    "hall":     "A long stone hall with flickering green torches.",
    "armory":   "Broken blades and rusted armour litter the floor.",
    "chapel":   "A ruined chapel. Something moves near the altar.",
    "library":  "Dusty bookshelves lean like drunk skeletons.",
    "lair":     "The walls are clawed open. Something very big lives here.",
    "treasury": "Coins glitter under centuries of dust.",
    "arena":    "This room was built for slaughter.",
    "swamp":    "Ankle-deep foul water. The air is thick with poison.",
}

# ─── Base enemy templates (floor 1, room 0 stats ─────────────────────────────
# Keep base stats LOW — scaling will handle the rest.
ENEMIES = {
    # TIER 1 — easy, floor 1-2
    "cave_goblin": Enemy("Cave Goblin", hp=22, attack=6, xp_reward=20, gold_reward=5,
        special={"name": "Cheap Shot", "desc": "pokes you in the eye!", "chance": 0.15, "multiplier": 1.2},
        loot_table=["health_potion"]),

    "rat": Enemy("Giant Rat", hp=18, attack=5, xp_reward=15, gold_reward=3,
        loot_table=["health_potion"]),

    "zombie": Enemy("Zombie", hp=30, attack=7, xp_reward=22, gold_reward=4,
        status_inflict={"name": "poison", "turns": 2, "value": 3, "chance": 0.2},
        loot_table=["antidote"]),

    # TIER 2 — medium, floor 2-3
    "goblin": Enemy("Goblin Warrior", hp=38, attack=10, xp_reward=35, gold_reward=8,
        special={"name": "Gold Snatch", "desc": "lunges for your pockets!", "chance": 0.18, "multiplier": 1.1},
        loot_table=["health_potion"]),

    "skeleton": Enemy("Skeleton", hp=45, attack=12, xp_reward=45, gold_reward=10,
        special={"name": "Bone Toss", "desc": "bones fly at your face!", "chance": 0.2, "multiplier": 1.3},
        loot_table=["antidote"]),

    "spider": Enemy("Giant Spider", hp=42, attack=11, xp_reward=40, gold_reward=9,
        status_inflict={"name": "poison", "turns": 3, "value": 5, "chance": 0.3},
        loot_table=["antidote", "health_potion"]),

    # TIER 3 — hard, floor 3+
    "orc": Enemy("Orc Warrior", hp=75, attack=17, xp_reward=75, gold_reward=18,
        special={"name": "Berserker Rage", "desc": "eyes go red!", "chance": 0.2, "multiplier": 1.8},
        loot_table=["big_potion"]),

    "vampire": Enemy("Vampire", hp=70, attack=19, xp_reward=85, gold_reward=22,
        special={"name": "Life Drain", "desc": "drinks your vitality!", "chance": 0.25, "multiplier": 1.6, "self_heal": 12},
        loot_table=["chain_mail", "big_potion"]),

    "necromancer": Enemy("Necromancer", hp=80, attack=16, xp_reward=100, gold_reward=26,
        special={"name": "Death Curse", "desc": "dark magic explodes!", "chance": 0.22, "multiplier": 2.0},
        status_inflict={"name": "burn", "turns": 3, "value": 7, "chance": 0.22},
        loot_table=["elixir", "steel_sword"]),

    # TIER 4 — elite, floor 4+
    "troll": Enemy("Cave Troll", hp=105, attack=17, xp_reward=110, gold_reward=28,
        special={"name": "Regenerate", "desc": "wounds close before your eyes!", "chance": 0.25, "multiplier": 1.0, "self_heal": 15},
        loot_table=["dragon_scale"]),

    "demon": Enemy("Demon", hp=120, attack=22, xp_reward=140, gold_reward=38,
        special={"name": "Hellfire", "desc": "infernal flames!", "chance": 0.25, "multiplier": 1.9},
        status_inflict={"name": "burn", "turns": 4, "value": 8, "chance": 0.3},
        loot_table=["cursed_blade", "elixir"]),
}

BOSSES = {
    4: Enemy("Mother of Shadows", hp=200, attack=27, xp_reward=280, gold_reward=90,
        special={"name": "Crushing Wail", "desc": "the whole room trembles!", "chance": 0.28, "multiplier": 2.0}),
    8: Enemy("The Fallen King", hp=300, attack=36, xp_reward=550, gold_reward=150,
        special={"name": "Royal Oblivion", "desc": "catastrophic strike!", "chance": 0.32, "multiplier": 2.3},
        status_inflict={"name": "bleed", "turns": 4, "value": 10, "chance": 0.25}),
}

# ─── Room templates tiered by difficulty ─────────────────────────────────────
# tier 1 = easy (first rooms), tier 2 = medium, tier 3 = hard (pre-boss)
ROOM_POOL = [
    # TIER 1
    {"tier": 1, "name": "Mossy Ruins",      "desc": "ruins",   "enemies": ["rat", "cave_goblin"],    "loot": ["health_potion"]},
    {"tier": 1, "name": "Dark Forest Path", "desc": "forest",  "enemies": ["rat", "rat"],             "loot": ["health_potion"]},
    {"tier": 1, "name": "Flooded Passage",  "desc": "swamp",   "enemies": ["zombie"],                 "loot": ["antidote"]},
    {"tier": 1, "name": "Crumbling Entry",  "desc": "ruins",   "enemies": ["cave_goblin", "cave_goblin"], "loot": ["health_potion"]},

    # TIER 2
    {"tier": 2, "name": "Bone Library",     "desc": "library", "enemies": ["skeleton", "skeleton"],  "loot": ["antidote"]},
    {"tier": 2, "name": "Webbed Chapel",    "desc": "chapel",  "enemies": ["spider", "spider"],       "loot": ["health_potion"]},
    {"tier": 2, "name": "Goblin Barracks",  "desc": "armory",  "enemies": ["goblin", "cave_goblin"],  "loot": ["iron_sword"]},
    {"tier": 2, "name": "Zombie Crypt",     "desc": "crypt",   "enemies": ["zombie", "skeleton"],     "loot": ["big_potion"]},

    # TIER 3
    {"tier": 3, "name": "Orc Throne Hall",  "desc": "hall",    "enemies": ["orc", "goblin"],          "loot": ["steel_sword"]},
    {"tier": 3, "name": "Vampire Chamber",  "desc": "crypt",   "enemies": ["vampire"],                "loot": ["chain_mail"]},
    {"tier": 3, "name": "Ritual Arena",     "desc": "arena",   "enemies": ["necromancer"],            "loot": ["big_potion"]},
    {"tier": 3, "name": "Beast Lair",       "desc": "lair",    "enemies": ["troll"],                  "loot": ["dragon_scale"]},
]


class FloorRoom:
    def __init__(self, name, description, enemies=None, loot=None, is_boss=False, room_type="combat"):
        self.name = name
        self.description = description
        self.enemies = enemies or []
        self.loot = loot or []
        self.is_boss = is_boss
        self.room_type = room_type
        self.cleared = False


def tier_for_floor_and_room(floor, room_index, total_rooms):
    """
    Map floor + room position to a difficulty tier.
    Early floors and early rooms = tier 1.
    Later floors and later rooms = tier 3.
    """
    # room_index goes 0..total_rooms-2 (last room is boss/shop)
    progress = room_index / max(total_rooms - 2, 1)  # 0.0 → 1.0 through the floor

    if floor == 1:
        # Floor 1: start at tier 1, reach tier 2 only at the very end
        if progress < 0.5:  return 1
        else:               return 2
    elif floor == 2:
        if progress < 0.4:  return 1
        elif progress < 0.8:return 2
        else:               return 3
    elif floor == 3:
        if progress < 0.3:  return 2
        else:               return 3
    else:
        # Floors 4+ always tier 3
        return 3


def generate_floor(floor_number, unlocks):
    rooms = []
    total_combat = 4  # combat rooms per floor

    for i in range(total_combat):
        tier = tier_for_floor_and_room(floor_number, i, total_combat + 2)
        candidates = [r for r in ROOM_POOL if r["tier"] == tier]
        template = random.choice(candidates)

        enemies = [
            ENEMIES[key].clone_scaled(floor_number, room_index=i)
            for key in template["enemies"]
        ]
        loot = [make_item(key) for key in template["loot"]]
        rooms.append(FloorRoom(template["name"], ROOM_TEXT[template["desc"]], enemies, loot))

    # Shop always between room 2 and the boss
    rooms.insert(3, FloorRoom(
        "Wandering Merchant",
        "A suspicious merchant has somehow beaten you here.",
        loot=[], room_type="shop"
    ))

    # Boss
    if floor_number in BOSSES:
        boss = BOSSES[floor_number].clone_scaled(floor_number, room_index=total_combat)
        boss_room = FloorRoom(
            f"Floor {floor_number} Boss", 
            "The air grows thick. Something enormous waits in the darkness.",
            [boss], [], True, "boss"
        )
    else:
        # Pick a hard enemy as mini-boss for non-special floors
        choices = ["orc", "vampire", "troll", "demon"]
        if floor_number < 4:
            choices = ["orc", "vampire"]
        boss_enemy = ENEMIES[random.choice(choices)].clone_scaled(floor_number, room_index=total_combat + 1)
        boss_enemy.name = "Elite " + boss_enemy.name
        boss_room = FloorRoom(
            "Floor Boss",
            "A stronger foe blocks the way downward.",
            [boss_enemy],
            [make_item(random.choice(["elixir", "dragon_scale", "cursed_blade", "chain_mail", "big_potion"]))],
            True, "boss"
        )
    rooms.append(boss_room)
    return rooms
