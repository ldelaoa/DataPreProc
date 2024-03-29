import nibabel as nib
import os

def CreateToTfromPandN(gtvP_path,gtvN_path):
    imgP = nib.load(gtvP_path)
    dataP = imgP.get_fdata()
    if gtvN_path ==None:
        merged_data = dataP
    else:
        imgN = nib.load(gtvN_path)
        dataN = imgN.get_fdata()
        # Ensure the images have the same shape
        assert imgP.shape == imgN.shape, "Images do not have the same shape."
        # Merge
        merged_data = dataP + dataN
    # Save the new image
    parent_dir = os.path.dirname(gtvP_path)
    output_file = os.path.join(parent_dir,'GTV_deform_made.nii.gz')
    merged_img = nib.Nifti1Image(merged_data, imgP.affine, imgP.header)
    #nib.save(merged_img, output_file)  
    
    return merged_img