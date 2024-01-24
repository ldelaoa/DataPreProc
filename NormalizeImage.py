import SimpleITK as sitk


def NormalizeImage(image,intFlag,saveFilename):
    desired_spacing = (2, 2, 4)
    currDirection = image.GetDirection()
    if currDirection[4] == -1:
        image = sitk.Flip(image,(False, True, False))
    current_spacing = image.GetSpacing()

    # Calculate the resampling factor
    resampling_factor = [current_spacing[i] / desired_spacing[i] for i in range(image.GetDimension())]
    # Calculate the new size based on the resampling factor
    new_size = [int(image.GetSize()[i] * resampling_factor[i]) for i in range(image.GetDimension())]

    # Create a resampler
    resampler = sitk.ResampleImageFilter()
    resampler.SetSize(new_size)
    resampler.SetOutputSpacing(desired_spacing)
    resampler.SetOutputOrigin(image.GetOrigin())
    resampled_image = resampler.Execute(image)

    sitk.WriteImage(resampled_image,saveFilename)

    return resampled_image


    #if intFlag :
    #    resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    #else:
    #    resampler.SetInterpolator(sitk.sitkLinear)