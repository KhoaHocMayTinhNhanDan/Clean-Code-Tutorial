from abc import ABC, abstractmethod
from typing import List
# Import ABC để định nghĩa interface chung (Component), giúp enforce polymorphism.

# Component: Graphic interface - Định nghĩa các method chung cho TẤT CẢ elements (leaf hoặc composite).
# Áp dụng: Trong thực tế, interface này cho phép client gọi method mà không biết object là leaf (đơn giản) hay composite (phức tạp).
# Ví dụ: Trong UI toolkit (như Tkinter), tất cả widgets (button, panel) đều có method render() qua interface chung.


class Graphic(ABC):
    @abstractmethod
    def move(self, x, y):
        # Method chung: Di chuyển element (hoặc toàn bộ sub-tree nếu composite).
        # Áp dụng: Recursion tự động di chuyển toàn cây (ví dụ: move toàn bộ folder trong file explorer).
        pass

    @abstractmethod
    def draw(self):
        # Method chung: Vẽ/render element.
        # Áp dụng: Trong DOM tree (HTML), gọi draw() trên <body> sẽ render recursively tất cả nested elements (div, span, text).
        pass

# Leaf: Dot - Element cơ bản, KHÔNG có children (end node).
# Áp dụng: Leaf thường làm việc thực tế. Ví dụ: Trong file system, File là leaf (không chứa file khác), chỉ trả kích thước của chính nó.


class Dot(Graphic):
    def __init__(self, x, y):
        self.x = x  # Tọa độ x
        self.y = y  # Tọa độ y

    def move(self, x, y):
        self.x += x
        self.y += y
        # Không delegate vì không có children - đơn giản!

    def draw(self):
        print(f"Draw dot at ({self.x}, {self.y})")
        # Output trực tiếp: Leaf làm việc thực tế, không recursion.

# Leaf: Circle - Một leaf khác, kế thừa ý tưởng từ Dot nhưng thêm thuộc tính.
# Áp dụng: Có thể có nhiều leaf classes (ví dụ: Line, Rectangle). Trong organizational chart, Employee là leaf (không có sub-employees).


class Circle(Graphic):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius  # Bán kính

    def move(self, x, y):
        self.x += x
        self.y += y

    def draw(self):
        print(f"Draw circle at ({self.x}, {self.y}) with radius {self.radius}")

# Composite: CompoundGraphic - Element phức tạp, CÓ children (có thể chứa leaf hoặc composite khác).
# Áp dụng: Composite delegate recursively. Ví dụ: Trong file system, Directory là composite, chứa Files (leaf) và sub-Directories (composite khác).
# Lợi ích: Gọi method trên root (Directory root) sẽ tính tổng (ví dụ: tổng kích thước files) mà không cần biết cấu trúc bên trong.


class CompoundGraphic(Graphic):
    def __init__(self):
        # List chứa references đến Graphic (polymorphism: có thể leaf hoặc composite)
        self.children: List[Graphic] = []

    def add(self, child: Graphic):
        # Thêm child (leaf hoặc composite) vào list.
        # Áp dụng: Trong UI, Panel.add(Button) hoặc Panel.add(another Panel) để xây dựng tree động.
        self.children.append(child)

    def remove(self, child: Graphic):
        # Xóa child.
        # Áp dụng: Cho phép rebuild tree (ví dụ: remove sub-folder trong file explorer).
        if child in self.children:
            self.children.remove(child)

    def move(self, x, y):
        # Delegate recursively: Duyệt hết children và gọi move() trên từng cái.
        # Áp dụng: Trong game engine, move() trên Group (composite) sẽ di chuyển tất cả sub-objects (như enemies trong squad).
        for child in self.children:
            # Recursion: Nếu child là composite, nó sẽ delegate tiếp.
            child.move(x, y)

    def draw(self):
        # Delegate recursively: Duyệt hết children và gọi draw() trên từng cái.
        # Áp dụng: Trong PDF renderer, draw() trên Document (composite) sẽ render tất cả pages và elements bên trong recursively.
        # Lưu ý: Có thể thêm logic tổng hợp (như sum bounding box) ở đây nếu cần.
        print("Draw compound graphic:")
        for child in self.children:
            # Recursion: Xử lý toàn tree mà không cần client biết.
            child.draw()

# Client: ImageEditor - Lớp sử dụng tree, chỉ làm việc qua Graphic interface.
# Áp dụng: Client không cần if-check (là leaf hay composite) - thống nhất xử lý. Ví dụ: Trong menu app, load_menu() xây dựng tree và gọi render() trên root.


class ImageEditor:
    def __init__(self):
        self.all = CompoundGraphic()  # Root composite

    def load(self):
        # Xây dựng tree: Add leaf và có thể composite.
        # Áp dụng: Trong e-commerce, load_order() add Products (leaf) và Boxes (composite) để tính tổng giá recursively.
        self.all.add(Dot(1, 2))
        self.all.add(Circle(5, 3, 10))

    def group_selected(self, components):
        # Tạo sub-composite mới từ selected items, add vào root.
        # Áp dụng: Trong IDE (như VS Code), group code blocks thành folder ảo, rồi render tree mới.
        group = CompoundGraphic()
        for component in components:
            group.add(component)
            self.all.remove(component)
        self.all.add(group)


# Sử dụng: Minh họa build tree, group, và operation trên toàn cây.
if __name__ == "__main__":
    editor = ImageEditor()
    editor.load()
    print("Before grouping:")
    editor.all.draw()  # Gọi trên root: Recursion tự động

    # Group all (tạo nested tree)
    components = editor.all.children.copy()  # Copy để tránh modify trong loop
    editor.group_selected(components)
    print("\nAfter grouping (nested tree):")
    editor.all.draw()  # Bây giờ có sub-composite

    print("\nMove toàn bộ tree:")
    # Di chuyển root: Áp dụng recursion đến tất cả leaves
    editor.all.move(10, 10)
    # Output sẽ thay đổi tọa độ nếu print lại
