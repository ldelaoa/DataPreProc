from LookFiles import LookFilesNiiRaw
import csv
from MergePandN_Fun import CheckTwoLabelCategories,GetNames
import logging
from MainPreProc import mainPreProc
import os


def CreatePxList():
    PxList_file  = "//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/ListsOfPatients/PxWithoutITVp.txt"
    with open(PxList_file, 'r') as file:
        PxList = [line.rstrip() for line in file]
    print(len(PxList))
    return PxList

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
    #PxList = CreatePxList()
    PxList = os.listdir(root_path)
    
    logger = logging.getLogger('Nii2Nii_Log_V8')
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler('Nii2Nii_Log_V8.log')
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    
    print("Total of PX:",len(PxList))

    for Px in PxList:
        savePath_Px = os.path.join(savePath,Px)        
        if False:
            delete_files_in_directory(savePath_Px)
        ITVconv_flag = False
        GTVconv_flag = False
        if not(os.path.exists(savePath_Px)):
            os.mkdir(savePath_Px)
            logger.info("Curr  "+str(Px))
            acct_path, PET_path,planct_path,itvTot,itvTumor,itvNodes,gtvTot,gtvTumor,gtvNodes,bp0,bp10,bp20,bp30,bp40,bp50,bp60,bp70,bp80,bp90,bp100 = LookFilesNiiRaw(os.path.join(root_path, Px),logger)

            #Check if any delineation is available, else not convert
            if not((len(itvTot)>0 or len(itvTumor)>0 or len(itvNodes)>0) and (len(gtvTot)>0 or len(gtvTumor)>0 or len(gtvNodes)>0)):
                print("ERROR Tumor Info Not existing")
                logger.warning("ERROR Tumor Info Not existing"+str(Px))
            else:

                listAllCTs_names = ["PlanCT","bp50","bp60","bp40",]
                listAllCTs_paths = [planct_path,bp50,bp60,bp40]

                numCT=0
                for currCTs in listAllCTs_paths:
                    if len(currCTs)>0:
                        if not(ITVconv_flag) and numCT==0:
                            currCT_name = currCTs[0].split("\\")[-1].split(".")[-3]+"_"+listAllCTs_names[numCT]
                            print(currCT_name,numCT)
                            ITVconv_flag = mainPreProc(currCTs,currCT_name,itvTot,itvTumor,itvNodes,savePath_Px,'ITV')

                        elif not(GTVconv_flag) and numCT>0:
                            currCT_name = currCTs[0].split("\\")[-1].split(".")[-3]+"_"+listAllCTs_names[numCT]
                            print(currCT_name,numCT)
                            GTVconv_flag = mainPreProc(currCTs,currCT_name,gtvTot,gtvTumor,gtvNodes,savePath_Px,'GTV')

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

