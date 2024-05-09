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
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/c589730f-4dfd-4640-b6d3-265d704d9c92" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/40677182-e110-4be4-b333-819e2b389806" alt="Elastic Transform" /> </td>
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
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/c589730f-4dfd-4640-b6d3-265d704d9c92" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/1a2f49c4-7f32-436f-a2fe-a55360dedec0" alt="Pixelated" /> </td>
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
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/c589730f-4dfd-4640-b6d3-265d704d9c92" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/40677182-e110-4be4-b333-819e2b389806" alt="Elastic Transform" /> </td>
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
