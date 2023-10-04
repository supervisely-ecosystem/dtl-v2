# Flip

`Flip` layer simply flips data (images + annotations) vertically or horizontally.

### Settings:

- **axis** - Choose between `horizontal` and `vertical` axis to flip images and annotations.

### Examples:

#### Example 1. Flip image by `horizontal` axis

Select `horizontal` axis in layer settings.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Flip axis: horizontal</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/4a70f4e7-b17b-4812-93df-481f90af18a6" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/25ac0b70-b6b9-4a4d-b8d3-7ee1fabcdc9d" alt="Flip axis: horizontal" /> </td>
</tr>
</table>

#### Example 2. Flip image by `vertical` axis

Select `vertical` axis in layer settings.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Flip axis: vertical</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/4a70f4e7-b17b-4812-93df-481f90af18a6" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/fd71f345-8e40-4f58-94f9-0bd787448c65" alt="Flip axis: vertical" /> </td>
</tr>
</table>

### JSON config example

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
