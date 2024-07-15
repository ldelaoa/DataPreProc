import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import os
from skimage.measure import label, regionprops

def Screenshot(ct_np, gtv_np, centroids, Px2Save=None, ImageType=None, root2save=None):
    dpi_val = 50
    
    if Px2Save is not None and root2save is not None:
        pathToSave = os.path.join(root2save,"JPEGs_Test_pt2", Px2Save)
        os.makedirs(pathToSave, exist_ok=True)
    else:
        raise ValueError("Px2Save and root2save must be provided")
    
    middle_x, middle_y, middle_z = centroids
    middle_x = np.round(middle_x).astype(int)
    middle_y = np.round(middle_y).astype(int)
    middle_z = np.round(middle_z).astype(int)
    
    plt.figure(figsize=(15, 15))
    plt.imshow(np.rot90(ct_np[middle_x, :, :]), cmap='gray')
    plt.axis('off')
    plt.contour(np.rot90(gtv_np[middle_x, :, :]), linewidths=1, colors='r')
    plt.savefig(os.path.join(pathToSave, f"{ImageType}_Coronal.jpeg"), dpi=dpi_val)
    plt.close()

    plt.figure(figsize=(15, 15), dpi=dpi_val)
    plt.imshow(np.rot90(ct_np[:, middle_y, :]), cmap='gray')
    plt.axis('off')
    plt.contour(np.rot90(gtv_np[:, middle_y, :]), linewidths=1, colors='r')
    plt.savefig(os.path.join(pathToSave, f"{ImageType}_Sagital.jpeg"), dpi=dpi_val)
    plt.close()

    plt.figure(figsize=(15, 15), dpi=dpi_val)
    plt.imshow(ct_np[:, :, middle_z], cmap='gray')
    plt.axis('off')
    plt.contour(gtv_np[:, :, middle_z], linewidths=1, colors='r')
    plt.savefig(os.path.join(pathToSave, f"{ImageType}_Axial.jpeg"), dpi=dpi_val)
    plt.close()

    return 0
