
import numpy as np


def number_of_channels(image):
    new_line=np.sum(image,axis=1)
    final_value = np.max(new_line)
    threshold = np.max(new_line)*0.5
    number_channels =0
    condition =0
    while condition == 0:
        pixels=[]
        if threshold > final_value:
            break
        opt_line = new_line > threshold
        number_channels = (sum(np.diff(opt_line)))
        diff_line=np.diff(opt_line)
        pixels=list(np.where(diff_line ==1))
        pixels=pixels[0]
        if number_channels ==2:
            differ=pixels[1]-pixels[0]
            if differ > 200 and differ < 500:
                condition = 1
        if number_channels ==4:
            differa=pixels[1]-pixels[0]
            differb=pixels[3]-pixels[2]
            if differa > 220 and differa < 400:
                if differb > 150 and differb < 400:
                    condition = 1
        #print(threshold, pixels, number_channels)
        threshold = threshold * 1.001
    return [number_channels,pixels]

def chan_det(image):
    profilex = image.sum(axis=0)
    lx = len(profilex)
    offset = []
    x = []
    for i in range(lx - 1):
        if profilex[i] < profilex[i - 1] and profilex[i] < profilex[i + 1]:
            num = profilex[i]
            numx = i
            offset.append(num)
            x.append(numx)
    max_off = np.amax(offset)
    profilex_off2 = []
    for i in range(lx):
        if profilex[i] > max_off:
            num = profilex[i] - max_off
            profilex_off2.append(num)
        else:
            num = 0
            profilex_off2.append(num)
    count_start = 0
    count_end = 0
    chan_startcoord = []
    chan_endcoord = []
    for i in range(1, lx - 1):
        if profilex_off2[i] == 0:
            if profilex_off2[i - 1] != 0:
                chan_endcoord.append(i)
                count_end += 1
            if profilex_off2[i + 1] != 0:
                count_start += 1
                chan_startcoord.append(i)
    if count_end == count_start:
        no_chan = count_end
    else:
        if count_start > count_end:
            chan_startcoord = chan_startcoord[0:count_end - 2]
            no_chan = len(chan_startcoord)
        if count_start < count_end:
            chan_endcoord = chan_endcoord[1:count_start - 1]
            no_chan = len(chan_endcoord)
    ch_wid = []
    for i in range(no_chan):
        ch_widnum = chan_endcoord[i] - chan_startcoord[i]
        ch_wid.append(ch_widnum)
    avg_chanwid = int(abs(np.mean(ch_wid)))

    return (chan_startcoord, no_chan, avg_chanwid)

def cut_clice(image,start,finish):
    spacing=20
    y_size, x_size=image.shape
    if start-spacing < 0:
        finish = finish + (spacing-start)
        start = 0
    if finish+spacing > y_size:
        start = start-(y_size-finish)
        finish = y_size
    image_cut=image[start-spacing:finish+spacing,:]
    return (image_cut)