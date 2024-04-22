from nilearn.image import resample_img
import nibabel as nib
from NiiLoadAndOrientationFun import *
from FixResolutionFun import *
import numpy as np

def DataPreprocTumor(tumorPath,nodesPath,ctReference):
    #Tumor Ground Truth
    gtvTumor_nii_ori = NiiLoadAndOrientation(tumorPath)#orient to LAS
    if not(np.all(gtvTumor_nii_ori.header['dim'] == ctReference.header['dim'])):
        madeupaffine = ctReference.affine
        madeupaffine[2][2] = madeupaffine[2][2]*((gtvTumor_nii_ori.header['dim'][3]/ctReference.header['dim'][3]))
        gtvTumor_nii_ori = resample_img(gtvTumor_nii_ori,  madeupaffine, ctReference.shape,interpolation='nearest')
        print("GTV Rescaled",gtvTumor_nii_ori.header['dim'],ctReference.header['dim'])
    gtvTumor_np = gtvTumor_nii_ori.get_fdata()
    #gtv_np[gtv_np>1.5]=0
    #gtv_np[gtv_np>0]=1
    gtvTumor_np_trans = np.transpose(gtvTumor_np,[1,0,2])
    gtvTumor_np_rot = np.rot90(gtvTumor_np_trans,axes=(0,1),k=1)
    gtvTumorResolution = FixResolution(gtvTumor_np_rot,ctReference)

    #Nodes Ground Truth
    gtvNodes_nii_ori = NiiLoadAndOrientation(nodesPath)#orient to LAS
    if not(np.all(gtvNodes_nii_ori.header['dim'] == ctReference.header['dim'])):
        madeupaffine = ctReference.affine
        madeupaffine[2][2] = madeupaffine[2][2]*((gtvNodes_nii_ori.header['dim'][3]/ctReference.header['dim'][3]))
        gtvNodes_nii_ori = resample_img(gtvNodes_nii_ori,  madeupaffine, ctReference.shape,interpolation='nearest')
        print("GTV Rescaled",gtvNodes_nii_ori.header['dim'],ctReference.header['dim'])
    gtvNodes_np = gtvNodes_nii_ori.get_fdata()
    #gtv_np[gtv_np>1.5]=0
    #gtv_np[gtv_np>0]=1
    gtvNodes_np_trans = np.transpose(gtvNodes_np,[1,0,2])
    gtvNodes_np_rot = np.rot90(gtvNodes_np_trans,axes=(0,1),k=1)
    gtvNodesResolution = FixResolution(gtvNodes_np_rot,ctReference)
    
    return gtvTumorResolution,gtvNodesResolution