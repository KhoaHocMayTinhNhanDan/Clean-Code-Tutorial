# Flyweight: TreeType – Lưu intrinsic state (chung giữa nhiều tree, immutable).
# ÁP DỤNG: Intrinsic là data duplicate cao (texture, color) – share để tiết kiệm RAM.
# ĐIỂM MẤU CHỐT #1: Flyweight nhỏ, reusable; không có setters (immutable sau constructor).
class TreeType:
    def __init__(self, name, color, texture):
        self.name = name  # Intrinsic: Chung (e.g., "oak" tree)
        self.color = color  # Intrinsic: Share (e.g., "green")
        self.texture = texture  # Intrinsic: Lớn, duplicate nếu lưu ở mỗi tree

    def draw(self, canvas, x, y):
        # Method dùng extrinsic (x, y – truyền từ context).
        # ÁP DỂM: Trong game (Unity), draw tree sprite tại vị trí động, share texture.
        print(
            f"Draw {self.name} tree (color: {self.color}, texture: {self.texture}) at ({x}, {y})")

# Flyweight Factory: TreeFactory – Quản lý pool flyweights.
# ĐIỂM MẤU CHỐT #2: Factory tránh duplicate – tìm existing dựa intrinsic, tạo mới nếu cần.
# ÁP DỤNG: Trong editor (Photoshop), factory share brush types giữa strokes.


class TreeFactory:
    _tree_types = {}  # Pool: Key = tuple(intrinsic), value = TreeType

    @classmethod
    def get_tree_type(cls, name, color, texture):
        key = (name, color, texture)
        if key not in cls._tree_types:
            cls._tree_types[key] = TreeType(name, color, texture)
            print(f"Created new TreeType: {key}")
        else:
            print(f"Reused existing TreeType: {key}")
        return cls._tree_types[key]

# Context: Tree – Lưu extrinsic state (riêng mỗi tree), reference đến flyweight.
# ÁP DỤNG: Context nhỏ (chỉ coords + ref), có thể tạo hàng triệu mà không tốn RAM.
# ĐIỂM MẤU CHỐT #3: Extrinsic truyền qua methods (không lưu trong flyweight để tránh duplicate).


class Tree:
    def __init__(self, x, y, tree_type: TreeType):
        self.x = x  # Extrinsic: Vị trí riêng (thay đổi runtime)
        self.y = y  # Extrinsic: Speed/vector có thể lưu ở đây
        self.tree_type = tree_type  # Ref đến flyweight (share intrinsic)

    def draw(self, canvas):
        # Delegate đến flyweight, truyền extrinsic.
        self.tree_type.draw(canvas, self.x, self.y)

# Client: Forest – Quản lý contexts, dùng factory tạo flyweights.
# ÁP DỤNG: Trong simulation (game map), Forest lưu hàng triệu Tree contexts, share 10 TreeTypes.
# Lợi ích: RAM tiết kiệm – 1M trees chỉ tốn ~1M * sizeof(context) + 10 * sizeof(flyweight).


class Forest:
    def __init__(self):
        self.trees = []  # List contexts (có thể hàng triệu)

    def plant_tree(self, x, y, name, color, texture):
        # Dùng factory để get flyweight (share).
        tree_type = TreeFactory.get_tree_type(name, color, texture)
        tree = Tree(x, y, tree_type)  # Tạo context mới (nhỏ)
        self.trees.append(tree)

    def draw(self, canvas):
        print("Drawing forest:")
        for tree in self.trees:
            tree.draw(canvas)  # Delegate recursion – dùng extrinsic.


# Sử dụng: Minh họa share flyweights.
if __name__ == "__main__":
    forest = Forest()
    # Plant trees với intrinsic giống → share flyweight
    forest.plant_tree(1, 2, "oak", "green", "rough")
    forest.plant_tree(3, 4, "oak", "green", "rough")  # Reuse!
    forest.plant_tree(5, 6, "pine", "dark_green", "smooth")  # New flyweight

    forest.draw("canvas")  # Draw toàn forest
