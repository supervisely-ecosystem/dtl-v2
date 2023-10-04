# Flip

`Flip` layer simply flips data (images + annotations) by vertical or horizontal axis. This layer supports `bitmap`, `polygon`, `rectangle`, `point`, `polyline`, `graph` (`keypoint`) geometries in annotations.

### Settings:

- **axis** - Choose the axis along which the images with annotations will be flipped (`vertical` or `horizontal` axis).

### Example 1. Horizontal axis flip

Select `horizontal` axis in layer settings.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Flip axis: horizontal</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/febfdbd2-58f2-4e3a-a3e9-57da99f13ec9" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/06709e30-2a14-4349-b6cd-67adc7dfc4a8" alt="Flip axis: horizontal" /> </td>
</tr>
</table>

### Example 2. Vertical axis flip

Select `vertical` axis in layer settings.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Flip axis: vertical</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/49761074-0bf1-44e3-81e8-30445afe8e9e" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/61001cff-71b2-4c12-9193-ddd551ea9ecc" alt="Flip axis: vertical" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON config</summary>
<pre>
{
  "action": "flip",
  "src": ["$data1"],
  "dst": "$data2",
  "settings": {
    "axis": "vertical"
  }
}
</pre>
</details>
