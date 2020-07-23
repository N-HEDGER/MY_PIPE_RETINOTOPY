import json


conf= {}
conf['paths']=[]


conf['paths'].append({'fmrirep_path':'/Volumes/BAHAMUT/PRF_DATA/ds002574-download/derivatives/fmriprep',
	'freesurfer_path': '/Volumes/BAHAMUT/PRF_DATA/ds002574-download/derivatives/freesurfer',
	'output_path':'/Volumes/BAHAMUT/MY_OUT'})




conf['savgol'].append({'polys':3,
	'deriv': 0,
	'wl': 120
	'tr': 1.5})


conf['noise'].append({'ncomps':5,
	'varr': ['std_dvars','dvars','framewise_displacement','a_comp_cor_00','a_comp_cor_01','a_comp_cor_02',
    'a_comp_cor_03',
    'a_comp_cor_04',
    'a_comp_cor_05',
    'trans_x',
    'trans_y',
    'trans_z',
    'rot_x',
    'rot_y',
    'rot_z',
    'cosine00']}





