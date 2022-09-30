import requests
import random
import time
import pandas as pd

try:
    plist = df = pd.read_csv('./resources/pokemon_list.csv', usecols=['pokemon'])['pokemon'].tolist()
except:
    # fallback in case file's not available
    plist = ['carvanha',
    'tangrowth',
    'simisear',
    'scyther',
    'tentacruel',
    'clawitzer',
    'trevenant',
    'gardevoir',
    'venomoth',
    'perrserker']

if __name__ == '__main__':
    
    for idx, pokemon_name in enumerate(plist):
        image_url = f'https://img.pokemondb.net/artwork/vector/large/{pokemon_name}.png'
        
        print(idx, image_url)
        img_data = requests.get(image_url).content
        with open(f'./resources/img_pokemon_png/{pokemon_name}.png', 'wb') as handler:
            handler.write(img_data)

        time.sleep(random.random() * 5)
