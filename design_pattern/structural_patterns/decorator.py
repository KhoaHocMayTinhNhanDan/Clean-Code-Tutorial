from abc import ABC, abstractmethod
# Import ABC để định nghĩa interface chung (Component), enforce polymorphism.
# ĐIỂM MẤU CHỐT #1: Interface chung là "linh hồn" của Decorator – tất cả (base + decorators) phải implement cùng methods,
# để client dùng thống nhất, không biết object đã được wrap bao nhiêu lớp.

# Component: DataSource interface – Định nghĩa methods chung có thể decorate.
# ÁP DỤNG: Dùng cho bất kỳ "core object" cần thêm behaviors động, như Stream (I/O), Logger, hoặc UI Widget.
# Ví dụ thực tế: Trong Java I/O, InputStream là Component; BufferedInputStream là Decorator thêm buffer.


class DataSource(ABC):
    @abstractmethod
    def write_data(self, data):
        # Method chung: Ghi data (có thể thêm encrypt/compress trước khi ghi).
        # ÁP DỤNG: Trong data pipeline (như ETL tools), decorate để thêm validation hoặc logging mà không sửa base class.
        pass

    @abstractmethod
    def read_data(self):
        # Method chung: Đọc data (thêm decrypt/decompress sau khi đọc).
        # ĐIỂM MẤU CHỐT #2: Methods này là "cầu nối" – decorator override để thêm logic trước/sau delegate.
        pass

# Concrete Component: FileDataSource – Base object, chứa behavior cốt lõi (không decorate).
# ÁP DỤNG: Đây là "core" bạn muốn mở rộng, như FileStream trong app lưu dữ liệu.
# Lợi ích: Không sửa class này khi thêm features mới – chỉ wrap bên ngoài.


class FileDataSource(DataSource):
    def __init__(self, filename):
        self.filename = filename  # File để ghi/đọc.

    def write_data(self, data):
        with open(self.filename, 'w') as f:
            f.write(data)
        print(f"Wrote plain data to {self.filename}")
        # Behavior cơ bản: Ghi trực tiếp, không thêm gì.

    def read_data(self):
        with open(self.filename, 'r') as f:
            data = f.read()
        print(f"Read plain data from {self.filename}: {data}")
        return data
        # ĐIỂM MẤU CHỐT #3: Base chỉ làm việc chính – decorator sẽ "bọc" để thêm (không kế thừa, tránh subclass explosion).

# Base Decorator: DataSourceDecorator – Wrapper cơ bản, delegate hết cho wrappee.
# ÁP DỤNG: Luôn tạo base này để concrete decorators kế thừa, đảm bảo delegate đúng.
# Ví dụ: Trong logging lib, BaseLoggerDecorator wrap core logger, thêm timestamp mà không thay core.


class DataSourceDecorator(DataSource):
    def __init__(self, source: DataSource):
        # <-- ĐIỂM MẤU CHỐT #4: Wrappee reference (type Component) – "chìa khóa" composition.
        self.wrappee = source
        # ÁP DỤNG: Cho phép stack nhiều lớp (wrappee có thể là base hoặc decorator khác).

    def write_data(self, data):
        # Delegate mặc định – thêm behavior ở concrete.
        self.wrappee.write_data(data)

    def read_data(self):
        # Delegate – concrete sẽ override để thêm.
        return self.wrappee.read_data()

# Concrete Decorator: EncryptionDecorator – Thêm behavior encrypt/decrypt.
# ÁP DỤNG: Dùng cho security layers, như wrap DB connection để encrypt data trước khi lưu (trong fintech apps).
# Lợi ích: Thêm an toàn runtime (dựa config), không sửa DB class gốc.


class EncryptionDecorator(DataSourceDecorator):
    def write_data(self, data):
        # Thêm trước delegate: Encrypt.
        encrypted_data = f"ENCRYPTED:{data}"  # Giả lập (thực tế dùng AES).
        print("Encrypting data...")  # Log để minh họa.
        # Delegate cho wrappee (có thể là base hoặc decorator khác).
        super().write_data(encrypted_data)

    def read_data(self):
        # Delegate trước, thêm sau: Decrypt.
        data = super().read_data()  # Lấy từ wrappee.
        decrypted_data = data.replace(
            "ENCRYPTED:", "") if data.startswith("ENCRYPTED:") else data
        print("Decrypting data...")
        return decrypted_data
        # ĐIỂM MẤU CHỐT #5: Thứ tự (trước/sau delegate) quyết định flow – encrypt trước write, decrypt sau read.

# Concrete Decorator: CompressionDecorator – Thêm behavior compress/decompress.
# ÁP DỤNG: Trong data storage (như cloud apps như AWS S3), wrap file handler để nén data lớn, tiết kiệm bandwidth.
# Ví dụ: Netflix dùng tương tự cho video streaming – thêm compression layer mà không thay player core.


class CompressionDecorator(DataSourceDecorator):
    def write_data(self, data):
        # Thêm trước: Compress.
        compressed_data = f"COMPRESSED:{data}"  # Giả lập (thực tế dùng gzip).
        print("Compressing data...")
        super().write_data(compressed_data)

    def read_data(self):
        # Delegate trước, thêm sau: Decompress.
        data = super().read_data()
        decompressed_data = data.replace(
            "COMPRESSED:", "") if data.startswith("COMPRESSED:") else data
        print("Decompressing data...")
        return decompressed_data

# Client: Application – Xây dựng stack decorators động.
# ÁP DỤNG: Client (như config file hoặc factory) quyết định stack dựa env (dev: no encrypt; prod: full stack).
# Lợi ích: Runtime flexibility – thay đổi behaviors mà không recompile.


class Application:
    def dumb_usage_example(self):
        data = "Salary records"  # Dữ liệu mẫu.

        # Base: Không decorate.
        source = FileDataSource("salary.dat")
        source.write_data(data)
        source.read_data()
        # Output: Plain data – minh họa base.
        print("\n---\n")

        # Wrap 1 layer: Compression.
        # <-- ĐIỂM MẤU CHỐT #6: Stacking – wrap nhiều lớp như onion.
        source = CompressionDecorator(source)
        source.write_data(data)
        source.read_data()
        # ÁP DỤNG: Dễ test từng layer riêng (unit test decorator với mock wrappee).
        print("\n---\n")

        # Wrap 2 layers: Encryption trên Compression.
        # Stack: Encrypt > Compress > Base.
        source = EncryptionDecorator(source)
        source.write_data(data)
        source.read_data()
        # Output: Full stack – client không biết bên trong, chỉ gọi write_data().


# Sử dụng: Chạy ví dụ.
if __name__ == "__main__":
    app = Application()
    app.dumb_usage_example()
    # ĐIỂM MẤU CHỐT #7: Client chỉ dùng interface – dễ thay stack (ví dụ: thêm CacheDecorator cho perf).
