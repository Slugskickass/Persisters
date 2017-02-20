import nd2reader
import Persister_utils as pu
import h5py
import numpy as np
from scipy import signal


#nd2 = nd2reader.Nd2("/Users/Ashley/Desktop/20160728_SDB1_LABPENAB001.nd2")
nd2 = nd2reader.Nd2("/Volumes/Samsung_T3/20160630_SJ102_persister_002.nd2")
print(nd2.channels)
holdall = np.zeros((nd2.height,nd2.width), 'double')
FOV=1

for image in nd2.select(channels="488nm_jt", fields_of_view=(FOV)):
    holdall=holdall+image

line_profile=np.sum(holdall,axis=1)
window = np.diff(signal.gaussian(nd2.height, std=15))
cor_line = np.convolve(line_profile, window, mode='same')

cor_line_fit=cor_line[40:-40]
mean_val=np.mean(cor_line_fit**2)

out=signal.find_peaks_cwt(cor_line_fit**2,np.arange(1,50))
myarray_out = np.asarray(out)

selected_points = np.where(cor_line_fit[out]**2 > mean_val)

myarray_selected_points =(selected_points)
new_points=(myarray_out[myarray_selected_points])

new_image=nd2[0]
new_image=new_image[new_points[0]-100:new_points[1]+50,:]
new_lines=(np.sum(new_image,axis=0))

window = np.diff(signal.gaussian(nd2.height, std=2))
cor_line = np.convolve(new_lines, window, mode='same')

outer_up=signal.find_peaks_cwt(cor_line,np.array([18, 19, 20, 21, 22, 23, 24, 25, 26, 27]),noise_perc=70)
outer_down=signal.find_peaks_cwt(-1*cor_line,np.arange(10,50))


number_frames=(len(nd2)/(len(nd2.channels)*np.size(nd2.fields_of_view)))
channel_name='channel'

number_channels=(np.size(outer_up))
print(number_channels)

filename='FOV'+str(FOV)+'.h5'
for x in range(0, number_channels-40):
    count=0
    channel_of_interest=x
    print(x)
    b=np.zeros((int(number_frames),new_points[1]-new_points[0]+150,30),'double')
    a = np.zeros((int(number_frames), new_points[1] - new_points[0] + 150, 30), 'double')
    for image in nd2.select(channels="PH_jt", fields_of_view=(FOV)):
        new_image=image[new_points[0]-50:new_points[1]+100,:]
        b[count,:,:]=new_image[:,outer_up[channel_of_interest]-10:outer_up[channel_of_interest]+20]
        count=count+1
    count=0
    for image in nd2.select(channels="mCH_jt", fields_of_view=(FOV)):
        new_image=image[new_points[0]-50:new_points[1]+100,:]
        a[count,:,:]=new_image[:,outer_up[channel_of_interest]-10:outer_up[channel_of_interest]+20]
        count=count+1

    pu.save_channel_phase(filename, b, str(x))
    pu.save_channel_PL(filename, a, str(x))