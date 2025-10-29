from abc import ABC, abstractmethod

# Abstract Products: Giao diện chung cho UI components


class Button(ABC):
    @abstractmethod
    def paint(self) -> str:
        pass


class Checkbox(ABC):
    @abstractmethod
    def paint(self) -> str:
        pass

# Concrete Products: Triển khai cho từng platform (Windows, macOS)


class WindowsButton(Button):
    def paint(self) -> str:
        return "Rendering a Windows-style button (square with bevel)."


class MacButton(Button):
    def paint(self) -> str:
        return "Rendering a macOS-style button (rounded, aqua theme)."


class WindowsCheckbox(Checkbox):
    def paint(self) -> str:
        return "Rendering a Windows-style checkbox (square box)."


class MacCheckbox(Checkbox):
    def paint(self) -> str:
        return "Rendering a macOS-style checkbox (rounded box)."

# Abstract Factory: Giao diện tạo family UI


class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

# Concrete Factories: Cho từng platform


class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()


class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()

# Client: App sử dụng factory (chọn theo OS)


class Application:
    def __init__(self, factory: GUIFactory):
        self.factory = factory

    def create_ui(self):
        button = self.factory.create_button()
        checkbox = self.factory.create_checkbox()
        print(button.paint())
        print(checkbox.paint())
        print("\n--- UI components match the OS style! ---\n")

# Initialization: Chọn factory dựa trên config (OS)


def main():
    os_type = "Windows"  # Giả lập từ sys.platform hoặc config
    if os_type == "Windows":
        factory = WindowsFactory()
    elif os_type == "macOS":
        factory = MacFactory()
    else:
        raise ValueError("Unsupported OS!")

    app = Application(factory)
    app.create_ui()


if __name__ == "__main__":
    main()
