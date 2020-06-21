# Tower Defense Game
This is a generic tower defense, everyone knows how these look like.

## game.py
This is the main game file.

## editor.py
This is the **level editor** for creating game levels.

You left click to place an enemy path and left click on an existing path to delete it. Make sure to click **in order!** This is crucial as enemies will follow the tiles you create in the order you created them. The red tile is where enemies spawn. The last tile you create will automatically become the exit.

The **Save button** will move the whole path to the center of the screen and then save it in levels.json. Tiles surrounding the enemy path (where you place your defensive buidlings) will be automatically generated when the level is loaded in *game.py*.
