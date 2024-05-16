# iaa.Geometric Perspective Transform

`Perspective Transform` layer transforms images by applying ImgAug's Perspective Transform augmentation.

### Annotation augmentation

At the current moment, layer only augments `Masks`, `Bounding Boxes` and `Polygons`. `Polygons` are being converted to `Masks` for better annotation precision. We plan on adding support for those labels in the following versions.


### Settings:

- **Scale** Set minimum and maximum values to specify the strength of the displacement.
- **Keep image size** checkbox
- **Fit to output** check to see the full image with the black bars
- **cval** todo


### Example. Transform the image

In this example, the image is transformed with scale (0.04, 0.15), Fit to Output unchecked, Keep Image size checked, and cval 0.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Perspective Transform</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/d8641687-6e0b-4d37-9d05-80617b06ffa8" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/40d0cdac-37b4-46c3-8fb2-6f3e60266e53" alt="Perspective Transform" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
	"action": "perspective_transform",
	"src": [
		"$images_project_1"
	],
	"dst": "$perspective_transform_2",
	"settings": {
		"scale": {
			"min": 0.04,
			"max": 0.15
		},
		"classes_mapping": {},
		"size_box": {
			"keep": true,
			"fit": false
		},
		"cval": {
			"value": 0
		}
	}
</pre>
</details>

# Acknowledgements

This layer is based on the great work of `ImgAug` ([github](https://github.com/aleju/imgaug)). ![GitHub Org's stars](https://img.shields.io/github/stars/aleju/imgaug?style=social)

