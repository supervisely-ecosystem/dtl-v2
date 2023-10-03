# Flip

`Flip` layer simply flips data (image + annotation) vertically or horizontally.

### Settings:

- Axis:
  - Possible values: "vertical" or "horizontal"

### Examples:

#### Axis: vertical

Json config example:

```json
{
  "action": "flip",
  "src": ["$data1"],
  "dst": "$data2",
  "settings": {
    "axis": "vertical"
  }
}
```

### Axis: horizontal

Json config example:

```json
{
  "action": "flip",
  "src": ["$data1"],
  "dst": "$data2",
  "settings": {
    "axis": "horizontal"
  }
}
```

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Flip axis: vertical</strong></td>
<td style="text-align:center"><strong>Flip axis: horizontal</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/ab85486c-84ce-4e32-9f82-84a22ff0a1c0" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/91fca97e-6e51-4966-a820-e6911a3cf545" alt="Crop type: Sides" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/2398e07c-058c-4e9c-b67d-2a8bb6845f72" alt="Crop type: Random part" /> </td>
</tr>
</table>
