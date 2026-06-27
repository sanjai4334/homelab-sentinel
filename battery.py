import asyncio

from dbus_next import BusType
from dbus_next.aio import MessageBus

from notifier import notify

BUS_NAME = "org.freedesktop.UPower"
UP_INTERFACE = "org.freedesktop.UPower"
UP_DEVICE = "org.freedesktop.UPower.Device"
DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"

UP_PATH = "/org/freedesktop/UPower"
BATTERY_PREFIX = f"{UP_PATH}/devices/battery_"

LOW_VALUE = 20
CRITICAL_VALUE = 10

CHARGING = 1
DISCHARGING = 2
FULLY_CHARGED = 4


class BatteryMonitor:
    def __init__(self) -> None:
        self.bus = None
        self.obj = None
        self.props = None

        self.low_notified = False
        self.critical_notified = False

    async def process_state(self) -> None:
        state = await self.get_state()

        if state["state"] in (CHARGING, FULLY_CHARGED):
            self.low_notified = False
            self.critical_notified = False
            return

        if state["percentage"] <= CRITICAL_VALUE and not self.critical_notified:
            notify(
                title="Critical Battery Alert",
                message=(
                    f"Battery has dropped to {state['percentage']:.0f}%. "
                    "Connect your charger immediately to avoid an unexpected shutdown."
                ),
                priority="urgent",
                tags=["battery", "skull"],
            )

            self.critical_notified = True
            self.low_notified = True
            return

        if state["percentage"] <= LOW_VALUE and not self.low_notified:
            notify(
                title="Low Battery Warning",
                message=(
                    f"Battery is at {state['percentage']:.0f}%. "
                    "Consider plugging in your charger soon."
                ),
                priority="high",
                tags=["battery", "warning"],
            )

            self.low_notified = True

    def on_properties_changed(
        self,
        interface_name,
        changed_properties,
        invalidated_properties,
    ) -> None:
        asyncio.create_task(self.process_state())

    async def get_battery_path(self) -> str:
        introspection = await self.bus.introspect(
            BUS_NAME,
            UP_PATH,
        )

        obj = self.bus.get_proxy_object(
            BUS_NAME,
            UP_PATH,
            introspection,
        )

        upower = obj.get_interface(UP_INTERFACE)

        devices = await upower.call_enumerate_devices()

        for device in devices:
            if device.startswith(BATTERY_PREFIX):
                return device

        raise RuntimeError("No battery device found.")

    async def initialize(self) -> None:
        self.bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

        battery_path = await self.get_battery_path()

        introspection = await self.bus.introspect(
            BUS_NAME,
            battery_path,
        )

        self.obj = self.bus.get_proxy_object(
            BUS_NAME,
            battery_path,
            introspection,
        )

        self.props = self.obj.get_interface(DBUS_PROPERTIES)

        self.props.on_properties_changed(self.on_properties_changed)

    async def get_state(self) -> dict[str, int | float]:
        percentage = await self.props.call_get(
            UP_DEVICE,
            "Percentage",
        )

        state = await self.props.call_get(
            UP_DEVICE,
            "State",
        )

        return {
            "percentage": percentage.value,
            "state": state.value,
        }


async def main():
    battery = BatteryMonitor()

    await battery.initialize()
    await battery.process_state()

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
