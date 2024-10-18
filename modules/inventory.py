from modules.item import Item


class Inventory:
    def __init__(self):
        self._container: dict[str, int] = {}

    def get_item_num(self, item: Item) -> int:
        return self._container.get(item.id, 0)

    def add_item(self, item: Item, n: int):
        self._container.setdefault(item.id, 0)
        self._container[item.id] += n
