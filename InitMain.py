from LookFiles import *
from DataPreProc import *
from SinglePxRegist import *
import csv
from RegistwStats import *


def saveMetrics(PxList,MetricsList,savePath):
    csv_file_path = os.path.join(savePath,'RegistMetricsV2.csv')
    data = list(zip(PxList, MetricsList))
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Px', 'DiceRegist'])
        csv_writer.writerows(data)
    print(f'Data has been saved to {csv_file_path}')
    return 0


def main(root_path):
    PxList = os.listdir(root_path)
    regist_metrics = []
    analizedPx = []
    for Px in PxList:
        if "JPEGRegistImages" not in Px and "RegistMetricsV2" not in Px:
            analizedPx.append(Px)
            acct_Path, acct_PathLM, PET_Path, planct_path, planct_pathLM, ITV_Path = LookFiles(os.path.join(root_path, Px))
            print(Px,"PlanCT")
            DataPreProc(planct_path, planct_pathLM,ITV_Path, os.path.join(root_path, Px),"PlanCT")
            print(Px, "ACCT")
            DataPreProc(acct_Path, acct_PathLM, PET_Path, os.path.join(root_path, Px), "ACCT")
            #Regist
            SinglePxRegist(os.path.join(root_path, Px),"CTRegistration")
            regist_metrics.append(SingPxRegistWMetrics_onlyCTRegist(root_path,Px))
            CheckImages(root_path, Px)

    _ = saveMetrics(analizedPx,regist_metrics,root_path)


if __name__ == "__main__" :
    rootPath = "/scratch/p308104/CT_RT_PET_ACCT_NiiToHabrok"
    #rootPath = "/home/umcg/Desktop/DataPreProces/CT_RT_PET_ACCT_NiiToHabrok"
    main(rootPath)

