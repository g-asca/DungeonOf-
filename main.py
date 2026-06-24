import os
import json
import random
from player import Player
from room import generate_floor
from items import make_item

TITLE = r"""
🌟  ____  _   _ _   _  ____ _____ ___  _   _    ___  _____  🌟
   |  _ \| | | | \ | |/ ___| ____/ _ \| \ | |  / _ \|  ___|
   | | | | | | |  \| | |  _|  _|| | | |  \| | | | | | |_
   | |_| | |_| | |\  | |_| | |__| |_| | |\  | | |_| |  _|
   |____/ \___/|_| \_|\____|_____\___/|_| \_|  \___/|_|

⚔️                     R O G U E L I T E                     ⚔️
"""

UNLOCKS_FILE = "unlocks.json"
SHOP_STOCK = {1:("health_potion",20),2:("big_potion",45),3:("antidote",15),4:("iron_sword",50),5:("steel_sword",100),6:("leather_armor",40),7:("chain_mail",80)}


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def divider(char="═", width=68):
    print(char * width)


def small_divider():
    print("─" * 68)


def pause():
    input("\n👉 Press ENTER to continue... ")


def load_unlocks():
    if os.path.exists(UNLOCKS_FILE):
        try:
            with open(UNLOCKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"endgame_unlocked": False, "paladin_unlocked": False, "start_potion": False}


def save_unlocks(unlocks):
    with open(UNLOCKS_FILE, "w", encoding="utf-8") as f:
        json.dump(unlocks, f, indent=2)


def class_emoji(player_class):
    return {
        "warrior": "⚔️",
        "rogue": "🗡️",
        "mage": "🔥",
        "paladin": "🛡️",
    }.get(player_class, "👤")


def status_emoji(name):
    return {
        "poison": "☠️",
        "bleed": "🩸",
        "burn": "🔥",
    }.get(name, "⚠️")


def rarity_emoji(item_type):
    return {
        "consumable": "🧪",
        "weapon": "⚔️",
        "armor": "🛡️",
        "trinket": "✨",
    }.get(item_type, "🎒")


def choose_class(unlocks):
    while True:
        clear()
        print(TITLE)
        print("🎮 Choose your class:\n")
        print("[1] ⚔️ Warrior  - High HP and defense; Shield Bash")
        print("[2] 🗡️ Rogue    - Huge burst; Backstab")
        print("[3] 🔥 Mage     - Hits all enemies; Fireball")
        if unlocks.get("paladin_unlocked"):
            print("[4] 🛡️ Paladin  - Balanced tank; Holy Light")
        print("[0] 🚪 Quit")
        choice = input("\n➡️  > ").strip()
        if choice == "1": return "warrior"
        if choice == "2": return "rogue"
        if choice == "3": return "mage"
        if choice == "4" and unlocks.get("paladin_unlocked"): return "paladin"
        if choice == "0": return None


def show_status(player, floor_rooms, room_index):
    divider()
    print(f"🏰 Floor {player.floor}   🚪 Room {room_index + 1}/{len(floor_rooms)}   🏆 Score {player.score}")
    small_divider()
    print(f"{class_emoji(player.player_class)}  {player.name} the {player.player_class.upper()}   ⭐ LV {player.level}   ✨ XP {player.xp}/{player.level * 100}")
    print(f"❤️  HP   {player.hp_bar()}")
    print(f"⚔️  ATK  {player.attack}     🛡️  DEF  {player.defense}     💰 Gold  {player.gold}")
    print(f"🎒 Items {len(player.inventory)}     💀 Kills {sum(player.kills.values())}")
    if player.status_effects:
        status_str = "  ".join(f"{status_emoji(e['name'])} {e['name']}({e['turns']}t)" for e in player.status_effects)
        print(f"⚠️  Status {status_str}")
    divider()
    print()


def print_room(room):
    divider()
    icon = "🛒" if room.room_type == "shop" else ("👑" if room.is_boss else "🏚️")
    print(f"{icon}  {room.name}")
    divider()
    print()
    print(f"📜 {room.description}")
    print()


