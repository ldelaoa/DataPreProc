import os
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt



def CheckImages(rootPath,Px):
    savePath = os.path.join(rootPath,"JPEGRegistImages")
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    image_step = "resampled3"  #
    #ACCT
    acctLM_img = sitk.ReadImage(os.path.join(rootPath,Px,"ACCT_lungMask_"+image_step+".nii.gz"))
    acctLM_array = sitk.GetArrayFromImage(acctLM_img)

    acct_img = sitk.ReadImage(os.path.join(rootPath, Px, "ACCT_image_"+image_step+".nii.gz"))
    acct_array = sitk.GetArrayFromImage(acct_img)

    acctPET_img = sitk.ReadImage(os.path.join(rootPath, Px, "ACCT_PET_"+image_step+".nii.gz"))
    acctPET_array = sitk.GetArrayFromImage(acctPET_img)

    #PLANCT
    planctLM_img = sitk.ReadImage(os.path.join(rootPath, Px, "PlanCT_lungMask_"+image_step+".nii.gz"))
    planctLM_array = sitk.GetArrayFromImage(planctLM_img)

    planct_img = sitk.ReadImage(os.path.join(rootPath, Px, "PlanCT_image_"+image_step+".nii.gz"))
    planct_array = sitk.GetArrayFromImage(planct_img)

    planctITV_img = sitk.ReadImage(os.path.join(rootPath, Px, "PlanCT_ITV_"+image_step+".nii.gz"))
    planctITV_img = sitk.Flip(planctITV_img, (True, False, False))
    planctITV_array = sitk.GetArrayFromImage(planctITV_img)

    #Registered
    PETRegist_img = sitk.ReadImage(os.path.join(rootPath, Px, "PET_IMGregistered4.nii.gz"))
    PETRegist_array = sitk.GetArrayFromImage(PETRegist_img)

    ACCTLMRegist_img = sitk.ReadImage(os.path.join(rootPath, Px, "ACCT_IMGregistered4.nii.gz"))
    ACCTLMRegistLM_array = sitk.GetArrayFromImage(ACCTLMRegist_img)

    print("Px Check Images",Px)
    print("Sizes ACCT",acctLM_array.shape,acct_array.shape,acctPET_array.shape)
    print("Sizes PlanCT", planctLM_array.shape, planct_array.shape, planctITV_array.shape)
    print("Sizes Registered", PETRegist_array.shape, ACCTLMRegistLM_array.shape)
    alphaVal=.5
    for i in range(0, planct_array.shape[-2], 3):
        if np.sum(planctITV_array[:, i, :]) > 0:
            plt.figure(figsize=(16, 14))
            plt.subplot(221), plt.imshow(planct_array[:, i, :], cmap='gray'), plt.axis("off")
            plt.contour(planctITV_array[:, i, :])
            plt.gca().invert_yaxis(), plt.title("Plan CT+ITV")

            plt.subplot(222), plt.imshow(planct_array[:, i, :], cmap='gray'), plt.axis("off")
            plt.imshow(ACCTLMRegistLM_array[:, i, :], cmap='hot', alpha=alphaVal, ), plt.axis("off")
            plt.gca().invert_yaxis(), plt.title("Regist CT")

            plt.subplot(223), plt.imshow(planct_array[:, i, :], cmap='gray'), plt.axis("off")
            plt.imshow(PETRegist_array[:, i, :], cmap='hot', alpha=alphaVal, ), plt.axis("off")
            plt.gca().invert_yaxis(), plt.title("Plan CT+PET")

            plt.subplot(224), plt.imshow(planct_array[:, i, :], cmap='gray'), plt.axis("off")
            plt.imshow(PETRegist_array[:, i, :], cmap='hot', alpha=alphaVal, ), plt.axis("off")
            plt.contour(planctITV_array[:, i, :])
            plt.gca().invert_yaxis(), plt.title("Plan CT+PET+ITV")

            plt.tight_layout()
            plt.savefig(os.path.join(savePath, Px + "_" + str(i)))
            plt.clf()
            plt.close()

    if False:
        for i in range(0,planct_array.shape[0],3):
            if np.sum(planctITV_array[i,:,:,]>0):
                plt.figure()
                plt.subplot(231), plt.imshow(planct_array[i, :, :], cmap="gray"), plt.axis('off')
                plt.contour(planctLM_array[i, :, :]), plt.title("PlanCT+PlanCT Lung")
                #plt.contour(planctITV_array[i, :, :])

                plt.subplot(232), plt.imshow(acct_array[i, :, :], cmap="gray"), plt.axis('off')
                plt.contour(acctLM_array[i, :, :]), plt.title("ACCT+ACCT Lungs")
                #plt.contour(planctITV_array[i, :, :])

                plt.subplot(233),plt.imshow(planct_array[i, :, :], cmap="gray", alpha=1), plt.axis('off')
                plt.contour(acctLM_array[i, :, :]),plt.title("PlanCT+PET+ACCTLung")

                plt.subplot(234),plt.imshow(planct_array[i, :, :], cmap="gray", alpha=1)
                plt.contour(ACCTLMRegistLM_array[i, :, :]), plt.axis('off'), plt.title("PlanCT+PETr+ACCTLungr")

                plt.subplot(235),plt.imshow(acctLM_array[i, :, :]), plt.axis('off')
                plt.contour(planctLM_array[i, :, :]), plt.title("ACCT LM+PlanCT LM")

                plt.subplot(236),plt.imshow(ACCTLMRegistLM_array[i, :, :]), plt.axis('off')
                plt.contour(planctLM_array[i, :, :]), plt.title("ACCT LM r+PlanCT LM")

                plt.tight_layout()
                plt.savefig(os.path.join(savePath,Px+"_"+str(i)))

    return 0