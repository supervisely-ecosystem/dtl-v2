# Instances Crop

Layer for cropping instances by specifying classes to crop and pixels or percentage to crop from each side.

### Settings:

- **Select classes** (class selection mode)
- **Set paddings**:
  - **top**, **left**, **right**, **bottom** (_int_ - pixels or percentage)

### Example:

#### Instances Crop (classes: kiwi, top: 40px, left: 40px, right: 40px, bottom: 40px)

Json config example:

```json
{
  "action": "instances_crop",
  "src": ["$data_3"],
  "dst": "$instances_crop_10",
  "settings": {
    "classes": ["camera", "cell phone", "glasses"],
    "pad": {
      "sides": {
        "top": "40px",
        "left": "40px",
        "right": "40px",
        "bottom": "40px"
      }
    }
  }
}
```

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Instances Crop (kiwi class, 40px padding from each side)</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/22476d1c-684b-4ce0-9675-ba5fc5b34370" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/ccdf3074-fbe9-4278-ba64-e067f4cdd939" alt="Instances Crop" /> </td>
</tr>
</table>
