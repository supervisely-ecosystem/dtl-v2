# ImgAug.ImgCorruptlike Compression

This layer contains set of ImgAug's image augmentations related to compression. Annotations are not being augmented.

[Learn more about ImgAug's Corruptlike augmenters in their documentation](https://imgaug.readthedocs.io/en/latest/source/api_augmenters_imgcorruptlike.html)

### Settings:

- **Augmentation option** - Select desired compression augmentation. Can be set to `JPEG Compression`, `Pixelate` and `Elastic Transform`

- **Severity** - Set value to specify the transformation intensity. Goes from 1 to 5.

Below you can see examples and json views for each augmentation option.

## JPEG Compression

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>JPEG Compression: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/894e0c45-44c9-4c67-9d9f-11cd5654fc90" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/a92f6184-998a-4dd0-9a0c-867c82544bc4" alt="JPEG" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_compression",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_compression_4",
    "settings": {
        "option": "jpeg_compression",
        "severity": 5
    }
}
</pre>
</details>

## Pixelate

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Pixelated: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/9126c6e6-8dd0-4bd6-b968-78f7dbcefe7e" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/9ddcf069-8715-42f7-a0d1-3e8291e436d9" alt="Pixelated" /> </td>
</tr>
</table>


<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_compression",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_compression_4",
    "settings": {
        "option": "pixelate",
        "severity": 5
    }
}
</pre>
</details>

## Elastic Transform


<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Elastic Transform: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/f85b7a80-f499-45a3-9d4c-7b9532facd97" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/5ba8a608-05eb-4839-98bc-261f00d9788e" alt="Elastic Transform" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_compression",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_compression_4",
    "settings": {
        "option": "elastic_transform",
        "severity": 5
    }
}
</pre>
</details>

# Acknowledgements

This layer is based on the great work of `ImgAug` ([github](https://github.com/aleju/imgaug)). ![GitHub Org's stars](https://img.shields.io/github/stars/aleju/imgaug?style=social)
