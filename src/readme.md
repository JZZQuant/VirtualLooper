### Package Setup
* Uses SoundDevice python for audio and pygame for midi , all dependencies can be installed using pip install -r requirements.txt
* Tries to use old floor pedals like GT-8 as midi controllers
* Can use virtual midi device like vkmp for mac for testing purposes


### Hardware Setup
There are 9 possible midi controllers on GT-8 floor board each one of them can be used in a variety of ways to achieve a looper like feel.
1. Bank Up 
2. Bank Down
3. Patch Selectors *4
4. Ctrl cc
5. Exp Pedal
6. Exp Pedal Switch


| Controller | Usage Logic | Midi Message  | Action | Expression switch Condition |
|------------|--------------|-------------|--------|-----------|
| Bank Down/Up | Rewrite particular overdub select|Program_no//4 is treated as drum change and not as phrase change| Changes drum pattern | Off|
| Patches 1-4 | Selects Phrase to work on and starts playing or waits for recording,Loop is padded with empty string if phrase changed in the middle of recording | Program_no%4 is the phrase number any time| Selects the Phrase to work on| Off|
| Ctrl CC | Press once | CC | Toggle between record/play|Off|
| Ctrl CC | Long Press | CC | Toggle between Stop_Save/Play |Off|
| Expression pedal CC| Changes volume of backing track and keeps the recording vol intact|CC Message  | Modifies volume of backing track| NA|
| Exp Switch On | Sets a flag value to work on switch mode | PC |sets flag for genre selection and tap tempo | NA|
| Bank Down/Up | Traverse through Drum Patterns|Program_no//4 is treated as drum change and not as phrase change| Changes Drum pattern | On|
| Patches 1-4 | Selects onw of the four genres| Program_no%4 is the Genre number any time| Selects the genre to work on| On|
| Ctrl CC | Press once | CC | Save and clear all on prompt|On|
| Ctrl CC | Long Press | CC | Tempo tap |On|


