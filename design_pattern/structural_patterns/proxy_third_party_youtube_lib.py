# Service Interface (giao diện chung), Service (object gốc), Proxy (đại diện thay thế), Client (người dùng)
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import time  # Để minh họa delay của service chậm (network/API).

# TÊN NGUYÊN BẢN: Service Interface – Giao diện chung cho proxy/service (ThirdPartyYouTubeLib).
# ÁNH XẠ THỰC TẾ: Đây là "YouTubeLib Interface" – định nghĩa methods như API contract, để proxy "giả dạng" service.
# BẢN CHẤT: Đảm bảo interchangeable – client gọi method nào cũng được, dù proxy hay real service.


class ThirdPartyYouTubeLib(ABC):
    @abstractmethod
    def list_videos(self) -> List[str]:
        pass

    @abstractmethod
    def get_video_info(self, id: str) -> Dict:
        pass

    @abstractmethod
    def download_video(self, id: str) -> str:
        pass

# TÊN NGUYÊN BẢN: Service – Object gốc chứa business logic (ThirdPartyYouTubeClass).
# ÁNH XẠ THỰC TẾ: Đây là "YouTube API Service" – logic thực (fetch data chậm từ network).
# BẢN CHẤT: Service không biết proxy – chỉ làm việc chính; proxy delegate calls đến đây sau khi thêm logic (e.g., cache check).


class ThirdPartyYouTubeClass(ThirdPartyYouTubeLib):
    def list_videos(self) -> List[str]:
        time.sleep(1)  # Giả lập delay chậm (network).
        print("Service: Fetching video list from YouTube API...")
        return ["Video1", "Video2", "Video3"]  # Giả lập results.

    def get_video_info(self, id: str) -> Dict:
        time.sleep(1.5)
        print(f"Service: Fetching info for video {id}...")
        # Giả lập metadata.
        return {"title": f"Video {id}", "duration": "5min"}

    def download_video(self, id: str) -> str:
        time.sleep(3)  # Chậm nhất, tốn bandwidth.
        print(f"Service: Downloading video {id}...")
        return f"downloaded_{id}.mp4"  # Giả lập file path.

# TÊN NGUYÊN BẢN: Proxy – Đại diện thay thế, wrap service và thêm logic (CachedYouTubeClass).
# ÁNH XẠ THỰC TẾ: Đây là "Cached YouTube Proxy" – wrap API service để thêm caching, kiểm soát access (cache hit/miss).
# BẢN CHẤT: Proxy giữ wrappee ref (service), delegate calls sau "kiểm soát" (e.g., check cache trước fetch) – mở rộng không sửa service.


class CachedYouTubeClass(ThirdPartyYouTubeLib):
    def __init__(self, service: ThirdPartyYouTubeLib):
        # Wrappee ref – "bọc" service, quản lý lifecycle (lazy nếu cần).
        self.service = service
        self.list_cache: Optional[List[str]] = None  # Cache cho list (global).
        self.video_cache: Dict[str, Dict] = {}  # Cache per ID.
        # Flag invalidate cache (e.g., nếu data expired).
        self.need_reset = False

    def list_videos(self) -> List[str]:
        # Thêm caching: Check cache trước delegate.
        if self.list_cache is None or self.need_reset:
            print("Proxy: Cache miss, fetching from service...")
            # Delegate đến service sau logic.
            self.list_cache = self.service.list_videos()
            self.need_reset = False
        else:
            # Bỏ qua service – kiểm soát access.
            print("Proxy: Cache hit, returning from cache!")
        return self.list_cache

    def get_video_info(self, id: str) -> Dict:
        # Caching per ID – tương tự list.
        if id not in self.video_cache or self.need_reset:
            print(f"Proxy: Cache miss for {id}, fetching...")
            self.video_cache[id] = self.service.get_video_info(id)
            self.need_reset = False
        else:
            print(f"Proxy: Cache hit for {id}!")
        return self.video_cache[id]

    def download_video(self, id: str) -> str:
        # Thêm check "download exists" (giả lập caching file).
        if self.need_reset:
            print(f"Proxy: Cache invalid, re-downloading {id}...")
            return self.service.download_video(id)
        else:
            print(f"Proxy: Using cached download for {id}!")
            return f"cached_{id}.mp4"  # Từ cache – delegate chỉ nếu miss.

# TÊN NGUYÊN BẢN: Client – Người dùng cuối, dùng qua interface (YouTubeManager).
# ÁNH XẠ THỰC TẾ: Đây là "YouTube App Manager" – code app (GUI/render) gọi methods qua interface.
# BẢN CHẤT: Client pass proxy như service thật – transparent, không thay code khi swap (real → proxy).


class YouTubeManager:
    def __init__(self, service: ThirdPartyYouTubeLib):
        self.service = service  # Proxy hoặc real – không phân biệt!

    def render_video_page(self, id: str):
        info = self.service.get_video_info(id)  # Proxy cache → nhanh lần 2.
        print(f"Manager: Rendering page for {info['title']}")

    def render_list_panel(self):
        videos = self.service.list_videos()  # Proxy cache → chỉ fetch 1 lần.
        print(f"Manager: Rendering list: {videos}")

    def react_on_user_input(self):
        self.render_video_page("vid123")
        self.render_list_panel()


# SỬ DỤNG: Ý NGHĨA CỐT LÕI CHUNG – App config proxy động (dev: real; prod: cached) – runtime flexibility, không sửa client.
if __name__ == "__main__":
    # Real service (chậm)
    real_service = ThirdPartyYouTubeClass()
    manager_real = YouTubeManager(real_service)
    print("=== Real Service (Slow, No Cache) ===")
    manager_real.react_on_user_input()

    print("\n=== Proxy (Cached, Fast) ===")
    # Proxy wrap real – client pass proxy như service.
    proxy_service = CachedYouTubeClass(real_service)
    manager_proxy = YouTubeManager(proxy_service)
    manager_proxy.react_on_user_input()  # Lần 1: Fetch
    manager_proxy.react_on_user_input()  # Lần 2: Cache – minh họa kiểm soát!
