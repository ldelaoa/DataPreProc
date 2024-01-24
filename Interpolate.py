import SimpleITK as sitk


def interpolate_image(target_image, input_image,name):
    # Get the size, spacing, and origin of the target image
    target_size = target_image.GetSize()
    target_spacing = target_image.GetSpacing()
    target_origin = target_image.GetOrigin()

    # Create a resampler
    resampler = sitk.ResampleImageFilter()

    # Set the interpolator (e.g., linear interpolation)
    if name == "ACCT":
        resampler.SetInterpolator(sitk.sitkLinear)
    else:
        threshold_filter = sitk.BinaryThresholdImageFilter()
        threshold_filter.SetLowerThreshold(0.5)
        threshold_filter.SetUpperThreshold(2.5)
        threshold_filter.SetInsideValue(1)
        threshold_filter.SetOutsideValue(0)
        input_image = threshold_filter.Execute(input_image)
        resampler.SetInterpolator(sitk.sitkNearestNeighbor)

    # Set the size, spacing, and origin of the output image
    resampler.SetSize(target_size)
    resampler.SetOutputSpacing(target_spacing)
    resampler.SetOutputOrigin(target_origin)

    # Perform resampling
    output_image = resampler.Execute(input_image)

    return output_image