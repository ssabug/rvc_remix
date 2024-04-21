import os
import platform

os = str(platform.platform()).lower();

os.system("python -m venv venv");

if "win" in os:
    os.system("venv\Scripts\activate"); # or "call venv/Scripts/activate"
else:
    os.system("source venv/bin/activate");

choice = input("Type gpu or cpu to install the right librairies\n");

if choice == "gpu":

    os.system('pip install "audio-separator[gpu]"');

    os.system("pip uninstall torch onnxruntime");
    os.system("pip cache purge");
    os.system("pip install --force-reinstall torch torchvision torchaudio");
    os.system("pip install --force-reinstall onnxruntime-gpu");


    os.system("sudo apt install nvidia-cuda-toolkit");

if choice == "cpu":
    os.system('pip install "audio-separator[cpu]"');

path=str(os.path.join("utils","requirements.txt"));
os.system('pip install -r ' + path);