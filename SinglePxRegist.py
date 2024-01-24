import SimpleITK as sitk
import os
from rigid_registration_lite import tailor_registration
import numpy as np
from GetContourFromMasks import *

def dice_coefficient(image1, image2):
    array1 = sitk.GetArrayFromImage(image1)
    array2 = sitk.GetArrayFromImage(image2)

    array1 = np.round(array1,0)
    array2 = np.round(array2, 0)

    flat_array1 = array1.flatten()
    flat_array2 = array2.flatten()
    intersection = np.sum(flat_array1 * flat_array2)
    union = np.sum(flat_array1) + np.sum(flat_array2)
    #intersection = np.sum(flat_array1 & flat_array2)
    #union = np.sum(flat_array1 | flat_array2)

    dice = (2.0 * intersection) / (union + intersection + 1e-6)
    return dice


def LookFilesResampled(rootPx_path):
    image_step = "resampled3"  #
    acctLM_img = sitk.ReadImage(os.path.join(rootPx_path, "ACCT_lungMask_" + image_step + ".nii.gz"))
    acct_img = sitk.ReadImage(os.path.join(rootPx_path, "ACCT_image_" + image_step + ".nii.gz"))
    acctPET_img = sitk.ReadImage(os.path.join(rootPx_path, "ACCT_PET_" + image_step + ".nii.gz"))

    planctLM_img = sitk.ReadImage(os.path.join(rootPx_path, "PlanCT_lungMask_" + image_step + ".nii.gz"))
    planct_img = sitk.ReadImage(os.path.join(rootPx_path, "PlanCT_image_" + image_step + ".nii.gz"))
    planctITV_img = sitk.ReadImage(os.path.join(rootPx_path, "PlanCT_ITV_" + image_step + ".nii.gz"))
    planctITV_img = sitk.Flip(planctITV_img, (True, False, False))

    return planct_img, planctITV_img, planctLM_img, acct_img, acctLM_img, acctPET_img


def SinglePxRegist(rootPx_path,registOption):
    print("Inside Registration module")

    transf_spec = "Scale3D"
    center_spec = "Geometry"
    metric_spec = "Correlation"
    optimizer = "RegularStepGradientDescent"
    shift_sepc = "PhysicalShift"
    iterations_spec = 300
    lr = 1
    minStep = 0.0001
    gradientT = 1e-8
    offset = "Diff"

    PlanCT_img, ITV_img, PlanCTLM_img, ACCT_img, ACCTLM_img, PET_img = LookFilesResampled(rootPx_path)

    if registOption=="LungMaskRegistration":
        PlanCTLM_img = create_contour_image(PlanCTLM_img)
        ACCTLM_img = create_contour_image(ACCTLM_img)

        moved_Image_LM, evaluationMetric_LM, final_transform_LM = tailor_registration(PlanCTLM_img, ACCTLM_img,transf_spec,center_spec, metric_spec,optimizer, shift_sepc,offset,iterations_spec=iterations_spec, lr=lr,minStep=minStep, gradientT=gradientT)

        PETmovedwLM_image = sitk.Resample(PET_img, PlanCTLM_img, final_transform_LM, sitk.sitkBSpline, 0.0,PET_img.GetPixelID())
        ACCTmovedwLM_image = sitk.Resample(ACCT_img, PlanCTLM_img, final_transform_LM, sitk.sitkBSpline, 0.0,ACCT_img.GetPixelID())

        sitk.WriteImage(moved_Image_LM, os.path.join(rootPx_path, "LungMask_LMregistered4.nii.gz"))
        sitk.WriteImage(PETmovedwLM_image, os.path.join(rootPx_path, "PET_LMregistered4.nii.gz"))
        sitk.WriteImage(ACCTmovedwLM_image, os.path.join(rootPx_path, "ACCT_LMregistered4.nii.gz"))
    
    if registOption=="CTRegistration":
        moved_Image_CT,evaluationMetric_CT,final_transform_CT = tailor_registration(PlanCT_img,ACCT_img,transf_spec,center_spec,metric_spec,optimizer, shift_sepc,offset,iterations_spec=iterations_spec, lr=lr,minStep=minStep, gradientT=gradientT)
        PETmovedwCT_image = sitk.Resample(PET_img, PlanCT_img, final_transform_CT, sitk.sitkBSpline, 0.0,PET_img.GetPixelID())
        LungMaskmovedwCT_image = sitk.Resample(ACCTLM_img, PlanCT_img, final_transform_CT, sitk.sitkNearestNeighbor, 0.0,ACCT_img.GetPixelID())

        sitk.WriteImage(LungMaskmovedwCT_image, os.path.join(rootPx_path, "LungMask_IMGregistered4.nii.gz"))
        sitk.WriteImage(PETmovedwCT_image, os.path.join(rootPx_path, "PET_IMGregistered4.nii.gz"))
        sitk.WriteImage(moved_Image_CT, os.path.join(rootPx_path, "ACCT_IMGregistered4.nii.gz"))
    
    return PlanCT_img, ITV_img
       