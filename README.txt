PyStarfire is a python-based computer version of Starfire 3rd Edition

The project is divided into several files
	Main - The main code running the game. Loading and saving of the game. Menus. Config handling.
	Worldgen - Library. Handles the generation of star systems.
	Shipyard - Library. Handles the creation of ships.
	Industry
	Combat
	
Internally, each file is organized thus.
	Generation - The stuff that relies on RNG.
	Calculation - The stuff that takes already generated data and uses it to output other data.
	Interface - Input of user data and output of game data.
