from LookFiles import *
from DataPreProc import *
from SinglePxRegist import *
import csv
from RegistwStats import *
from MergePandN_Fun import *
from NiiLoadAndOrientationFun import *
from FixResolutionFun import *
from DataPreProcTumor import *
from SaveFuns import *
import logging

def CreatePxList():
    PxList_file  = "//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/ListsOfPatients/PxSelectionforDCM2Nii_pt1.txt"
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


def main(root_path,savePath):
    PxList = CreatePxList()
    #PxList = os.listdir(root_path)


    logger = logging.getLogger('Nii2Nii_Log_V2_pt1')
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler('Nii2Nii_Log_V2_pt1.log')
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    
    print("Total of PX:",len(PxList))

    for Px in PxList:
        savePath_Px = os.path.join(savePath,Px)
        ITVconv_flag = False
        GTVconv_flag = False        
        if False:
            delete_files_in_directory(savePath_Px)

        if not(os.path.exists(savePath_Px)):
            os.mkdir(savePath_Px)
        if False and len(os.listdir(savePath_Px))>0:
            print("Patient already with Files on the folder, not analyzing"+Px)
            logger.info("Patient already with Files on the folder, not analyzing"+str(Px))
        else:
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

                listAllCTs_paths = [acct_path,planct_path,bp0,bp10,bp20,bp30,bp40,bp50,bp60,bp70,bp80,bp90,bp100]
                listAllCTs_names = ["ACCT","PlanCT","bp0","bp10","bp20","bp30","bp40","bp50","bp60","bp70","bp80","bp90","bp100"]

                numCT=0
                for currCTs in listAllCTs_paths:
                    if len(currCTs)>0:
                        #Tumor and Crop
                        if numCT>0 and itvTumor is not None and itvNodes is not None and not(ITVconv_flag):
                            currCT_name = currCTs[0].split("\\")[-1].split(".")[-3]+"_"+listAllCTs_names[numCT]
                            print(currCT_name,numCT)
                            #CT
                            ct_nii_ori = NiiLoadAndOrientation(currCTs[0])#orient to LAS
                            ct_np_ori = ct_nii_ori.get_fdata()
                            ctnpori_rot = np.rot90(ct_np_ori,axes=(0,1),k=-1)
                            ctResolution = FixResolution(ctnpori_rot,ct_nii_ori)

                            #Lung
                            currCT_LungMask = CreateNOSaveLungMask(currCTs[0],SavePath=None)
                            lungResolution = FixResolution(currCT_LungMask,ct_nii_ori)

                            itvTumorResolution,itvNodesResolution = DataPreprocTumor(itvTumor[0],itvNodes[0],ct_nii_ori)
                            itvTumorFilled = FixHoles(itvTumorResolution)
                            itvNodesFilled = FixHoles(itvNodesResolution)
                            logger.info("Check Sizes before Cropping"+str(Px)+str(itvTumorFilled.shape)+str(itvNodesFilled.shape)+str(ctResolution.shape)+str(lungResolution.shape))
                            ctcropped,lungcropped,itvTumorcropped,itvNodesCropped = CropForegroundFunctionMONAI(ctResolution,lungResolution,itvTumorFilled,itvNodesFilled)
                            nametumor = 'ITV'
                            tumor2save = itvTumorcropped
                            nodes2save = itvNodesCropped
                            ITVconv_flag = True
                            saveNiiwName(savePath_Px,currCT_name,ctcropped,lungcropped,tumor2save,nodes2save,tumorname=nametumor)
                        elif numCT>1 and gtvTumor is not None and gtvNodes is not None and not(GTVconv_flag):
                            currCT_name = currCTs[0].split("\\")[-1].split(".")[-3]+"_"+listAllCTs_names[numCT]
                            print(currCT_name,numCT)
                            #CT
                            ct_nii_ori = NiiLoadAndOrientation(currCTs[0])#orient to LAS
                            ct_np_ori = ct_nii_ori.get_fdata()
                            ctnpori_rot = np.rot90(ct_np_ori,axes=(0,1),k=-1)
                            ctResolution = FixResolution(ctnpori_rot,ct_nii_ori)

                            #Lung
                            currCT_LungMask = CreateNOSaveLungMask(currCTs[0],SavePath=None)
                            lungResolution = FixResolution(currCT_LungMask,ct_nii_ori)

                            gtvTumorResolution,gtvNodesResolution = DataPreprocTumor(gtvTumor[0],gtvNodes[0],ct_nii_ori)
                            gtvTumorFilled = FixHoles(gtvTumorResolution)
                            gtvNodesFilled = FixHoles(gtvNodesResolution)
                            logger.info("Check Sizes before Cropping"+str(Px)+str(gtvTumorFilled.shape)+str(gtvNodesFilled.shape)+str(ctResolution.shape)+str(lungResolution.shape))
                            ctcropped,lungcropped,gtvTumorcropped,gtvNodesCropped = CropForegroundFunctionMONAI(ctResolution,lungResolution,gtvTumorFilled,gtvNodesFilled) #fix
                            nametumor='GTV'
                            tumor2save = gtvTumorcropped
                            nodes2save = gtvNodesCropped
                            GTVconv_flag = True
                            saveNiiwName(savePath_Px,currCT_name,ctcropped,lungcropped,tumor2save,nodes2save,tumorname=nametumor)
                        elif False:
                            logger.info("Check Sizes before Cropping"+str(Px)+str(ctResolution.shape)+str(lungResolution.shape))
                            ctcropped,lungcropped,_,_ = CropForegroundFunctionMONAI(ctResolution,lungResolution,None)
                            nametumor = None
                            tumor2save = None
                            nodes2save = None
                            saveNiiwName(savePath_Px,currCT_name,ctcropped,lungcropped,tumor2save,nodes2save,tumorname=nametumor)
                    numCT+=1
            print("----------------------")



    #print(Px,"PlanCT")
    #DataPreProc(planct_path, planct_pathLM,ITV_Path, os.path.join(root_path, Px),"PlanCT")
    #print(Px, "ACCT")
    #DataPreProc(acct_Path, acct_PathLM, PET_Path, os.path.join(root_path, Px), "ACCT")
    #Regist
    #regist_metrics.append(SingPxRegistWMetrics_onlyCTRegist(root_path,Px))
    #CheckImages(root_path, Px)

    #analizedPx.append(Px)
    #_ = saveMetrics(analizedPx,regist_metrics,root_path)


if __name__ == "__main__" :
    #rootPath = "Z:/inbox/transferApr3_Ch2a/CT_ITV_GTV_XBP_Nii/CT_ITV_GTV_XBP_Nii/"
    rootPath = "//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/CT_ITV_GTV_XBP_Nii/"
    savePath = "//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/CT_ITV_GTV_XBP_Nii_Processed/"
    #savePath = "Z:/Projectline_modelling_lung_cancer/Nii_Processed2/"
    main(rootPath,savePath)

