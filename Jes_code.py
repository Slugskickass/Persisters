import nd2reader
import matplotlib.pyplot as plt
import Persister_utils as pu
import numpy as np
from PIL import Image
import skimage.io as io
import os
from scipy import signal

# nd2 = nd2reader.Nd2("C:\\Users\\jessf\\Documents\\PHY480\\20160728_SDB1_LABPENAB001.nd2")
nd2 = nd2reader.Nd2("/Volumes/Samsung_T3/20160630_SJ102_persister_002.nd2")
holdall = np.zeros((3, nd2.height, nd2.width), 'uint16')
no_f_v = len(nd2.fields_of_view)
print(no_f_v, ' fields of view detected')


# not yet for all fields of view, just loop over all fields of view to extract images

def set_chan_num(image):
    line_profile = image.sum(axis=1)
    window = np.diff(signal.gaussian(nd2.height, std=15))
    ch_line = np.convolve(line_profile, window, mode='same')
    ch_line = ch_line[35:-35] ** 2

    mean_threshold = np.mean(ch_line)
    peaks = signal.find_peaks_cwt(ch_line, np.arange(1, 50))
    det_peaks = np.asarray(peaks)

    sel_peaks = np.where(ch_line[peaks] > mean_threshold)
    peaks_detf = det_peaks[sel_peaks]

    no_sets = len(peaks_detf)
    print(no_sets)
    print(peaks_detf)
    return (no_sets, peaks_detf)


def one_set_chan(peaks_detf, image):
    thresh = 60
    starty = peaks_detf[0] - thresh
    endy = peaks_detf[1] + 1.5 * thresh
    imy_crop = image[starty:endy, :]
    return (imy_crop, starty, endy)


def two_set_chan(peaks_detf, image):
    thresh = 60
    starty1 = peaks_detf[0] - thresh
    endy1 = peaks_detf[1] + 1.5 * thresh
    starty2 = peaks_detf[2] - thresh
    endy2 = peaks_detf[3] + 1.5 * thresh
    imy_crop1 = image[starty1:endy1, :]
    imy_crop2 = image[starty2:endy2, :]
    return (imy_crop1, imy_crop2, starty1, endy1, starty2, endy2)


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


def extraction(no_chan, chan_startcoord, avg_chanwid, images, starty, endy, setchan, f_v):
    for i in range(no_chan):
        threshold = 10
        start_xcoord = chan_startcoord[i] - threshold
        if start_xcoord < 0:
            start_xcoord = 0
        else:
            start_xcoord = start_xcoord
        end_xcoord = chan_startcoord[i] + avg_chanwid + threshold * 1.5

        l = len(images)
        new_im = []
        chan_matrix = []
        togo=[]
        for j in range(l):
            temp = images[j]
            tempcrop = temp[starty:endy, start_xcoord:end_xcoord]
            chan_matrix.append(tempcrop)
            ######save chan_matrix as hdf5 file############## figure out how to do entire file (append?)

            fn0 = str(setchan)
            fn1 = str('_f_v')
            fn2 = str(f_v + 1)
            fn3 = str('ch_')
            fn4 = str(i + 1)
            fn5 = str('_t_')
            fn6 = str(j)
            #final = fn0 + fn1 + fn2 + fn3 + fn4 + fn5 + fn6
            #final = fn3 + fn4
            #io.imsave('{final}.tif'.format(final=final), tempcrop)
            togo.append(tempcrop)
        filename = 'FOV' + fn1 + fn2 + '.h5'
        print(filename)
        final = fn3 + fn4
        print(final)
        #print(type(togo))
        #print(np.asarray(togo))
        check_channel = pu.does_the_channel_exist(filename, final)
        if check_channel == 0:
            pu.save_channel_phase(filename, np.asarray(togo), final)
    return ()


def extract_save(field_of_view_range):
    f_v = field_of_view_range
    # for f_v in range(f_v):
    images = []
    flu_im = []

    for image in nd2.select(channels="PH_jt", fields_of_view=((f_v))):
        images.append(image)
    for ref in nd2.select(channels='488nm_jt', fields_of_view=((f_v))):
        flu_im.append(ref)

    image = flu_im[0]
    no_sets, peaks_detf = set_chan_num(image)
    print(no_sets)
    #if no_sets == 3:
    #    no_sets = no_sets[1,:]
    #    print(no_sets)

    if no_sets == 2:
        imy_crop, starty, endy = one_set_chan(peaks_detf, image)

        chan_startcoord, no_chan, avg_chanwid = chan_det(imy_crop)

        setchan = str(1 / 1)
        print('one')

    if no_sets == 4:
        imy_crop1, imy_crop2, starty1, endy1, starty2, endy2 = two_set_chan(peaks_detf, image)
        chan_startcoord1, no_chan1, avg_chanwid1 = chan_det(imy_crop1)
        chan_startcoord2, no_chan2, avg_chanwid2 = chan_det(imy_crop2)

        setchan1 = str('a')
        extraction(no_chan1, chan_startcoord1, avg_chanwid1, images, starty1, endy1, setchan1, f_v)

        setchan2 = str('b')
        extraction(no_chan2, chan_startcoord2, avg_chanwid2, images, starty2, endy2, setchan2, f_v)
        print('two')

    return ()


extract_no = 59 #int(input('Enter which of the views to extract.', ))
if extract_no > no_f_v:
    extract_no = no_f_v
print(extract_no)
extract_save(extract_no)


