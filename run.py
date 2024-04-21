import sys
import json
from pathlib import Path
from modules.rvcRemix import *

def bulkProcess():

    songs=[
        { "name" : "pochonbleu", "file" : "/home/cala/Downloads/rvcremix/pochonbleu.mp4", "modelTag" : "booba", "pitch" : 0 }
        
        #{ "name" : "licence4", "file" : "/home/cala/Downloads/rvcremix/licence4.mp4", "modelTag" : "goldman", "pitch" : 0 }
        #{ "name" : "simplebasique", "file" : "/home/cala/Downloads/simplebasique.mkv", "modelTag" : "macron", "pitch" : 0 },
        #{ "name" : "dudule", "file" : "/home/cala/Downloads/dudule.mkv", "modelTag" : "patton", "pitch" : 0 },
        #{ "name" : "auteuilneuilly", "file" : "/home/cala/Downloads/auteuilneuilly.mkv", "modelTag" : "vianney", "pitch" : 0 },
        #{ "name" : "retienslanuit", "file" : "/home/cala/Downloads/retienslanuit.webm", "modelTag" : "brassens", "pitch" : -3 },
        #{ "name" : "jevousemmerde", "file" : "/home/cala/Downloads/jevousemmerde.mkv", "modelTag" : "bud", "pitch" : 0 },
        #{ "name" : "lafievre", "file" : "/home/cala/Downloads/lafievre.mkv", "modelTag" : "sarkozy", "pitch" : 0 },
        #{ "name" : "pochespleines", "file" : "/home/cala/Downloads/pochespleines.mkv", "modelTag" : "claudefrancois", "pitch" : 0 } 
        #{ "name" : "poinconneur", "file" : "Le Poinconneur des Lilas-N5onILE73a0.m4a", "modelTag" : "dalida", "pitch" : 0 }
        #{ "name" : "lezizi", "file" : "/home/cala/Downloads/lezizi.mkv", "modelTag" : "dalida", "pitch" : 0 },
        #{ "name" : "henrydes", "file" : "/home/cala/Downloads/henrydes.mkv", "modelTag" : "booba", "pitch" : 0 }
        #{ "name" : "corsmalade", "url" : "https://www.youtube.com/watch?v=HHd1gBWjKmo", "modelTag" : "servietsky", "pitch" : +3 }
        #{ "name" : "caroline", "file" : "/home/cala/Downloads/caroline.mkv", "modelTag" : "macron", "pitch" : 0 },
        #{ "name" : "connemara", "file" : "/home/cala/Downloads/connemara.mp4", "modelTag" : "montmirail", "pitch" : 0 }
        #{"name" : "cagoule", "file" : "/home/cala/Downloads/foustacagoule.mp4", "modelTag" : "booba", "pitch" : 0 },
        #{"name" : "marchalombre" , "file"  :"/home/cala/Downloads/marchalombre.mkv","modelTag" : "bunny","pitch" : +2 },
    ]

    for song in songs:

        try:

            if "pitch" not in song.keys():
                song |= {"pitch":0};

            if "file" in song.keys():
                r=RVCRemix(modelsPath=modelsPath,mode=mode,workingDir=workingDir,name=song["name"],file=song["file"],model=song["modelTag"],pitch=song["pitch"]);
            elif "url" in song.keys():
                r=RVCRemix(modelsPath=modelsPath,mode=mode,workingDir=workingDir,name=song["name"],url=song["url"],model=song["modelTag"],pitch=song["pitch"]);
        
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

    if len(sys.argv) >=3 and len(sys.argv)<5 :

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

            if len(sys.argv)==4:
                pitch=int(sys.argv[3]);

            r=RVCRemix(modelsPath=modelsPath,mode=mode,workingDir=workingDir,name=Path(file).stem,file=file,model=modelTag,pitch=pitch,keepTempFiles=keepTempFiles,copySeparatedFiles=copySeparatedFiles);
    else:
        print(len(sys.argv))
        usage();

main();