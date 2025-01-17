# TekkenBot
AI and tools for playing and understanding Tekken 7.

Created by roguelike2d. Maintained by the community.

## Related
1. The original repository:
    - WAZAAAAA0: [https://github.com/WAZAAAAA0/TekkenBot](https://github.com/WAZAAAAA0/TekkenBot)
2. Check out this additional fork for new TekkenBotPrime features:
    - compsyguy: [https://github.com/compsyguy/TekkenBot/](https://github.com/compsyguy/TekkenBot/)

## New Features in this fork

### Executable
 - [x] No more external dependecies, just one .exe file and a *data* folder.

### GUI
- [x] Menu-bar has been re-organized to make its usage more intuituve.
- [x] New custom themes can be added by placing new theme files under *./data/themes/overlay/*
- [x] Changes in themes and overlay settings can be dynamically reloaded by restarting the app *Tekken Bot > restart*. (No need to close the App)
- [x] Automatic scrolling can be now disabled to read previous log files with ease *Tekken Bot > Preferences > Scroll on Output*
- [x] A tekkenbotprime.log file is created/overwritten every time the app is run.
- [x] Added the possibility to write into the Tekken's process memory to overwrite characters, stages, among other settings. (Includes *non-playable* characters and stages)

### Overlays
- [x] Automatic overlay position change when Tekkens enters/exits Fullscreen mode.
- [x] Overlays show and hide automatically on battle's start and end. Configurable in *./data/settings.ini*
- [x] Overlays scale to different resolutions.
- [x] Resizable overlay windows on draggable mode.

#### Frame data overlay
- [x] Up to 4 frame data lines.
- [x] Frame data text widget width fits to its content.
- [x] Custom column ordering. Configurable in *./data/settings.ini*

#### Command input overlay
- [x] Input arrows and buttons mimic Tekken GUI's style. (Credits to: [mspkvp](https://github.com/mspkvp/tk7movespretty))
- [x] Support for Rage button.
- [x] SVG icon scaling.

### Audio
- [x] Overlay independent Punish Coach Alarm.
- [x] Customizable sounds and voices under under *./data/audios/voice/* and *./data/audios/sound/* respectively.

### Networking
- [x] Check for new releases on github repository and download them.

### Default settings
- [x] Initial overlay configuration can be changed in *./data/settings.ini*

### TODO
- [ ] Add a settings menu to the GUI to display or hide frame data columns and save configuration into a file.
- [ ] Reimplement other overlays (Only frame-data and command input overlays have been implemented)
- [ ] Endless bug fixes
- [ ] Complete this list :P

## Disclaimer
**Tekken's process memory overwrite has only been tested in offline mode, it probably won't work in online mode, nor I intend to make it work. Its only purpose is for debugging or for training with specific character/stages. No piracy is intended. Use at your own risk, please support BANDAI NAMCO Entertainment and buy the DLC content**

## Screenshot
![Memory Overwrite](Screenshots/memory_overwrite.png?raw=true)

## Frequently asked questions
**Q:** What is this thing?\
**A:** It's a program for Tekken 7 that shows frame data information of your moves in real-time on PC.

**Q:** How do I use this thing?\
**A:** Go to the releases page, download the latest `TekkenBotPrime_vXXX.zip`, extract the files somewhere, open `TekkenBotPrime.exe`, and finally hop into practice mode.\
If you want to run from source instead, install Python 3 and run `pip install -r requirements.txt` then `python tekken_bot_prime.py`

**Q:** The bot stopped working after a game patch!\
**A:** Wait for a good soul to update the `memory_address.ini` file, or fix it yourself by following the guide on the Wiki.

**Q:** The frame advantage of this move seems wrong!\
**A:** Double check using the alternative "manual" method to find frame advantage with the help of `tiny live frame data numbers`:
1. mirror match (because not all characters have the same jumps)
2. do your attack, neutral jump, and don't do anything else
3. set the dummy to neutral jump as second action\
...the little numbers near the big frame advantage ones should now hopefully display the correct advantage.

**Q:** I'm getting the `PID not found` error even though the game is running!\
**A:** Start the bot as admin (or alternatively start the game as non-admin).

**Q:** The bot doesn't show!\
**A:** Play borderless or windowed, full screen doesn't work.

**Q:** But I really really want to play full screen otherwise my game will lag!\
**A:** If you have a multi-monitor setup, set the Overlay Position to *Draggable* in Overlay > Position > Draggable and move the overlay to a different monitor.
## Tools
### FrameDataOverlay
A window that can go over the game to display real time move information read from memory. Requires the game to be in windowed or borderless to work or can be run as a standalone window on a second screen.
![Robot feet and bear paws 1](Screenshots/frame_data.png?raw=true)
### CommandInputOverlay
Display command inputs, similar to the one already in Tekken 7 except it gives frame by frame information and includes cancelable frames.
![Robot feet and bear paws 2](Screenshots/command_input.png?raw=true)
## Bots
Currently in progress.
### Details
Tekken Bot bots are programs that plays Tekken 7 on PC by reading the game's memory, making decisions based on the game state, and then inputting keyboarding commands. Ultimately the goal is to create emergent behavior either through specific coding it or, if possible, a generalized learning algorithm.
### Frame Trap Bot
Pushes jab or a user inputted move when getting out of block stun.
### Punisher Bot
Attempts to punish negative attacks with the best available punish. Punishes are listed in the character's file in the /TekkenData folder.
## Project details
### Prerequisites
Tekken Bot is developed on Python 3.7 and tries to use only core libraries to improve portability, download size, and, someday, optimization. It targets the 64-bit version of Tekken 7 available through Steam on Windows 7/8/10.
### Deployment
Tekken Bot distributable is built using pyinstaller with Python 3.7. On Windows, use the included build_project.ps1 file with Powershell 5.
