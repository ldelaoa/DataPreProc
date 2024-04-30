import csv
import shutil
import os
from tqdm import tqdm


def LookFilesLite_Snapshot(folder_path):
    bp50_list = None
    for root,dirs,files in os.walk(folder_path):
        for f in files:
            if "PlanCT_CTProcessed.nii" in f:
                planCT_list = os.path.join(folder_path,f)
            if "bp50_CTProcessed.nii" in f:
                bp50_list = os.path.join(folder_path,f)
            if "GTVtot_GTProcessed.nii" in f:
                gtvTOT = os.path.join(folder_path,f)
            if "ITVtot_GTProcessed.nii.gz" in f:
                itvTOT = os.path.join(folder_path,f)
    if bp50_list == None: 
        for root,dirs,files in os.walk(folder_path):
            for f in files:
                if "bp60_CTProcessed.nii" in f:
                    bp50_list = os.path.join(folder_path,f)
    if bp50_list == None: 
        for root,dirs,files in os.walk(folder_path):
            for f in files:
                if "bp40_CTProcessed.nii" in f:
                    bp50_list = os.path.join(folder_path,f)


    return planCT_list,bp50_list,itvTOT,gtvTOT
    


if __name__ == "__main__":
    # Define your source folder and destination folders
    root = "//zkh/appdata/RTDicom/Projectline_modelling_lung_cancer/Users/Luis/"
    tranining_folder = root+"CT_ITV_GTV_XBP_NII_Processed_Select/Training/"
    training_folder_lite = root+"CT_ITV_GTV_XBP_NII_Processed_Select/TrainingLite/"
    PxList = os.listdir(tranining_folder)

    iter = len(PxList)
    progress_bar = tqdm(total=iter, desc="Processing", unit="iteration")

    for Px in PxList:
        planCT_list,bp50_list,itvTOT,gtvTOT = LookFilesLite_Snapshot(tranining_folder+Px)

        currDestFold = os.path.join(training_folder_lite,Px)
        if not(os.path.exists(currDestFold)):
            os.mkdir(currDestFold)
        if len(os.listdir(currDestFold))<3:
            shutil.copy(planCT_list, currDestFold)
            shutil.copy(bp50_list, currDestFold)
            shutil.copy(itvTOT, currDestFold)
            shutil.copy(gtvTOT, currDestFold)
        progress_bar.update(1)
    progress_bar.close()

    print("done")
