import Persister_utils as pu
import nd2reader
import numpy as np
import matplotlib.pyplot as plt
import h5py


filename='FOV_f_v61.h5'


#pu.save_channel(filename, channel_data, channel_name)
#print(pu.does_the_channel_exist(filename, channel_name))
#print(pu.list_channel_contents(filename, channel_name))
#out = pu.list_channel_names(filename)



out = pu.list_channel_names(filename)
temp='/'+out[1]
print(pu.does_the_channel_exist(filename, temp))
outer = pu.list_channel_contents(filename, temp)
bunnies =str(outer)
bunnies=bunnies[2:-2]
kittens = str(temp) + '/' + str(bunnies)
print(kittens)
holdall, error = pu.get_channel(kittens, filename)