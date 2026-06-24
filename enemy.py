import random
import copy

class Enemy:
    def __init__(self, name, hp, attack, xp_reward, gold_reward, special=None, status_inflict=None, loot_table=None):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.special = special
        self.status_inflict = status_inflict
        self.loot_table = loot_table or []
        self.stunned = False

    def clone_scaled(self, floor, room_index=0):
        """
        Scale enemy stats.
        floor 1 room 0 = base stats (very weak)
        Each floor adds 20%, each room within a floor adds ~8%.
        """
        enemy = copy.deepcopy(self)
        floor_scale = 1 + (floor - 1) * 0.20
        room_scale  = 1 + room_index * 0.08
        scale = floor_scale * room_scale
        enemy.hp      = max(1, int(enemy.hp      * scale))
        enemy.max_hp  = enemy.hp
        enemy.attack  = max(1, int(enemy.attack  * scale))
        enemy.xp_reward   = int(enemy.xp_reward  * scale)
        enemy.gold_reward = int(enemy.gold_reward * scale)
        return enemy

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def attack_player(self, player):
        if self.stunned:
            print(f"  {self.name} is stunned and skips the turn!")
            self.stunned = False
            return
        dmg = random.randint(max(1, self.attack - 3), self.attack + 3)
        if self.special and random.random() < self.special.get("chance", 0.2):
            print(f"  ⚡ {self.name} uses {self.special['name']}! {self.special['desc']}")
            dmg = int(dmg * self.special.get("multiplier", 1.5))
            if self.special.get("self_heal"):
                self.hp = min(self.max_hp, self.hp + self.special["self_heal"])
                print(f"  {self.name} heals for {self.special['self_heal']} HP!")
        print(f"  {self.name} attacks!")
        player.take_damage(dmg)
        if self.status_inflict and not player.has_status(self.status_inflict["name"]):
            if random.random() < self.status_inflict.get("chance", 0.25):
                player.status_effects.append(copy.deepcopy(
                    {k: v for k, v in self.status_inflict.items() if k != "chance"}
                ))
                print(f"  {self.name} inflicted {self.status_inflict['name'].upper()}!")
