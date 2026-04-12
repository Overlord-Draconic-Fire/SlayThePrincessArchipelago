# Archipelago Mod – Installation Guide

## Installation

1. **Extract the mod archive**
   Unzip the downloaded mod file to access its contents.

2. **Locate the game folder**
   Navigate to your *Slay the Princess* installation directory.
   If you are using Steam:

   * Right-click the game in your library
   * Select **Manage → Browse local files**
   * This should open a folder similar to:
     `C:\Program Files (x86)\Steam\steamapps\common\Slay the Princess`

4. **Move mod files**

   * Open the `game` folder inside the installation directory
   * Copy all extracted mod files into this folder
   * Ensure the file structure is correct (for example):
     `...\Slay the Princess\game\archipelago_init.rpy`

5. **Remove existing saves in the game folder**

   * Inside the `game` folder, locate the `saves` folder
   * You can delete it or move it elsewhere
   * Note: another save location exists at:
     `C:\Users\<YourUser>\AppData\Roaming\RenPy\SlaythePrincess-1651597024`
     You do not need to modify this. A new folder named
     `SlaythePrincess-Archipelago` will be created automatically.

6. **Launch the game**
   Start the game normally.
   If the installation was successful, the Archipelago menu should appear.

7. **Connect to the server**
   Follow the in-game instructions to connect and start playing.

---

## Uninstallation

To remove the mod:

* Delete all files that were added to the `game` folder
* You may safely remove any folders introduced by the mod
* **Do not delete the `staging` folder**, as it is part of the base game
  (it originally contains `scratchpad.txt`)

---

### Debug Menu

The mod includes access to several Ren'Py debug features:

* **Shift + O** → Opens the Ren'Py console
  This is intended for viewing logs/messages only. Do not use it to run commands.

* **Shift + R** → Restarts the game
  Avoid using this while connected to the server. If you do, you should fully close the game to properly disconnect.

* **Shift + D** → Opens the developer menu
  Use at your own risk. No responsibility is taken for issues caused by its usage.
