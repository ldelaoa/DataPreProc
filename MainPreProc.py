import SimpleITK as sitk
import numpy as np
import nibabel as nib

from DataPreProcTumor import DataPreprocStruct
from NiiLoadAndOrientationFun import *
from FixResolutionFun import *
from DataPreProc import *
from SaveFuns import saveNiiwName

def DataPreProcLung(CT4Lung):
    currCT_LungMask = CreateNOSaveLungMask(CT4Lung,SavePath=None)
    normLungMask  = NormalizeImage(currCT_LungMask,None,None,None,(1,1,1),None)
    normLungMask_Nii = Sitk2Nii(normLungMask).get_fdata()
    normLustmask_rot = np.rot90(normLungMask_Nii,axes=(0,1),k=-1)  
    del normLungMask
    return  normLustmask_rot


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

def mainPreProc(currCTs,currCT_name,itvTot,itvTumor,itvNodes,savePath_Px,nametumor):
    #CT
    ct_nii_ori = NiiLoadAndOrientation(currCTs[0])#orient to LAS    
    normCT = NormalizeImage(Nii2Sitk(ct_nii_ori),None,None,None,(1,1,1),None)
    ct_np_ori = Sitk2Nii(normCT).get_fdata()
    ctnpori_rot = np.rot90(ct_np_ori,axes=(0,1),k=-1)

    #Lung
    normLustmask_rot = DataPreProcLung(normCT)
    del normCT

    #Tumor
    listStructNames = []
    listStructImages = []
    if len(itvTot)>0: 
        itvTotResolution,tot_name = DataPreprocStruct(itvTot[0],ct_nii_ori)
        listStructImages.append(itvTotResolution)
        listStructNames.append(tot_name)
    if len(itvTumor)>0: 
        itvTumorResolution,tumor_name = DataPreprocStruct(itvTumor[0],ct_nii_ori)
        listStructImages.append(itvTumorResolution)
        listStructNames.append(tumor_name)
    if len(itvNodes)>0: 
        itvNodesResolution,nodes_name = DataPreprocStruct(itvNodes[0],ct_nii_ori)
        listStructImages.append(itvNodesResolution)
        listStructNames.append(nodes_name)

    #itvTumorFilled = FixHoles(itvTumorResolution)
    #itvNodesFilled = FixHoles(itvNodesResolution)

    ctcropped,struct1cropped,struct2cropped,struct3cropped = CropForegroundFunctionMONAI_v2(ctnpori_rot,normLustmask_rot,listStructImages,listStructNames)
    saveNiiwName(savePath_Px,currCT_name,ctcropped,struct1cropped,struct2cropped,struct3cropped,tumorname=nametumor,listStructNames=listStructNames)
    del ctcropped,itvTumorcropped,itvNodesCropped,itvTumorResolution,itvNodesResolution,normLustmask_rot,ctnpori_rot,ct_nii_ori
    ITVconv_flag = True
    return ITVconv_flag