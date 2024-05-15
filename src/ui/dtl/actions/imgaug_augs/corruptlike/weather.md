# ImgAug.ImgCorruptlike Weather

This layer contains set of ImgAug's image augmentations related to weather. Annotations are not being augmented.

### Settings:

- **Augmentation option** - Select desired weather augmentation. Can be set to `Fog`, `Frost`, `Snow` and `Spatter`

- **Severity** - Set value to specify the transformation intensity. Goes from 1 to 5.

Below you can see examples and json views for each augmentation option.

## Fog

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Fog: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/894e0c45-44c9-4c67-9d9f-11cd5654fc90" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/b72facdd-8f97-46fe-a998-f0d75f60b185" alt="Fog" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_weather",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_weather_7",
    "settings": {
        "option": "fog",
        "severity": 5
    }
}
</pre>
</details>

## Frost
<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Frost: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/894e0c45-44c9-4c67-9d9f-11cd5654fc90" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/d146a2a7-20e7-43a0-aaf1-13685286c1c1" alt="Frost" /> </td>
</tr>
</table>


<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_weather",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_weather_7",
    "settings": {
        "option": "Frost",
        "severity": 5
    }
}
</pre>
</details>

## Snow
<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Snow: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/894e0c45-44c9-4c67-9d9f-11cd5654fc90" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/d377be8b-81be-403f-8756-a5ca29f42c64" alt="Snow" /> </td>
</tr>   
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_weather",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_weather_7",
    "settings": {
        "option": "snow",
        "severity": 5
    }
}
</pre>
</details>

## Spatter
<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Spatter: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/894e0c45-44c9-4c67-9d9f-11cd5654fc90" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/300f1ed6-d32f-4b02-87d8-002f549503ff" alt="Spatter" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_weather",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_weather_7",
    "settings": {
        "option": "spatter",
        "severity": 5
    }
}
</pre>
</details>

# Acknowledgements

This layer is based on the great work of `ImgAug` ([github](https://github.com/aleju/imgaug)). ![GitHub Org's stars](https://img.shields.io/github/stars/aleju/imgaug?style=social)
