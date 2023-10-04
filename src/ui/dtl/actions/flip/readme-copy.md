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
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/15ef4c3c-3b52-4c61-84bd-329c9b7b5e1d" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/0f415368-3ed3-4311-854c-1ba58e867dfa" alt="Flip axis: horizontal" /> </td>
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
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/15ef4c3c-3b52-4c61-84bd-329c9b7b5e1d" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/8b079f03-c3b6-4926-8f24-21cff9837be5" alt="Flip axis: vertical" /> </td>
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
