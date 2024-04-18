import os
import numpy as np
import yaml
import logging

def ReadTumorLabels():
    with open('TumorLabels.yaml','r') as stream:
        config = yaml.safe_load(stream)

        itvtot_labels = config['itv_tot_labels']
        itvtum_labels= config['itv_tumor_labels_withCreated']#['itv_tumor_labels']
        itvnod_labels = config['itv_ln_labels_withCreated']

        gtvtot_labels = config['gtv_tot_labels']
        gtvtum_labels = config['gtv_tumor_labels_withCreated']
        gtvnod_labels = config['gtv_ln_labels_withCreated']

    return itvtot_labels,itvtum_labels,itvnod_labels,gtvtot_labels,gtvtum_labels,gtvnod_labels


def BPLabels():
    bPTags= {"0%":["t0","100_ex","delay_0","qr40_s3_0","_0_imar"], 
             "10%":["t10","90_ex","delay_10","qr40_s3_10","_10_imar"], 
             "20%":["t20","60_ex","delay_20","qr40_s3_20","_20_imar"], 
             "30%":["t30","delay_30","qr40_s3_30","_30_imar"], 
             "40%":["t40","30_ex","delay_40","qr40_s3_40","_40_imar"], 
             "50%":["t50","5_ex","_1_ex","_2_ex","_3_ex","_4_ex","_8_ex","delay_50","qr40_s3_50","_50_imar"], 
             "60%":["t60","0_ex","0_in","delay_60","qr40_s3_60","_60_imar"], 
             "70%":["t70","40_in","delay_70","qr40_s3_70","_70_imar"], 
             "80%":["t80","60_in","delay_80","qr40_s3_80","_80_imar"], 
             "90%":["t90","90_in","95_in","94_in","delay_90","qr40_s3_90"], 
             "100%":["t100","100_in","98_in","delay_100","qr40_s3_100"]}

    return bPTags

