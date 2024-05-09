# ImgAug.ImageCorruptlike Noise

This layer contains set of ImgAug's image augmentations related to noise. Annotations are not being augmented.

### Settings:

- **Augmentation option** - Select desired noise augmentation. Can be set to `Gaussian Noise`, `Shot Noise`, `Impulse Noise` and `Speckle Noise`

- **Severity** - Set value to specify the transformation intensity. Goes from 1 to 5.

Below you can see examples and json views for each augmentation option.

## Gaussian Noise

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Gaussian Noise: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="xxx" alt="Original image" /> </td>
<td> <img src="xxx" alt="Gaussian Noise" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_noise",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_noise_6",
    "settings": {
        "option": "gaussian_noise",
        "severity": 5
    }
}
</pre>
</details>

## Shot Noise
<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Shot Noise: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="xxx" alt="Original image" /> </td>
<td> <img src="xxx" alt="Shot Noise" /> </td>
</tr>
</table>


<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_noise",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_noise_6",
    "settings": {
        "option": "shot_noise",
        "severity": 5
    }
}
</pre>
</details>

## Impulse Noise
<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Impulse Noise: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="xxx" alt="Original image" /> </td>
<td> <img src="xxx" alt="Impulse Noise" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_noise",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_noise_6",
    "settings": {
        "option": "impulse_noise",
        "severity": 5
    }
}
</pre>
</details>

## Speckle Noise
<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Speckle Noise: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="xxx" alt="Original image" /> </td>
<td> <img src="xxx" alt="Speckle Noise" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "iaa_imgcorruptlike_noise",
    "src": [
        "$images_project_1"
    ],
    "dst": "$iaa_imgcorruptlike_noise_6",
    "settings": {
        "option": "speckle_noise",
        "severity": 5
    }
}
</pre>
</details>

# Acknowledgements

This layer is based on the great work of `ImgAug` ([github](https://github.com/aleju/imgaug)). ![GitHub Org's stars](https://img.shields.io/github/stars/aleju/imgaug?style=social)
