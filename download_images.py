import sys
import requests
import random
import time
import pandas as pd


df = pd.read_csv('./resources/pokemon_list.csv')

if __name__ == '__main__':
    confirm = input(f'This script will download {len(df)} images. Are you sure?[y/n]: ')
    if confirm.lower() == 'y':
        for idx, pokemon_name in enumerate(df['pokemon']):
            image_url = f'https://img.pokemondb.net/artwork/vector/large/{pokemon_name}.png'
            
            print(idx, image_url)
            img_data = requests.get(image_url).content
            with open(f'./resources/img_pokemon_png/{pokemon_name}.png', 'wb') as handler:
                handler.write(img_data)

            time.sleep(random.random() * 5)
    else:
        sys.exit(0)