import asyncio

import httpx

from app.core.config import settings


class PokeAPIClient:
    def __init__(self):
        self.base_url = settings.pokeapi_base_url

    async def get_pokemon_name_by_id(self, client: httpx.AsyncClient, pokemon_id: int) -> str | None:
        if pokemon_id < 1:
            return None

        try:
            response = await client.get(f"{self.base_url}/{pokemon_id}")

            if response.status_code == 200:
                data = response.json()
                return data["name"]
            else:
                return None
        except httpx.RequestError as error:
            print(f"An error occurred while requesting {error.request.url}")
            return None

    async def get_pokemon_names_by_ids(self, pokemon_ids: list[int]) -> list[str]:
        if not pokemon_ids:
            return []

        async with httpx.AsyncClient() as client:
            tasks = [
                self.get_pokemon_name_by_id(client, pokemon_id)
                for pokemon_id in pokemon_ids
            ]
            results = await asyncio.gather(*tasks)

        pokemon_names = []

        for result in results:
            if result is not None:
                pokemon_names.append(result)

        return pokemon_names