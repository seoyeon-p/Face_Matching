import os
import subprocess
import csv
from collections import defaultdict
import operator

def openface_execute(aviname, csvname):
    args = [
    ".\\OpenFace_0.2.3_win_x64\\FeatureExtraction.exe",
    "-f",
    ".\\" + aviname +".avi", "-of",
    csvname + ".csv"]
    subprocess.call(args)
