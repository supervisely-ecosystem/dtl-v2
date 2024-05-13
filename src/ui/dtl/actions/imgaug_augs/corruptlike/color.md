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
<td style="text-align:center; width:50%"><strong>Contrast: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/894e0c45-44c9-4c67-9d9f-11cd5654fc90" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/6283435f-d610-4c44-af7c-0326f4b8d027" alt="Contrast" /> </td>
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
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/894e0c45-44c9-4c67-9d9f-11cd5654fc90" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/8773dde8-ebcd-43e2-986b-5764d2921044" alt="Brightness" /> </td>
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
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/894e0c45-44c9-4c67-9d9f-11cd5654fc90" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/bb70d2db-5830-41b2-b00d-b965db26e603" alt="Saturate" /> </td>
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
