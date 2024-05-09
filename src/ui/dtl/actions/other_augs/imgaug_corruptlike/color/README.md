# ImgAug.ImageCorruptlike Color

This layer contains set of ImgAug's image augmentations related to color. Annotations are not being augmented.

### Settings:

- **Augmentation option** - Select desired color augmentation. Can be set to `Contrast`, `Brightness`, and `Saturate`

- **Severity** - Set value to specify the transformation intensity. Goes from 1 to 5.

Below you can see examples and json views for each augmentation option.

## Contrast

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Fog: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="xxx" alt="Original image" /> </td>
<td> <img src="xxx" alt="Fog" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_color",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_color_8",
    "settings": {
        "option": "contrast",
        "severity": 5
    }
}
</pre>
</details>

## Brightness
<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Brightness: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="xxx" alt="Original image" /> </td>
<td> <img src="xxx" alt="Brightness" /> </td>
</tr>
</table>


<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_color",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_color_8",
    "settings": {
        "option": "brightness",
        "severity": 5
    }
}
</pre>
</details>

## Saturate
<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Saturate: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="xxx" alt="Original image" /> </td>
<td> <img src="xxx" alt="Saturate" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_color",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_color_8",
    "settings": {
        "option": "saturate",
        "severity": 5
    }
}
</pre>
</details>

# Acknowledgements

This layer is based on the great work of `ImgAug` ([github](https://github.com/aleju/imgaug)). ![GitHub Org's stars](https://img.shields.io/github/stars/aleju/imgaug?style=social)
