from abc import ABC, abstractmethod

# Implementation Interface: Device


class Device(ABC):
    @abstractmethod
    def is_enabled(self):
        pass

    @abstractmethod
    def enable(self):
        pass

    @abstractmethod
    def disable(self):
        pass

    @abstractmethod
    def get_volume(self):
        pass

    @abstractmethod
    def set_volume(self, percent):
        pass

    @abstractmethod
    def get_channel(self):
        pass

    @abstractmethod
    def set_channel(self, channel):
        pass

# Concrete Implementations


class TV(Device):
    def __init__(self):
        self.enabled = False
        self.volume = 30
        self.channel = 1

    def is_enabled(self):
        return self.enabled

    def enable(self):
        self.enabled = True
        print("TV is enabled")

    def disable(self):
        self.enabled = False
        print("TV is disabled")

    def get_volume(self):
        return self.volume

    def set_volume(self, percent):
        self.volume = max(0, min(100, percent))
        print(f"TV volume: {self.volume}")

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        print(f"TV channel: {self.channel}")


class Radio(Device):
    def __init__(self):
        self.enabled = False
        self.volume = 20
        self.channel = 89.5  # FM

    def is_enabled(self):
        return self.enabled

    def enable(self):
        self.enabled = True
        print("Radio is enabled")

    def disable(self):
        self.enabled = False
        print("Radio is disabled")

    def get_volume(self):
        return self.volume

    def set_volume(self, percent):
        self.volume = max(0, min(100, percent))
        print(f"Radio volume: {self.volume}")

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        print(f"Radio channel: {self.channel}")

# Abstraction: RemoteControl


class RemoteControl(ABC):
    def __init__(self, device: Device):
        self.device = device

    def toggle_power(self):
        if self.device.is_enabled():
            self.device.disable()
        else:
            self.device.enable()

    def volume_down(self):
        self.device.set_volume(self.device.get_volume() - 10)

    def volume_up(self):
        self.device.set_volume(self.device.get_volume() + 10)

    def channel_down(self):
        self.device.set_channel(self.device.get_channel() - 1)

    def channel_up(self):
        self.device.set_channel(self.device.get_channel() + 1)

# Refined Abstraction: AdvancedRemoteControl


class AdvancedRemoteControl(RemoteControl):
    def mute(self):
        self.device.set_volume(0)


# Client sử dụng
if __name__ == "__main__":
    # Tạo TV và remote cơ bản
    tv = TV()
    basic_remote = RemoteControl(tv)
    basic_remote.toggle_power()  # Enable TV
    basic_remote.volume_up()     # Volume 40

    # Tạo Radio và remote nâng cao
    radio = Radio()
    advanced_remote = AdvancedRemoteControl(radio)
    advanced_remote.toggle_power()  # Enable Radio
    advanced_remote.mute()          # Volume 0
    advanced_remote.channel_up()    # Channel 90.5
