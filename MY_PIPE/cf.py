

# Courtesy of pycortex team.
def zoom_to_roi(subject, roi, hem, margin=5.0):
    roi_verts = cortex.get_roi_verts(subject, roi)[roi]
    roi_map = cortex.Vertex.empty(subject)
    roi_map.data[roi_verts] = 1

    (lflatpts, lpolys), (rflatpts, rpolys) = cortex.db.get_surf(subject, "flat",
                                                                nudge=True)
    sel_pts = dict(left=lflatpts, right=rflatpts)[hem]
    roi_pts = sel_pts[np.nonzero(getattr(roi_map, hem))[0], :2]

    xmin, ymin = roi_pts.min(0) - margin
    xmax, ymax = roi_pts.max(0) + margin
    plt.axis([xmin, xmax, ymin, ymax])


def get_candidate_mask(ROIvec, ROIval, R2vec, R2thresh, eccvec, eccthresh, idxvec):

    m1 = ROIvec == ROIval
    m2 = R2vec > R2thresh
    m3 = eccvec < eccthresh

    mymask = np.logical_and(m1 == True, m2 == True)

    mymask2 = np.logical_and(m3 == True, mymask == True)

    filtmask = np.array(idxvec[mymask2]).astype(int)

    pmask = np.array(mymask2.astype(float))
    pmask[pmask == 0] = np.nan

    return filtmask, pmask



# Courtesy of Tomas Knapen
def gauss1D_cart(x, mu=0.0, sigma=1.0):

    """gauss1D_cart
    gauss1D_cart takes a 1D array x, a mean and standard deviation,
    and produces a gaussian with given parameters, with a peak of height 1.
    Parameters
    ----------
    x : numpy.ndarray (1D)
        space on which to calculate the gauss
    mu : float, optional
        mean/mode of gaussian (the default is 0.0)
    sigma : float, optional
        standard deviation of gaussian (the default is 1.0)
    Returns
    -------
    numpy.ndarray
        gaussian values at x
    """
    gau=np.exp(-((x-mu)**2)/(2*sigma**2)).astype('float32')

    return 




def plot_V1_mask(sub,maskdat,hem,fig):
    heavy=cortex.Vertex(maskdat,subject=sub, vmin=0, vmax=1,cmap='plasma')
    mfig=cortex.quickshow(heavy,with_curvature=True,fig=fig,with_colorbar=False)
    zoom_to_roi(sub,'V1',hem)




def get_subject_surfaces(sub,surf):
    surfs = [cortex.polyutils.Surface(*d)
    for d in cortex.db.get_surf(sub, surf)]
    return surfs



# Cannot be run in paralell due to awkward interaction with the geodesic distances function.
def get_geodesic_distance_array(surf,verts):
    dists=list()
    for vert in verts:
        dists.append(surf.geodesic_distance(vert))
    distarr=np.array(dists)
    return distarr


def lightplot(sub,dat,fig):
    light=cortex.Vertex(dat,subject=sub, vmin=np.nanmin(dat), vmax=np.nanmax(dat),cmap='plasma')
    mfig=cortex.quickshow(light,with_curvature=True,fig=fig,with_colorbar=False,with_rois=False)



def make_gaussian_patches(sizes,distarray,invmask):
    glist=list()
    for s in sizes:
        print(s)
        garray=gauss1D_cart(distarray,0,s)
        garray[:,[invmask]]=0
        glist.append(garray)
    garray=np.array(glist)
    return garray



def alphaplot(sub,dat,R2,thresh,fig):
    light=cortex.Vertex2D(dat,R2,subject=sub, vmin=np.nanmin(dat), vmax=np.nanmax(dat),vmin2=thresh,vmax2=1,cmap='plasma_alpha')
    mfig=cortex.quickshow(light,with_curvature=True,fig=fig)




