def savgol_filter(data, polyorder, deriv, window_length,tr,fmt):
    """ Applies a savitsky-golay filter to a nifti-file.

    Fits a savitsky-golay filter to a 4D fMRI nifti-file and subtracts the
    fitted data from the original data to effectively remove low-frequency
    signals.

    Parameters
    ----------
    in_file : str
        Absolute path to nifti-file.
    polyorder : int (default: 3)
        Order of polynomials to use in filter.
    deriv : int (default: 0)
        Number of derivatives to use in filter.
    window_length : int (default: 120)
        Window length in seconds.

    Returns
    -------
    out_file : str
        Absolute path to filtered nifti-file.


    Courtesy of knapenlab.
    """

    import nibabel as nib
    from scipy.signal import savgol_filter
    import numpy as np
    import os

    dims = data.shape
    

    # TR must be in seconds
    if tr < 0.01:
        tr = np.round(tr * 1000, decimals=3)
    if tr > 20:
        tr = tr / 1000.0

    window = np.int(window_length / tr)
    
    # Window must be odd
    if window % 2 == 0:
        window += 1

    data = data.reshape((np.prod(data.shape[:-1]), data.shape[-1]))
    data_filt = savgol_filter(data, window_length=window, polyorder=polyorder,
                              deriv=deriv, axis=1, mode='nearest')

    data_filt = data - data_filt + data_filt.mean(axis=-1)[:, np.newaxis]
    data_filt = data_filt.reshape(dims)
    data_filt=data_filt.astype(fmt)

    return data_filt










def perform_savgol (dlist, polyorder, deriv, window_length,tr,procs,fmt):
    filt_dat=Parallel(n_jobs=procs,verbose=9)(delayed(savgol_filter)(data,polyorder, deriv, window_length,tr,fmt)  for data in dlist)
    return filt_dat




def savgol_filter_1D(data, polyorder, deriv, window_length,TR):


    from scipy.signal import savgol_filter

    window = np.int(window_length / TR)

    # Window must be odd
    if window % 2 == 0:
        window += 1

    data_filt = savgol_filter(data, window_length=window, polyorder=polyorder,
                              deriv=deriv, mode='nearest')

    data_filtered = data - data_filt + data_filt.mean()

    return data_filtered



def denoise(data,nuissance,varr,n_components, polyorder, deriv, window_length,TR,fmt):
    df = pd.read_csv(nuissance, sep='\t', header=0,index_col=None)
    # get the wanted variables and do stuff with it
    nuissances = []
    for var in varr:
        # get wanted nuissance variables
        ndat = np.array(df[var])
        # fill in nans
        ndat[ndat=='n/a'] = np.nan
        # cast to float
        ndat = ndat.astype(fmt)
            # median fill nan values (i.e. first value )
        ndat[np.isnan(ndat)] = np.nanmedian(ndat)
            # temporally filter 
        filtered_data = savgol_filter_1D(ndat, polyorder, deriv, window_length,TR)
            # z-score (so that explained variance ratios is interpretable)
        filtered_data_z = (filtered_data - np.mean(filtered_data)) / np.std(filtered_data)
            # and append
        nuissances.append(filtered_data_z)

    nuissances = np.array(nuissances)    

        # now do pca and grab first 5:
    pca = PCA(n_components=n_components)  
    pcas = pca.fit_transform(nuissances.T)

    datashape = data.shape

        # do nuissance regression
    dm = np.hstack([np.ones((pcas.shape[0],1)),pcas]) # add intercept
    model = OLSModel(dm)
    fit = model.fit(data.reshape(-1,datashape[-1]).T)
    resid = fit.resid.T.reshape(datashape)
    resid += np.mean(data,axis=-1)[:,np.newaxis] # re-add the signal offset which was regressed out by the intercept
    return resid, fit.theta,fit.r_square


def perform_denoising (dlist,nlist,varr,n_components, polyorder, deriv, window_length,TR,procs,fmt):

    if len(nlist) != len(dlist):

        raise Exception("The number of datafiles and nuissance files do not match")

    denoised_dat=Parallel(n_jobs=procs,verbose=9)(delayed(denoise)(dlist[i],nlist[i],varr,n_components, polyorder, deriv, window_length,TR,fmt)  for i in range(len(dlist)))
    return denoised_dat

import nibabel
import os



def export_noisefit(denoised_dat,export,sub,path,hem):
    R2s=[]
    for dn in denoised_dat:
        R2s.append(np.nan_to_num(dn[2],0))
        bs.append(np.nan_to_num(dn[1],0))  




    bs=np.mean(bs,axis=0)    
    R2s=np.squeeze(np.mean(R2s,axis=0))

    if export:
        nibabel.freesurfer.io.write_morph_data(os.path.join(path,sub+'_'+hem+'_'+'noise_R2_curv'),R2s)
        minimal_plot(sub,R2s,True,full_fig,True,os.path.join(path,sub+'_'+hem+'_'+'noise_R2.png'))

    for i in range(t.shape[0]):

        nibabel.freesurfer.io.write_morph_data(os.path.join(path,sub+'_'+hem+'_'+'pc'+str(i)+'noise_beta_curv'),s[i,:])
        minimal_plot(sub,bs[i,:],True,full_fig,True,os.path.join(path,sub+'_'+hem+'_'+'pc'+str(i)+'noise_beta.png'))



    return R2s, bs



def compute_tsnr(data,fmt):
    tsnr = np.mean(data,axis=-1)/np.std(data,axis=-1)
    tsnr[np.isnan(tsnr)] = 0
    tsnr[np.isinf(tsnr)] = 0
    tsnr += np.abs(np.min(tsnr))+0.01
    tsnr=np.squeeze(tsnr)
    return tsnr.astype(fmt)


def perform_tsnring(dlist,procs,fmt):
    tsnr_dat=Parallel(n_jobs=procs,verbose=9)(delayed(compute_tsnr)(data,fmt)  for data in dlist)
    return tsnr_dat



def export_tsnr(tsnr_dat,export,sub,path,hem):
    tsnr=[]
    for ts in tsnr_dat:
        tsnr.append(ts)


    tsnr=np.mean(tsnr,axis=0)    

    if export:
        nibabel.freesurfer.io.write_morph_data(os.path.join(path,sub+'_'+hem+'_'+'tsnr_curv'),tsnr)
        minimal_plot(sub,R2s,True,full_fig,True,os.path.join(path,sub+'_'+hem+'_'+'tsnr.png'))


    return tsnr



