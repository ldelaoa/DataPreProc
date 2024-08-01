import SimpleITK as sitk


def NormalizeImage(image,intFlag=None,saveFilename=None,originReference=None,desired_spacing = None,desired_Size = None):    

    currDirection = image.GetDirection()
    if currDirection[4] == -1:
        image = sitk.Flip(image,(False, True, False))
    
    resampler = sitk.ResampleImageFilter()


    if desired_spacing is not None:
        current_spacing = image.GetSpacing()
        resampling_factor = [current_spacing[i] / desired_spacing[i] for i in range(image.GetDimension())]
        new_size = [int(image.GetSize()[i] * resampling_factor[i]) for i in range(image.GetDimension())]    
        resampler.SetSize(new_size)
        resampler.SetOutputSpacing(desired_spacing)
        #print("Change Spacing",desired_spacing)
    elif desired_Size is not None:
        spacing_ratio = [sz1/sz2 for sz1, sz2 in zip(image.GetSize(), desired_Size)]
        new_spacing = [sz * ratio for sz, ratio in zip(image.GetSpacing(), spacing_ratio)]
        resampler.SetSize(desired_Size)
        resampler.SetOutputSpacing(new_spacing)
        #print("Changing Size",desired_Size)
    else:
        resampler.SetSize(image.GetSize())
        resampler.SetOutputSpacing(image.GetSpacing())
    
    if originReference is None:
        resampler.SetOutputOrigin(image.GetOrigin())
    else:
        resampler.SetOutputOrigin(originReference)
        #print("Change Origin",originReference)

    if intFlag=="NN":
        resampler.SetInterpolator(sitk.sitkLabelGaussian)
    #else:
    #    resampler.SetInterpolator(sitk.sitkBSpline)

    if saveFilename is not None:
        sitk.WriteImage(resampled_image,saveFilename)

    resampled_image = resampler.Execute(image)
    del image
    return resampled_image
