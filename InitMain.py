from LookFiles import LookFilesNiiRaw
from DataPreProc import *
from SinglePxRegist import *
import csv
from RegistwStats import *
from MergePandN_Fun import CheckTwoLabelCategories
from NiiLoadAndOrientationFun import *
from FixResolutionFun import *
from DataPreProcTumor import *
from SaveFuns import saveNiiwName
import logging

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

def CreatePxList():
    PxList_file  = "//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/ListsOfPatients/PxWithoutITVp.txt"
    with open(PxList_file, 'r') as file:
        PxList = [line.rstrip() for line in file]
    print(len(PxList))
    return PxList

import os

def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            if os.path.isfile(filepath):
                os.remove(filepath)
                print(f"Deleted {filepath}")
            else:
                print(f"{filepath} is not a file, skipping...")
        except Exception as e:
            print(f"Error deleting {filepath}: {e}")

def DataPreProcLung(CT4Lung):
    currCT_LungMask = CreateNOSaveLungMask(CT4Lung,SavePath=None)
    normLungMask  = NormalizeImage(currCT_LungMask,None,None,None,(1,1,1),None)
    normLungMask_Nii = Sitk2Nii(normLungMask).get_fdata()
    normLustmask_rot = np.rot90(normLungMask_Nii,axes=(0,1),k=-1)  
    del normLungMask
    return  normLustmask_rot

