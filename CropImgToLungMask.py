import SimpleITK as sitk
import numpy as np
import os


def RegionXtra(min_indices,max_indices,image,array):
    xtra = 46 # in mm
    min_indices_xtra = np.zeros(3)
    max_indices_xtra = np.zeros(3)
    spacingCT = image.GetSpacing()
    spacingCTt = spacingCT[2], spacingCT[0], spacingCT[1]
    pixelsToAdd = np.divide(xtra, spacingCTt)
    min_indices_xtra[0] = max(min_indices[0] - pixelsToAdd[0], 0)
    min_indices_xtra[1] = max(min_indices[1] - pixelsToAdd[1], 0)
    min_indices_xtra[2] = max(min_indices[2] - pixelsToAdd[2], 0)
    max_indices_xtra[0] = min(max_indices[0] + pixelsToAdd[0], array.shape[0])
    max_indices_xtra[1] = min(max_indices[1] + pixelsToAdd[1], array.shape[1])
    max_indices_xtra[2] = min(max_indices[2] + pixelsToAdd[2], array.shape[2])

    return min_indices_xtra, max_indices_xtra


def CropWithRegion(region,array,sitkImage):
    # Crop the image
    cropped_array = array[region[0][0]:region[1][0], region[0][1]:region[1][1], region[0][2]:region[1][2]]

    # Create a new SimpleITK image from the cropped array
    cropped_img = sitk.GetImageFromArray(cropped_array)

    # Set the spacing, origin, and direction of the cropped image to match the original
    cropped_img.SetSpacing(sitkImage.GetSpacing())
    cropped_img.SetOrigin(sitkImage.GetOrigin())
    cropped_img.SetDirection(sitkImage.GetDirection())

    return cropped_img


def CropImgToLungMask(LungMask,CT,AddImg,rootPx_path,name):
    lung_array = sitk.GetArrayFromImage(LungMask)
    CT_array = sitk.GetArrayFromImage(CT)
    addImg_array = sitk.GetArrayFromImage(AddImg)

    # Find the bounding box containing values greater than 0
    nonzero_indices = np.nonzero(lung_array)
    min_indices = np.min(nonzero_indices, axis=1)
    max_indices = np.max(nonzero_indices, axis=1)

    #Add Extra Margin to the Crop
    min_indices_xtra,max_indices_xtra = RegionXtra(min_indices, max_indices, CT, lung_array)

    # Define the cropping region
    #region = [int(min_index) for min_index in min_indices], [int(max_index) + 1 for max_index in max_indices]
    region = [int(min_index) for min_index in min_indices_xtra], [int(max_index) + 1 for max_index in max_indices_xtra]
    cropped_CT = CropWithRegion(region, CT_array, CT)
    cropped_LM = CropWithRegion(region, lung_array, LungMask)
    cropped_AddImg = CropWithRegion(region, addImg_array, AddImg)

    #SAVE
    sitk.WriteImage(cropped_CT, os.path.join(rootPx_path, name + "_image_cropped2.nii.gz"))
    sitk.WriteImage(cropped_LM, os.path.join(rootPx_path, name + "_lungMask_cropped2.nii.gz"))
    if name == "ACCT":
        sitk.WriteImage(cropped_AddImg, os.path.join(rootPx_path, name + "_PET_cropped2.nii.gz"))
    if name == "PlanCT":
        sitk.WriteImage(cropped_AddImg, os.path.join(rootPx_path, name + "_ITV_cropped2.nii.gz"))

    return cropped_CT,cropped_LM,cropped_AddImg
