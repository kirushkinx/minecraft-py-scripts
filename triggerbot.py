import time
import minescript

class TriggerBot:
    # - Configuration -
    ATTACK_DISTANCE = 3.0
    ATTACK_COOLDOWN = 0.6
    IGNORE_WHILE_HAND_EMPTY = True
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
        if self.IGNORE_WHILE_HAND_EMPTY and self._is_hand_empty():
            return

        target = minescript.player_get_targeted_entity(max_distance=self.ATTACK_DISTANCE)
        if target and self._is_player(target):
            self._try_attack()

    def _is_hand_empty(self):
        hand_items = minescript.player_hand_items()
        return hand_items.main_hand is None

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
