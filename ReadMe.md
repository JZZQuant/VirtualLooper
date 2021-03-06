### Program Setup
```
brew install portaudio
pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio
pip install -r requirements.txt
```
* Tries to use old floor pedals like GT-8 as midi controllers
* Can use virtual midi device like vkmp for mac for testing purposes
* on Gt-8 Set to immediate for sys bank response , you would want bank up and down to sent immediate midi message
* on Gt-8 Exp pedal switch calibrate to low force

### Hardware Setup
There are 9 possible midi controllers on GT-8 floor board ,each one of them can be used in a variety of ways to achieve a looper like feel.
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


### Midi codes for GT-8 
Ctrl :  [[[176, 80, 127, 0], 140206]]
 [[[176, 80, 0, 0], 140646]]

Exp: 
[[[176, 7, 84, 0], 712934]] to 
[[[176, 7, 0, 0], 712934]]

Expswitch:
[[[176, 81, 127, 0], 1474288]] to 
[[[176, 81, 0, 0], 1474798]]

Program:
[[[176, 0, 0, 0], 1841938]]
[[[176, 32, 0, 0], 1841939]]
[[[192, 0, 0, 0], 1841940]]
 To
[[[176, 0, 3, 0], 1841938]].   100*3
[[[176, 32, 0, 0], 1841939]]
[[[192, 39, 0, 0], 1841940]].   + 40. /85

### Finite Automata Table

State machine for running the looper. Below table explains the corresponding action committed.


| State-Action  | Stop      | Record/Overdub | Play/loop | Rhythm-Switch |
|---------------|-----------|----------------|-----------|---------------|
| Bank UP       | AutoStart | AutoStop       |SelectLayer| SelectRhythm  |
| Bank Down     | RollnStart| RollnStop      | ClearLayer| SelectRhythm  |
| Phrase 1-4    | ArmPhrase | RollnArmPhrase | PlayPhrase| SelectGenre   |
| CTL           | Record    | Loop           | Record    | NewSession    |
| CTL Long      | PlayRhythm| ExtendLoop     | StopPlay  | StopPlay      |
| Exp Pedal     | BackVol   | BackVol        | BackVol   | BackVol       |
| Exp Switch    | SaveAll   | SaveAll        | SaveAll   | SaveAll       |      


State-State Transition model:

| State-Action  | Stop(S)   | Record/OverD(R)|Play/loop(P)|Rhythm-Switch(X)|
|---------------|-----------|----------------|-----------|------------------|
| Bank UP       | Lazy R    | Lazy P         | P         | X                |
| Bank Down     | Lazy R    | Lazy P         | P         | X                |
| Phrase 1-4    | S         | Lazy R         | P         | X                |
| CTL           | R         | P              | R         | X                |
| CTL Long      | P         | Lazy R         | S         | X                |
| Exp Pedal     | S         | R              | P         | X                |
| Exp Switch    | X         | X              | X         | S                |   

todo : 
* add quantize feature in place of tap tempo.
* deploy on an external arduino like device.

MVP :

1. Single Phrase
2. No RhythmSwitch
3. Simple five alphabets automata on one track : record ,loop ,stop, play ,save all

V2: 
1. exp switch /save to file
2. autostart/autostop
3. mute/clear layer
4. program change
5. set midi out to initialize program_bank



V2.5
* **auto stop**
* **create an overdubbing state/void state**
* **split control and long_control to different events in base class**
* **code cleanup**
* **testing**
* comments 
* logging
* add config file

V3: 
*  Rhythm switch

V4:
* rollstart/rollstop/rollarmphrase
* load preset from a folder
* merge layers in a phrase and write to files
* create stickers for the pedal


### Not feasible:
1. Incremental extend loop is not feasible as it would break overdubs discontinuous so only *2 is possible
2. void state optional for now
3. for mid https://github.com/nwhitehead/pyfluidsynth and https://pypi.org/project/MIDIFile/ to create a wav