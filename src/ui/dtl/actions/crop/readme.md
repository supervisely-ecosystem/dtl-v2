# Crop

Layer for cropping images by specifying pixels or percentage to crop from each side or by cropping the random part of the image with specified size.

### Settings:

- Crop type: **Side**
  - **top**, **left**, **right**, **bottom** (_int_ - pixels or percentage)
- Crop type: **Random part**
  - **width, height** (_int_ - min, max percentage range)
  - **keep aspect ratio** (_bool_ - keep aspect ratio or not)

### Examples:

#### Crop type: Sides, top: 15%, left: 15%, right: 15%, bottom: 15%

Json config example:

```json
{
  "action": "crop",
  "src": ["$data_3"],
  "dst": "$crop_5",
  "settings": {
    "mode": "sides",
    "sides": {
      "top": "15%",
      "left": "15%",
      "right": "15%",
      "bottom": "15%"
    }
  }
}
```

#### Crop type: Random part, width: 50-70%, height: 50-70%, keep aspect ratio: true

Json config example:

```json
{
  "action": "crop",
  "src": ["$data_3"],
  "dst": "$crop_5",
  "settings": {
    "mode": "random_part",
    "random_part": {
      "height": {
        "min_percent": 1,
        "max_percent": 1
      },
      "width": {
        "min_percent": 1,
        "max_percent": 1
      },
      "keep_aspect_ratio": true
    }
  }
}
```

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Sides: 15% from each side</strong></td>
<td style="text-align:center"><strong>Random part: 50-70% for width and height. Keep aspect ratio.</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/ab85486c-84ce-4e32-9f82-84a22ff0a1c0" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/59edb43f-9269-4efe-a78f-279b21d5a420" alt="Crop type: Sides" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/a2cce606-5c7f-4439-9c5c-2188ed21ae96" alt="Crop type: Random part" /> </td>
</tr>
</table>
