import skimage.transform as skTrans
from skimage import morphology
import numpy as np
import nibabel as nib

def FixHoles(struct_np):
    struct_np[struct_np>0] = 1
    struct_bool = morphology.binary_closing(struct_np.astype(bool))
    struct_filled = struct_bool.astype(np.uint8)
    return struct_filled


def FixResolution(np2Resize,nii_wInfo):
    
    current_pixdims = nii_wInfo.header.get_zooms()
    desired_pixdims = (1.0,1.0,1.0)
    scaling_factors = [current / desired for desired, current in zip(desired_pixdims, current_pixdims)]
    
    newshape=np2Resize.shape[0]*scaling_factors[0],np2Resize.shape[1]*scaling_factors[1],np2Resize.shape[2]*scaling_factors[2]
    
    resized_nii_data = skTrans.resize(np2Resize, newshape, order=1, preserve_range=True)

    #print("ScalingFactors",scaling_factors)
    #print("Old shape",np2Resize.shape)
    #print("New shape",resized_nii_data.shape)
    return resized_nii_data