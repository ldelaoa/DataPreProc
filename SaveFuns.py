import csv
import os
import nibabel as nib
import numpy as np


def saveMetrics(PxList,MetricsList,savePath):
    csv_file_path = os.path.join(savePath,'RegistMetricsV2.csv')
    data = list(zip(PxList, MetricsList))
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Px', 'DiceRegist'])
        csv_writer.writerows(data)
    print(f'Data has been saved to {csv_file_path}')
    return 0

def saveNiiwName(savePath,nameCT,ct2save,struct1Tosave=None,struct2Tosave=None,struct3Tosave=None,tumorname=None,listStructNames=[]):
    if not(os.path.exists(savePath)):
        os.mkdir(savePath)

    CT_nii_2save = nib.Nifti1Image(ct2save, np.eye(4))   
    nib.save(CT_nii_2save, os.path.join(savePath,nameCT+"_CTProcessed.nii.gz"))

    if not(struct1Tosave is None):
        tumor_nii_2save = nib.Nifti1Image(struct1Tosave, np.eye(4))  
        nib.save(tumor_nii_2save, os.path.join(savePath,listStructNames[0]+"_GTProcessed.nii.gz"))

    if not(struct2Tosave is None):
        tumor_nii_2save = nib.Nifti1Image(struct2Tosave, np.eye(4))  
        nib.save(tumor_nii_2save, os.path.join(savePath,listStructNames[1]+"_GTProcessed.nii.gz"))

    if not(struct3Tosave is None):
        tumor_nii_2save = nib.Nifti1Image(struct3Tosave, np.eye(4))  
        nib.save(tumor_nii_2save, os.path.join(savePath,listStructNames[2]+"_GTProcessed.nii.gz"))

    return 0