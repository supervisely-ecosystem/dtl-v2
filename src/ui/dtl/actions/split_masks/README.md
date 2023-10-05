# Split Masks

`Split Masks` layer takes one bitmap label mask and split it into few bitmap masks if it contain non-connected components.

### Settings

**classes** - list of class names for split operation.

### Example

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Splitted masks</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/3722ccf2-3f2d-411d-a9a0-182438b96c8b" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/831d1051-76aa-40cf-8374-ebf31e837a44" alt="Splitted masks" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
```json
{
    "action": "split_masks",
    "src": [
        "$data_12"
    ],
    "dst": "$split_masks_23",
    "settings": {
        "classes": [
            "cat"
            "dog",
            "horse",
            "sheep",
            "squirrel"
        ]
    }
}
```
</details>