def main(root_path,savePath):
    #PxList = CreatePxList()
    PxList = os.listdir(root_path)

    logger = logging.getLogger('Nii2Nii_Log_V8')
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler('Nii2Nii_Log_V8.log')
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    
    print("Total of PX:",len(PxList))

    for Px in PxList:
        if Px == '1187341':
            savePath_Px = os.path.join(savePath,Px)
            ITVconv_flag = False
            GTVconv_flag = False        
            if False:
                delete_files_in_directory(savePath_Px)

            if not(os.path.exists(savePath_Px)):
                os.mkdir(savePath_Px)
            if True or len(os.listdir(savePath_Px))==0:
                print("Empty Folder Px ",Px)
                logger.info("Empty Folder Px "+str(Px))
                acct_path, PET_path,planct_path,itvTot,itvTumor,itvNodes,gtvTot,gtvTumor,gtvNodes,bp0,bp10,bp20,bp30,bp40,bp50,bp60,bp70,bp80,bp90,bp100 = LookFilesNiiRaw(os.path.join(root_path, Px),logger)

                #Check if any delineation is available, else not convert
                if len(gtvTot)+len(gtvTumor)+len(gtvNodes)+len(itvTot)+len(itvTumor)+len(itvNodes)==0:
                    print("ERROR Tumor Info Not existing")
                    logger.warning("ERROR Tumor Info Not existing"+str(Px))
                else:

                    gtvTumor,gtvNodes = CheckTwoLabelCategories(gtvTot,gtvTumor,gtvNodes,"GTV",logger)
                    itvTumor,itvNodes = CheckTwoLabelCategories(itvTot,itvTumor,itvNodes,"ITV",logger)

                    #listAllCTs_paths = [acct_path,planct_path,bp0,bp10,bp20,bp30,bp40,bp50,bp60,bp70,bp80,bp90,bp100]
                    #listAllCTs_names = ["ACCT","PlanCT","bp0","bp10","bp20","bp30","bp40","bp50","bp60","bp70","bp80","bp90","bp100"]
                    listAllCTs_names = ["PlanCT","bp50","bp60","bp40",]
                    listAllCTs_paths = [planct_path,bp50,bp60,bp40]

                    numCT=0
                    for currCTs in listAllCTs_paths:
                        if False and len(currCTs)>0:
                            #Tumor and Crop
                            if numCT==0 and itvTumor is not None and itvNodes is not None and not(ITVconv_flag):
                                currCT_name = currCTs[0].split("\\")[-1].split(".")[-3]+"_"+listAllCTs_names[numCT]
                                print(currCT_name,numCT)
                                #CT
                                ct_nii_ori = NiiLoadAndOrientation(currCTs[0])#orient to LAS    
                                normCT = NormalizeImage(Nii2Sitk(ct_nii_ori),None,None,None,(1,1,1),None)
                                ct_np_ori = Sitk2Nii(normCT).get_fdata()
                                ctnpori_rot = np.rot90(ct_np_ori,axes=(0,1),k=-1)

                                #Lung
                                normLustmask_rot = DataPreProcLung(normCT)
                                del normCT

                                #Tumor
                                itvTumorResolution,itvNodesResolution = DataPreprocTumor(itvTumor[0],itvNodes[0],ct_nii_ori)

                                #itvTumorFilled = FixHoles(itvTumorResolution)
                                #itvNodesFilled = FixHoles(itvNodesResolution)

                                logger.info("Check Sizes before Cropping"+str(Px)+str(itvTumorResolution.shape)+str(itvNodesResolution.shape)+str(ctnpori_rot.shape)+str(normLustmask_rot.shape))
                                ctcropped,itvTumorcropped,itvNodesCropped = CropForegroundFunctionMONAI(ctnpori_rot,normLustmask_rot,itvTumorResolution,itvNodesResolution)
                                nametumor = 'ITV'
                                ITVconv_flag = True
                                print("Rs Sum",np.sum(itvTumorcropped),np.sum(itvNodesCropped))
                                saveNiiwName(savePath_Px,currCT_name,ctcropped,itvTumorcropped,itvNodesCropped,tumorname=nametumor)
                                del ctcropped,itvTumorcropped,itvNodesCropped,itvTumorResolution,itvNodesResolution,normLustmask_rot,ctnpori_rot,ct_nii_ori
                            elif numCT!= 0 and gtvTumor is not None and gtvNodes is not None and not(GTVconv_flag): 
                                currCT_name = currCTs[0].split("\\")[-1].split(".")[-3]+"_"+listAllCTs_names[numCT]
                                print(currCT_name,numCT)
                                #CT
                                ct_nii_ori = NiiLoadAndOrientation(currCTs[0])#orient to LAS    
                                normCT = NormalizeImage(Nii2Sitk(ct_nii_ori),None,None,None,(1,1,1),None)
                                ct_np_ori = Sitk2Nii(normCT).get_fdata()
                                ctnpori_rot = np.rot90(ct_np_ori,axes=(0,1),k=-1)

                            #Lung
                                normLustmask_rot = DataPreProcLung(normCT)
                                del normCT

                                #Tumor
                                gtvTumorResolution,gtvNodesResolution = DataPreprocTumor(gtvTumor[0],gtvNodes[0],ct_nii_ori)

                                logger.info("Check Sizes before Cropping"+str(Px)+str(gtvTumorResolution.shape)+str(gtvNodesResolution.shape)+str(ctnpori_rot.shape)+str(normLustmask_rot.shape))
                                ctcropped,gtvTumorcropped,gtvNodesCropped = CropForegroundFunctionMONAI(ctnpori_rot,normLustmask_rot,gtvTumorResolution,gtvNodesResolution)
                                nametumor='GTV'
                                GTVconv_flag = True
                                saveNiiwName(savePath_Px,currCT_name,ctcropped,gtvTumorcropped,gtvNodesCropped,tumorname=nametumor)
                                del ctcropped,gtvTumorcropped,gtvNodesCropped,ctnpori_rot,normLustmask_rot,gtvTumorResolution,gtvNodesResolution,ct_nii_ori
                            elif False:
                                #CT
                                ct_nii_ori = NiiLoadAndOrientation(currCTs[0])#orient to LAS    
                                normCT = NormalizeImage(Nii2Sitk(ct_nii_ori),None,None,None,(1,1,1),None)
                                ct_np_ori = Sitk2Nii(normCT).get_fdata()
                                ctnpori_rot = np.rot90(ct_np_ori,axes=(0,1),k=-1)

                                #Lung
                                normLustmask_rot = DataPreProcLung(normCT)
                                del normCT

                                logger.info("Check Sizes before Cropping"+str(Px)+str(ctnpori_rot.shape)+str(normLustmask_rot.shape))
                                ctcropped,_,_ = CropForegroundFunctionMONAI(ctnpori_rot,normLustmask_rot,None,None)
                                nametumor = None
                                saveNiiwName(savePath_Px,currCT_name,ctcropped,None,None,tumorname=None)
                        numCT+=1
                print("----------------------")

if __name__ == "__main__" :
    #rootPath = "//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/CT_ITV_GTV_XBP_Nii/"
    #savePath = "//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/CT_ITV_GTV_XBP_Nii_Processed_v2/"
    rootPath = "Z:/inbox/Nii_Data/CT_ITV_GTV_XBP_Nii/"
    savePath = "Z:/inbox/Nii_Data/CT_ITV_GTV_XBP_Nii_Processed_v3/"
    main(rootPath,savePath)
    print("FINISHED!")

