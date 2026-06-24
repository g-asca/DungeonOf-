import copy

ITEMS = {
    "health_potion": {"name": "Health Potion", "description": "Restores 30 HP", "item_type": "consumable", "value": 30},
    "big_potion": {"name": "Big Potion", "description": "Restores 70 HP", "item_type": "consumable", "value": 70},
    "elixir": {"name": "Elixir", "description": "Fully restores HP", "item_type": "consumable", "value": 9999},
    "antidote": {"name": "Antidote", "description": "Cures poison, bleed, burn", "item_type": "consumable", "value": 0},
    "iron_sword": {"name": "Iron Sword", "description": "+8 attack", "item_type": "weapon", "value": 8},
    "steel_sword": {"name": "Steel Sword", "description": "+15 attack", "item_type": "weapon", "value": 15},
    "cursed_blade": {"name": "Cursed Blade", "description": "+25 attack, -10 HP each floor", "item_type": "weapon", "value": 25},
    "leather_armor": {"name": "Leather Armor", "description": "+5 defense", "item_type": "armor", "value": 5},
    "chain_mail": {"name": "Chain Mail", "description": "+10 defense", "item_type": "armor", "value": 10},
    "dragon_scale": {"name": "Dragon Scale", "description": "+18 defense", "item_type": "armor", "value": 18},
    "lucky_charm": {"name": "Lucky Charm", "description": "+10 score when found", "item_type": "trinket", "value": 10},
}

def make_item(key):
    return copy.deepcopy(ITEMS[key])
