import nd2reader
import numpy as np
import matplotlib.pyplot as plt
import channel_utils as cu
x=[]
FOV=0
Original_filename ="/Volumes/Samsung_T3/20160630_SJ102_persister_002.nd2"
nd2 = nd2reader.Nd2(Original_filename)
for image in nd2.select(channels='488nm_jt', fields_of_view=(FOV)):
    x.append(image)
final=np.sum(x,axis=0)
number_channels,pixels=cu.number_of_channels(final)
print("number of channel sections",number_channels/2)
print(pixels)
print("First located at ",pixels[0],"ending at",pixels[1])

