from lungmask import LMInferer
import SimpleITK as sitk


def CreateSaveLungMask(LoadPath,SavePath):
    inferer = LMInferer()
    img_sitk = sitk.ReadImage(LoadPath)
    print(sitk.GetArrayFromImage(img_sitk).shape)
    segmentation = inferer.apply(img_sitk)
    segmentation_sitk = sitk.GetImageFromArray(segmentation)
    segmentation_sitk.CopyInformation(img_sitk)
    sitk.WriteImage(segmentation_sitk, SavePath)
    return segmentation_sitk

