from CreateSaveLungMask import *
from CropImgToLungMask import *
from NormalizeImage import *
from CheckImages import *
from Interpolate import *

def DataPreProc(img_path,lm_path,aditionalImg1_path,rootPx_path,name):
    #Create Lung Mask
    if len(lm_path) == 0:
        lungmask_img = CreateSaveLungMask(img_path[0], os.path.join(rootPx_path, name+"_lungMask1.nii.gz"))
    else:
        lungmask_img = sitk.ReadImage(lm_path[0])

    #Read Rest of images
    CT_img = sitk.ReadImage(img_path[0])
    addImg1_img = sitk.ReadImage(aditionalImg1_path[0])
    print("Init Sizes:",CT_img.GetSize(),lungmask_img.GetSize(),addImg1_img.GetSize())
    if addImg1_img.GetSize() != CT_img.GetSize():
        #Interpolate
        print("Itnerpolate Add Img before Cropping")
        addImg1_img_Interp = interpolate_image(CT_img, addImg1_img, name)
        addImg1_img = addImg1_img_Interp

    #Crop
    cropped_CT,cropped_LM,cropped_AddImg = CropImgToLungMask(lungmask_img,CT_img,addImg1_img,rootPx_path,name)
    print("Cropped:", cropped_CT.GetSize(), cropped_LM.GetSize(), cropped_AddImg.GetSize())

    # Normalize
    resized_CT = NormalizeImage(cropped_CT, False, os.path.join(rootPx_path, name + "_image_resampled3.nii.gz"))
    resized_LM = NormalizeImage(cropped_LM, False, os.path.join(rootPx_path, name + "_lungMask_resampled3.nii.gz"))
    if name == "ACCT":
        resized_AddImg = NormalizeImage(cropped_AddImg, False, os.path.join(rootPx_path, name + "_PET_resampled3.nii.gz"))
    else:
        resized_AddImg = NormalizeImage(cropped_AddImg, True, os.path.join(rootPx_path, name + "_ITV_resampled3.nii.gz"))
    print("Normalized Sizes:", resized_CT.GetSize(), resized_LM.GetSize(), resized_AddImg.GetSize())

    return 0

def DataPreProc_DEPRECATED(img_path,lm_path,aditionalImg1_path,rootPx_path,name):
    #Create Lung Mask
    if len(lm_path) == 0:
        lungmask_img = CreateSaveLungMask(img_path[0], os.path.join(rootPx_path, name+"_lungMask1.nii.gz"))
    else:
        lungmask_img = sitk.ReadImage(lm_path[0])

    #Read Rest of images
    CT_img = sitk.ReadImage(img_path[0])
    addImg1_img = sitk.ReadImage(aditionalImg1_path[0])
    print("Init Sizes:",CT_img.GetSize(),lungmask_img.GetSize(),addImg1_img.GetSize())
    if addImg1_img.GetSize() != CT_img.GetSize():
        #Interpolate
        print("Itnerpolate Add Img before Cropping")
        addImg1_img_Interp = interpolate_image(CT_img, addImg1_img, name)
        addImg1_img = addImg1_img_Interp

    #Crop
    cropped_CT,cropped_LM,cropped_AddImg = CropImgToLungMask(lungmask_img,CT_img,addImg1_img,rootPx_path,name)
    print("Cropped:", cropped_CT.GetSize(), cropped_LM.GetSize(), cropped_AddImg.GetSize())

    # Normalize
    resized_CT = NormalizeImage(cropped_CT, False, os.path.join(rootPx_path, name + "_image_resampled3.nii.gz"))
    resized_LM = NormalizeImage(cropped_LM, False, os.path.join(rootPx_path, name + "_lungMask_resampled3.nii.gz"))
    if name == "ACCT":
        resized_AddImg = NormalizeImage(cropped_AddImg, False, os.path.join(rootPx_path, name + "_PET_resampled3.nii.gz"))
    else:
        resized_AddImg = NormalizeImage(cropped_AddImg, True, os.path.join(rootPx_path, name + "_ITV_resampled3.nii.gz"))
    print("Normalized Sizes:", resized_CT.GetSize(), resized_LM.GetSize(), resized_AddImg.GetSize())

    return 0