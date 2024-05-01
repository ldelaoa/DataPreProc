import sys
sys.path.append("C:/Users/LuisRicardo/Documents/GitHub/JoHof_lungmask/lungmask")
from lungmask import LMInferer
import SimpleITK as sitk
import numpy as np


def CreateSaveLungMask(LoadPath,SavePath):
    inferer = LMInferer()
    img_sitk = sitk.ReadImage(LoadPath)
    print(sitk.GetArrayFromImage(img_sitk).shape)
    segmentation = inferer.apply(img_sitk)
    segmentation_sitk = sitk.GetImageFromArray(segmentation)
    segmentation_sitk.CopyInformation(img_sitk)
    sitk.WriteImage(segmentation_sitk, SavePath)
    return segmentation_sitk

def CreateNOSaveLungMask(img_sitk,SavePath=None):
    inferer = LMInferer()
    #img_sitk = sitk.ReadImage(LoadPath)
    #print(sitk.GetArrayFromImage(img_sitk).shape)
    segmentation = inferer.apply(img_sitk)
    segmentation[segmentation>0]=1
    segmentation_sitk = sitk.GetImageFromArray(segmentation)
    segmentation_sitk.CopyInformation(img_sitk)
    segmentation_np = sitk.GetArrayFromImage(segmentation_sitk)
    segmentation_np[segmentation_np>0]=1
    segmentation_transp = np.transpose(segmentation_np,[1,2,0])

    return segmentation_sitk