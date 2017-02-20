import nd2reader
import h5py
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import channel_utils as cu
import Persister_utils as pu

#Inputs and blank variables
FOV=0
x=[]
Original_filename ="/Volumes/Samsung_T3/20160630_SJ102_persister_002.nd2"
#Original_filename = "/Users/Ashley/Desktop/20160728_SDB1_LABPENAB001.nd2"
nd2 = nd2reader.Nd2(Original_filename)
channel_names = nd2.channels
number_of_exposure_types=np.size(channel_names)

#We need a PL image to load for the channel work
for image in nd2.select(channels='488nm_jt', fields_of_view=(FOV)):
    x.append(image)
new_image=np.sum(x,axis=0)
#print('Sent')

# Calulate the number of channel sections (1 returns (2) 2 returns (4) and the top and bottom of the channels
number_channels,pixels=cu.number_of_channels(new_image)
print("number of channel sections",number_channels/2)
print(pixels)
print("First located at ",pixels[0],"ending at",pixels[1])

#Use the cut image to calculate the positions of the
image_cut = cu.cut_clice(new_image,pixels[0],pixels[1])
chan_startcoord, no_chan, avg_chanwid = cu.chan_det(image_cut)
print("channel_positions",chan_startcoord)
#print(chan_startcoord)
#print(no_chan)
#print(avg_chanwid)

#Build a file name
fn1='FOV_'
fn2=str(FOV)
if number_channels == 2:
    fn3='_a'
if number_channels == 4:
    fn3='_b'
filename = fn1+fn2+fn3+'.h5'
print(filename)

#This can be looped over channels and channel types
for channel in range(1, 10):
    for X in channel_names:
        x = []
        time_stamp = []
        text_data=[]
        print("Channel #", channel, "Measurement", X)
        for image in nd2.select(channels=X, fields_of_view=(FOV)):
            time_stamp.append(image.timestamp)
            image= cu.cut_clice(image,pixels[0],pixels[1])
            image = image[:,chan_startcoord[channel]:chan_startcoord[channel]+avg_chanwid]
            x.append(image)
        x=np.array(x)
        time_stamp=np.array(time_stamp)
        #channel_test=x[:,:,chan_startcoord[channel]-4:chan_startcoord[channel]+avg_chanwid+10]
        channel_test=x
        # Here we save the data to the file
        pu.save_channel_general(filename, channel_test, str(channel), str(X))
        pu.save_channel_general(filename, time_stamp, str(channel), str(X)+'time_data')
        #Here we assign attributes to the data
        pu.set_channel_attribute(filename, str(channel), str(X), "Channel_position", str(chan_startcoord[channel]))
        pu.set_channel_attribute(filename, str(channel), str(X), "Pixel_size", str(nd2.pixel_microns))
    #Here we will save channel specific information
