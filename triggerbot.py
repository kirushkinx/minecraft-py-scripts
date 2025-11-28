import time
import minescript

class TriggerBot:
    # - Configuration -
    ATTACK_DISTANCE = 3.0
    ATTACK_COOLDOWN = 0.6
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
        target = minescript.player_get_targeted_entity(max_distance=self.ATTACK_DISTANCE)
        if target and self._is_player(target):
            self._try_attack()

    def _is_player(self, entity):
        player_names = [p.name for p in minescript.players()]
        return hasattr(entity, 'name') and entity.name in player_names

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
