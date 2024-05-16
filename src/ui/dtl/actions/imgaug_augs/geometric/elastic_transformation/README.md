# iaa.Geometric Elastic Transformation

`Elastic Transformation` layer transforms images by moving pixels locally around using displacement fields.

### Annotation augmentation

At the current moment, layer only augments `Masks`, `Bounding Boxes` and `Polygons`. `Polygons` are being converted to `Masks` for better annotation precision. We plan on adding support for those labels in the following versions.


### Settings:

- **Alpha** Set minimum and maximum values to specify the strength of the displacement.
- **Sigma** Set minimum and maximum values to specify the smoothness of the displacement.

A proportion of 10:1 between alpha and sigma (e.g. alpha=30, sigma=3 or alpha=70, sigma=7) seems work really well to achieve water-like effect.


### Example. Transform the image

In this example, the image is transformed with alpha (0, 70), sigma (4, 6).

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Elastic Transformation</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/a44c195b-1e81-4bab-9435-0271bd3c6741" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/ee0c3838-3392-4d21-8dd4-8e373e746510" alt="Elastic Transformation" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
"action": "elastic_transformation",
		"src": [
			"$images_project_1"
		],
		"dst": "$elastic_transformation_2",
		"settings": {
			"alpha": {
				"min": 0,
				"max": 70
			},
			"sigma": {
				"min": 4,
				"max": 6
			},
			"classes_mapping": {
				"neutral": "neutral",
				"person_poly": "person_poly"
			}
		}
}
</pre>
</details>

# Acknowledgements

This layer is based on the great work of `ImgAug` ([github](https://github.com/aleju/imgaug)). ![GitHub Org's stars](https://img.shields.io/github/stars/aleju/imgaug?style=social)

