# Tạo ra một hệ thống đối tượng liên quan đến nhau (Không chỉ tạo một object, mà tạo hệ thống object liên quan (family))


from abc import ABC, abstractmethod

# 1. Abstract Products


class Chair(ABC):
    @abstractmethod
    def sit_on(self) -> str:
        pass


class Sofa(ABC):
    @abstractmethod
    def watch_tv(self) -> str:
        pass


class CoffeeTable(ABC):
    @abstractmethod
    def place_coffee(self) -> str:
        pass

# 2. Concrete Products (cho 2 variants: Modern, Victorian)


class ModernChair(Chair):
    def sit_on(self) -> str:
        return "Sitting on a modern minimalist chair."


class VictorianChair(Chair):
    def sit_on(self) -> str:
        return "Sitting on an ornate Victorian chair."


class ModernSofa(Sofa):
    def watch_tv(self) -> str:
        return "Watching TV on a sleek modern sofa."


class VictorianSofa(Sofa):
    def watch_tv(self) -> str:
        return "Watching TV on a plush Victorian sofa."


class ModernCoffeeTable(CoffeeTable):
    def place_coffee(self) -> str:
        return "Placing coffee on a glass modern coffee table."


class VictorianCoffeeTable(CoffeeTable):
    def place_coffee(self) -> str:
        return "Placing coffee on a carved Victorian coffee table."

# 3. Abstract Factory


class FurnitureFactory(ABC):
    @abstractmethod
    def create_chair(self) -> Chair:
        pass

    @abstractmethod
    def create_sofa(self) -> Sofa:
        pass

    @abstractmethod
    def create_coffeetable(self) -> CoffeeTable:
        pass

# 4. Concrete Factories


class ModernFurnitureFactory(FurnitureFactory):
    def create_chair(self) -> Chair:
        return ModernChair()

    def create_sofa(self) -> Sofa:
        return ModernSofa()

    def create_coffeetable(self) -> CoffeeTable:
        return ModernCoffeeTable()


class VictorianFurnitureFactory(FurnitureFactory):
    def create_chair(self) -> Chair:
        return VictorianChair()

    def create_sofa(self) -> Sofa:
        return VictorianSofa()

    def create_coffeetable(self) -> CoffeeTable:
        return VictorianCoffeeTable()

# 5. Client


class FurnitureShop:
    def __init__(self, factory: FurnitureFactory):
        self.factory = factory

    def create_furniture_set(self):
        chair = self.factory.create_chair()
        sofa = self.factory.create_sofa()
        table = self.factory.create_coffeetable()

        print(chair.sit_on())
        print(sofa.watch_tv())
        print(table.place_coffee())
        print("\n--- All furniture matches the same style! ---\n")

# Sử dụng: Initialization dựa trên config (ví dụ: variant từ input hoặc env)


def main():
    variant = "Modern"  # Giả sử config: có thể là "Victorian"

    if variant == "Modern":
        factory = ModernFurnitureFactory()
    elif variant == "Victorian":
        factory = VictorianFurnitureFactory()
    else:
        raise ValueError("Unknown furniture variant!")

    shop = FurnitureShop(factory)
    shop.create_furniture_set()


if __name__ == "__main__":
    main()
