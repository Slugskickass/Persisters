import h5py
import numpy as np
## The fileformat is going to be Channel(number) / Channel_data
##                                               / Average
##                                               / Bacteria data


#File stuff

def save_channel_general(filename, channel_data, channel_name, data_type):
    #This needs to be smarter, it needs to have a switch the swap from write to annote.  Possible also an error check
    with h5py.File(filename, 'a') as f:
        final_data = channel_name + '/' + data_type
        dset = f.create_dataset(final_data, channel_data.shape,data=channel_data)
        #f.close()


def get_channel(channel_number, filename):
    f = h5py.File(filename, 'r')
    error = 0
    total_number = np.size(list(f.keys()))
    if channel_number > total_number:
        error = 1
    ash = list(f.keys())
    newer = ash[channel_number]
    cad = f[newer].keys()
    by = list(cad)
    final_data = ash[channel_number] + '/' + by[0]
    holdall = f[final_data]
    f.close()
    return [holdall, error]



def does_the_channel_exist(filename, channel_name):
    f = h5py.File(filename, 'r')
    out = f.get(channel_name)
    if out == None:
        return('0')
    else:
        return('1')

def list_channel_contents(filename, channel_name):
    f = h5py.File(filename, 'r')
    temp_name = '/' + channel_name
    contents = list(f[temp_name].keys())
    return(contents)

def list_channel_names(filename):
    f = h5py.File(filename, 'r')
    names=list(f.keys())
    return(names)
# Channel_name is going to be a number in the form of a string i.e. str(1)
# Channel data is likley to be one of the following ['488nm_jt', 'PH_jt', 'mCH_jt']
def get_cdata(filename, channel_name, channel_data):
    with h5py.File(filename, 'r') as f:
        final_data = channel_name + '/' + channel_data
        holdall = f[final_data]
        data_to_save = np.copy(holdall)
        return(data_to_save)

def set_channel_attribute(filename,channel_name, channel_data,attribute_name, attribute_value):
    with h5py.File(filename, 'a') as f:
        final_data = channel_name + '/' + channel_data
        holdall = f[final_data]
        f[final_data].attrs[attribute_name] = attribute_value