def show_inventory(player):
    clear()
    print("🎒 INVENTORY\n")
    divider()
    print(f"❤️  {player.hp_bar()}")
    print(f"⚔️ ATK {player.attack}   🛡️ DEF {player.defense}   💰 Gold {player.gold}")
    divider()
    print()
    if not player.inventory:
        print("😅 You have nothing.")
        pause()
        return
    for i, item in enumerate(player.inventory, 1):
        print(f"[{i}] {rarity_emoji(item['item_type'])} {item['name']} - {item['description']}")
    print("[0] 🔙 Back")
    choice = input("\n👉 Use item: ").strip()
    if choice == "0":
        return
    try:
        idx = int(choice) - 1
        item = player.inventory[idx]
    except Exception:
        return

    print()
    if item["item_type"] == "consumable":
        if item["name"] == "Antidote":
            player.status_effects = [e for e in player.status_effects if e["name"] not in ("poison", "bleed", "burn")]
            print("🧪 You cured your status effects.")
        else:
            healed = player.heal(item["value"])
            print(f"💚 You used {item['name']} and healed {healed} HP.")
        player.inventory.pop(idx)
    elif item["item_type"] == "weapon":
        player.attack += item["value"]
        print(f"⚔️ Equipped {item['name']}. Attack is now {player.attack}.")
        player.inventory.pop(idx)
    elif item["item_type"] == "armor":
        player.defense += item["value"]
        print(f"🛡️ Equipped {item['name']}. Defense is now {player.defense}.")
        player.inventory.pop(idx)
    elif item["item_type"] == "trinket":
        player.score += item["value"]
        print(f"✨ {item['name']} boosts your score by {item['value']}!")
        player.inventory.pop(idx)
    pause()


def show_bestiary(player):
    clear()
    print("📖 BESTIARY\n")
    divider()
    print(f"💀 Total kills: {sum(player.kills.values())}")
    divider()
    print()
    if not player.kills:
        print("😶 No kills yet.")
    else:
        for name, count in sorted(player.kills.items()):
            print(f"👾 {name:<22} x{count}")
    pause()


def enemy_drop(enemy):
    if enemy.loot_table and random.random() < 0.35:
        return make_item(random.choice(enemy.loot_table))
    return None


