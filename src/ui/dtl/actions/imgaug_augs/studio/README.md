# ImgAugStudio

`ImgAugStudio` layer is a wrapper around great [ImgAug Library](https://github.com/aleju/imgaug). It helps you build augmentation pipelines with ease.

Only labels of types `Polygon`, `Rectangle` and `Bitmap` in supervisely format can be converted automatically to imgaug format (and vice versa).

<details>
  <summary><b>List of supported augmentations</b></summary>

```python
{
    "arithmetic": [
        arithmetic.Add,
        arithmetic.AddElementwise,
        arithmetic.AdditiveGaussianNoise,
        arithmetic.AdditiveLaplaceNoise,
        arithmetic.AdditivePoissonNoise,
        arithmetic.Multiply,
        arithmetic.MultiplyElementwise,
        arithmetic.Cutout,
        arithmetic.Dropout,
        arithmetic.CoarseDropout,
        arithmetic.Dropout2d,
        arithmetic.ImpulseNoise,
        arithmetic.SaltAndPepper,
        arithmetic.CoarseSaltAndPepper,
        arithmetic.Salt,
        arithmetic.CoarseSalt,
        arithmetic.Pepper,
        arithmetic.CoarsePepper,
        arithmetic.Invert,
        arithmetic.Solarize,
        arithmetic.ContrastNormalization,
        arithmetic.JpegCompression,
    ],
    "blur": [
        blur.GaussianBlur,
        blur.AverageBlur,
        blur.MedianBlur,
        blur.BilateralBlur,
        blur.MotionBlur,
        blur.MeanShiftBlur,
    ],
    "color": [
        color.MultiplyAndAddToBrightness,
        color.MultiplyBrightness,
        color.AddToBrightness,
        color.MultiplyHueAndSaturation,
        color.MultiplyHue,
        color.MultiplySaturation,
        color.RemoveSaturation,
        color.AddToHueAndSaturation,
        color.AddToHue,
        color.AddToSaturation,
        color.Grayscale,
        color.ChangeColorTemperature,
        color.KMeansColorQuantization,
        color.UniformColorQuantization,
        color.Posterize,
    ],
    "contrast": [
        contrast.GammaContrast,
        contrast.SigmoidContrast,
        contrast.LogContrast,
        contrast.LinearContrast,
        contrast.AllChannelsHistogramEqualization,
        contrast.HistogramEqualization,
        contrast.AllChannelsCLAHE,
        contrast.CLAHE,
    ],
    "convolutional": [
        convolutional.Sharpen,
        convolutional.Emboss,
        convolutional.EdgeDetect,
        convolutional.DirectedEdgeDetect,
    ],
    "flip": [
        flip.Fliplr,
        flip.Flipud,
    ],
    "geometric": [
        geometric.ScaleX,
        geometric.ScaleY,
        geometric.TranslateX,
        geometric.TranslateY,
        geometric.Rotate,
        geometric.ShearX,
        geometric.ShearY,
        geometric.PiecewiseAffine,
        geometric.PerspectiveTransform,
        geometric.ElasticTransformation,
        geometric.Rot90,
    ],
    "imgcorruptlike": [
        imgcorruptlike.GaussianNoise,
        imgcorruptlike.ShotNoise,
        imgcorruptlike.ImpulseNoise,
        imgcorruptlike.SpeckleNoise,
        imgcorruptlike.GaussianBlur,
        imgcorruptlike.GlassBlur,
        imgcorruptlike.DefocusBlur,
        imgcorruptlike.MotionBlur,
        imgcorruptlike.ZoomBlur,
        imgcorruptlike.Fog,
        imgcorruptlike.Frost,
        imgcorruptlike.Snow,
        imgcorruptlike.Spatter,
        imgcorruptlike.Contrast,
        imgcorruptlike.Brightness,
        imgcorruptlike.Saturate,
        imgcorruptlike.JpegCompression,
        imgcorruptlike.Pixelate,
    ],
    "pillike": [
        pillike.Solarize,
        pillike.Equalize,
        pillike.Autocontrast,
        pillike.EnhanceColor,
        pillike.EnhanceContrast,
        pillike.EnhanceBrightness,
        pillike.EnhanceSharpness,
        pillike.FilterBlur,
        pillike.FilterSmooth,
        pillike.FilterSmoothMore,
        pillike.FilterEdgeEnhance,
        pillike.FilterEdgeEnhanceMore,
        pillike.FilterFindEdges,
        pillike.FilterContour,
        pillike.FilterEmboss,
        pillike.FilterSharpen,
        pillike.FilterDetail,
    ],
    "segmentation": [
        segmentation.Superpixels,
        segmentation.UniformVoronoi,
        segmentation.RegularGridVoronoi,
        segmentation.RelativeRegularGridVoronoi,
    ],
}
```

</details>

### Annotation augmentation

At the current moment, layer only augments `Masks`, `Bounding Boxes` and `Polygons`. `Polygons` are being converted to `Masks` for better annotation precision. We plan on adding support for those labels in the following versions.


### Settings:

- **Category** - Augmentation category. Select one of the aug categories: `arithmetic`, `blur`, `color`, `contrast`, `convolutional`, `flip`, `geometric`, `imgcorruptlike`, `pillike`, `segmentation`.
- **Method** - Augmentation method. Select one of the methods from the selected category.
- **Parameters** - Augmentation parameters. Each method has its own set of parameters. You can find the full list of parameters in the [ImgAug documentation](https://imgaug.readthedocs.io/en/latest/source/overview_of_augmenters.html).

### Example. Transform the image

In this example, the image is transformed with alpha (0, 70), sigma (4, 6).

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Elastic Transformation</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/a44c195b-1e81-4bab-9435-0271bd3c6741" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/ee0c3838-3392-4d21-8dd4-8e373e746510" alt="Elastic Transformation" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
"action": "elastic_transformation",
		"src": [
			"$images_project_1"
		],
		"dst": "$elastic_transformation_2",
		"settings": {
			"alpha": {
				"min": 0,
				"max": 70
			},
			"sigma": {
				"min": 4,
				"max": 6
			},
			"classes_mapping": {
				"neutral": "neutral",
				"person_poly": "person_poly"
			}
		}
}
</pre>
</details>

# Acknowledgements

This layer is based on the great work of `ImgAug` ([github](https://github.com/aleju/imgaug)). ![GitHub Org's stars](https://img.shields.io/github/stars/aleju/imgaug?style=social)
