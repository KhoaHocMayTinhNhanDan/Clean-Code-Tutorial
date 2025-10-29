from abc import ABC, abstractmethod

# Product interface (trừu tượng)


class Product(ABC):
    """Abstract product interface."""
    @abstractmethod
    def use(self):
        pass

# Concrete Products


class ConcreteProductA(Product):
    """Specific product A."""

    def use(self):
        print("Using Product A")


class ConcreteProductB(Product):
    """Specific product B."""

    def use(self):
        print("Using Product B")

# Abstract Factory (thay vì Creator - dễ hiểu hơn)


class AbstractFactory(ABC):
    """Abstract factory that defines the factory method."""
    @abstractmethod
    def factory_method(self):
        """Factory method to create a product."""
        pass

# Concrete Factories


class ConcreteFactoryA(AbstractFactory):
    """Factory for creating Product A."""

    def factory_method(self):
        return ConcreteProductA()


class ConcreteFactoryB(AbstractFactory):
    """Factory for creating Product B."""

    def factory_method(self):
        return ConcreteProductB()


# Sử dụng
if __name__ == "__main__":
    # Client chọn factory và tạo sản phẩm
    factory_a = ConcreteFactoryA()
    product_a = factory_a.factory_method()
    product_a.use()

    factory_b = ConcreteFactoryB()
    product_b = factory_b.factory_method()
    product_b.use()
