from mcp.server.fastmcp import FastMCP
from tools import (
    find_indicator,
    get_data,
    compare_values,
    calculate_change
)

mcp = FastMCP("WDI Research Assistant")


@mcp.tool()
def search_indicator(query: str) -> dict:
    return find_indicator(query)


@mcp.tool()
def lookup_data(
    country: str,
    indicator: str,
    year: int,
    offline: bool = False
) -> dict:
    return get_data(country, indicator, year, offline)


@mcp.tool()
def compare(first: float, second: float) -> dict:
    return compare_values(first, second)


@mcp.tool()
def percentage_change(first: float, second: float) -> dict:
    return calculate_change(first, second)


if __name__ == "__main__":
    mcp.run()