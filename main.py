import asyncio
import sys
from core import VoiceClient

async def main() -> None:
    server_url = "http://163.221.125.26:8000"
    
    try:
        client = VoiceClient(server_url)
        await client.run_conversation()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")
