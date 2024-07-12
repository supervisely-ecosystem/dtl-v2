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
- **Random order** - If enabled, the augmentations will be applied in a random order. If disabled, the augmentations will be applied in the order they are listed in the pipeline.

## Example. Transform the image

The ImgAug Studio allows for unlimited combinations of different augmentations, in the examples below you can see the combination of two augmentation methods per 3 categories (the parameters can be seen in the JSON view)

### Iaa.Arithmetic: Add + ImpulseNoise

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Augmented</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/user-attachments/assets/b107d22f-2f0e-4558-b73f-3de08c4740cc" alt="Original image" /> </td>
<td> <img src="https://github.com/user-attachments/assets/ec01a485-ea16-4cfb-87df-17b1a6466134" alt="Augmented" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "imgaug_studio",
    "src": {"source": ["$images_project_1"]},
    "dst": "$imgaug_studio_2",
    "settings": {
        "pipeline": [
            {
                "category": "arithmetic",
                "name": "Add",
                "params": {"value": [111, 138], "per_channel": false},
                "sometimes": null,
                "python": "iaa.Add(value=[111, 138], per_channel=False)"
            },
            {
                "category": "arithmetic",
                "name": "ImpulseNoise",
                "params": {"p": [0, 0.03]},
                "sometimes": null,
                "python": "iaa.ImpulseNoise(p=[0, 0.03])",
            }
        ],
        "shuffle": false
    },
    "scene_location": {
        "order_idx": 1,
        "position": {"x": 540, "y": 140}
    }
}
</pre>
</details>

### Iaa.Geometric: ScaleX + ShearY

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Augmented</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/user-attachments/assets/02c12a33-a3ab-4463-8c81-c2191734b860" alt="Original image" /> </td>
<td> <img src="https://github.com/user-attachments/assets/2836502f-4349-4287-a386-d4e85eee4fcc" alt="Augmented" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "imgaug_studio",
    "src": {"source": ["$images_project_1"]},
    "dst": "$imgaug_studio_2",
    "settings": {
        "pipeline": [
            {
                "category": "geometric",
                "name": "ScaleX",
                "params": {
                    "scale": [
                        0.5,
                        1.5
                    ],
                    "order": 1,
                    "cval": 0,
                    "mode": "constant",
                    "fit_output": false
                },
                "sometimes": null,
                "python": "iaa.ScaleX(scale=[0.5, 1.5], order=1, cval=0, mode='constant', fit_output=False)",
            },
            {
                "category": "geometric",
                "name": "ShearY",
                "params": {
                    "shear": [-30, 30],
                    "order": 1,
                    "cval": 0,
                    "mode": "constant",
                    "fit_output": false
                },
                "sometimes": null,
                "python": "iaa.ShearY(shear=[-30, 30], order=1, cval=0, mode='constant', fit_output=False)",
            }
        ],
        "shuffle": false
    },
    "scene_location": {
        "order_idx": 1,
        "position": {"x": 540, "y": 140}
    }
}
</pre>
</details>

### Iaa.Piilike: Solarize + Equalize

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Augmented</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/user-attachments/assets/c920ef8b-81a6-435c-b684-2a649fae378e" alt="Original image" /> </td>
<td> <img src="https://github.com/user-attachments/assets/5e0cd31a-5395-4039-b2b3-e2e4394c42af" alt="Augmented" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "imgaug_studio",
    "src": {"source": ["$images_project_1"]},
    "dst": "$imgaug_studio_2",
    "settings": {
        "pipeline": [
            {
                "category": "pillike",
                "name": "Solarize",
                "params": {"p": 1, "threshold": [32, 128]},
                "sometimes": null,
                "python": "iaa.Solarize(p=1, threshold=[32, 128])",
            },
            {
                "category": "pillike",
                "name": "Equalize",
                "params": {},
                "sometimes": null,
                "python": "iaa.Equalize()",
            }
        ],
        "shuffle": false
    },
    "scene_location": {
        "order_idx": 1,
        "position": {"x": 540, "y": 140}
    }
}
</pre>
</details>

# Acknowledgements

This layer is based on the great work of `ImgAug` ([github](https://github.com/aleju/imgaug)). ![GitHub Org's stars](https://img.shields.io/github/stars/aleju/imgaug?style=social)