def combat(player, enemies):
    special_used = False
    while player.is_alive() and any(e.is_alive() for e in enemies):
        clear()
        print("⚔️ COMBAT\n")
        divider()
        print(f"❤️  {player.hp_bar()}")
        print(f"⚔️  ATK {player.attack}   🛡️  DEF {player.defense}   💰 {player.gold}g")
        if player.status_effects:
            status_str = "  ".join(f"{status_emoji(e['name'])} {e['name']}({e['turns']}t)" for e in player.status_effects)
            print(f"⚠️  {status_str}")
        divider()
        print()

        if player.status_effects:
            player.tick_status()
            print()
            if not player.is_alive():
                break

        alive = [e for e in enemies if e.is_alive()]
        print("👹 Enemies:")
        for i, e in enumerate(alive, 1):
            print(f"[{i}] {e.name:<22} ❤️ {e.hp}/{e.max_hp}")
        print()

        special_label = player.special_name
        if player.player_class == "rogue" and special_used:
            special_label += " (used)"
        elif player.player_class != "rogue" and player.special_cooldown > 0:
            special_label += f" ({player.special_cooldown})"

        print("Choose action:")
        print("[1] ⚔️ Attack")
        print(f"[2] ✨ {special_label}")
        print("[3] 🎒 Use Item")
        print("[4] 💨 Run")
        choice = input("\n👉 > ").strip()

        if choice == "1":
            t = input("🎯 Target #: ").strip()
            try:
                target = alive[int(t)-1]
            except Exception:
                target = alive[0]
            dmg = random.randint(max(1, player.attack - 5), player.attack + 5)
            target.take_damage(dmg)
            print(f"\n💥 You hit {target.name} for {dmg} damage.")
            if player.special_cooldown > 0:
                player.special_cooldown -= 1
        elif choice == "2":
            target = alive[0]
            if player.player_class == "warrior":
                if player.special_cooldown > 0:
                    print("\n⏳ Still on cooldown.")
                else:
                    dmg = random.randint(player.attack, player.attack + 8)
                    target.take_damage(dmg)
                    target.stunned = True
                    print(f"\n🛡️ Shield Bash deals {dmg} and stuns {target.name}!")
                    player.special_cooldown = 3
            elif player.player_class == "rogue":
                if special_used:
                    print("\n❌ You already used Backstab this fight.")
                else:
                    dmg = player.attack * 3
                    target.take_damage(dmg)
                    print(f"\n🗡️ Backstab deals {dmg} damage!")
                    special_used = True
            elif player.player_class == "mage":
                if player.special_cooldown > 0:
                    print("\n⏳ Still on cooldown.")
                else:
                    print("\n🔥 Fireball scorches all enemies for 40 damage!")
                    for enemy in alive:
                        enemy.take_damage(40)
                    player.special_cooldown = 4
            elif player.player_class == "paladin":
                if player.special_cooldown > 0:
                    print("\n⏳ Still on cooldown.")
                else:
                    healed = player.heal(35)
                    print(f"\n✨ Holy Light heals you for {healed} HP and smites all foes for 20 damage!")
                    for enemy in alive:
                        enemy.take_damage(20)
                    player.special_cooldown = 4
        elif choice == "3":
            show_inventory(player)
            continue
        elif choice == "4":
            if random.random() < 0.4:
                print("\n💨 You escaped.")
                pause()
                return False, []
            print("\n❌ You fail to escape!")
        else:
            continue

        print()
        loot = []
        for enemy in alive:
            if enemy.is_alive() and player.is_alive():
                enemy.attack_player(player)
        for enemy in enemies:
            if enemy.hp == 0 and not hasattr(enemy, "rewarded"):
                enemy.rewarded = True
                player.gain_xp(enemy.xp_reward)
                player.gold += enemy.gold_reward
                player.register_kill(enemy.name)
                player.score += 15
                drop = enemy_drop(enemy)
                if drop:
                    loot.append(drop)
        if player.special_cooldown > 0 and choice != "1":
            player.special_cooldown -= 1
        if loot:
            print()
            for item in loot:
                print(f"🎁 Loot dropped: {rarity_emoji(item['item_type'])} {item['name']}")
                player.inventory.append(item)
        pause()

    return player.is_alive(), []


def visit_shop(player):
    while True:
        clear()
        print("🛒 WANDERING MERCHANT\n")
        divider()
        print(f"💰 Gold: {player.gold}")
        print(f"❤️  {player.hp_bar()}")
        divider()
        print()
        for key, (item_key, price) in SHOP_STOCK.items():
            item = make_item(item_key)
            print(f"[{key}] {rarity_emoji(item['item_type'])} {item['name']:<16} {price:>3}g  {item['description']}")
        print("[0] 🔙 Leave")
        choice = input("\n👉 > ").strip()
        if choice == "0":
            return
        try:
            key = int(choice)
            item_key, price = SHOP_STOCK[key]
        except Exception:
            continue
        if player.gold >= price:
            player.gold -= price
            bought = make_item(item_key)
            player.inventory.append(bought)
            print(f"\n✅ Bought {bought['name']}.")
        else:
            print("\n❌ Not enough gold.")
        pause()


def apply_floor_effects(player):
    cursed = any(item["name"] == "Cursed Blade" for item in player.inventory)
    if cursed:
        player.hp = max(1, player.hp - 10)
        print("☠️ The Cursed Blade drains 10 HP as you descend...")
        pause()


def unlock_progress(unlocks, floor):
    changed = False
    messages = []
    if floor >= 4 and not unlocks.get("endgame_unlocked"):
        unlocks["endgame_unlocked"] = True
        unlocks["start_potion"] = True
        changed = True
        messages.append("🔓 Unlocked endgame floors 5-8")
        messages.append("🧪 Future runs start with a Health Potion")
    if floor >= 8 and not unlocks.get("paladin_unlocked"):
        unlocks["paladin_unlocked"] = True
        changed = True
        messages.append("🛡️ Unlocked Paladin class")
    if changed:
        save_unlocks(unlocks)
    return messages


