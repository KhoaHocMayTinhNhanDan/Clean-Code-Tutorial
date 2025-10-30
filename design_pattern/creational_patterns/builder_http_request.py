from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import urllib.parse


# ========================================
# 1. PRODUCT - HTTP Request
# ========================================
class HttpRequest:
    """
    Sản phẩm cuối cùng: một HTTP Request đầy đủ.
    Không cần interface chung với các sản phẩm khác.
    """
    def __init__(self) -> None:
        self.method: str = "GET"
        self.url: str = ""
        self.headers: Dict[str, str] = {}
        self.body: Optional[Dict[str, Any]] = None
        self.query_params: Dict[str, str] = {}
        self.timeout: int = 10
        self.auth: Optional[tuple] = None
        self.retry_count: int = 0

    def add(self, part: str) -> None:
        """Giữ lại để tương thích với Product1.add() nếu cần."""
        pass  # Không dùng trong ví dụ này

    def list_parts(self) -> None:
        """In thông tin request - giống list_parts() trong ví dụ chuẩn."""
        print(f"HTTP Request: {self.method} {self.url}")
        if self.headers:
            print(f"  Headers: {self.headers}")
        if self.body:
            print(f"  Body: {self.body}")
        if self.query_params:
            print(f"  Query: {self.query_params}")
        print(f"  Timeout: {self.timeout}s, Retry: {self.retry_count}, Auth: {'Yes' if self.auth else 'No'}")

    def __str__(self) -> str:
        return f"{self.method} {self.url}"


# ========================================
# 2. BUILDER INTERFACE
# ========================================
class Builder(ABC):
    """
    Giao diện Builder - khai báo các bước xây dựng.
    Tương tự produce_part_a/b/c.
    """
    @property
    @abstractmethod
    def product(self) -> HttpRequest:
        """Trả về sản phẩm hoàn chỉnh."""
        pass

    @abstractmethod
    def produce_method_and_url(self, method: str, url: str) -> None:
        pass

    @abstractmethod
    def produce_header(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def produce_body(self, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def produce_query_param(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def produce_timeout(self, seconds: int) -> None:
        pass

    @abstractmethod
    def produce_auth(self, username: str, password: str) -> None:
        pass

    @abstractmethod
    def produce_retry(self, count: int) -> None:
        pass


# ========================================
# 3. CONCRETE BUILDER
# ========================================
class HttpRequestBuilder(Builder):
    """
    Builder cụ thể cho HTTP Request.
    Implement từng bước xây dựng.
    """

    def __init__(self) -> None:
        """Khởi tạo với sản phẩm rỗng."""
        self.reset()

    def reset(self) -> None:
        """Tạo lại sản phẩm mới."""
        self._product = HttpRequest()

    @property
    def product(self) -> HttpRequest:
        """
        Trả về sản phẩm và reset builder.
        ĐÚNG THEO HƯỚNG DẪN: gọi reset() sau khi trả kết quả.
        """
        # Xử lý query params trước khi trả
        if self._product.query_params:
            query = urllib.parse.urlencode(self._product.query_params)
            separator = "&" if "?" in self._product.url else "?"
            self._product.url += separator + query

        product = self._product
        self.reset()  # Sẵn sàng cho lần xây mới
        return product

    def produce_method_and_url(self, method: str, url: str) -> None:
        self._product.method = method.upper()
        self._product.url = url

    def produce_header(self, key: str, value: str) -> None:
        self._product.headers[key] = value

    def produce_body(self, data: Dict[str, Any]) -> None:
        self._product.body = data
        self.produce_header("Content-Type", "application/json")

    def produce_query_param(self, key: str, value: str) -> None:
        self._product.query_params[key] = value

    def produce_timeout(self, seconds: int) -> None:
        self._product.timeout = seconds

    def produce_auth(self, username: str, password: str) -> None:
        self._product.auth = (username, password)

    def produce_retry(self, count: int) -> None:
        self._product.retry_count = count

    # === FLUENT INTERFACE (thêm để dễ dùng) ===
    def set_method_and_url(self, method: str, url: str):
        self.produce_method_and_url(method, url)
        return self

    def add_header(self, key: str, value: str):
        self.produce_header(key, value)
        return self

    def set_body(self, data: Dict[str, Any]):
        self.produce_body(data)
        return self

    def add_query(self, key: str, value: str):
        self.produce_query_param(key, value)
        return self

    def set_timeout(self, seconds: int):
        self.produce_timeout(seconds)
        return self

    def set_auth(self, username: str, password: str):
        self.produce_auth(username, password)
        return self

    def set_retry(self, count: int):
        self.produce_retry(count)
        return self


# ========================================
# 4. DIRECTOR
# ========================================
class ApiDirector:
    """
    Điều phối thứ tự xây dựng cho các cấu hình phổ biến.
    """

    def __init__(self) -> None:
        self._builder: Builder | None = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder

    # === Cấu hình: Tạo User ===
    def build_create_user_request(self) -> None:
        self.builder.produce_method_and_url("POST", "https://api.example.com/users")
        self.builder.produce_header("Authorization", "Bearer token123")
        self.builder.produce_body({"name": "John", "email": "john@example.com"})
        self.builder.produce_timeout(30)
        self.builder.produce_retry(2)

    # === Cấu hình: Lấy danh sách User ===
    def build_get_users_request(self) -> None:
        self.builder.produce_method_and_url("GET", "https://api.example.com/users")
        self.builder.produce_header("Accept", "application/json")
        self.builder.produce_query_param("page", "1")
        self.builder.produce_query_param("limit", "10")
        self.builder.produce_timeout(15)


# ========================================
# 5. CLIENT - DÙNG ĐÚNG THEO HƯỚNG DẪN
# ========================================
if __name__ == "__main__":
    director = ApiDirector()
    builder = HttpRequestBuilder()
    director.builder = builder

    print("=== 1. Tạo User (dùng Director) ===")
    director.build_create_user_request()
    request1 = builder.product  # Lấy qua @property
    request1.list_parts()
    print()

    print("=== 2. Lấy danh sách User (dùng Director) ===")
    director.build_get_users_request()
    request2 = builder.product
    request2.list_parts()
    print()

    print("=== 3. Tùy chỉnh thủ công (không Director) ===")
    builder.produce_method_and_url("DELETE", "https://api.example.com/users/123")
    builder.produce_header("Authorization", "Bearer xyz")
    builder.produce_retry(1)
    custom_request = builder.product
    custom_request.list_parts()
    print()

    print("=== 4. Dùng Fluent Interface (vẫn hợp lệ) ===")
    fluent_request = (HttpRequestBuilder()
                      .set_method_and_url("PUT", "/users/456")
                      .add_header("Content-Type", "application/json")
                      .set_body({"name": "Jane"})
                      .set_timeout(20)
                      .product)
    fluent_request.list_parts()