# Flip

`Flip` layer simply flips data (images + annotations) by vertical or horizontal axis. 

Supports flipping `bitmap`, `polygon`, `rectangle`, `point`, `polyline`, `graph` (`keypoint`) geometry types.

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
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/5a89a164-7965-49ac-a749-d3a32b690dd0" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/143c010a-e225-4113-83d6-1f52064f0227" alt="Flip axis: horizontal" /> </td>
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
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/a44f0fe0-c7cb-488f-8831-44f41f92b506" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/c1d95d19-fc85-4e15-acf7-801172ff3e68" alt="Flip axis: vertical" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view for vertical axis flip</summary>
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
