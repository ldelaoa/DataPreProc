import skimage.metrics as metrics
import numpy as np
from scipy.signal import correlate2d

def similarMetrics_axial(img1,img2,itv):
    count,cross_corr,ssim,mutual_info =(0,0,0,0)
    for i in range(img1.shape[-1]):
        if np.sum(itv[:,:,i])>0:
            ssim = ssim+ metrics.structural_similarity(img1[:,:,i], img2[:,:,i],data_range=img2[:,:,i].max() - img2[:,:,i].min())
            mutual_info =mutual_info+ metrics.normalized_mutual_information(img1[:,:,i], img2[:,:,i],bins=100)
            cross_corr =cross_corr+ np.max(correlate2d(img1[:,:,i], img2[:,:,i], mode='same'))
            count += 1
    mutual_avg = mutual_info/count
    ssim_avg = ssim/count
    cross_avg = cross_corr/count
    return mutual_avg,ssim_avg,cross_avg

def similarMetrics_coronal(img1,img2,itv):
    count,cross_corr,ssim,mutual_info =(0,0,0,0)
    for i in range(img1.shape[-2]):
        if np.sum(itv[:,i,:])>0:
            ssim = ssim+ metrics.structural_similarity(img1[:,i,:], img2[:,i,:],data_range=img2[:,i,:].max() - img2[:,i,:].min())
            mutual_info =mutual_info+ metrics.normalized_mutual_information(img1[:,i,:], img2[:,i,:],bins=100)
            cross_corr =cross_corr+ np.max(correlate2d(img1[:,i,:], img2[:,i,:], mode='same'))
            count += 1
    mutual_avg = mutual_info/count
    ssim_avg = ssim/count
    cross_avg = cross_corr/count
    return mutual_avg,ssim_avg,cross_avg

def similarMetrics_sagital(img1,img2,itv):
    count,cross_corr,ssim,mutual_info =(0,0,0,0)
    for i in range(img1.shape[-3]):
        if np.sum(itv[i,:,:])>0:
            ssim = ssim+ metrics.structural_similarity(img1[i,:,:], img2[i,:,:],data_range=img2[i,:,:].max() - img2[i,:,:].min())
            mutual_info = mutual_info+ metrics.normalized_mutual_information(img1[i,:,:], img2[i,:,:],bins=100)
            cross_corr =cross_corr+ np.max(correlate2d(img1[i,:,:], img2[i,:,:], mode='same'))
            count += 1
    mutual_avg = mutual_info/count
    ssim_avg = ssim/count
    cross_avg = cross_corr/count
    return mutual_avg,ssim_avg,cross_avg