# Skeletonize

`Skeletonize` layer extracts skeletons from bitmap figures.

### Settings

**classes** - list of classes to apply transformation. Only classes with shape `bitmap` are allowed.
**method** - algorithm of processing. Available options: `skeletonization`, `medial_axis`, `thinning`.

### Example

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Skeletonized image</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/5215ff13-d53d-4911-a156-8efe4d2b63a1" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/57fbff6c-a434-4c7f-83cd-b961e8f37c48" alt="Skeletonized image" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "skeletonize",
  "src": ["$data_12"],
  "dst": "$skeletonize_15",
  "settings": {
    "classes": ["Cat", "Squirrel"],
    "method": "skeletonization"
  }
}
</pre>
</details>
