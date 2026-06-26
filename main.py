from battery import BatteryMonitor
import asyncio


async def main():
    battery = BatteryMonitor()

    await battery.initialize()
    await battery.process_state()

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
