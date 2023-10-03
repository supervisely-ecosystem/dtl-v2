# Contrast and Brightness

`contrast_brightness` layer randomly changes contrast and brightness of images.

### Settings:

- **Contrast (optional)**:
  - min (type: _float_, minimum: 0, maximum: 10)
  - max (type: _float_, minimum: 0, maximum: 10)
  - center_grey (type: boolean, default: false)
- **Brightness (optional)**:
  - min (type: _float_, minimum: -255, maximum: 255)
  - max (type: _float_, minimum: -255, maximum: 255)

### Examples:

#### Contrast: 6-8, center_grey: true, Brightness: 0-0

Json config example:

```json
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
      "min": 0,
      "max": 0
    }
  }
}
```

#### Contrast: 1-1, center_grey: false, Brightness: 60-110

Json config example:

```json
{
  "action": "contrast_brightness",
  "src": ["$data_5"],
  "dst": "$contrast_brightness_9",
  "settings": {
    "contrast": {
      "min": 0,
      "max": 0,
      "center_grey": false
    },
    "brightness": {
      "min": 60,
      "max": 110
    }
  }
}
```

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
