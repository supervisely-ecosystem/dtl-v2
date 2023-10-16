# Merge Masks

`Merge Masks` layer takes all bitmap labels with selected class and merge them into single bitmap label. Support only `bitmap` shape labels.

### Settings

**class** — name of class for merging. You can select only one class.

### Example. Merge masks

Merge masks with class `bird`

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Merged masks</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/060f54c7-abe9-4097-ae84-5630be822596" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/57d3cc8e-0222-49f3-bb75-77c39cd30bcc" alt="Merged masks" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
  <per>
{
  "action": "merge_bitmap_masks",
  "src": ["$data_17"],
  "dst": "$merge_bitmap_masks_18",
  "settings": {
    "class": "bird"
  }
}
</per>
</details>
