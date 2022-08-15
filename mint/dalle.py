import asyncio
import base64
import os
from pathlib import Path

import cv2
from dotenv import load_dotenv
import numpy as np
import aiohttp


class NoImageError(Exception):
    pass


async def generate_image(search_query: str) -> str:
    prompt = str(search_query).replace(" ", "_")
    data = {"prompt": search_query}
    url = "https://backend.craiyon.com/generate"

    # Generate Image from Search Query
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            # If status is not ok
            if response.status != 200:
                print(await response.text())
                raise NoImageError
            image_dict = await response.json()

    # Decode and combine images
    for i, _image in enumerate(image_dict["images"]):
        image_string = base64.b64decode(_image)
        np_arr = np.frombuffer(image_string, dtype=np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        BASE_DIR = Path(__file__).resolve().parent.parent
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
        art_dir = os.path.join(MEDIA_ROOT, 'art/')
        print(art_dir)

        art_dir += prompt + ".jpg"
        print(art_dir)
        cv2.imwrite(art_dir, image)

        return "/art/" + prompt + ".jpg"


def generate_art(game, bet_type):
    if bet_type == "home_ml_win":
        game.ml_win_art = asyncio.run(generate_image(game.home_team))
    if bet_type == "away_ml_win":
        game.ml_win_art = asyncio.run(generate_image(game.away_team))
    if bet_type == "home_spread_win":
        game.spread_win_art = asyncio.run(generate_image(game.home_team))
    if bet_type == "away_spread_win":
        game.spread_win_art = asyncio.run(generate_image(game.away_team))

    game.save()
