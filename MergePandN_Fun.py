import nibabel as nib
import os
import numpy as np
    
def GetNames(list_of_paths):
    name_list = []
    if len(list_of_paths)>0: 
        for currstruct in list_of_paths:
            name_list.append(currstruct.split('\\')[-1].split('.')[0])
    return name_list

def CheckTwoLabelCategories(gtvTot,gtvTumor,gtvNodes,TumorType_str,logger):
    tot_name = GetNames(gtvTot)
    tumor_name  = GetNames(gtvTumor)
    nodes_name = GetNames(gtvNodes)

    if len(gtvTumor)>0 and len(gtvNodes)>0:
        return  gtvTumor,gtvNodes
    
    if len(gtvTumor)==0 and len(gtvNodes)>0:
        if len(gtvTot)==0:
            print("only nodes available, ERROR")
            logger.warning("only nodes available, ERROR")            
            return None,None
        if len(gtvTot)>0:
            #gtvTumor = gtvTot - gtvNodes
            print("gtvTumor = gtvTot - gtvNodes")
            logger.info("gtvTumor = gtvTot - gtvNodes")
            imgTot = nib.load(gtvTot[0]).get_fdata()
            imgNodes_nii = nib.load(gtvNodes[0])
            imgNod = imgNodes_nii.get_fdata()  
            imgTum = imgTot-imgNod
            parent_dir = os.path.dirname(gtvNodes[0])
            output_file = os.path.join(parent_dir,TumorType_str+'p_created.nii.gz')                      
            merged_img = nib.Nifti1Image(imgTum, imgNodes_nii.affine, imgNodes_nii.header)
            nib.save(merged_img, output_file)
            return [output_file],gtvNodes
        
    if len(gtvTumor)==0 and len(gtvNodes)==0:
        if len(gtvTot)>0:
            #GTVp = GTVtot and GTVNodes = Blank
            print("GTVp = GTVtot and GTVNodes = Blank")
            logger.info("GTVp = GTVtot and GTVNodes = Blank")
            parent_dir = os.path.dirname(gtvTot[0])
            imgTot_nii = nib.load(gtvTot[0])
            imgTot = imgTot_nii.get_fdata()

            imgTum = np.copy(imgTot)
            output_file_tumor = os.path.join(parent_dir,TumorType_str+'p_created.nii.gz') 
            merged_img_tumor = nib.Nifti1Image(imgTum, imgTot_nii.affine, imgTot_nii.header)
            nib.save(merged_img_tumor, output_file_tumor)

            imgNodes = np.copy(imgTot)
            imgNodes[imgNodes>0] = 0
            output_file_nodes = os.path.join(parent_dir,TumorType_str+'n_created.nii.gz') 
            merged_img_nodes = nib.Nifti1Image(imgNodes, imgTot_nii.affine, imgTot_nii.header)
            nib.save(merged_img_nodes, output_file_nodes)
            print("Sum Created",TumorType_str,"p",np.sum(imgTum),"n",np.sum(imgNodes))
            return [output_file_tumor],[output_file_nodes]

        if len(gtvTot)==0:
            print("No tumor info")
            logger.warning("No tumor info")
            return None,None

    if len(gtvTumor)>0 and len(gtvNodes)==0:
        if len(gtvTot)>0:
            #gtvNodes = gtvTot-gtvTumor
            print("gtvNodes = gtvTot-gtvTumor")
            logger.info("gtvNodes = gtvTot-gtvTumor")
            imgTot = nib.load(gtvTot[0]).get_fdata()
            imgTum_nii = nib.load(gtvTumor[0])
            imgTum = imgTum_nii.get_fdata()  
            imgNod = imgTot-imgTum
            parent_dir = os.path.dirname(gtvTumor[0])
            output_file = os.path.join(parent_dir,TumorType_str+'n_created.nii.gz')                      
            merged_img = nib.Nifti1Image(imgNod, imgTum_nii.affine, imgTum_nii.header)
            nib.save(merged_img, output_file)
            return gtvTumor,[output_file]
        if len(gtvTot)==0:
            #gtvNodes = Blank
            print("gtvNodes = Blank")
            logger.info("gtvNodes = Blank")
            imgTum_nii = nib.load(gtvTumor[0])
            imgTum = imgTum_nii.get_fdata()  
            imgTum[imgTum>0] = 0
            imgNod = np.copy(imgTum)
            parent_dir = os.path.dirname(gtvTumor[0])
            output_file = os.path.join(parent_dir,TumorType_str+'n_created.nii.gz')                      
            merged_img = nib.Nifti1Image(imgNod, imgTum_nii.affine, imgTum_nii.header)
            nib.save(merged_img, output_file)
            return gtvTumor,[output_file]


