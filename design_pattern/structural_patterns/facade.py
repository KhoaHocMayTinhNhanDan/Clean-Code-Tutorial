# Complex Subsystem: Các class phức tạp từ thư viện bên thứ 3 (giả lập).
# GIẢI THÍCH MẪU: Subsystem là "hệ thống phức tạp" với nhiều dependencies, sequence calls, và objects cần init đúng order.
# ĐIỂM MẤU CHỐT #1: Client KHÔNG nên gọi trực tiếp subsystem (dẫn đến coupling cao, code dài, khó maintain/upgrade).
# ÁP DỤNG: Trong thực tế, như thư viện FFmpeg (video conversion) với 10+ classes – Facade simplify thành 1 method.
# Lợi ích: Giảm boilerplate (init, error handling) ở client, dễ thay subsystem (chỉ sửa Facade).

######################################################################################################
# Subsystem (VideoFile, CodecFactory, BitrateReader, AudioMixer, v.v.) có nhiều class, dependencies (phụ thuộc lẫn nhau),
# và sequence (thứ tự gọi) phức tạp. Nếu client gọi trực tiếp, code sẽ dài dòng, dễ lỗi (quên step, sai order)
class VideoFile:
    def __init__(self, filename):
        self.filename = filename
        # Init file – step phức tạp, client không cần biết.
        print(f"Created VideoFile: {filename}")


class CodecFactory:
    @staticmethod
    def extract(file: VideoFile):
        print(f"Extract codec from {file.filename}")
        # Giả lập extract codec – cần đúng order, dependencies.
        return "ogg_codec"


class MPEG4CompressionCodec:
    def __init__(self):
        print("Created MPEG4 codec")  # Codec cụ thể cho format mp4.


class OggCompressionCodec:
    def __init__(self):
        print("Created OGG codec")  # Codec cho format ogg.


class BitrateReader:
    @staticmethod
    def read(filename, source_codec):
        print(f"Read bitrate from {filename} with {source_codec}")
        return "bitrate_buffer"  # Giả lập read buffer – phụ thuộc codec.

    @staticmethod
    def convert(buffer, destination_codec):
        print(f"Convert buffer with {destination_codec}")
        return "converted_buffer"  # Convert – sequence quan trọng.


class AudioMixer:
    def __init__(self):
        print("Created AudioMixer")  # Mixer cho audio post-processing.

    def fix(self, buffer):
        print(f"Fix audio in buffer: {buffer}")
        return "fixed_buffer"  # Fix final – step cuối, cần buffer từ trước.
######################################################################################################


# Facade: VideoConverter – Class cung cấp interface đơn giản cho subsystem.
# GIẢI THÍCH MẪU: Facade là "mặt tiền" – biết cách phối hợp subsystem (init objects, gọi đúng order, quản lý lifecycle).
# ĐIỂM MẤU CHỐT #2: Facade expose ít methods (1-3), che giấu complexity – trade-off: Đơn giản nhưng không full features.
# ÁP DỤNG: Trong microservices, Facade wrap gRPC calls + auth + retry thành `processOrder(order)` – che giấu network/dependencies.
# Lợi ích: Client code ngắn gọn, dễ test (mock Facade), upgrade subsystem chỉ sửa Facade.


class VideoConverter:
    def convert(self, filename, format_type):
        # Phối hợp subsystem: Gọi đúng order, quản lý dependencies – client không cần biết 5+ steps.
        print(f"Starting conversion of {filename} to {format_type}")

        # Bước 1: Init VideoFile (subsystem object 1) – Facade xử lý thay client.
        file = VideoFile(filename)

        # Bước 2: Extract source codec qua Factory (object 2) – Dependencies tự động.
        source_codec = CodecFactory.extract(file)

        # Bước 3: Chọn codec đích dựa format (conditional logic ở Facade, không expose cho client).
        if format_type == "mp4":
            destination_codec = MPEG4CompressionCodec()
        else:
            destination_codec = OggCompressionCodec()

        # Bước 4: Read và convert bitrate (objects 3-4, sequence quan trọng – Facade đảm bảo order).
        buffer = BitrateReader.read(filename, source_codec)
        result = BitrateReader.convert(buffer, destination_codec)

        # Bước 5: Fix audio (object 5, step cuối – Facade kết thúc lifecycle).
        audio_mixer = AudioMixer()
        result = audio_mixer.fix(result)

        # Trả kết quả đơn giản (giả lập output file).
        output_file = f"{filename.rsplit('.', 1)[0]}.{format_type}"
        print(f"Conversion complete: {output_file}")
        return output_file
        # ĐIỂM MẤU CHỐT #3: Facade "biết hết" subsystem – nếu thêm codec mới, chỉ sửa method này, client không ảnh hưởng.

# Client: Application – Lớp sử dụng Facade (không chạm subsystem trực tiếp).
# GIẢI THÍCH MẪU: Client chỉ biết Facade – giảm coupling, tập trung business logic.
# ĐIỂM MẤU CHỐT #4: Nếu subsystem có layers (ví dụ: video + audio), tách refined facades (VideoFacade, AudioFacade) để tránh god object.
# ÁP DỤNG: Trong e-commerce, OrderFacade wrap PaymentGateway + Inventory + Shipping thành `placeOrder(order)` – client chỉ gọi 1 method.
# Lợi ích: Code client sạch, dễ refactor (thay gateway chỉ sửa Facade).


class Application:
    def main(self):
        # Init Facade một lần – đơn giản, không cần init subsystem.
        converter = VideoConverter()
        # Gọi 1 method – che giấu 5+ steps bên trong.
        mp4_file = converter.convert("funny-cat.ogg", "mp4")
        print(f"Saved: {mp4_file}")
        # ÁP DỤNG: Dễ test: Mock `convert()` return fake file, không cần mock 6+ subsystem classes.


# Sử dụng: Chạy ví dụ để thấy Facade simplify subsystem phức tạp.
if __name__ == "__main__":
    app = Application()
    app.main()
    # ĐIỂM MẤU CHỐT #5: Nếu có multiple facades, client dùng chúng như entry points (layered structure, giống Mediator).
