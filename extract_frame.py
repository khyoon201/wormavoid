#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import ffmpeg
import tkinter as tk
from tkinter import filedialog


# In[ ]:


root = tk.Tk()
root.withdraw()  

f = filedialog.askopenfilename()


# In[ ]:


#spit out frame pic first
#must input file_path

def extract_frame(file_path):
    dir_path = os.path.dirname(file_path)
    basename = os.path.basename(file_path)
    name, extension = os.path.splitext(basename)

    #extract a single frame to find coordinates of plates
    frame = ffmpeg.input(file_path, ss=50)
    folder = os.path.dirname(file_path)
    output_frame = ffmpeg.output(frame, dir_path+'/'+name+'.jpeg', vframes=1, format='image2')
    output_frame.run(capture_stdout=True)   


# In[ ]:


extract_frame(f)