def LookFilesNiiRaw(folder,logger):
    acct_path, PET_path, = ([],[])
    planct_path = []
    itvTot,itvTumor,itvNodes = ([],[],[])
    gtvTot,gtvTumor,gtvNodes = ([],[],[])

    bp0,bp10,bp20,bp30,bp40,bp50,bp60,bp70,bp80,bp90,bp100 = ([],[],[],[],[],[],[],[],[],[],[])

    itvtot_labels,itvtum_labels,itvnod_labels,gtvtot_labels,gtvtum_labels,gtvnod_labels = ReadTumorLabels()
    bp_Tags = BPLabels()
    totalFiles = []
    for root,dirs,files in os.walk(folder):
        for f in files:
            totalFiles.append(f)
            if "PET" in f and "resampled" not in f and "cropped" not in f and "registered" not in f.lower():
                PET_path.append(os.path.join(root, f))
            if "AC_CT_Body" in f or "CT van PET" in f or "CT LD" in f or "AC CT" in f or "AC  CT" in f and "registered" not in f.lower():
                acct_path.append(os.path.join(root, f))
            
            
            #if "trigger_delay" not in f.lower() and("thorax" in f.lower() or "ave" in f.lower() or "mip" in f.lower()): planct_path.append(os.path.join(root,f))
            if "thorax_3mm" in f.lower() or "thorax_2mm" in f.lower() or "ave" in f.lower() or "mip" in f.lower(): planct_path.append(os.path.join(root,f))

            if any(label_tt in f for label_tt in itvtot_labels): itvTot.append(os.path.join(root,f))
            if any(label_tt in f for label_tt in itvtum_labels): itvTumor.append(os.path.join(root,f))
            if any(label_tt in f for label_tt in itvnod_labels): itvNodes.append(os.path.join(root,f))
            
            if any(label_tt in f for label_tt in gtvtot_labels) and "igtv" not in f.lower(): gtvTot.append(os.path.join(root,f))
            if any(label_tt in f for label_tt in gtvtum_labels) and "igtv" not in f.lower(): gtvTumor.append(os.path.join(root,f))
            if any(label_tt in f for label_tt in gtvnod_labels) and "igtv" not in f.lower(): gtvNodes.append(os.path.join(root,f))

            if any(bpTags_tt in f.lower() for bpTags_tt in bp_Tags['0%']): bp0.append(os.path.join(root, f))
            if any(bpTags_tt in f.lower() for bpTags_tt in bp_Tags['10%']): bp10.append(os.path.join(root, f))
            if any(bpTags_tt in f.lower() for bpTags_tt in bp_Tags['20%']): bp20.append(os.path.join(root, f))
            if any(bpTags_tt in f.lower() for bpTags_tt in bp_Tags['30%']): bp30.append(os.path.join(root, f))
            if any(bpTags_tt in f.lower() for bpTags_tt in bp_Tags['40%']): bp40.append(os.path.join(root, f))
            if any(bpTags_tt in f.lower() for bpTags_tt in bp_Tags['50%']): bp50.append(os.path.join(root, f))
            if any(bpTags_tt in f.lower() for bpTags_tt in bp_Tags['60%']): bp60.append(os.path.join(root, f))
            if any(bpTags_tt in f.lower() for bpTags_tt in bp_Tags['70%']): bp70.append(os.path.join(root, f))
            if any(bpTags_tt in f.lower() for bpTags_tt in bp_Tags['80%']): bp80.append(os.path.join(root, f))
            if any(bpTags_tt in f.lower() for bpTags_tt in bp_Tags['90%']): bp90.append(os.path.join(root, f))
            if any(bpTags_tt in f.lower() for bpTags_tt in bp_Tags['100%']): bp100.append(os.path.join(root, f))
    if False:
        print("ACCT",len(acct_path),"PET",len(PET_path))
        print("PlanCT",len(planct_path))
        print("ITVtot",len(itvTot),"ITVtum",len(itvTumor),"ITVnod",len(itvNodes))
        print("GTVtot",len(gtvTot),"GTVtum",len(gtvTumor),"GTVnod",len(gtvNodes))
        print("BP0",len(bp0),"bp10",len(bp10),"bp20",len(bp20),"bp30",len(bp30),"bp40",len(bp40))
        print("BP50",len(bp50),"bp60",len(bp60),"bp70",len(bp70),"bp80",len(bp80),"bp90",len(bp90),"bp100",len(bp100))
        print("Total Files in Px Folder",len(totalFiles))
    if False:
        logger.info("ACCT"+str(len(acct_path))+"PET"+str(len(PET_path)))
        logger.info("PlanCT"+str(len(planct_path)))
        logger.info("ITVtot"+str(len(itvTot))+"ITVtum"+str(len(itvTumor))+"ITVnod"+str(len(itvNodes)))
        logger.info("GTVtot"+str(len(gtvTot))+"GTVtum"+str(len(gtvTumor))+"GTVnod"+str(len(gtvNodes)))
        logger.info("BP0"+str(len(bp0))+"bp10"+str(len(bp10))+"bp20"+str(len(bp20))+"bp30"+str(len(bp30))+"bp40"+str(len(bp40)))
        logger.info("BP50"+str(len(bp50))+"bp60"+str(len(bp60))+"bp70"+str(len(bp70))+"bp80"+str(len(bp80))+"bp90"+str(len(bp90))+"bp100"+str(len(bp100)))
        logger.info("Total Files in Px Folder"+str(len(totalFiles)))

    return acct_path, PET_path,planct_path,itvTot,itvTumor,itvNodes,gtvTot,gtvTumor,gtvNodes,bp0,bp10,bp20,bp30,bp40,bp50,bp60,bp70,bp80,bp90,bp100



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


def LookFiles_DEPRECATED(folder):
    acct_path, PET_path, planct_path, itv_path = ([],[],[],[])
    acct_pathLM , planct_pathLM = [],[]
    for root,dirs,files in os.walk(folder):
        for f in files:
            if ("%" in f or "thorax" in f.lower() or "ave" in f.lower() or "mip" in f.lower()) or ("ct" in f.lower() and not "ac_ct" in f.lower() and not "RTSTRUCT" in f and not "lungmask" in f.lower() and not "CORRECTED" in f and not "resampled" in f and not "cropped"in f and not "registered" in f.lower() and not "ac ct" in f.lower() and not "ac_ct" in f.lower() and not "ld wb" in f.lower() and not "wb ld" in f.lower() and not "ac  ct" in f.lower()):
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
    if len(planct_path)>1:
        print("PlanCTs",planct_path)
    return acct_path,acct_pathLM,PET_path,planct_path,planct_pathLM,itv_path
