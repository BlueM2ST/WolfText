 # WolfText v1.0

 WolfText Tool by BlueMist

 Localization and ease of writing tool for the Wolf RPG Editor.

 **This tool is still in development, so there may be bugs. This tool does not modify the original
 files, it just reads them and outputs new modified files. However, it is always good to have a 
 backup of your maps.**

 # What it does

 Taking inspiration from a number of RPGMaker localization plugins, I have attempted
 to give similar functionality to the Wolf RPG Editor.

 However, due to my inexperience with the engine, I am currently unable to load text 
 directly from a json file during runtime. This tool gets around this in one simple
 way: the tool must be run on the map files prior to building the game.

 This tool allows you to keep all of your text in a single json file for easy
 reference, addition, and localization.

 **Note:** if you are planning to use this version of the tool, **ALL** of your text must use 
 it. If even one `Show Message` is in the incorrect format, this tool will almost
 certainly output a broken map.

 # What is the Wolf RPG Editor?
 
 From the User Manual: 
 
 > WOLF RPG Editor is a game construction tool that can create complex role playing games.  
 > The games you make with it can be freely distributed, submitted to contests, and sold.  
 > It's completely free, so all its functions are available, including encryption functionality.  
 > With the proper mastery, you can make any kind of game, not just RPGs. 
 
 Created and maintained by SmokingWOLF, it was translated into English by Velella Himmel(vgperson) and edited by Jeffrey Casey(Widderune).
 
 You can download the latest version on Widderune's [website](https://widderune.wixsite.com/widderune/wolf-rpg-editor-english). 
 
 # How the tool works
 
 To show text in the Wolf RPG Editor, there is the command `Show Message` which then
 stores this text in the map file.
 
 Instead of inserting the text directly into the editor, this tool allows you to 
 write a placeholder such as `$$newmap_0001$$`. This text will be then linked to 
 the json keys like:
 ```
 
 "text": {

      "newmap_test": {
        "$$newmap_0001$$": "This text will be replacing the key 1.",
        "$$newmap_0002$$": "This text will be replacing the key 2."
       }
  }

```

 Where `newmap_test` is the name of the map file. 
 By default, all placeholder text must begin and end with `$$`, but this can be 
 modified with any other dual-characters in the json file
 
 **The json file in this repo holds the template to use as well as other important config data.**

 This tool handles inserting the text from the json file into the map files. 
 It just needs the directory of the map files to be set in the json file.
 
 For more advanced projects, some values can be changed in the json file such
 as the `maxCharactersHex` value if the text box has been modified.
 
 #TODO
 For version 1.1:
 - Add easier placeholder text support (likely to be something like `@01_01`)
 - Rewrite how it reads and extracts the text from the map files.
 - Which will lead to being able to pull existing text out of map files,
 possibly leading to easier translations of existing games.
 - make it harder for the tool to output broken maps due to format issues, or add a map
 check function to the tool.
