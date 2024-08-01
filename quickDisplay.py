import nibabel as nib
import SimpleITK as sitk
import os
from NormalizeImage import NormalizeImage
import matplotlib.pyplot as plt
import numpy as np

def LoopInFile(loop_path):
    for root,dir,files in os.walk(loop_path):
        for f in files:
            if "thorax_2mm" in f.lower():
                return True
    return False



if __name__== '__main__':
    root_path = "Z:/inbox/Nii_Data/CT_ITV_GTV_XBP_Nii_Processed_v3/"
    px = '1396853'#os.listdir(root_path)
    file_ct_path = '5_4d_thorax_20_20_i30f_3_0_-_90__trigger_delay_50_bp50_CTProcessed.nii.gz'
    file_gtv_path = 'GTV_GTProcessed.nii.gz'
   
    image_ct = sitk.ReadImage(os.path.join(root_path,px,file_ct_path))
    image_gtv = sitk.ReadImage(os.path.join(root_path,px,file_gtv_path))

    print("CT","Origin",image_ct.GetOrigin(),"spacing",image_ct.GetSpacing(),"Size",image_ct.GetSize())
    print("GTV","Origin",image_gtv.GetOrigin(),"spacing",image_gtv.GetSpacing(),"Size",image_gtv.GetSize())

    imgCT_np = sitk.GetArrayFromImage(image_ct)
    imgGTV_np = sitk.GetArrayFromImage(image_gtv)
    count=0
    for i in range(0,imgGTV_np.shape[-2],5):
        if np.sum(imgGTV_np[:,i,:])>0:
            plt.imshow(imgCT_np[:,i,:],cmap="gray")
            plt.contour(imgGTV_np[:,i,:])
            plt.show()
            count+=1
        if count>5:
            break
                  