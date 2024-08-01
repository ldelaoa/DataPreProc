import nibabel as nib
import SimpleITK as sitk
import os
from NormalizeImage import NormalizeImage


def LoopInFile(loop_path):
    for root,dir,files in os.walk(loop_path):
        for f in files:
            if "thorax_2mm" in f.lower():
                return True
    return False



if __name__== '__main__':
    root_path = "Z:/inbox/Nii_Data/CT_ITV_GTV_XBP_Nii/"
    px = '147625'#os.listdir(root_path)
    file_ct_path = '106_t60pr46_-_82ar64_-_78.nii.gz'
    file_gtv_path = 'GTV.nii.gz'
   
    image_ct = sitk.ReadImage(os.path.join(root_path,px,file_ct_path))
    image_gtv = sitk.ReadImage(os.path.join(root_path,px,file_gtv_path))

    print("CT","Origin",image_ct.GetOrigin(),"spacing",image_ct.GetSpacing(),"Size",image_ct.GetSize())
    print("GTV","Origin",image_gtv.GetOrigin(),"spacing",image_gtv.GetSpacing(),"Size",image_gtv.GetSize())

    image_ct1 = NormalizeImage(image_ct,None,None,None,(1,1,1),None)
    image_gtv = NormalizeImage(image_gtv,None,None,image_ct.GetOrigin(),(1,1,1),None)

    print("CT","Origin",image_ct1.GetOrigin(),"spacing",image_ct1.GetSpacing(),"Size",image_ct1.GetSize())
    print("GTV","Origin",image_gtv.GetOrigin(),"spacing",image_gtv.GetSpacing(),"Size",image_gtv.GetSize())
