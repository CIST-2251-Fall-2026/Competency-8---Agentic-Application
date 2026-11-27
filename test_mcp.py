import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(tool.name)

            result = await session.call_tool(
                "lookup_data",
                {
                    "country": "USA",
                    "indicator": "SP.POP.TOTL",
                    "year": 2022,
                    "offline": True
                }
            )

            print("\nTool result:")
            print(result.content)


asyncio.run(main())