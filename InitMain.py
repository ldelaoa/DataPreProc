from LookFiles import *
from DataPreProc import *
from SinglePxRegist import *
import csv
from RegistwStats import *
from MergePandN_Fun import CreateToTfromPandN
from NiiLoadAndOrientationFun import *
from FixResolutionFun import *
from DataPreProcTumor import *

def saveMetrics(PxList,MetricsList,savePath):
    csv_file_path = os.path.join(savePath,'RegistMetricsV2.csv')
    data = list(zip(PxList, MetricsList))
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Px', 'DiceRegist'])
        csv_writer.writerows(data)
    print(f'Data has been saved to {csv_file_path}')
    return 0

def saveNiiwName(savePath,nameCT,ct2save,lung2save,tumor2save=None,tumorname=None):
    if not(os.path.exists(savePath)):
        os.mkdir(savePath)

    CT_nii_2save = nib.Nifti1Image(ct2save, np.eye(4))  
    lung_nii_2save = nib.Nifti1Image(lung2save, np.eye(4))  
    nib.save(CT_nii_2save, os.path.join(savePath,nameCT+"_CTProcessed.nii.gz"))
    nib.save(lung_nii_2save, os.path.join(savePath,nameCT+"_LungProcessed.nii.gz"))
    if not(tumorname is None):
        tumor_nii_2save = nib.Nifti1Image(tumor2save, np.eye(4))  
        nib.save(tumor_nii_2save, os.path.join(savePath,tumorname+"_GTProcessed.nii.gz"))
    print("saved CT: ",nameCT,"tumor",tumorname)
    return 0


def main(root_path,savePath):
    PxList = os.listdir(root_path)
    regist_metrics = []
    analizedPx = []
    print("Tot PX:",len(PxList))
    for Px in PxList:
        savePath_Px = os.path.join(savePath,Px)
        ITVconv_flag = False
        GTVconv_flag = False
        if os.path.exists(savePath_Px):
            print("Folder Already Exist",Px)
        else:
            os.mkdir(savePath_Px)
        if len(os.listdir(savePath_Px))==0:
            print("------------------")
            print("Empty Folder",Px)
            acct_path, PET_path,planct_path,itvTot,itvTumor,itvNodes,gtvTot,gtvTumor,gtvNodes,bp0,bp10,bp20,bp30,bp40,bp50,bp60,bp70,bp80,bp90,bp100 = LookFilesNiiRaw(os.path.join(root_path, Px))
            if len(itvTot)==0 and len(itvTumor)>0: 
                print("ITVTot created")
                itvTot_nii,itvTot = CreateToTfromPandN(itvTumor,itvNodes)
            if len(gtvTot)==0 and len(gtvTumor)>0: 
                print("GTVTot created")
                gtvTot_nii,gtvTot = CreateToTfromPandN(gtvTumor,gtvNodes)

            listAllCTs_paths = [acct_path,planct_path,bp0,bp10,bp20,bp30,bp40,bp50,bp60,bp70,bp80,bp90,bp100]
            listAllCTs_names = ["ACCT","PlanCT","bp0","bp10","bp20","bp30","bp40","bp50","bp60","bp70","bp80","bp90","bp100"]

            numCT=0
            for currCTs in listAllCTs_paths:
                if len(currCTs)>0:
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
                    
                    #Tumor and Crop
                    if numCT>0 and len(itvTot)> 0 and not(ITVconv_flag):
                        itvResolution = DataPreprocTumor(itvTot[0],ct_nii_ori)
                        ctcropped,lungcropped,itvcropped = CropForegroundFunctionMONAI(ctResolution,lungResolution,itvResolution)
                        nametumor = 'ITV'
                        tumor2save = itvcropped
                        ITVconv_flag = True
                    elif numCT>1 and len(gtvTot)> 0 and not(GTVconv_flag):
                        gtvResolution = DataPreprocTumor(gtvTot[0],ct_nii_ori)
                        ctcropped,lungcropped,gtvcropped = CropForegroundFunctionMONAI(ctResolution,lungResolution,gtvResolution)
                        nametumor='GTV'
                        tumor2save = gtvcropped
                        GTVconv_flag = True
                    else:
                        ctcropped,lungcropped,_ = CropForegroundFunctionMONAI(ctResolution,lungResolution,None)
                        nametumor = None
                        tumor2save = None

                    saveNiiwName(savePath_Px,currCT_name,ctcropped,lungcropped,tumor2save,tumorname=nametumor)
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
    rootPath = "Z:/inbox/transferApr3_Ch2a/CT_ITV_GTV_XBP_Nii/CT_ITV_GTV_XBP_Nii/"
    savePath = "Z:/Projectline_modelling_lung_cancer/Nii_Processed/"
    main(rootPath,savePath)