def floor_limit(unlocks):
    return 8 if unlocks.get("endgame_unlocked") else 4


def room_menu(player, floor_rooms, room_index, room):
    while True:
        clear()
        print_room(room)
        show_status(player, floor_rooms, room_index)
        if room.room_type == "shop":
            print("[1] 🛒 Browse shop")
            print("[2] 🎒 Inventory")
            print("[3] 📖 Bestiary")
            print("[4] 🚪 Continue")
            choice = input("\n👉 > ").strip()
            if choice == "1":
                visit_shop(player)
            elif choice == "2":
                show_inventory(player)
            elif choice == "3":
                show_bestiary(player)
            elif choice == "4":
                room.cleared = True
                return True
        elif room.cleared:
            print("[1] 🚪 Continue")
            print("[2] 🎒 Inventory")
            print("[3] 📖 Bestiary")
            choice = input("\n👉 > ").strip()
            if choice == "1":
                return True
            elif choice == "2":
                show_inventory(player)
            elif choice == "3":
                show_bestiary(player)
        else:
            print("[1] ⚔️ Enter fight")
            print("[2] 🎒 Inventory")
            print("[3] 📖 Bestiary")
            choice = input("\n👉 > ").strip()
            if choice == "1":
                alive, _ = combat(player, room.enemies)
                if not alive:
                    return False
                room.cleared = True
                player.rooms_cleared += 1
                for item in room.loot:
                    print(f"\n🎁 You found {rarity_emoji(item['item_type'])} {item['name']}!")
                    player.inventory.append(item)
                    if item["name"] == "Lucky Charm":
                        player.score += 10
                pause()
                return True
            elif choice == "2":
                show_inventory(player)
            elif choice == "3":
                show_bestiary(player)


def ending_screen(player, unlock_messages, victory_floor):
    clear()
    print("👑 VICTORY\n")
    divider()
    print(f"🏆 You cleared floor {victory_floor}!")
    print(f"⭐ Score: {player.score}")
    print(f"💀 Kills: {sum(player.kills.values())}")
    print(f"💰 Gold: {player.gold}")
    divider()
    if unlock_messages:
        print("\n🔓 Unlocks:")
        for msg in unlock_messages:
            print(f"- {msg}")
    pause()


def death_screen(player):
    clear()
    print("💀 GAME OVER\n")
    divider()
    print(f"🏰 Reached floor: {player.floor}")
    print(f"⭐ Score: {player.score}")
    print(f"💀 Kills: {sum(player.kills.values())}")
    print(f"💰 Gold: {player.gold}")
    divider()
    pause()


def main():
    unlocks = load_unlocks()
    chosen = choose_class(unlocks)
    if not chosen:
        return
    clear()
    print(TITLE)
    name = input("📝 Enter your hero's name: ").strip() or "Hero"
    player = Player(name, chosen, unlocks)

    max_floor = floor_limit(unlocks)
    while player.floor <= max_floor and player.is_alive():
        apply_floor_effects(player)
        floor_rooms = generate_floor(player.floor, unlocks)
        room_index = 0
        while room_index < len(floor_rooms) and player.is_alive():
            room = floor_rooms[room_index]
            success = room_menu(player, floor_rooms, room_index, room)
            if not success:
                break
            room_index += 1
            player.score += 5

        if not player.is_alive():
            break

        if player.floor == max_floor:
            unlock_messages = unlock_progress(unlocks, player.floor)
            ending_screen(player, unlock_messages, player.floor)
            return

        player.floor += 1
        player.score += 50
        clear()
        print(f"⬇️ You descend to floor {player.floor}...")
        print()
        print(f"{class_emoji(player.player_class)} {player.name} prepares for the next nightmare.")
        pause()

    death_screen(player)


if __name__ == "__main__":
    main()
