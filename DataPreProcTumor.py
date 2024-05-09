from nilearn.image import resample_img
import nibabel as nib
from NiiLoadAndOrientationFun import *
from FixResolutionFun import *
import numpy as np
from NormalizeImage import *

def Sitk2Nii(sitk_image):
    image_array = sitk.GetArrayFromImage(sitk_image)
    image_array2 = np.transpose(image_array,[1,2,0])
    nifti_image = nib.Nifti1Image(image_array2, affine=np.eye(4)) 
    nifti_image.header["pixdim"][1:4] = sitk_image.GetSpacing()
    nifti_image.header["qoffset_x"] = sitk_image.GetOrigin()[0]
    nifti_image.header["qoffset_y"] = sitk_image.GetOrigin()[1]
    nifti_image.header["qoffset_z"] = sitk_image.GetOrigin()[2]
    del sitk_image
    return nifti_image


def Nii2Sitk(nifti_image):
    image_array = nifti_image.get_fdata()
    image_array2 = np.transpose(image_array,[2,0,1])
    sitk_image = sitk.GetImageFromArray(image_array2)
    sitk_image.SetSpacing((float(nifti_image.header["pixdim"][1]),float(nifti_image.header["pixdim"][2]),float(nifti_image.header["pixdim"][3])))
    sitk_image.SetOrigin((float(nifti_image.header["qoffset_x"]),float(nifti_image.header["qoffset_y"]),float(nifti_image.header["qoffset_z"])))
    del nifti_image
    return sitk_image

def DataPreprocTumor(tumorPath,nodesPath,ctReference):
    
    gtvTumor_nii_ori = NiiLoadAndOrientation(tumorPath)#orient to LAS
    gtvTumor_itk_norm = NormalizeImage(Nii2Sitk(gtvTumor_nii_ori),None,None,Nii2Sitk(ctReference).GetOrigin(),(1,1,1),None)
    gtvTumor_nii_norm = Sitk2Nii(gtvTumor_itk_norm)
    del gtvTumor_itk_norm
    del gtvTumor_nii_ori
    if False and not(np.all(gtvTumor_nii_norm.header['dim'] == ctReference.header['dim'])):
        madeupaffine = ctReference.affine
        madeupaffine[2][2] = madeupaffine[2][2]*((gtvTumor_nii_norm.header['dim'][3]/ctReference.header['dim'][3]))
        gtvTumor_nii_norm = resample_img(gtvTumor_nii_norm,  madeupaffine, ctReference.shape,interpolation='nearest')
        print("GTV Rescaled",gtvTumor_nii_norm.header['dim'],ctReference.header['dim'])
    gtvTumor_np = gtvTumor_nii_norm.get_fdata()
    del gtvTumor_nii_norm
    #gtv_np[gtv_np>1.5]=0
    #gtv_np[gtv_np>0]=1
    gtvTumor_np_trans = np.transpose(gtvTumor_np,[1,0,2])
    gtvTumor_np_rot = np.rot90(gtvTumor_np_trans,axes=(0,1),k=1)
    #gtvTumorResolution = FixResolution(gtvTumor_np_rot,gtvTumor_nii_norm)

    #Nodes Ground Truth
    gtvNodes_nii_ori = NiiLoadAndOrientation(nodesPath)#orient to LAS
    gtvNodes_itk_norm = NormalizeImage(Nii2Sitk(gtvNodes_nii_ori),None,None,Nii2Sitk(ctReference).GetOrigin(),(1,1,1),None)
    gtvNodes_nii_norm = Sitk2Nii(gtvNodes_itk_norm)
    del gtvNodes_itk_norm
    del gtvNodes_nii_ori
    if False and not(np.all(gtvNodes_nii_norm.header['dim'] == ctReference.header['dim'])):
        madeupaffine = ctReference.affine
        madeupaffine[2][2] = madeupaffine[2][2]*((gtvNodes_nii_norm.header['dim'][3]/ctReference.header['dim'][3]))
        gtvNodes_nii_norm = resample_img(gtvNodes_nii_norm,  madeupaffine, ctReference.shape,interpolation='nearest')
        print("GTV Rescaled",gtvNodes_nii_norm.header['dim'],ctReference.header['dim'])
    gtvNodes_np = gtvNodes_nii_norm.get_fdata()
    del gtvNodes_nii_norm
    #gtv_np[gtv_np>1.5]=0
    #gtv_np[gtv_np>0]=1
    gtvNodes_np_trans = np.transpose(gtvNodes_np,[1,0,2])
    gtvNodes_np_rot = np.rot90(gtvNodes_np_trans,axes=(0,1),k=1)
    #gtvNodesResolution = FixResolution(gtvNodes_np_rot,gtvNodes_nii_norm)

    #print(gtvTumor_itk_norm.GetSpacing(),gtvNodes_itk_norm.GetSpacing())
    #print(gtvTumor_nii_norm.header['dim'],gtvNodes_nii_norm.header['dim'])
    #print(Nii2Sitk(ctReference).GetOrigin(),gtvTumor_itk_norm.GetOrigin(),gtvNodes_itk_norm.GetOrigin())
    
    return gtvTumor_np_rot,gtvNodes_np_rot