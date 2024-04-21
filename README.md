# rvcRemix

## Description

This program takes any audio/video file (preferably with vocals and instruments), separates vocal and instrumental tracks, applies a RVC model to vocals and re-mix them with the instrumental.
You'll need just at least one RVC model ( find some [here](https://voice-models.com/) ) store them in a folder, find an input file and you're OK!

## Features

 - [x] Generate from video/audio file (any format)
 - [ ] Generate from youtube link
 - [ ] Pitch shift the instrumental if the rvc voice has pitch shift too
 - [ ] Automatically find original pitch and fit the rvc model pitch ( if possible )
 - [ ] Edit audio separator models

## Requirements
 - python 3
 - pip
 - ffmpeg

## Installation
 - `git clone` the repo
 - `cd rvcRemix`
<details>
  <summary> (optional) you can create a python virtual environnement to avoid the project python libraries to interfere with the ones already present on your system </summary>

 - run `python -m venv venv`
 - then `source venv/bin/activate` (some IDEs can do this automatically) 
 </details>
 
 - `pip install -r install/requirements.txt`
 
## Configure

 - edit the file **utils/config.json** with a text editor and change the sections :
 - `"modelsPath" : "a path to a folder"` 2nd part with the path to the folder you put your models in (preferably each model in its subfolder)
 - `"workingDir" : "a path to a folder"` 2nd part with the path to the folder where the temporary files will be put
 - `"mode" : "cpu"` 2nd part with the mode to use, "cpu" or  "cuda"
 - `"keepTempFiles" : false` 2nd part with wether or not to keep intermediate  temp files

## Running

 - (optional) if you created a virtual environnement, run command `source venv/bin/activate` on linux or `venv\Scripts\activate` on windows (some IDEs can do this automatically)
 - then, still in a command window, `python run.py [path to the audio file] [keyword of the rvc model] [pitch (optional)]` 

## Utilities

Some useful ressources:

 - [RVC python lib](https://pypi.org/project/rvc-python/)
 - [Audio separator lib](https://pypi.org/project/audio-separator/)
 - [FFMPEG](https://ffmpeg.org/)
 
## Compatibility
Linux, Mac, Windows (as in python)

Tested systems:
ArchLinux

## Licensing
WTFPL.

**This stuff is provided as is with no warranty at all, take your own precautions before using it**.
 