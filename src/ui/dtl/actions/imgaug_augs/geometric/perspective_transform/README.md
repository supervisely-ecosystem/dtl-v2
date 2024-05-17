# iaa.geometric.PerspectiveTransform

`PerspectiveTransform` layer applies random four point perspective transformations to images.

Each of the four points is placed on the image using a random distance from its respective corner. The distance is sampled from a normal distribution. As a result, most transformations don’t change the image very much, while some “focus” on polygons far inside the image.

[Read more about Perspective Transform in the ImgAug's documentation](https://imgaug.readthedocs.io/en/latest/source/api_augmenters_geometric.html#imgaug.augmenters.geometric.PerspectiveTransform)

### Annotation augmentation

At the current moment, layer only augments `Masks`, `Bounding Boxes` and `Polygons`. `Polygons` are being converted to `Masks` for better annotation precision. We plan on adding support for those labels in the following versions.


### Settings:

- **Scale** - Set minimum and maximum values to specify the strength of the perspective transformation.
- **Keep image size** - Whether to resize image’s back to their original size after applying the perspective transform. If set to False, the resulting images may end up having different shapes.
- **Fit to output** - If True, the image plane size and position will be adjusted to still capture the whole image after perspective transformation. (Followed by image resizing if keep_size is set to True.) Otherwise, parts of the transformed image may be outside of the image plane. This setting should not be set to True when using large scale values as it could lead to very large images.
- **cval** - The constant value used to fill up pixels in the result image that didn’t exist in the input image


### Example. Transform the image

In this example, the image is transformed with scale (0.04, 0.15), Fit Output unchecked and Keep Image size checked.

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

