import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize, integrate
from numpy import gradient as grad, diff

def recursive_fit_piecewise(x,y, err_thresh, level=0, slope=10.):
    """ Recursive top-down algorithm for piece-wise linear 
        fitting. Consecutive splits of domain based on error
        threshold.

    Args:
        x (1D array): independent variable (float)
        y (1D array): dependent variable (float)
        err_thresh (float): rms err threshold for curve segment

    Returns:
        elbow points: list of (x,y) points
    """
    p, cov, left_rms, right_rms = fit_piecewise(x,y)
    #print(p[0], left_rms, right_rms)
    lpoints, rpoints = [], []
    if left_rms > err_thresh:        
        lx, ly = x[x<=p[0]], y[x<=p[0]]
        if len(lx) > 10:
            lpoints = recursive_fit_piecewise(lx,ly, err_thresh, level=level+1)
    if right_rms > err_thresh:
        rx, ry = x[x>=p[0]], y[x>=p[0]]
        if len(rx) > 10:
            rpoints = recursive_fit_piecewise(rx,ry, err_thresh, level=level+1)
    
    if level ==0:
        lpoints = [(x[0],y[0])]+lpoints
        rpoints = rpoints + [(x[-1],y[-1])]
        #print(left_rms,right_rms,p)
    if left_rms < err_thresh or right_rms < err_thresh:
        ret = lpoints + [(p[0],p[1])] + rpoints
    else:
        ret = lpoints + rpoints

    if level == 0:
        ret = check_segments(x,y,ret,thresh=err_thresh)
        ret = merge_similar_segments(ret, slope=slope)
        ret = np.array(ret)
    
    return ret

def check_segments(x,y,pts,thresh=7.5):
    new_pts =[pts[0]]
    for i in range(1,len(pts)):
        x0,y0 = pts[i-1]
        x1,y1 = pts[i]
        
        inds = (x>=x0)*(x<=x1)
        xp,yp = x[inds],y[inds]

        yi = (y1-y0)*(xp-x0) + y0
        rms = np.sqrt(np.mean((yi-yp)**2))
        if rms > thresh:
            p, cov, left_rms, right_rms = fit_piecewise(xp,yp)
            new_pts.append((p[0],p[1]))
        new_pts.append(pts[i])
    return new_pts

def piecewise_linear(x, x0, y0, k1, k2):
    x = np.array(x, dtype=np.float)
    return np.piecewise(x, [x <= x0, x>x0], 
                        [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])

def linear(x, x0, y0, k1):
    return lambda x:k1*x + y0-k1*x0

def fit_linear(x,y):
    ymax= max(y.min()+1,y.max())
    p, cov = optimize.curve_fit(linear, x, y, p0=(np.mean(x),np.mean(y),0.), 
                                bounds=([x.min(),y.min(),-np.inf],
                                        [x.max(),ymax, np.inf]))
    rms = np.sqrt( np.mean((linear(x,*p) - y)**2) )
    return p, cov, rms

