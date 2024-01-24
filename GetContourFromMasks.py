import numpy as np
import SimpleITK as sitk
import skimage


def create_contour_image(input_image):
    input_array = sitk.GetArrayFromImage(input_image)
    contour_image = np.zeros_like(input_array)

    for z in range(input_array.shape[1]):
        slice_image = np.copy(input_array[:, z,:])
        slice_image[slice_image==2]=0
        contours = skimage.measure.find_contours(slice_image, .5,fully_connected='high',positive_orientation='high')
        for contour in contours:
            contour = np.round(contour).astype(int)
            contour_image[contour[:, 0], z,contour[:, 1]] = 1

        slice_image2 = np.copy(input_array[:,  z,:])
        slice_image2[slice_image2==1] =0
        contours2 = skimage.measure.find_contours(slice_image2, 1, fully_connected='high', positive_orientation='high')
        for contour in contours2:
            contour = np.round(contour).astype(int)
            contour_image[contour[:, 0], z,contour[:, 1]] = 2

    contour_image_sitk = sitk.GetImageFromArray(contour_image)
    contour_image_sitk.SetOrigin(input_image.GetOrigin())
    contour_image_sitk.SetSpacing(input_image.GetSpacing())

    return contour_image_sitk