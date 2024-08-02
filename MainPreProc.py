import SimpleITK as sitk
import numpy as np
import nibabel as nib
#from FixResolutionFun import *
from DataPreProcTumor import DataPreprocStruct
from NiiLoadAndOrientationFun import *
from DataPreProc import *
from SaveFuns import saveNiiwName
#from Screenshot_fun import Screenshot

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

def mainPreProc(currCTs,currCT_name,structTot,structTumor,structNodes,savePath_Px,nametumor):
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
    minShape = [0,0,0]
    minShape[0] = ctnpori_rot.shape[0]
    minShape[1] = ctnpori_rot.shape[1]
    minShape[2] = ctnpori_rot.shape[0]
    print(minShape)
    if len(structTot)>0: 
        itvTotResolution,tot_name = DataPreprocStruct(structTot[0],ct_nii_ori)
        listStructImages.append(itvTotResolution)
        listStructNames.append(tot_name)
        if itvTotResolution.shape[0]<minShape[0]: minShape[0]=itvTotResolution.shape[0]
        if itvTotResolution.shape[1]<minShape[1]: minShape[1]=itvTotResolution.shape[1]
        if itvTotResolution.shape[2]<minShape[2]: minShape[2]=itvTotResolution.shape[2]
    if len(structTumor)>0: 
        itvTumorResolution,tumor_name = DataPreprocStruct(structTumor[0],ct_nii_ori)
        listStructImages.append(itvTumorResolution)
        listStructNames.append(tumor_name)
        if itvTumorResolution.shape[0]<minShape[0]: minShape[0]=itvTumorResolution.shape[0]
        if itvTumorResolution.shape[1]<minShape[1]: minShape[1]=itvTumorResolution.shape[1]
        if itvTumorResolution.shape[2]<minShape[2]: minShape[2]=itvTumorResolution.shape[2]
    if len(structNodes)>0: 
        itvNodesResolution,nodes_name = DataPreprocStruct(structNodes[0],ct_nii_ori)
        listStructImages.append(itvNodesResolution)
        listStructNames.append(nodes_name)
        if itvNodesResolution.shape[0]<minShape[0]: minShape[0]=itvNodesResolution.shape[0]
        if itvNodesResolution.shape[1]<minShape[1]: minShape[1]=itvNodesResolution.shape[1]
        if itvNodesResolution.shape[2]<minShape[2]: minShape[2]=itvNodesResolution.shape[2]

    #itvTumorFilled = FixHoles(itvTumorResolution)
    #itvNodesFilled = FixHoles(itvNodesResolution)
    
    ctcropped,struct1cropped,struct2cropped,struct3cropped = CropForegroundFunctionMONAI_v2(
        ctnpori_rot,normLustmask_rot,listStructImages,listStructNames,MinStruct_Size=minShape)
    
    saveNiiwName(savePath_Px,currCT_name,ctcropped,struct1cropped,struct2cropped,struct3cropped,tumorname=nametumor,listStructNames=listStructNames)
    return True