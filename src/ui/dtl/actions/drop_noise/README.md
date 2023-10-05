# Drop Noise

`Drop Noise` layer removes connected components smaller than the specified size from bitmap annotations.

This can be useful to eliminate noise after running neural network.

### Settings

**classes** - list of classes that will be affected.
**min_area** - minimal area of connected component to keep. Can be set in pixels or percents.
**src_type** - type of source data.

### Example

<table>
<tr>
<td style="text-align:center"><strong>Original label</strong></td>
<td style="text-align:center"><strong>Result label</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/56297428-4fd1-4ddc-b04e-593d2d2a233a" alt="Original label"/> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/78aecdcc-7d94-4e65-acff-b79f79806d74" alt="Result label"/> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>

```json
{
  "action": "drop_noise",
  "src": ["$data_1"],
  "dst": "$drop_noise_2",
  "settings": {
    "classes": ["shoes"],
    "min_area": "5%",
    "src_type": "image"
  }
}
```

</details>
