from LookFiles import LookFilesNiiRaw
import csv
from MergePandN_Fun import CheckTwoLabelCategories,GetNames
import logging
from MainPreProc import mainPreProc
import os
from multiprocessing import Pool
from tqdm import tqdm


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


def main(PxList):
    root_path = "Z:/inbox/Nii_Data/CT_ITV_GTV_XBP_Nii/"
    savePath = "Z:/inbox/Nii_Data/CT_ITV_GTV_XBP_Nii_Processed_v3/"
    for Px in PxList:
        savePath_Px = os.path.join(savePath,Px)        
        if False and os.path.exists(savePath_Px):
            delete_files_in_directory(savePath_Px)
        GTVconv_flag = False
        logger = None
        if True or not(os.path.exists(savePath_Px)):
            #print("Px:",Px)
            #logger.info("Curr  "+str(Px))
            acct_path, PET_path,planct_path,itvTot,itvTumor,itvNodes,gtvTot,gtvTumor,gtvNodes,bp0,bp10,bp20,bp30,bp40,bp50,bp60,bp70,bp80,bp90,bp100 = LookFilesNiiRaw(os.path.join(root_path, Px),logger)
            
            #Check if any delineation is available, else not convert
            if not((len(itvTot)>0 or len(itvTumor)>0 or len(itvNodes)>0) and (len(gtvTot)>0 or len(gtvTumor)>0 or len(gtvNodes)>0)):
                print(Px,"ERROR Tumor Info Not existing")
                #logger.warning("ERROR Tumor Info Not existing"+str(Px))
            elif len(planct_path)==0 or len(bp50)+len(bp60)+len(bp40)==0:
                print(Px,"CTs are insufficient")
                #logger.warning("CTs are insufficient"+str(Px))
            elif "thorax25mm" in planct_path[0]:
                print(Px,"Num PlanCTs",len(planct_path),"BPs",len(bp50)+len(bp60)+len(bp40))
                if not(os.path.exists(savePath_Px)):
                    os.mkdir(savePath_Px)

                #ITV
                planCT_name = planct_path[0].split("\\")[-1].split(".")[-3]+"_"+"PlanCT"
                print(planCT_name)
                mainPreProc(planct_path,planCT_name,itvTot,itvTumor,itvNodes,savePath_Px,'ITV')

                #GTV
                listAllCTs_names = ["bp50","bp60","bp40",]
                listAllCTs_paths = [bp50,bp60,bp40]
                numCT=0
                for currCTs in listAllCTs_paths:
                    if len(currCTs)>0:
                        if not(GTVconv_flag):
                            currCT_name = currCTs[0].split("\\")[-1].split(".")[-3]+"_"+listAllCTs_names[numCT]
                            print(currCT_name,numCT)
                            GTVconv_flag = mainPreProc(currCTs,currCT_name,gtvTot,gtvTumor,gtvNodes,savePath_Px,'GTV')
                    numCT+=1
                print("----------------------")



def init(root_path,savePath):
    #PxList = CreatePxList()
    PxList = os.listdir(root_path)
    if False:
        logger = logging.getLogger('Nii2Nii_Log_V8')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('Nii2Nii_Log_V8.log')
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
    else:
        logger = None
    
    print("Total of PX:",len(PxList))
    
    num_workers = os.cpu_count()
    print("Workers",num_workers)

    pool = Pool(processes=num_workers)
    pool.map(main,[PxList])
    pool.close()
    pool.join()
    

    

if __name__ == "__main__" :
    #rootPath = "//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/CT_ITV_GTV_XBP_Nii/"
    #savePath = "//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/CT_ITV_GTV_XBP_Nii_Processed_v2/"
    rootPath = "Z:/inbox/Nii_Data/CT_ITV_GTV_XBP_Nii/"
    savePath = "Z:/inbox/Nii_Data/CT_ITV_GTV_XBP_Nii_Processed_v3/"
    init(rootPath,savePath)
    print("FINISHED!")

