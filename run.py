import sys
import json
from pathlib import Path
from modules.rvcRemix import *

def bulkProcess(jsonFile=""):

    if jsonFile != "":
        jsonData=json.load(open(jsonFile));
        songs=jsonData['songs'];
    else:
        songs=[
            { "name" : "remix1", "file" : "path to original file.mp4", "modelTag" : "booba", "pitch" : 0 }
        ];

    for song in songs:
        try:
            data=getConfigFile(os.path.join("utils","config.json"));

            if data != None:

                config=data["config"];
                modelsPath=config["modelsPath"];
                mode=config["mode"] # or cuda;
                workingDir=config["workingDir"];
                keepTempFiles=config["keepTempFiles"];
                copySeparatedFiles=config["copySeparatedFiles"];
                              
                modelTag=song["modelTag"];

                #r=RVCRemix(modelsPath=modelsPath,mode=mode,workingDir=workingDir,name=Path(file).stem,file=file,model=modelTag,pitch=pitch,keepTempFiles=keepTempFiles,copySeparatedFiles=copySeparatedFiles);
    
            if "pitch" not in song.keys():
                song |= {"pitch":0};

            pitch=song['pitch'];

            if "file" in song.keys():
                name=Path(song["file"]).stem;
                r=RVCRemix(modelsPath=modelsPath,mode=mode,workingDir=workingDir,name=name,file=song["file"],model=modelTag,pitch=pitch,keepTempFiles=keepTempFiles,copySeparatedFiles=copySeparatedFiles);
                #r=RVCRemix(modelsPath=modelsPath,mode=mode,workingDir=workingDir,name=name.stem,file=song["file"],model=song["modelTag"],pitch=song["pitch"]);
            elif "url" in song.keys():
                r=RVCRemix(modelsPath=modelsPath,mode=mode,workingDir=workingDir,name=name,url=song["url"],model=modelTag,pitch=pitch);
        
        except:
            print("error for song " + song['name'])

def getConfigFile(path):
    data=None;
    if not os.path.exists(os.path.join("utils","config.json")):
        shutil.copy(os.path.join("utils","default_config.json"),os.path.join("utils","config.json"))

    #try:
    data=json.load(open(path));

    #except:
    #    print("error while loading config file")

    return data

def main():

    def usage():
        print("usage:");
        print("python run.py [path to the audio file] [keyword of the rvc model] [pitch]");

    if len(sys.argv) >=3 and len(sys.argv)<5 and sys.argv[1] != "--bulk":

        data=getConfigFile(os.path.join("utils","config.json"));

        if data != None:

            config=data["config"];
            modelsPath=config["modelsPath"];
            mode=config["mode"] # or cuda;
            workingDir=config["workingDir"];
            keepTempFiles=config["keepTempFiles"];
            copySeparatedFiles=config["copySeparatedFiles"];

            file=sys.argv[1];
            modelTag=sys.argv[2];
            pitch=0;

            if not os.path.exists(file):

                print("file does not exist : " + file);

            else:

                if len(sys.argv)==4:
                    pitch=int(sys.argv[3]);

                r=RVCRemix(modelsPath=modelsPath,mode=mode,workingDir=workingDir,name=Path(file).stem,file=file,model=modelTag,pitch=pitch,keepTempFiles=keepTempFiles,copySeparatedFiles=copySeparatedFiles);
        
    elif sys.argv[1] == "--bulk":
        print("Bulk mode with json file selected");
        if len(sys.argv) == 3:
            jsonFile=sys.argv[2];
            if os.path.exists(jsonFile):
                bulkProcess(jsonFile);
            else:
                print("Json bulk remix file does not exist : " + jsonFile);

    else:
        print(len(sys.argv));
        usage();

main();