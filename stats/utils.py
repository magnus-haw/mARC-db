import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize, ndimage

def recursive_fit_piecewise(x,y, err_thresh, level=0):
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
    print(p[0], left_rms, right_rms)
    lpoints, rpoints = [], []
    if left_rms > err_thresh:        
        lx, ly = x[x<=p[0]], y[x<=p[0]]
        # print("left", lx[0], lx[-1])
        lpoints = recursive_fit_piecewise(lx,ly, err_thresh, level=level+1)
    if right_rms > err_thresh:
        rx, ry = x[x>=p[0]], y[x>=p[0]]
        # print("right", rx[0], rx[-1])
        rpoints = recursive_fit_piecewise(rx,ry, err_thresh, level=level+1)
    
    if level ==0:
        lpoints = [(x[0],y[0])]+lpoints
        rpoints = rpoints + [(x[-1],y[-1])]
    if left_rms < err_thresh or right_rms < err_thresh:
        return lpoints + [(p[0],p[1])] + rpoints
    else:
        return lpoints + rpoints

def piecewise_linear(x, x0, y0, k1, k2):
    x = np.array(x, dtype=np.float)
    return np.piecewise(x, [x <= x0, x>x0], 
                        [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])

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
    p, cov = optimize.curve_fit(piecewise_linear, x, y, p0=(np.mean(x),np.mean(y),0.,0.), 
                                bounds=([x.min(),y.min(),-np.inf, -np.inf],
                                        [x.max(),y.max(), np.inf, np.inf]))
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

    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    ret = y[int(window_len/2)-1:-int(window_len/2)-1] 

    assert len(ret) == len(x)
    return ret

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

if __name__ == "__main__":
    x = np.arange(0,51.)
    y = np.arange(0,51.)

    y[x>10] *= .1
    y[x>10] -= y[11]-y[10]

    y[x>35] /= .1
    y[x>35] -= y[36]-y[35]
    y_noise = 1 * np.random.normal(size=y.size)
    y += y_noise
    #y = smooth(y)
    y[25] +=7
    y[26] +=7
    y[40] +=4
    mask = getOutlierMask(y)
    y = y[mask==0]
    x = x[mask==0]
    # y = np.cumsum(y)

    points = recursive_fit_piecewise(x,y,1.5)
    pts = np.array(points)
    # p, cov, Lrms, Rrms = fit_piecewise(x,y)
    # print(p, cov)
    # print(Lrms, Rrms)

    plt.plot(x,y, 'ro')
    plt.plot(pts[:,0], pts[:,1])
    # plt.plot(x,piecewise_linear(x,*p),'bo')
    plt.show()