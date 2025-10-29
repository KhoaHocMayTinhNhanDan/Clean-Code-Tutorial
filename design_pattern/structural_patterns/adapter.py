from abc import ABC, abstractmethod

# Target: Interface abstract (dùng ABC)


class Target(ABC):
    @abstractmethod
    def request(self):
        pass

# Adaptee (lớp cũ không thay đổi)


class Adaptee:
    def specific_request(self):
        return "Specific request"

# Adapter: Phải implement request() vì kế thừa ABC


class Adapter(Target):  # Nếu không override request, sẽ lỗi khi tạo instance!
    def __init__(self, adaptee: Adaptee):
        self.adaptee = adaptee

    def request(self):  # Bắt buộc phải có
        return f"Adapted: {self.adaptee.specific_request()}"


# Sử dụng
adaptee = Adaptee()
adapter = Adapter(adaptee)
print(adapter.request())  # Output: Adapted: Specific request

# Test lỗi nếu quên implement
# class BadAdapter(Target):  # Không có request()
#     pass
# bad = BadAdapter()  # TypeError: Can't instantiate abstract class BadAdapter...
