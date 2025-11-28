import time
import math
import minescript


class AimBot:
    # - Configuration -
    SEARCH_RADIUS = 4.0
    MIN_SMOOTHNESS = 0.18
    MAX_SMOOTHNESS = 0.42
    UPDATE_INTERVAL = 0.015
    PREDICTION_MULTIPLIER = 0.35
    # - -

    def __init__(self):
        self.running = False
        self.last_target_pos = None
        self.locked_target_name = None

    def start(self):
        self.running = True
        minescript.echo("§aAimBot enabled")
        self._loop()

    def _loop(self):
        while self.running:
            self._tick()
            time.sleep(self.UPDATE_INTERVAL)

    def _tick(self):
        target = self._find_nearest_player()
        if target:
            self._smooth_aim(target)
            self.last_target_pos = target.position
            self.locked_target_name = target.name
        else:
            self.last_target_pos = None
            self.locked_target_name = None

    def _find_nearest_player(self):
        all_players = minescript.players()
        my_name = minescript.player().name
        my_pos = minescript.player_position()

        if self.locked_target_name:
            for p in all_players:
                if p.name == self.locked_target_name:
                    dx = p.position[0] - my_pos[0]
                    dy = p.position[1] - my_pos[1]
                    dz = p.position[2] - my_pos[2]
                    dist = math.sqrt(dx * dx + dy * dy + dz * dz)
                    if dist <= self.SEARCH_RADIUS:
                        return p
            self.locked_target_name = None

        nearest = None
        min_dist = self.SEARCH_RADIUS

        for p in all_players:
            if p.name == my_name:
                continue

            dx = p.position[0] - my_pos[0]
            dy = p.position[1] - my_pos[1]
            dz = p.position[2] - my_pos[2]
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)

            if dist < min_dist:
                min_dist = dist
                nearest = p

        return nearest

    def _normalize_angle(self, angle):
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle

    def _smooth_aim(self, target):
        my_pos = minescript.player_position()
        my_rot = minescript.player_orientation()

        target_pos = target.position

        predicted_x = target_pos[0]
        predicted_y = target_pos[1] + 1.5
        predicted_z = target_pos[2]

        if self.last_target_pos:
            velocity_x = target_pos[0] - self.last_target_pos[0]
            velocity_z = target_pos[2] - self.last_target_pos[2]

            predicted_x += velocity_x * self.PREDICTION_MULTIPLIER
            predicted_z += velocity_z * self.PREDICTION_MULTIPLIER

        dx = predicted_x - my_pos[0]
        dy = predicted_y - (my_pos[1] + 1.62)
        dz = predicted_z - my_pos[2]

        distance = math.sqrt(dx * dx + dz * dz)
        target_yaw = math.degrees(math.atan2(-dx, dz))
        target_pitch = math.degrees(math.atan2(-dy, distance))

        current_yaw = my_rot[0]
        current_pitch = my_rot[1]

        yaw_diff = self._normalize_angle(target_yaw - current_yaw)
        pitch_diff = self._normalize_angle(target_pitch - current_pitch)

        angle_distance = math.sqrt(yaw_diff * yaw_diff + pitch_diff * pitch_diff)
        smoothness = self.MIN_SMOOTHNESS + (self.MAX_SMOOTHNESS - self.MIN_SMOOTHNESS) * min(1.0, angle_distance / 25.0)

        new_yaw = current_yaw + yaw_diff * smoothness
        new_pitch = current_pitch + pitch_diff * smoothness

        minescript.player_set_orientation(new_yaw, new_pitch)


_bot = AimBot()


def run():
    _bot.start()


if __name__ == "__main__":
    run()
