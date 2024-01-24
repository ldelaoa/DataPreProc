import os


def LookFiles(folder):
    acct_path, PET_path, planct_path, itv_path = ([],[],[],[])
    acct_pathLM , planct_pathLM = [],[]
    for root,dirs,files in os.walk(folder):
        for f in files:
            if "%" in f or "thorax" in f.lower() or "ave" in f.lower() or "mip" in f.lower() or ("ct" in f.lower() and "ac_ct" not in f.lower() and "RTSTRUCT" not in f and "lungmask" not in f.lower() and "CORRECTED" not in f and "resampled" not in f and "cropped" not in f and "registered" not in f.lower() and "ac ct" not in f.lower() and "ac_ct" not in f.lower()):
                planct_path.append(os.path.join(folder,f))
            if "AC_CT_Body" in f or "CT van PET" in f or "CT LD" in f or "AC CT" in f or "AC  CT" in f and "registered" not in f.lower():
                acct_path.append(os.path.join(folder, f))
            if "PlanCT_lungMask" in f and "resampled" not in f and "cropped" not in f and "registered" not in f.lower():
                planct_pathLM.append(os.path.join(folder, f))
            if "ACCT_lungMask" in f and "resampled" not in f and "cropped" not in f and "registered" not in f.lower():
                acct_pathLM.append(os.path.join(folder, f))
            if "PET" in f and "resampled" not in f and "cropped" not in f and "registered" not in f.lower():
                PET_path.append(os.path.join(folder, f))
            if "ITV" in f and "resampled" not in f and "cropped" not in f and "registered" not in f.lower():
                itv_path.append(os.path.join(folder, f))



    print("ACCT",len(acct_path),"ACCT_LM",len(acct_pathLM),"PET",len(PET_path),"PlanCT",len(planct_path),"PlanCT_LM",len(planct_pathLM),"ITV",len(itv_path))
    return acct_path,acct_pathLM,PET_path,planct_path,planct_pathLM,itv_path



def LookRegistrationFiles(folder):
    acctIMG_path, acctLM_path, = ([],[])
    for root,dirs,files in os.walk(folder):
        for f in files:
            if "ACCT_IMGregistered4.nii" in f:
                acctIMG_path.append(os.path.join(folder,f))
            if "ACCT_LMregistered4.nii" in f:
                acctLM_path.append(os.path.join(folder, f))

    print("ACCTr img",len(acctIMG_path),"ACCTr LM",len(acctLM_path))
    return acctIMG_path, acctLM_path

