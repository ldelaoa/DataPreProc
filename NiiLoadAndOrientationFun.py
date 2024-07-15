
import nibabel as nib
from nibabel.orientations import aff2axcodes

#From path loads and returns nii
def NiiLoadAndOrientation(path2nii):
    ct00_nii  = nib.load(path2nii)
    target_orientation_CT = ('L','A','S') #(LPI)(RAS)
    originalOrient_CT = aff2axcodes(ct00_nii.affine)
    las_ornt = nib.orientations.axcodes2ornt('LAS')
    if not(originalOrient_CT == target_orientation_CT):
        ct00_data = ct00_nii.get_fdata()
        transformed_data = nib.orientations.apply_orientation(ct00_data, las_ornt)
        ct00_nii = nib.Nifti1Image(transformed_data, ct00_nii.affine, ct00_nii.header)
        #print("Reoriented")
    return ct00_nii