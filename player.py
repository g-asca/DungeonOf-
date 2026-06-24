class Player:
    def __init__(self, name, player_class="warrior", unlocks=None):
        self.name = name
        self.player_class = player_class
        self.level = 1
        self.xp = 0
        self.gold = 0
        self.inventory = []
        self.status_effects = []
        self.kills = {}
        self.special_cooldown = 0
        self.floor = 1
        self.rooms_cleared = 0
        self.score = 0
        self.boss_kills = 0
        self.unlocked_endgame = False
        unlocks = unlocks or {}

        if player_class == "warrior":
            self.hp = self.max_hp = 120
            self.attack = 18
            self.defense = 8
            self.special_name = "Shield Bash"
        elif player_class == "rogue":
            self.hp = self.max_hp = 90
            self.attack = 24
            self.defense = 4
            self.special_name = "Backstab"
        elif player_class == "mage":
            self.hp = self.max_hp = 80
            self.attack = 14
            self.defense = 3
            self.special_name = "Fireball"
        elif player_class == "paladin":
            self.hp = self.max_hp = 110
            self.attack = 17
            self.defense = 10
            self.special_name = "Holy Light"
        else:
            self.hp = self.max_hp = 100
            self.attack = 15
            self.defense = 5
            self.special_name = "Focus"

        if unlocks.get("start_potion"):
            self.inventory.append({"name": "Health Potion", "description": "Restores 30 HP", "item_type": "consumable", "value": 30})

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        actual = max(0, amount - self.defense)
        self.hp -= actual
        if self.hp < 0:
            self.hp = 0
        print(f"  {self.name} takes {actual} damage! {self.hp_bar()}")

    def heal(self, amount):
        healed = min(amount, self.max_hp - self.hp)
        self.hp += healed
        return healed

    def hp_bar(self):
        filled = int((self.hp / self.max_hp) * 20) if self.max_hp else 0
        filled = max(0, min(20, filled))
        bar = "█" * filled + "░" * (20 - filled)
        return f"[{bar}] {self.hp}/{self.max_hp}"

    def tick_status(self):
        still_active = []
        for effect in self.status_effects:
            if effect["name"] in ("poison", "bleed", "burn"):
                print(f"  ☠ {effect['name'].capitalize()} deals {effect['value']} damage!")
                self.hp -= effect["value"]
                if self.hp < 0:
                    self.hp = 0
            effect["turns"] -= 1
            if effect["turns"] > 0:
                still_active.append(effect)
            else:
                print(f"  {effect['name'].capitalize()} wore off.")
        self.status_effects = still_active

    def has_status(self, name):
        return any(e["name"] == name for e in self.status_effects)

    def gain_xp(self, amount):
        self.xp += amount
        print(f"  ✨ Gained {amount} XP!")
        while self.xp >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 18
        self.hp = self.max_hp
        self.attack += 4
        self.defense += 2
        print(f"\n  ⬆ LEVEL UP! Now level {self.level}! HP restored.")

    def register_kill(self, enemy_name):
        self.kills[enemy_name] = self.kills.get(enemy_name, 0) + 1
        self.score += 10
