# Satellite
This is a lightweight tool designed to automate the process of baking Skybox and Camera images in scenes.  While i've built it to create content for game engines it's designed to be flexible.

## Installation
* ZIP the Satellite folder.
* Under Preferences > Addons, click the Install button in the top-left and locate the ZIP folder you just created.
* Activate the addon by clicking the tick next to the box that will appear in the list.

You can find Satellite under the **Properties Panel > Output > Satellite**.


## Notes on Excluding and Including Objects
* Satellite will exclude all collections in a scene unless they contain a specific string you define (by default this is "Skybox").
* Satellite however *cannot exclude any objects that don't belong to a collection in the Hierarchy*, so keep this in mind when organizing your scenes.

