# Resize

Resize the image to the specified width and height. If aspect ratio is enabled, the image will be resized to fit within the specified width and height boundaries.

#### Settings:

- **Width**:
  - _int_. Possible values: positive integer
- **Height**:
  - _int_. Possible values: positive integer

### Example:

#### Resized Image (width: 400, height: 200, keep aspect ratio: true)

Json config example:

```json
{
  "action": "resize",
  "src": ["$data_5"],
  "dst": "$resize_14",
  "settings": {
    "width": 400,
    "height": 200,
    "aspect_ratio": {
      "keep": true
    }
  }
}
```

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Resized Image</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/22476d1c-684b-4ce0-9675-ba5fc5b34370" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/4d039e70-916e-422a-8151-4e62ee433a73" alt="Resized Image" /> </td>
</tr>
</table>
