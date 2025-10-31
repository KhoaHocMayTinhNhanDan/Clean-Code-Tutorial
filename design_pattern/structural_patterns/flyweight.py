import json
from typing import Dict

# Flyweight: Lớp lưu intrinsic state (shared_state – phần chung, immutable).
# GIẢI THÍCH MẪU: Flyweight là "object nhẹ" – chỉ lưu data duplicate cao (như brand/model/color của xe),
# để share giữa nhiều xe. Extrinsic (unique, như plates/owner) truyền qua parameters.
# ĐIỂM MẤU CHỐT #1: Intrinsic state set một lần (constructor), không thay đổi – đảm bảo safe share (immutable).
# ÁP DỤNG: Trong database lớn (như CRM), share "product type" giữa 1M records để tiết kiệm RAM.


class Flyweight:
    """ The Flyweight stores a common portion of the state (also called intrinsic state) that belongs to multiple real business entities.
    The Flyweight accepts the rest of the state (extrinsic state, unique for each entity) via its method parameters. """

    def __init__(self, shared_state: str) -> None:
        # Intrinsic: Chung (e.g., "BMW_M5_red") – share cho xe cùng loại.
        self._shared_state = shared_state

    def operation(self, unique_state: str) -> None:
        # Method dùng extrinsic (unique_state – truyền từ client).
        s = json.dumps(self._shared_state)  # Đọc intrinsic (nhanh, share).
        u = json.dumps(unique_state)  # Xử lý extrinsic (riêng mỗi xe).
        print(
            f"Flyweight: Displaying shared ({s}) and unique ({u}) state.", end="")
        # ĐIỂM MẤU CHỐT #2: Operation delegate extrinsic qua params – tránh lưu trong flyweight (tiết kiệm RAM).
        # ÁP DỤNG: Trong game, draw() nhận position (extrinsic) để vẽ sprite share (intrinsic).

# FlyweightFactory: Factory quản lý pool flyweights (dict _flyweights).
# GIẢI THÍCH MẪU: Factory tránh tạo duplicate – hash key từ intrinsic, reuse nếu tồn tại.
# ĐIỂM MẤU CHỐT #3: Key = hash(intrinsic) – đảm bảo unique flyweight cho mỗi combo chung (e.g., "BMW_M5_red").
# ÁP DỤNG: Trong text editor, factory share font glyphs cho ký tự giống, chỉ tạo mới nếu style khác.


class FlyweightFactory:
    """ The Flyweight Factory creates and manages the Flyweight objects. It ensures that flyweights are shared correctly.
    When the client requests a flyweight, the factory either returns an existing instance or creates a new one, if it doesn't exist yet. """
    _flyweights: Dict[str, Flyweight] = {
    }  # Pool: Key = hash intrinsic, value = flyweight.

    def __init__(self, initial_flyweights: Dict) -> None:
        # Init pool với flyweights ban đầu (pre-populate để nhanh).
        for state in initial_flyweights:
            self._flyweights[self.get_key(state)] = Flyweight(state)
            # ÁP DỤNG: Trong app khởi động, load common types (e.g., 100 font styles) vào pool.

    def get_key(self, state: Dict) -> str:
        """ Returns a Flyweight's string hash for a given state. """
        # Tạo key unique từ intrinsic (sorted để ổn định).
        # E.g., {"BMW", "M5", "red"} → "BMW_M5_red".
        return "_".join(sorted(state))
        # ĐIỂM MẤU CHỐT #4: Hash key đơn giản (string join) – O(1) lookup, tránh duplicate.

    def get_flyweight(self, shared_state: Dict) -> Flyweight:
        """ Returns an existing Flyweight with a given state or creates a new one. """
        key = self.get_key(shared_state)
        if not self._flyweights.get(key):
            print("FlyweightFactory: Can't find a flyweight, creating new one.")
            # Tạo mới nếu chưa có.
            self._flyweights[key] = Flyweight(shared_state)
        else:
            # Reuse – tiết kiệm RAM!
            print("FlyweightFactory: Reusing existing flyweight.")
        return self._flyweights[key]
        # ÁP DỤNG: Trong factory, log để debug (production: remove print cho perf).

    def list_flyweights(self) -> None:
        # List pool để minh họa share (debug tool).
        count = len(self._flyweights)
        print(f"FlyweightFactory: I have {count} flyweights:")
        print("\n".join(map(str, self._flyweights.keys())), end="")
        # ĐIỂM MẤU CHỐT #5: Pool size nhỏ (e.g., 5 types cho 1M xe) – chứng tỏ share hiệu quả.

# Client function: add_car_to_police_database – Minh họa sử dụng factory + flyweight.
# GIẢI THÍCH MẪU: Client truyền intrinsic cho factory (get flyweight), extrinsic cho operation.
# ÁP DỤNG: Trong DB app, add record xe – share type (brand/model/color) cho triệu records.


def add_car_to_police_database(
    factory: FlyweightFactory, plates: str, owner: str, brand: str, model: str, color: str
) -> None:
    print("\n\nClient: Adding a car to database.")
    # Get flyweight từ intrinsic (brand, model, color – chung).
    flyweight = factory.get_flyweight([brand, model, color])
    # Operation với extrinsic (plates, owner – riêng mỗi xe).
    flyweight.operation([plates, owner])
    # Lợi ích: Xe cùng loại share flyweight – DB chỉ lưu ref + extrinsic (tiết kiệm storage).


if __name__ == "__main__":
    """ The client code usually creates a bunch of pre-populated flyweights in the initialization stage of the application. """
    # Init factory với initial flyweights (pre-load common types).
    factory = FlyweightFactory([
        ["Chevrolet", "Camaro2018", "pink"],
        ["Mercedes Benz", "C300", "black"],
        ["Mercedes Benz", "C500", "red"],
        ["BMW", "M5", "red"],
        ["BMW", "X6", "white"],
    ])
    # ĐIỂM MẤU CHỐT #6: Pre-populate pool – nhanh cho runtime, đặc biệt app lớn (e.g., load từ DB/cache).

    factory.list_flyweights()  # Hiển thị pool ban đầu (5 flyweights).

    add_car_to_police_database(
        factory, "CL234IR", "James Doe", "BMW", "M5", "red"
    )  # Reuse "BMW_M5_red".

    add_car_to_police_database(
        factory, "CL234IR", "James Doe", "BMW", "X1", "red"
    )  # Tạo mới "BMW_X1_red" (khác model).

    print("\n")
    # Pool tăng lên 6 – minh họa share (BMW_M5_red reuse).
    factory.list_flyweights()
    # ÁP DỤNG: Trong production, factory.load_from_db() để populate từ cache/Redis.
