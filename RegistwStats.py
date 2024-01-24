from SinglePxRegist import *
from similarityMetrics_fun import *
from LookFiles import LookRegistrationFiles


def SingPxRegistWMetrics(root_path,Px):

    acctIMG_path, acctLM_path = LookRegistrationFiles(os.path.join(root_path, Px))
    PlanCT_img, ITV_img, PlanCTLM_img, ACCT_img, ACCTLM_img, PET_img = LookFilesResampled(os.path.join(root_path, Px))
    
    if len(acctLM_path)==0 or len(acctIMG_path)==0:
        SinglePxRegist(os.path.join(root_path, Px),"LungMaskRegistration")
        SinglePxRegist(os.path.join(root_path, Px),"CTRegistration")
        acctIMG_path, acctLM_path = LookRegistrationFiles(os.path.join(root_path, Px))

    acctIMG_img =sitk.ReadImage(acctIMG_path[0])
    acctLM_img =sitk.ReadImage(acctLM_path[0])

    img1_np = sitk.GetArrayViewFromImage(acctIMG_img)
    img2_np = sitk.GetArrayViewFromImage(PlanCT_img)
    itv_np =  sitk.GetArrayViewFromImage(ITV_img)
    mutual_avg,ssim_avg,cross_avg = similarMetrics_axial(img1_np,img2_np,itv_np)
    print("CTCT Axial: {:.2f}, {:.2f}, {:.2f}".format(mutual_avg, ssim_avg, cross_avg))
    mutual_avg,ssim_avg,cross_avg = similarMetrics_coronal(img1_np,img2_np,itv_np)
    print("CTCT Coronal {:.2f}, {:.2f}, {:.2f}".format(mutual_avg, ssim_avg, cross_avg))
    mutual_avg,ssim_avg,cross_avg = similarMetrics_sagital(img1_np,img2_np,itv_np)
    print("CTCT Sagital {:.2f}, {:.2f}, {:.2f}".format(mutual_avg, ssim_avg, cross_avg))

    img1_np = sitk.GetArrayViewFromImage(acctLM_img)
    mutual_avg,ssim_avg,cross_avg = similarMetrics_axial(img1_np,img2_np,itv_np)
    print("LMLM Axial {:.2f}, {:.2f}, {:.2f}".format(mutual_avg, ssim_avg, cross_avg))
    mutual_avg,ssim_avg,cross_avg = similarMetrics_coronal(img1_np,img2_np,itv_np)
    print("LMLM Coronal {:.2f}, {:.2f}, {:.2f}".format(mutual_avg, ssim_avg, cross_avg))
    mutual_avg,ssim_avg,cross_avg = similarMetrics_sagital(img1_np,img2_np,itv_np)
    print("LMLM Sagital {:.2f}, {:.2f}, {:.2f}".format(mutual_avg, ssim_avg, cross_avg))
    return 0