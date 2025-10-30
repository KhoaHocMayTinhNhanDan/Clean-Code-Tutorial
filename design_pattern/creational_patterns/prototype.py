from abc import ABC, abstractmethod
# Để hỗ trợ deep copy nếu cần, nhưng ở đây dùng manual copy cho minh họa
from copy import deepcopy

# Prototype interface (dùng ABC)


class Shape(ABC):
    def __init__(self, x=0, y=0, color='black'):
        self.x = x
        self.y = y
        self.color = color

    # Constructor prototype: Copy từ source (gọi trong clone())
    @classmethod
    def from_prototype(cls, source):
        # Tạo instance mới và copy fields từ source
        instance = cls(source.x, source.y, source.color)
        return instance

    @abstractmethod
    def clone(self):
        pass

    def __str__(self):
        return f"Shape at ({self.x}, {self.y}) with color {self.color}"

# Concrete Prototype: Rectangle


class Rectangle(Shape):
    def __init__(self, x=0, y=0, color='black', width=0, height=0):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def clone(self):
        # Tạo copy bằng cách gọi constructor với dữ liệu gốc
        cloned = Rectangle(self.x, self.y, self.color, self.width, self.height)
        return cloned

    def __str__(self):
        return f"Rectangle: {super().__str__()}, width={self.width}, height={self.height}"

# Concrete Prototype: Circle


class Circle(Shape):
    def __init__(self, x=0, y=0, color='black', radius=0):
        super().__init__(x, y, color)
        self.radius = radius

    def clone(self):
        # Tạo copy tương tự
        cloned = Circle(self.x, self.y, self.color, self.radius)
        return cloned

    def __str__(self):
        return f"Circle: {super().__str__()}, radius={self.radius}"

# Client: Application sử dụng Prototype


class Application:
    def __init__(self):
        self.shapes = []

    def add_shapes(self):
        # Tạo original objects
        circle = Circle(10, 10, 'red', 20)
        self.shapes.append(circle)

        rectangle = Rectangle(5, 5, 'blue', 10, 20)
        self.shapes.append(rectangle)

    def business_logic(self):
        # Clone tất cả shapes mà không biết class cụ thể (nhờ polymorphism)
        shapes_copy = []
        for shape in self.shapes:
            cloned_shape = shape.clone()  # Gọi clone() của subclass tương ứng
            shapes_copy.append(cloned_shape)

        print("Original shapes:")
        for s in self.shapes:
            print(s)

        print("\nCloned shapes:")
        for s in shapes_copy:
            print(s)


# Sử dụng
app = Application()
app.add_shapes()
app.business_logic()
