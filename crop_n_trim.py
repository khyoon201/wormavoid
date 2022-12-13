#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import ffmpeg
import pandas as pd
import tkinter as tk
from tkinter import filedialog


# In[ ]:


root = tk.Tk()
root.withdraw()  

coordinates = filedialog.askopenfilename(title = "Select file",filetypes = (("CSV Files","*.csv"),))


# In[ ]:


square_size = input("Enter cropped video size: ")


# In[ ]:


def trim_byhour_cropped_avi(coordinates, square_size):
    
    #read each video file in the Results.csv file
    df = pd.read_csv(coordinates)
    dir_path = os.path.dirname(coordinates)
    
    #extract video names from list
    video = df['Label'].tolist()
    video = list(set(video))
    
    vid_extensions = [".MOV", ".mp4", ".MP4", ".mov"]
    
    for a in video: 
        name, extension = os.path.splitext(a)
        
        for (root, dirs, file) in os.walk(dir_path):
            for f in file:
                if name in f:
                    name_1, extension_1 = os.path.splitext(f)
                    if extension_1 in vid_extensions:
                        video_file = f
                
        video_path = os.path.join(dir_path, video_file)
        
        #figure out how many hours long the movie is
        probe = ffmpeg.probe(video_path)
        stream = probe['streams'][0]
        duration = stream['duration']
        hr = int(float(duration)/60)

        #extract start times from the same video:
        df_1 = df[df['Label']==a]
        start_time = df_1["start"].tolist()
        start_time = list(set(start_time))
    
        #loop through start time
        for s in start_time:
            #check how many plates have the same start time in the same video
            df_2 = df_1.loc[df_1["start"] == s]
            df_2.reset_index(inplace=True)
            i = len(df_2)
            
            #make folder to store the extracted movies
            new_folder = name+'_'+str(s)
            new_path = os.path.join(dir_path,new_folder)
            os.mkdir(new_path)    

            for n in range(i):
                os.mkdir(os.path.join(new_path,new_folder+"_"+str(n+1)))           
            
            #extract movies
            pts = "PTS-STARTPTS"
            h=1

            while h <= hr:      
                input_stream = ffmpeg.input(video_path, ss=h*60-(5)+s)
                trimmed = input_stream.trim(duration = 10).setpts(pts)
                
                for m in range(i):
                    cropped_1 = ffmpeg.filter(trimmed, 'crop', w=square_size, h=square_size, x=df_2["X"][m], y=df_2["Y"][m])
                    out_vid_1 = ffmpeg.output(cropped_1, new_path+'/'+new_folder+"_"+str(m+1)+'/'+new_folder+"_"+str(m+1)+"_{0:0=2d}".format(h)+'.avi', vcodec='rawvideo', preset='veryfast')
                    out_vid_1.run()       
        
                h += 1


# In[ ]:


trim_byhour_cropped_avi(coordinates, 480)

