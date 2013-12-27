from parse_rest.connection import register
from parse_rest.datatypes import Object

register("66Z4aux6QXjcfTS4HqsyxXGyBpfXrrT2a6BUaXxe", 
		 "ZIJhoPJHoOIIv9ZYC0c76LJS1ZHLeCcNoRq8k3WE")

class pGnome(Object):
    pass

gnomeScore = pGnome(moisture_level=50, gnome_name='Jono', isBelow=False)
gnomeScore.isBelow = True
gnomeScore.save()