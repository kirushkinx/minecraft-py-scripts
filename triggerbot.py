import time
import minescript

class TriggerBot:
    # - Configuration -
    ATTACK_DISTANCE = 3.1
    ATTACK_COOLDOWN = 0.6

    ITEM_FILTER_MODE = "whitelist"  # "whitelist" или "blacklist"
    ITEM_FILTER = [
        "minecraft:netherite_sword",
        "minecraft:diamond_sword",
    ]
    # - -

    def __init__(self):
        self.running = False
        self.last_attack_time = 0.0

    def start(self):
        self.running = True
        minescript.echo("§aTriggerBot enabled")
        self._loop()

    def _loop(self):
        while self.running:
            self._tick()
            time.sleep(0.05)

    def _tick(self):
        if not self._is_item_allowed():
            return

        target = minescript.player_get_targeted_entity(max_distance=self.ATTACK_DISTANCE)
        if target and self._is_player(target):
            self._try_attack()

    def _extract_item_id(self, item):
        try:
            if hasattr(item, "id") and isinstance(item.id, str):
                return item.id
            if hasattr(item, "name") and isinstance(item.name, str):
                return item.name

            s = str(item)

            marker = 'id:"'
            idx = s.find(marker)
            if idx != -1:
                start = idx + len(marker)
                end = s.find('"', start)
                if end != -1:
                    return s[start:end]

            marker = "item='"
            idx = s.find(marker)
            if idx != -1:
                start = idx + len(marker)
                end = s.find("'", start)
                if end != -1:
                    return s[start:end]

            return None
        except:
            return None

    def _is_item_allowed(self):
        try:
            hand_items = minescript.player_hand_items()
            item = hand_items.main_hand

            if item is None:
                return False if self.ITEM_FILTER_MODE == "whitelist" else True

            item_id = self._extract_item_id(item)
            if not item_id:
                return True

            if self.ITEM_FILTER_MODE == "whitelist":
                return item_id in self.ITEM_FILTER
            else:
                return item_id not in self.ITEM_FILTER

        except:
            return True

    def _is_player(self, entity):
        if not hasattr(entity, 'name'):
            return False
        player_names = [p.name for p in minescript.players()]
        return entity.name in player_names

    def _try_attack(self):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.ATTACK_COOLDOWN:
            minescript.player_press_attack(True)
            minescript.player_press_attack(False)
            self.last_attack_time = current_time

_bot = TriggerBot()

def run():
    _bot.start()

if __name__ == "__main__":
    run()
