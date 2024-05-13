# ImgAug.ImageCorruptlike Compression

This layer contains set of ImgAug's image augmentations related to compression. Annotations are not being augmented.

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
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/894e0c45-44c9-4c67-9d9f-11cd5654fc90" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/6f889dd6-4c8d-43ae-80f2-29be5ebf0aad" alt="Pixelated" /> </td>
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
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/894e0c45-44c9-4c67-9d9f-11cd5654fc90" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/9f31bc1d-6d75-47cc-8377-2a3076bfaeeb" alt="Elastic Transform" /> </td>
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
