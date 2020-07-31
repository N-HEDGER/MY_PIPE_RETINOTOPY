

import json
import os


def init(jpath):
    with open(jpath) as json_file:
        data = json.load(json_file)
    return data


def findtype(FOLDER, ext):

    # Function goal: return nifti files within a directory

    # Detail: could be used for a file with any extension...

    # Inputs

    # FOLDER (directory to search)
    # ext (the suffix (.gii or .gii.gz))

    def fprintf(stream, format_spec, *args):
        stream.write(format_spec % args)
    import os
    import sys
    giftilist = list()
    for file in os.listdir(FOLDER):
        if not file.startswith('.') and file.endswith(ext):
            giftilist.append(os.path.join(FOLDER, file))
    fprintf(sys.stdout, "Found %d gifti files \n", len(giftilist))
    return(sorted(giftilist))


def dill_save(obj, directory, fname):

    with open(os.path.join(directory, fname), 'wb') as output:
        dill.dump(obj, output)


def load(filename):
    input_file = open(filename, 'rb')
    obj = dill.load(input_file)
    return obj


def make_gifti_list(base_folder, sessionstring, space):

    def fprintf(stream, format_spec, *args):
        stream.write(format_spec % args)

    import os
    import sys
    sessionlist = list()
    for session in os.listdir(base_folder):
        if not session.startswith('.') and session.startswith(tuple(sessionstring)):
            sessionlist.append(os.path.join(base_folder, session))
    fprintf(sys.stdout, "Found %d sessions \n", len(sessionlist))

    gifts = []

    for sess in sorted(sessionlist):
        gifts.append(findtype(os.path.join(sess, 'func'), '.gii'))

    flatgifts = []

    for sublist in gifts:
        for item in sublist:
            flatgifts.append(item)

    leftgifts = [gift for gift in flatgifts if space + "_hemi-L" in(gift)]
    rightgifts = [gift for gift in flatgifts if space + "_hemi-R" in(gift)]

    return leftgifts, rightgifts, gifts, flatgifts




def make_tsv_list(base_folder, sessionstring, space):

    def fprintf(stream, format_spec, *args):
        stream.write(format_spec % args)

    import os
    import sys
    sessionlist = list()
    for session in os.listdir(base_folder):
        if not session.startswith('.') and session.startswith(tuple(sessionstring)):
            sessionlist.append(os.path.join(base_folder, session))
    fprintf(sys.stdout, "Found %d sessions \n", len(sessionlist))

    gifts = []

    for sess in sorted(sessionlist):
        gifts.append(findtype(os.path.join(sess, 'func'), '.tsv'))

    flatgifts = []

    for sublist in gifts:
        for item in sublist:
            flatgifts.append(item)


    return gifts, flatgifts


from nilearn import surface

from joblib import Parallel, delayed


def import_surf_astype(fn,fmt):
    impt=surface.load_surf_data(fn).astype(fmt)
    return impt



def import_gifts(flist, procs,fmt):
    gifts = Parallel(n_jobs=procs, verbose=9)(delayed(import_surf_astype)(fn,fmt) for fn in flist)
    return gifts





def make_webviewer_dict(sub,data,labels):


    mydict= {}

    for d in range(len(data)):
        data[d]=data[d].astype('float64')
        vdat = cortex.Vertex(data[d], subject=sub,vmin=np.nanmin(data[d]),vmax=np.nanmax(data[d]),cmap='plasma')
        mydict[labels[d]]=vdat

    return mydict








