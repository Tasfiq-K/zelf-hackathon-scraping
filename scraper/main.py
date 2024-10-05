from functions import get_searched_links

#  
def main():
    kw_list = ['beautiful destinations',   
               'places to visit',
               'places to travel',
               "places that don't feel real",
               'travel hacks']
    hash_tags = ['traveltok',
                'wanderlust',
                'backpackingadventures',
                'luxurytravel',
                'hiddengems',
                'solotravel',
                'roadtripvibes',
                'travelhacks',
                'foodietravel',
                'sustainabletravel'
                ]
        
    get_searched_links(kw_list, hash_tags)

    return

if __name__ == "__main__":
    main()