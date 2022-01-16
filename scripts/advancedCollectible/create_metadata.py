from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import getBreed
from metadata.sample_metadata import metadata_template

# until https://youtu.be/M576WGiDBdQ?t=40287

def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        # returns a number 0 to 2, then we use python function to return the name
        breed = getBreed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        print(metadata_file_name)




