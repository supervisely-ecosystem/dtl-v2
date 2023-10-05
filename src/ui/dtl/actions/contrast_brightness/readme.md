# Contrast and Brightness

`contrast_brightness` layer randomly changes contrast and brightness of images.

### Settings:

- **contrast** - Set `min` and `max` values for contrast. Image contrast is changed by multiplying each pixel by random value with uniform distribution from min to max. To center colors of images (subtract 128) first, set `center_grey` to `true`.
- **brightness** - Set `min` and `max` values for brightness. Image brightness is changed by adding to each pixel a random value with uniform distribution from min to max.


### Examples:

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Contrast: 6-8, center_grey: true</strong></td>
<td style="text-align:center"><strong>Brightness: 60-110</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/22476d1c-684b-4ce0-9675-ba5fc5b34370" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/ab6a60d8-56ac-4012-b4b1-168ef201a41c" alt="Contrast" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/ff1afc6e-94cf-4a3b-a414-7e345ec44057" alt="Brightness" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "contrast_brightness",
  "src": ["$data_5"],
  "dst": "$contrast_brightness_9",
  "settings": {
    "contrast": {
      "min": 6,
      "max": 8,
      "center_grey": true
    },
    "brightness": {
      "min": 60,
      "max": 110
    }
  }
}
</pre>
</details>