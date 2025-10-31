# Cách 1: Dùng nhiều dòng bắt đầu bằng "#"
# Đây là dòng chú thích 1
# Đây là dòng chú thích 2
# ...

# Cách 2: Dùng chuỗi nhiều dòng ("""...""") — thường dùng như block comment,
# nhưng lưu ý: đây là một string literal; nếu nó đứng ở đầu module/class/function
# thì sẽ trở thành docstring. Nếu đặt giữa code, Python sẽ bỏ qua nó nếu không gán.
"""
Ví Dụ Code Mẫu Proxy: Thẻ Tín Dụng Là Proxy Cho Tài Khoản Ngân Hàng

Dựa trên ẩn dụ real-world: Thẻ tín dụng (Proxy) là đại diện thay thế cho tài khoản ngân hàng (Service). 
Bạn dùng thẻ để thanh toán (interface chung: makePayment(amount)), thẻ kiểm tra auth (PIN) và limit trước khi
trừ tiền từ tài khoản (trước delegate), và log sau khi trừ (sau request). Client (cửa hàng) không biết là thẻ hay tài khoản – transparent.

Ý NGHĨA CỐT LÕI: Proxy kiểm soát access (thêm auth/limit) mà không sửa service, dùng composition (wrappee ref) để delegate calls. 
Dễ mở rộng (thêm caching/logging) runtime.

Code Python đơn giản: Giả lập trừ tiền, với PIN check và limit. Chạy để thấy proxy từ chối nếu PIN sai/limit vượt.
"""

# Service Interface (giao diện chung), Service (object gốc), Proxy (đại diện thay thế), Client (người dùng)

from abc import ABC, abstractmethod

# SERVICE INTERFACE: PaymentInterface – Giao diện chung cho proxy/service (thanh toán).
# ÁNH XẠ ĐƠN: Đây là "cầu nối" – định nghĩa method thanh toán chung, proxy "giả dạng" service.
# BẢN CHẤT: Đảm bảo interchangeable – client gọi `makePayment()` giống nhau, dù thẻ hay tài khoản.
# SỬA LỖI: Làm `pin` optional để proxy thêm param (auth) mà không phá service gốc.


class PaymentInterface(ABC):
    @abstractmethod
    def make_payment(self, amount: float, pin: str = "") -> str:
        # Method chung: Thanh toán số tiền (trả status), pin optional cho proxy.
        pass

# SERVICE: BankAccount – Object gốc chứa business logic (trừ tiền thực từ tài khoản).
# ÁNH XẠ ĐƠN: Đây là "tài khoản ngân hàng" – logic chính (trừ balance), chậm/tốn nếu connect DB thực.
# BẢN CHẤT: Service không biết proxy – chỉ trừ tiền; proxy delegate sau khi kiểm tra (auth/limit).
# SỬA LỖI: Thêm optional `pin` (ignore) để khớp interface – không ảnh hưởng logic gốc.


class BankAccount(PaymentInterface):
    def __init__(self, balance: float):
        self.balance = balance  # Số dư tài khoản.

    def make_payment(self, amount: float, pin: str = "") -> str:
        # Logic thực: Trừ tiền nếu đủ (pin ignored ở service).
        if self.balance >= amount:
            self.balance -= amount
            print(
                f"Service (BankAccount): Deducted {amount} from balance. New balance: {self.balance}")
            return "Payment successful"
        else:
            print(
                f"Service (BankAccount): Insufficient funds. Balance: {self.balance}")
            return "Payment failed - insufficient funds"

# PROXY: CreditCard – Đại diện thay thế, wrap service và thêm logic (auth/check limit).
# ÁNH XẠ ĐƠN: Đây là "thẻ tín dụng" – giữ ref đến tài khoản (wrappee), kiểm tra PIN/limit trước delegate.
# BẢN CHẤT: Proxy thêm behaviors (auth trước, log sau) – kiểm soát access, client thấy như service thật.


class CreditCard(PaymentInterface):
    def __init__(self, account: PaymentInterface, card_limit: float, pin: str):
        self.account = account  # Wrappee ref – "bọc" tài khoản ngân hàng.
        self.card_limit = card_limit  # Limit thẻ (e.g., 1000 USD).
        self.pin = pin  # PIN để auth.
        self.remaining_limit = card_limit  # Số dư limit hiện tại.

    def make_payment(self, amount: float, provided_pin: str = "") -> str:
        # Thêm logic trước delegate: Check auth (PIN) và limit.
        if provided_pin != self.pin:
            print("Proxy (CreditCard): Authentication failed - Wrong PIN!")
            return "Payment failed - Invalid PIN"
        if amount > self.remaining_limit:
            print(
                f"Proxy (CreditCard): Limit exceeded! Requested: {amount}, Limit: {self.remaining_limit}")
            return "Payment failed - Limit exceeded"

        # Delegate đến service sau check.
        # Trừ tiền từ tài khoản (pass pin nếu cần).
        result = self.account.make_payment(amount, provided_pin)

        # Thêm logic sau delegate: Update limit và log.
        if "successful" in result:
            self.remaining_limit -= amount
            print(
                f"Proxy (CreditCard): Payment approved. New limit: {self.remaining_limit}")
            return "Payment successful via credit card"
        else:
            return result  # Trả lỗi từ service.

# CLIENT: ShopOwner – Người dùng cuối, dùng qua interface (pass proxy thay service).
# ÁNH XẠ ĐƠN: Đây là "cửa hàng" – code thanh toán, không biết là thẻ hay tài khoản – chỉ gọi make_payment().
# BẢN CHẤT: Transparent – dễ swap (thẻ → tài khoản trực tiếp), tập trung business (xử lý giao dịch) mà không lo auth/limit.


class ShopOwner:
    def __init__(self, payment_method: PaymentInterface):
        self.payment_method = payment_method  # Proxy hoặc real – không phân biệt!

    def process_sale(self, amount: float, pin: str = ""):
        # Client gọi method chung – proxy tự xử lý auth trước delegate.
        result = self.payment_method.make_payment(amount, pin)
        print(f"Client (ShopOwner): Sale processed: {result}")


# SỬ DỤNG: Ý NGHĨA CỐT LÕI CHUNG – App config proxy động (thẻ = proxy wrap account) – client pass proxy như service.
if __name__ == "__main__":
    # Real service (tài khoản trực tiếp – không check PIN/limit)
    account = BankAccount(1000.0)  # Số dư 1000 USD.
    shop_direct = ShopOwner(account)
    print("=== Direct Bank Account (No Proxy – No Auth/Limit) ===")
    shop_direct.process_sale(200.0)  # Trừ trực tiếp, không check.

    print("\n=== Credit Card Proxy (With Auth/Limit) ===")
    # Proxy wrap real service
    card = CreditCard(account, 500.0, "1234")  # Limit 500, PIN 1234.
    shop_card = ShopOwner(card)
    # PIN đúng, limit OK → delegate trừ tiền.
    shop_card.process_sale(150.0, "1234")
    # PIN sai → từ chối trước delegate.
    shop_card.process_sale(400.0, "wrong")
    # Limit vượt → từ chối trước delegate.
    shop_card.process_sale(600.0, "1234")
