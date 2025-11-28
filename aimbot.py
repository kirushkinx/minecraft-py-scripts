import time
import math
import minescript


class AimBot:
    # - Configuration -
    SEARCH_RADIUS = 4.0
    MIN_SMOOTHNESS = 0.15
    MAX_SMOOTHNESS = 0.35
    UPDATE_INTERVAL = 0.015
    PREDICTION_MULTIPLIER = 0.35
    FOV = 180.0
    TARGET_BONE = 'closest'  # 'head', 'neck', 'torso', 'legs', 'feet', 'closest'

    ITEM_FILTER_MODE = "whitelist"  # "whitelist" or "blacklist"
    ITEM_FILTER = [
        "minecraft:netherite_sword",
        "minecraft:diamond_sword",
    ]
    # - -

    BONE_OFFSETS = {
        'head': 1.65,
        'neck': 1.3,
        'torso': 1.0,
        'legs': 0.5,
        'feet': 0.1,
        'closest': None
    }

    def __init__(self):
        self.running = False
        self.last_target_pos = None
        self.locked_target_name = None
        self.mouse_sensitivity = 0.5

    def start(self):
        self.running = True
        minescript.echo("§aAimBot enabled")
        self._loop()

    def _loop(self):
        while self.running:
            self._tick()
            time.sleep(self.UPDATE_INTERVAL)

    def _tick(self):
        if not self._is_item_allowed():
            self.locked_target_name = None
            return

        target = self._find_nearest_player()
        if target:
            self._smooth_aim(target)
            self.last_target_pos = self._get_target_position(target)
            self.locked_target_name = target.name
        else:
            self.last_target_pos = None
            self.locked_target_name = None

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

    def _get_target_position(self, target):
        target_pos = list(target.position)

        if self.TARGET_BONE == 'closest':
            return self._get_closest_point(target)

        bone_height = self.BONE_OFFSETS.get(self.TARGET_BONE, 1.5)
        target_pos[1] += bone_height

        if self.last_target_pos:
            velocity_x = target_pos[0] - self.last_target_pos[0]
            velocity_y = target_pos[1] - self.last_target_pos[1]
            velocity_z = target_pos[2] - self.last_target_pos[2]

            target_pos[0] += velocity_x * self.PREDICTION_MULTIPLIER
            target_pos[1] += velocity_y * self.PREDICTION_MULTIPLIER
            target_pos[2] += velocity_z * self.PREDICTION_MULTIPLIER

        return target_pos

    def _get_closest_point(self, target):
        my_pos = minescript.player_position()
        my_eye_y = my_pos[1] + 1.62

        target_x, target_y, target_z = target.position

        best_point = None
        min_dist = float('inf')

        for bone_name, height in self.BONE_OFFSETS.items():
            if bone_name == 'closest' or height is None:
                continue

            test_y = target_y + height
            dx = target_x - my_pos[0]
            dy = test_y - my_eye_y
            dz = target_z - my_pos[2]
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)

            if dist < min_dist:
                min_dist = dist
                best_point = [target_x, test_y, target_z]

        if self.last_target_pos and best_point:
            velocity_x = best_point[0] - self.last_target_pos[0]
            velocity_y = best_point[1] - self.last_target_pos[1]
            velocity_z = best_point[2] - self.last_target_pos[2]

            best_point[0] += velocity_x * self.PREDICTION_MULTIPLIER
            best_point[1] += velocity_y * self.PREDICTION_MULTIPLIER
            best_point[2] += velocity_z * self.PREDICTION_MULTIPLIER

        return best_point if best_point else [target_x, target_y + 1.5, target_z]

    def _find_nearest_player(self):
        all_players = minescript.players()
        my_name = minescript.player().name
        my_pos = minescript.player_position()
        my_yaw = minescript.player_orientation()[0]

        if self.locked_target_name:
            for p in all_players:
                if p.name == self.locked_target_name:
                    dx = p.position[0] - my_pos[0]
                    dy = p.position[1] - my_pos[1]
                    dz = p.position[2] - my_pos[2]
                    dist = math.sqrt(dx * dx + dy * dy + dz * dz)

                    if dist <= self.SEARCH_RADIUS:
                        fov_angle = self._get_fov_to_entity(p, my_pos, my_yaw)
                        if fov_angle <= self.FOV:
                            return p

            self.locked_target_name = None

        nearest = None
        min_fov = self.FOV

        for p in all_players:
            if p.name == my_name:
                continue

            dx = p.position[0] - my_pos[0]
            dy = p.position[1] - my_pos[1]
            dz = p.position[2] - my_pos[2]
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)

            if dist > self.SEARCH_RADIUS:
                continue

            fov_angle = self._get_fov_to_entity(p, my_pos, my_yaw)

            if fov_angle < min_fov:
                min_fov = fov_angle
                nearest = p

        return nearest

    def _get_fov_to_entity(self, entity, my_pos, my_yaw):
        dx = entity.position[0] - my_pos[0]
        dz = entity.position[2] - my_pos[2]

        target_yaw = math.degrees(math.atan2(-dx, dz))
        yaw_diff = abs(self._normalize_angle(target_yaw - my_yaw))

        return yaw_diff

    def _normalize_angle(self, angle):
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle

    def _smooth_aim(self, target):
        my_pos = minescript.player_position()
        my_rot = minescript.player_orientation()

        target_pos = self._get_target_position(target)

        dx = target_pos[0] - my_pos[0]
        dy = target_pos[1] - (my_pos[1] + 1.62)
        dz = target_pos[2] - my_pos[2]

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

        new_pitch = max(-90.0, min(90.0, new_pitch))

        minescript.player_set_orientation(new_yaw, new_pitch)


_bot = AimBot()


def run():
    _bot.start()


if __name__ == "__main__":
    run()
