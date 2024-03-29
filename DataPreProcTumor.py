from nilearn.image import resample_img
import nibabel as nib
from NiiLoadAndOrientationFun import *
from FixResolutionFun import *
import numpy as np

def DataPreprocTumor(tumorPath,ctReference):
    #Tumor Ground Truth ITV and GTV
    gtv_nii_ori = NiiLoadAndOrientation(tumorPath)#orient to LAS
    if not(np.all(gtv_nii_ori.header['dim'] == ctReference.header['dim'])):
        madeupaffine = ctReference.affine
        madeupaffine[2][2] = 5
        gtv_nii_ori = resample_img(gtv_nii_ori,  madeupaffine, ctReference.shape,interpolation='nearest')
        #print("GTV Rescaled",gtv_nii_ori.header['dim'],ctReference.header['dim'])
    gtv_np = gtv_nii_ori.get_fdata()
    gtv_np[gtv_np>1.5]=0
    gtv_np[gtv_np>0]=1
    gtv_np_trans = np.transpose(gtv_np,[1,0,2])
    gtv_np_rot = np.rot90(gtv_np_trans,axes=(0,1),k=1)
    gtvResolution = FixResolution(gtv_np_rot,ctReference)
    
    return gtvResolution