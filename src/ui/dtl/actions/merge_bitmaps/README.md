# Merge Masks

`Merge Masks` layer takes all bitmap labels with selected classes and merge them into single bitmap label.

### Settings

**class** — name of class for merging.

### Example

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Merged masks</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/5482d336-cc5b-4a4f-8f77-b8d16472a5f5" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/a66bfa8f-1c14-40c3-8e3d-d16db3da0252" alt="Merged masks" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
```json
{
    "action": "merge_bitmap_masks",
    "src": [
        "$data_12"
    ],
    "dst": "$merge_bitmap_masks_24",
    "settings": {
        "class": "cat"
    }
}
```
</details>
