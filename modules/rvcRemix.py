#Youtube-dl LIBS
from __future__ import unicode_literals
import youtube_dl

# General
import os
import shutil
import json
from pathlib import Path
import random
import math

#project libs
from modules.utils import *

# audio separator libs
from audio_separator.separator import Separator

#RVC-python libs
from rvc_python.infer import infer_file

#pitchsifter
import librosa
import soundfile

class RVCRemix:

    def __init__(self,
                file="",
                url="",
                name="test",
                model="",
                modelsPath="",
                mode="cpu",
                pitch=0,
                workingDir="",
                keepTempFiles=False):

        self.file=file;
        self.url=url;
        self.rvcModel=model;
        self.name=name;
        self.modelsPath=modelsPath;
        self.ffmpegCommand="ffmpeg -hide_banner -loglevel error -y ";
        self.mode=mode;#cpu or cuda
        self.pitch=pitch;
        self.keepTempFiles=keepTempFiles;

        self.workingDir=self.initWorkingDirectory(workingDir);

        self.run();
        
    def log(self,text):
        log(str(text),"RVCRemix")

    def run(self):
        

        inputAudioFile = self.getAudioFile();
        outputFile=os.path.join(self.workingDir,Path(inputAudioFile).stem + "_final.wav")

        self.log("Starting rvc remix creation ...");
        self.log(" audio file : " + inputAudioFile);
        self.log(" model tag : " + self.rvcModel);

        if inputAudioFile == None:
            self.log("No input audio file");
        else:

            instrumental,acapella=self.separateAudio(inputAudioFile);

            if instrumental == None:
                self.log("No input instrumental file");
            else:
                rvcModel=self.getRVCModel(self.rvcModel);

                if rvcModel == None:
                    self.log("No input rvc model");
                else:
                    self.log("Applying RVC model to " + acapella);

                    rvcAudioFile=self.RVCInference(acapella,rvcModel);

                    if rvcAudioFile == None:
                        self.log("No input rvc processed file");
                    else:

                        if self.pitch > 0 or self.pitch < 0:
                            self.audioPitchShift(instrumental,self.pitch);

                        finalFile= self.mix(instrumental,rvcAudioFile,outputFile);

                        if self.file !="":
                            originalFile=Path(self.file);
                        else:
                            originalFile=Path(inputAudioFile);

                        copyPath=os.path.join(str(originalFile.parents[0]),str(originalFile.stem)+"_"+self.rvcModel+"_remix.wav");
                        self.log("coying finalfile to " + copyPath)
                        shutil.copy(finalFile,copyPath);

                        if not self.keepTempFiles and self.file != "":
                            shutil.rmtree(self.workingDir);
        return None;

    def getAudioFile(self):

        if self.url != "":
            self.log("using youtube link " + self.url)
            inputAudioFile=self.getVideo(self.url);
        elif self.file != "" :
            self.log("using file " + self.file)
            if os.path.exists(self.file):
                inputAudioFile=self.file
            else:
                inputAudioFile=None;

        if inputAudioFile != None:
            filename=os.path.basename(inputAudioFile);
            copiedFile=os.path.join(self.workingDir,filename);
            shutil.copy(inputAudioFile,copiedFile);
            inputAudioFile=copiedFile;

            convertedFile=os.path.join(self.workingDir,Path(filename).stem + ".wav");

            if not os.path.exists(convertedFile):
                os.system(self.ffmpegCommand + "-i "+ '"' +copiedFile + '"' + " " +  '"' + convertedFile + '"' )

                inputAudioFile = convertedFile;
                os.remove(copiedFile);

        return inputAudioFile

    def getVideo(self,url):
        opts = {
            'format': 'bestaudio/best',
            'forcefilename':"yt_"+self.name+".wav"
        }

        ydl= youtube_dl.YoutubeDL(opts);
        y=ydl.download([url]);
        self.log("ytdownload output : " + str(y));

        #convert video to wav file
        '''
        audioFile="youtube_audio.wav"
        cmd="ffmpeg -i " + my_video.mp4 +" -c copy -map 0:a " + audioFile
        os.system(cmd);
        '''

    def separateAudio(self,inputAudioFile):
        acapella=None;
        instrumental=None;

        # Initialize the Separator class (with optional configuration properties below)
        separator = Separator()

        # Load a machine learning model (if unspecified, defaults to 'UVR-MDX-NET-Inst_HQ_3.onnx')
        separator.load_model()

        # Perform the separation on specific audio files without reloading the model
        output_files = separator.separate(inputAudioFile)

        self.log("separated audio files : "  + str(output_files));

        acapella=os.path.join(self.workingDir,"acapella.wav");
        instrumental=os.path.join(self.workingDir,"instrumental.wav");

        shutil.move(output_files[0],acapella);
        shutil.move(output_files[1],instrumental);

        return instrumental,acapella; 

    def initWorkingDirectory(self,rootDir):
        if not os.path.exists(rootDir):
            os.mkdir(rootDir)

        self.log("Working root dir : " + rootDir);

        workingDir=os.path.join(rootDir,self.name);

        if os.path.exists(workingDir):
            shutil.rmtree(workingDir);

        os.mkdir(workingDir);
        
        return workingDir;

    def scanAvailableRVCModels(self):
        availableModels=[];
        self.log("Available models : ")
        for root, dirs, files in os.walk(self.modelsPath):
            for file in files:
                if file.endswith(".pth"):
                    availableModels.append(os.path.join(root, file));
                    self.log(file)
                if file.endswith(".index"):
                    index=os.path.join(root, file);
        
        return availableModels;

    def getRVCModel(self,rvcModel):
        rvcmodel=None
        availableModels=self.scanAvailableRVCModels();

        for model in availableModels:
            if rvcModel.lower() in model.lower():
                rvcmodel=str(model);
                return rvcmodel;
        
        if rvcmodel == None and len(availableModels) >0 :
            rvcmodel=str(availableModels[random(math.floor(len(availableModels)))]);

        self.log("Returned rvc model : " + rvcmodel);

        return rvcmodel;

    def RVCInference(self,acapella,rvcModel):
        outfile=None;

        try:
            out=os.path.join(self.workingDir,"final.wav")

            result = infer_file(
                input_path=acapella,
                model_path=rvcModel,
                #index_path="",  # Optional: specify path to index file if available
                device=self.mode+":0", # Use cpu or cuda
                f0method="harvest",  # Choose between 'harvest', 'crepe', 'rmvpe', 'pm'
                f0up_key=self.pitch,  # Transpose setting
                opt_path=out,  # Output file path
                index_rate=0.5,
                filter_radius=3,
                resample_sr=0,  # Set to desired sample rate or 0 for no resampling.
                rms_mix_rate=0.25,
                protect=0.33,
                version="v2"
            );
            outfile=out;
          
            self.log("RVC processed file : " +  outfile);

        except Exception as error:
            handleErrors(error);
            self.log("Error while doing RVC inference")

        return outfile;

    def mix(self,channel1,channel2,outputFile):
        sampleFreq=44100;
        mixOut=None
        d="0"
        adelay=str(0);
        self.resampleAudioFile(channel1,sampleFreq=sampleFreq);
        self.audioNormalize(channel1);
        self.resampleAudioFile(channel2,sampleFreq=sampleFreq);
        command = [
            self.ffmpegCommand + "-i " + '"' + channel2 + '"' +  " -i " + '"' + channel1 + '"',
            "-filter_complex",
            #'"[0]afade=t=in:curve=esin:ss=0:d='+d+',adelay='+adelay+'|'+adelay+'[bg];',
            '"[0]afade=t=in:curve=esin:ss=0:d='+d+',adelay='+adelay+'|'+adelay+'[bg];',
            "[1]volume=1[fg];",
            '[bg][fg]amix=inputs=2:duration=longest"',
            '"'+outputFile+'"'
        ]

        result=os.system(" ".join(command));

        os.remove(channel1);
        os.remove(channel2);

        mixOut=outputFile;

        return mixOut;
    
    def resampleAudioFile(self,file,sampleFreq=44100):
        self.log("resampling "+ file)
        audioFormat=file[file.index("."):]
        filedResampled = file[:file.index(".")]+"_"+str(sampleFreq) +audioFormat;
        os.system("ffmpeg -hide_banner -loglevel error -y -i " + file +" -ar "+ str(sampleFreq) +" -ac 2 "+ filedResampled);
        os.remove(file);
        shutil.copyfile(filedResampled,file);
        os.remove(filedResampled);

    def audioNormalize(self,file): 
        self.log("Normalize file " + file);    
        os.system('ffmpeg-normalize -f ' + os.path.join(file) + ' -o ' + os.path.join(file))

    def audioPitchShift(self,file,pitch):
        self.log("Running pitch shift to " + file);
        pitchshiftedFile=os.path.join(self.workingDir,"pitchshifted.wav");

        y, sr = librosa.core.load(file);
            
        # Applying +6 semitone pitch shift
        y_pitched = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=pitch*2)

        # Save the modified audio to a new file
        #librosa.output.write_wav(pitchshiftedFile, y_pitched, sr)
        soundfile.write(pitchshiftedFile,y_pitched,sr);

        os.remove(file);
        shutil.copyfile(pitchshiftedFile,file);
        os.remove(pitchshiftedFile);

