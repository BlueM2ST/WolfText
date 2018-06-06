 # WolfText version 1.1

 WolfText Tool by BlueMist

 Localization and ease of writing tool for the Wolf RPG Editor.
 
 **Due to not properly decoding shift-jis (or any non-UTF8 or ASCII encoding) the program will currently only work if the game text was input in UTF8 or ASCII (like on Windows under an English locale).**

 **This tool is still in development, so there may be bugs (it was only tested on the Sample 
 Game). This tool does not modify the original
 files, it just reads them and outputs new modified files. However, you should make a 
 backup of your maps before using it and move your modified maps out of the output folder
 after using it.**

 # What it does

 Taking inspiration from a number of RPGMaker localization plugins, I have attempted
 to give similar functionality to the Wolf RPG Editor.

 However, due to my inexperience with the engine, I am currently unable to load text 
 directly from a file during runtime. This tool gets around this in one simple
 way: the tool must be run on the map files prior to building the game.

 This tool allows you to keep all of your text in a single json file for easy
 reference, addition, and localization.

 **Note:** if you are planning to use this version of the tool, **ALL** of your text must use 
 it. If even one `Show Message` is in the incorrect format, this tool **will** output a
 broken map.
 
 **Fortunately**, there is a text extraction feature of this tool. Any existing text in a map
 will be extracted to the json file in the correct format. The map will also be modified into
 the correct format for easy editing. 

 # What is the Wolf RPG Editor?
 
 From the User Manual: 
 
 > WOLF RPG Editor is a game construction tool that can create complex role playing games.  
 > The games you make with it can be freely distributed, submitted to contests, and sold.  
 > It's completely free, so all its functions are available, including encryption functionality.  
 > With the proper mastery, you can make any kind of game, not just RPGs. 
 
 Created and maintained by SmokingWOLF, it was translated into English by Velella Himmel
 (vgperson) and edited by Jeffrey Casey(Widderune).
 
 You can download the latest version on Widderune's [website](https://widderune.wixsite.com/widderune/wolf-rpg-editor-english). 
 
 # How the tool works
 
 To show text in the Wolf RPG Editor, there is the command `Show Message` which
 stores this text in the map file.
 
 Instead of inserting the text directly into the editor, this tool allows you to 
 write a placeholder such as `@text001`. This text will be then linked to 
 the json keys like:
 ```
 
 "text": {
      "newmap_test": {
          "@text001": "This text will be replacing the value of key 1 in the map.",
          "@text002": "This text will be replacing the value of key 2 in the map."
       }
  }

```

 Where `newmap_test` is the name of the map file. 
 All placeholder text must begin with a setter character like `@`. This character
 can be modified in the json file to any character supported by the engine.
 
 **The json file in this repo holds the template to use as well as other important config data.**

 This tool handles extracting text from map files into a json file, and also
 handles inserting the text from the json file into the map files. 
 It just needs the directory of the map files to be set in the json file.
 
 For more advanced projects, some values can be changed in the json file such
 as the `maxCharactersInt` value if the text box has been modified.
 
 # Fixes from version 1.0
 - Linebreaks now work properly and will account for default image placement in the textbox.
 - The functionality to extract text has been added.
 - Fixed some bugs causing output map files to be corrupt.
 - Better handling of almost everything.
 - Added better custom placeholder support, easier-to-write placeholder keys.
 
 # TODO
 For version 1.2:
 - Extract choice text and comments.
 - Add a few more situations where linebreaks might not be accurate.
 - Add support for maps that are not only in the tools format.
 - Extract and reinsert text from the database and common event files.
 - Fix encoding issues, most notably with shift-jis.
 - Extract system variables.
