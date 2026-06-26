import asyncio
from dbus_next.aio import MessageBus
from dbus_next import BusType

from notifier import notify

BUS_NAME = "org.freedesktop.UPower"
UP_DEVICE = "org.freedesktop.UPower.Device"
DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"
BATTERY_PATH = "/org/freedesktop/UPower/devices/battery_BAT0"


LOW_VALUE = 20
CRITICAL_VALUE = 10

CHARGING = 1
DISCHARGING = 2
FULLY_CHARGED = 4


class BatteryMonitor:
    def __init__(self):
        self.bus = None
        self.obj = None
        self.props = None

        self.low_notified = False
        self.critical_notified = False

    async def process_state(self):
        state = await self.get_state()
        if state["state"] in (CHARGING, FULLY_CHARGED):
            self.low_notified = False
            self.critical_notified = False
            return

        elif state["percentage"] <= CRITICAL_VALUE and not self.critical_notified:
            notify(
                title="🔴 Critical Battery Alert",
                message=(
                    f"Battery has dropped to {state['percentage']:.0f}%. "
                    "Connect your charger immediately to avoid an unexpected shutdown."
                ),
                priority="urgent",
                tags=["battery", "warning"],
            )
            self.critical_notified = True
            self.low_notified = True
            return

        elif state["percentage"] <= LOW_VALUE and not self.low_notified:
            notify(
                title="🟡 Low Battery Warning",
                message=(
                    f"Battery is at {state['percentage']:.0f}%. "
                    "Consider plugging in your charger soon."
                ),
                priority="high",
                tags=["battery"],
            )
            self.low_notified = True
            return

    def on_properties_changed(
        self, interface_name, changed_properties, invalidated_properties
    ):
        asyncio.create_task(self.process_state())

    async def initialize(self) -> None:
        self.bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

        introspection = await self.bus.introspect(BUS_NAME, BATTERY_PATH)

        self.obj = self.bus.get_proxy_object(
            BUS_NAME,
            BATTERY_PATH,
            introspection,
        )

        self.props = self.obj.get_interface(DBUS_PROPERTIES)

        self.props.on_properties_changed(self.on_properties_changed)

    async def get_state(self) -> dict:
        percentage = await self.props.call_get(UP_DEVICE, "Percentage")
        state = await self.props.call_get(UP_DEVICE, "State")

        return {"percentage": percentage.value, "state": state.value}


async def main():
    battery = BatteryMonitor()

    await battery.initialize()
    await battery.process_state()

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
