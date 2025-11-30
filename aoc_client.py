import httpx
from bs4 import BeautifulSoup


class AdventOfCodeClient:
    def __init__(self, session_cookie: str) -> None:
        self.client = httpx.Client(
            base_url="https://adventofcode.com/",
            cookies={"session": session_cookie},
        )

    def get_puzzle_description(self, year: int, day: int) -> str:
        response = self.client.get(f"/{year}/day/{day}")
        response.raise_for_status()
        return response.text

    def get_puzzle_test_inputs(self, year: int, day: int) -> list[str]:
        description = self.get_puzzle_description(year=year, day=day)
        soup = BeautifulSoup(description, "html.parser")
        return [pre.code.text for pre in soup.find_all("pre")]

    def get_puzzle_input(self, year: int, day: int) -> str:
        response = self.client.get(f"/{year}/day/{day}/input")
        response.raise_for_status()
        return response.text

    def close(self) -> None:
        self.client.close()
