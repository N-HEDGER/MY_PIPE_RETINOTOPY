

import json


def init(jpath):
    with open(jpath) as json_file:
        data = json.load(json_file)
    return data


def findgiftis(FOLDER, ext):

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
    	gifts.append(findgiftis(os.path.join(sess, 'func'), '.gii'))

	flatgifts = []
	for sublist in gifts:
		for item in sublist:
                flatgifts.append(item)

	leftgifts = [gift for gift in flatgifts if space + "_hemi-L" in(gift)]
	rightgifts = [gift for gift in flatgifts if space + "_hemi-R" in(gift)]

	return leftgifts, rightgifts, gifts, flatgifts
