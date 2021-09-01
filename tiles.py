from tile import Tile


class GroundTile(Tile):
    def __repr__(self):
        return "🟢"


class WaterTile(Tile):
    def __repr__(self):
        return "💦"


class DestructableTile(Tile):
    """Abstract Base Class for Mountain and Building Tiles"""

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    def can_move_through(self):
        return False

    def vek_can_emerge(self):
        return False


class MountainTile(DestructableTile):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "🗻"


class ForestTile(Tile):
    def __repr__(self):
        return "🌲"


class ForestFireTile(Tile):
    def __repr__(self):
        return "🔥"


class SpawnTile(Tile):
    def __repr__(self):
        return "⬆️"


class CivilianTile(DestructableTile):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"🏘️ {'ϟ' * self.health}"


class CorporateTile(CivilianTile):
    def __repr__(self):
        return f"🏢 {'ϟ' * self.health}"