def fit_piecewise(x,y):
    """Fits 2-piece linear function to data

    Args:
        x (1D array): independent variable (float)
        y (1D array): dependent variable (float)

    Returns:
        p: parameter tuple (x0,y0,k1,k2)
        cov: covariance matrix
        left_rms: left curve rms
        right_rms: right curve rms
    """
    ymax= max(y.min()+1,y.max())
    p, cov = optimize.curve_fit(piecewise_linear, x, y, p0=(np.mean(x),np.mean(y),0.,0.), 
                                bounds=([x.min(),y.min(),-np.inf, -np.inf],
                                        [x.max(),ymax, np.inf, np.inf]))
    left_rms = np.sqrt( np.mean((piecewise_linear(x[x<=p[0]],*p) - y[x<=p[0]])**2) )
    right_rms = np.sqrt( np.mean((piecewise_linear(x[x>p[0]],*p) - y[x>p[0]])**2) )
    return p, cov, left_rms, right_rms

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
    
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also: 

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    x = np.array(x)
    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len<3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    #s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    N = window_len
    spad = np.pad(x, (N//2, N-1-N//2), mode='edge')
    ret = np.convolve(w/w.sum(),spad,mode='valid')
    #ret = y[int(window_len/2)-1:-int(window_len/2)-1] 

    assert len(ret) == len(x)
    return ret

def merge_similar_segments(pts, slope=10.):
    ### Merge adjacent segements with similar slopes
    clean_pts = [pts[0]]
    for i in range(1,len(pts)-1):
        dx1,dx2 = pts[i][0] - pts[i-1][0], pts[i+1][0] - pts[i][0]
        dy1,dy2 = pts[i][1] - pts[i-1][1], pts[i+1][1] - pts[i][1]
        
        m1, m2 = dy1/dx1, dy2/dx2
        
        if abs(m1-m2)>slope:
            clean_pts.append(pts[i])
    clean_pts.append(pts[-1])
    return clean_pts

def remove_small_segments(clean_pts):
    ### Eliminate small segments between larger segments
    if len(clean_pts) >= 5:
        extra_clean = [clean_pts[0]]
        pts = np.array(clean_pts)
        dp = np.diff(pts,axis=0)
        xnorm = pts[:,0].max() - pts[:,0].min()
        ynorm = pts[:,1].max() - pts[:,1].min()
        dp[:,0] /= xnorm
        dp[:,1] /= ynorm
        
        i=1
        while i < len(clean_pts)-2:
            dl1 = np.linalg.norm(dp[i-1])
            dl2 = np.linalg.norm(dp[i])
            dl3 = np.linalg.norm(dp[i+1])

            if dl1/dl2 > 5 and dl3/dl2 > 5:
                extra_clean.append(clean_pts[i+1])
                i += 2
            else:
                extra_clean.append(clean_pts[i])
                i += 1
        extra_clean.append(clean_pts[-2])
        extra_clean.append(clean_pts[-1])
        return np.array(extra_clean)
    else:
        return np.array(clean_pts)
    
def getOutlierMask(metric,threshold=2,method="stdev"):
    """Returns mask for outliers in time series

    Args:
        metric (array): 1D numpy array, presumably time series
        threshold (int, optional): Threshold value. Default is 2 for stdev.
        method (str, optional): "stdev" or "percent". Defaults to "stdev".

    Returns:
        mask: numpy masked array
    """
    mask = np.zeros_like(metric)
    if len(metric) > 25:
        smetric = smooth(metric)
        diff = abs(smetric - metric)

        if method=="percent":
            rdiff = abs(diff/(metric + 1e-3))
            mask += rdiff > threshold

        if method=="stdev":
            dmean = np.mean(diff)
            dstd = np.std(diff)
            mask += diff > dmean + threshold*dstd
    else:
        print("Input array len must be > 25")
    return mask

def clean_series(x,y):
    inds = ~np.isnan(y)
    xn = x[inds]
    yn = y[inds]
    mask = getOutlierMask(yn)
    ynn = yn[mask==0]
    xnn = xn[mask==0]
    return xnn.copy(),ynn.copy()
    
def integral_estimator(xi,yi, thresh=40., slope=10.):
    x,y = clean_series(xi,yi)
    y_int = integrate.cumtrapz(y, x, initial=0)
    pts = recursive_fit_piecewise(x,y_int,thresh,slope=slope)
    pts = remove_small_segments(pts)
    return np.array(pts)

def infer_stable_portions(t,yi, fraction_thresh=0.1, buffer_dt=[10,2]):
    wd = min(len(t)//20, 75)
    #extract each condition segment
    y = smooth(yi,window_len=wd)
    # pick out value at halfway mark
    n = len(t)//2
    constval = np.nanmean(yi[n:n+20])
    # find first point where value stabilizes within threshold (e.g. 10%)
    dy,dymax = abs(y - constval), constval*fraction_thresh
    ts = t[0:n]
    unstable = ts[dy[0:n] > dymax]
    try:
        stable_start = unstable[-1] + buffer_dt[0]
    except:
        stable_start = ts[0] + buffer_dt[0]
    # find last point where value stabilizes within threshold (e.g. 10%)
    stable = t[dy < dymax]
    try:
        stable_end = stable[-1] - buffer_dt[1]
    except:
        stable_end = t[-1] - buffer_dt[1]

    # plt.plot(t,dy)
    # print(constval)
    # plt.show()
    return stable_start, stable_end, constval

def infer_conditions(t,yi, thresh=40., minval=10.):
    pts = integral_estimator(t,yi, thresh=thresh, slope=minval)
    dt = diff(pts[:,0])
    dI = diff(pts[:,1])
    conditions = []
    for i in range(0,len(dt)):
        if dt[i] >5 and dI[i]/dt[i] > minval:
            inds = (t>pts[i,0])*(t<pts[i+1,0])
            if len(conditions) == 0:
                buffer_dt = [10,3]
            else:
                buffer_dt = [2,3]
            stable_start, stable_end, avg = infer_stable_portions(t[inds],yi[inds],buffer_dt=buffer_dt)
            conditions.append({'value':avg, 'start':pts[i,0], 'end':pts[i+1,0], 
                               'stable_start':stable_start, 'stable_end':stable_end})
    return conditions

def get_intersection(a0,a1,b0,b1):
    t0,t1 = max(a0,b0),min(a1,b1)
    if t0 > t1:
        return None, None
    else:
        return t0,t1

def collate_conditions(condsI,condsF):
    allconds = []
    for icond in condsI:
        for fcond in condsF:
            t0,t1 = get_intersection(icond['start'],icond['end'],fcond['start'],fcond['end'])
            ts0,ts1 = get_intersection(icond['stable_start'],icond['stable_end'],fcond['stable_start'],fcond['stable_end'])
            ival,fval = icond['value'],fcond['value']
            if t0 is not None:
                allconds.append({'I_val':ival,'F_val':fval, 'start':t0, 'end':t1,
                                 'stable_start':ts0, 'stable_end':ts1})
    return allconds

def get_ConditionInstance(cond_dict, ListInsts, thresh=.15):
    score = np.zeros(len(ListInsts))
    for i in range(0,len(ListInsts)):
        cinst = ListInsts[i]
        I = cinst.condition.current
        F = cinst.condition.plasma_gas_flow
        ierr = abs(cond_dict['I_val'] - I)/cond_dict['I_val']
        ferr = abs(cond_dict['F_val']-F)/cond_dict['F_val']
        score[i] = np.sqrt(ierr**2 + ferr**2)
    if score.min() < thresh:
        return ListInsts[int(np.argmin(score))]
    else:
        return None

def get_condition_match(cond_dict, cinst, thresh=.15):
    I = cinst.condition.current
    F = cinst.condition.plasma_gas_flow
    ierr = abs(cond_dict['I_val'] - I)/cond_dict['I_val']
    ferr = abs(cond_dict['F_val']-F)/cond_dict['F_val']
    score = np.sqrt(ierr**2 + ferr**2)
    if score < thresh:
        return True
    else:
        return False


if __name__ == "__main__":
    import os
    import sys
    import django

    proj_path = "/Users/mhaw/Desktop/mARC-db"
    proj_path = "/Volumes/TSF Databases/mARC II documents/mARC-db"
    sys.path.append(proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mARC.settings")
    django.setup()

    from system.models import Condition, ConditionInstance
    from stats.models import ConditionInstanceFit, SeriesStableStats, SeriesStartupStats
    from data.models import Run, Apparatus
    from stats.views import updateConditionAvgs, updateSeriesStats, updateConditionInstanceFits

    app = Apparatus.objects.filter(name = "mini-ARC v2.0").first()

    # conditionInstances = ConditionInstance.objects.exclude(valid=False)
    # updateConditionInstanceFits(conditionInstances)

    conditionInstanceFits = ConditionInstanceFit.objects.all()[29:]
    updateSeriesStats(conditionInstanceFits)

    # conditions = Condition.objects.all()
    # updateConditionAvgs(app,conditions)
    
    # for run in runs[0:]:
    #     series = run.diagnosticseries_set.all()
    #     currentlist = series.filter(name__contains="Arc Current [A]")
    #     flowlist = series.filter(name__contains="Plasma gas [g/s]")

    #     conditionInstances = run.conditioninstance_set.all()
    #     #print(conditionInstances)
    #     if len(conditionInstances)>=1 and len(currentlist)==1 and len(flowlist)==1:
    #         current = currentlist[0]
    #         flow = flowlist[0]
    #         ti,I = current.time.time, current.values
    #         tf,F = flow.time.time, flow.values
    #         condsI = infer_conditions(ti,I)
    #         condsF = infer_conditions(tf,F, minval=0.1, thresh=.05)
    #         # tff = tf[(tf>condsF[0]['start'])*(tf<condsF[0]['end'])]
    #         # FF = F[(tf>condsF[0]['start'])*(tf<condsF[0]['end'])] - condsF[0]['value']

    #         # fig0 = plt.figure(0)
    #         # plt.plot(tff,smooth(FF,window_len=50))
    #         # plt.plot(tf,F)
    #         # plt.plot([condsF[0]['stable_start'],condsF[0]['stable_start']], [0,.8], 'k-')
    #         # plt.plot([condsF[0]['stable_end'],condsF[0]['stable_end']], [0,.8], 'k-')

    #         # fig1 = plt.figure(1)
    #         # tii = ti[(ti>condsI[0]['start'])*(ti<condsI[0]['end'])]
    #         # II = I[(ti>condsI[0]['start'])*(ti<condsI[0]['end'])] - condsI[0]['value']
    #         # plt.plot(tii,smooth(II,window_len=50))
    #         # plt.plot(ti,I)
    #         # for cond in condsI:
    #         #     plt.plot([cond['stable_start'],cond['stable_start']], [0,200], 'k-')
    #         #     plt.plot([cond['stable_end'],cond['stable_end']], [0,200], 'k-')

    #         condsall = collate_conditions(condsI,condsF)
    #         ListInsts = ConditionInstance.objects.filter(run = run)
            
    #         print(run.name)
    #         #print(condsall)
    #         for cond in condsall:
    #             ci = get_ConditionInstance(cond, ListInsts, thresh=.15)
    #             if hasattr(ci, 'conditioninstancefit'):
    #                 cif = ci.conditioninstancefit
    #             else:
    #                 cif = ConditionInstanceFit(instance= ci, start= cond['start'], end= cond['end'],
    #                                     stable_start=cond['stable_start'],stable_end=cond['stable_end'])
    #                 cif.save()
    #             print(cif)
    #             dg_series = run.diagnosticseries_set.all()
    #             for dgs in dg_series:
    #                 ts = dgs.time.time 
    #                 vals = dgs.values

    #                 # stable segment stats
    #                 t0,t1 = cif.stable_start, cif.stable_end
    #                 inds = (ts>t0)*(ts<t1)
    #                 t,v = ts[inds],vals[inds]
    #                 # plt.plot(t,v)
    #                 # plt.title(dgs.diagnostic.name)
    #                 # plt.show()
    #                 avg = np.nanmean(v)
    #                 stdev = np.nanstd(v)
    #                 vmin,vmax = np.nanmin(v),np.nanmax(v)
                    
    #                 existing = SeriesStableStats.objects.filter(condition=cif, series=dgs)
    #                 if len(existing) == 0:
    #                     sss = SeriesStableStats(series=dgs, condition=cif,avg=avg,stdev=stdev,min=vmin,max=vmax)
    #                     print(sss.avg,sss.stdev,sss.min,sss.max)
    #                     sss.save()

    #                 # startup stats
    #                 t0,t1 = cif.start, cif.stable_start
    #                 inds = (ts>t0)*(ts<t1)
    #                 t,v = ts[inds],vals[inds]
    #                 stdev = np.nanstd(v)
    #                 vmin,vmax = np.nanmin(v),np.nanmax(v)
    #                 existing = SeriesStartupStats.objects.filter(condition=cif, series=dgs)
    #                 if len(existing) == 0:
    #                     sss = SeriesStartupStats(series=dgs, condition=cif,dt=t1-t0,stdev=stdev,
    #                                                                 min=vmin,max=vmax)
    #                     sss.save()
    #         # plt.show()
