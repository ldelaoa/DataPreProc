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