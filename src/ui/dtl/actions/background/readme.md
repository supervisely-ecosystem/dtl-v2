# Background

Layer adds background rectangle (size equals to image size) with custom class to image annotations. This layer is used to prepare data to train Neural Network for semantic segmentation.

### Settings:

- **Background class name**:
  - Possible values: _string_

## Example:

### Background class "bg"

Json config example:

```json
{
  "action": "background",
  "src": ["$data_1"],
  "dst": "$background_3",
  "settings": {
    "class": "bg"
  }
}
```

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Background class: "bg"</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/22476d1c-684b-4ce0-9675-ba5fc5b34370" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/cd9454bf-5fb1-474c-8e1c-889ace1ebdc0" alt="Background" /> </td>
</tr>
</table>
