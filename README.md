# ModSync

Python script : "Script.py"                 
Executable : "dist/Script/Script.exe" (need whole dist folder to launch)

# What does it do 

- Creates files to send to your friends containing everything necessary to sync your mods (check you have the same mods, copy modlists, syncs config)
- If you don't have the same mods It will show you mismatch and allow you to open the modpages so that you can sub/unsub if necessary
- Note that the source will need to create the modlist manually in rimworld before using the script, and the recipient will need to load it manually in rimworld after using the script
- The script won't check mod version, only that the mod is present
- The scripts syncs the whole config folder so your MP username will be the same for every player (+ some numbers) not a problem but you can still modify it manually if you want your username (could be integrated to script but I'm lazy)
- Mod compare only works if mods are installed through workshop

# How to use

- Choose whether to automatically resolve pathing or not (if folders can't be found automaticlaly it should prompt you to manually enter paths, if it still doesn't work choose manual)
- To Share mods :
    - Click generate Sync Folder
    - Enter the name of the folder you want to save the necessary files in (and the one you'll send to your friends) the folder will be created on desktop
    - Fill the necessary paths (if auto pathing is enabled only name should be necessary)
    - Click create sync file
 - To load mods :
    - Click Import Sync folder
    - Enter the path of the folder sent by the source (see previous point)
    - Fill the necessary paths (if auto pathing is enabled only name should be necessary)
    - Click Sync
    - If there is a mod mismatch the mismatch window will open listing which mods you need to remove or add, you can then open the respective modpages by clicking open modpage
