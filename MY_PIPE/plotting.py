




import cortex




def make_figspace(height,x,y):

	flatmap_height = height
	full_figsize = (x,y)

	full_fig = plt.figure(constrained_layout=True, figsize=full_figsize)
	return full_fig



def minimal_plot(sub,dat,zeronan,fig,savefig,fname):


    if zeronan==True:
        dat[dat==0]=np.nan

    light=cortex.Vertex(dat,subject=sub, vmin=np.nanmin(dat), vmax=np.nanmax(dat),cmap='plasma')
    mfig=cortex.quickshow(light,with_curvature=True,fig=fig,with_colorbar=True,with_rois=False)

    if savefig==True:
        mfig.savefig(fname, dpi=300, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format='png',transparent=False)


def alphaplot(sub,dat,R2,thresh,fig,save,fname):
    light=cortex.Vertex2D(dat,R2,subject=sub, vmin=np.nanmin(dat), vmax=np.nanmax(dat),vmin2=thresh,vmax2=1,cmap='plasma_alpha')
    mfig=cortex.quickshow(light,with_curvature=True,fig=fig)
    sp.savefig(fname, dpi=300, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format='png',transparent=False, bbox_inches=None, pad_inches=0.1,
    frameon=None)