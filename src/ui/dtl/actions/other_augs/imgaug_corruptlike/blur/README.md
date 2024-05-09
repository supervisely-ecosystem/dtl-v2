# ImgAug.ImageCorruptlike Blur

This layer contains set of ImgAug's image augmentations related to blur. Annotations are not being augmented.

### Settings:

- **Augmentation option** - Select desired blur augmentation. Can be set to `Defocus Blur`, `Motion Blur` and `Zoom Blur`

- **Severity** - Set value to specify the transformation intensity. Goes from 1 to 5.

Below you can see examples and json views for each augmentation option.

## Defocus Blur

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Defocus Blur: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="xxx" alt="Original image" /> </td>
<td> <img src="xxx" alt="Defocus Blur" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_blur",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_blur_5",
    "settings": {
        "option": "defocus_blur",
        "severity": 5
    }
}
</pre>
</details>

## Motion Blur
<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Motion Blur: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="xxx" alt="Original image" /> </td>
<td> <img src="xxx" alt="Motion Blur" /> </td>
</tr>
</table>


<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_blur",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_blur_5",
    "settings": {
        "option": "motion_blur",
        "severity": 5
    }
}
</pre>
</details>

## Zoom Blur


<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Zoom Blur: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="xxx" alt="Original image" /> </td>
<td> <img src="xxx" alt="Zoom Blur" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_blur",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_blur_5",
    "settings": {
        "option": "zoom_blur",
        "severity": 5
    }
}
</pre>
</details>

# Acknowledgements

This layer is based on the great work of `ImgAug` ([github](https://github.com/aleju/imgaug)). ![GitHub Org's stars](https://img.shields.io/github/stars/aleju/imgaug?style=social)
