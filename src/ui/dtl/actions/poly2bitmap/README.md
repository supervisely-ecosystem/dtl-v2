# Polygon to Bitmap

`Polygon to Bitmap` converts annotations of shape polygon to shape bitmap.

Polygons will be drawn filled, considering holes.

### Settings

**classes_mapping** — Assign a new class name to each class. If name is not specified, then the class will not be modified.

</details>

<table>
<tr>
<td style="text-align:center"><strong>Original label (Polygon)</strong></td>
<td style="text-align:center"><strong>Result label (Bitmap)</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/73c90c70-42a3-4a6c-be50-455777db962d" alt="Original label (Polygon)"/> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/9cd65865-31e2-49e7-9475-4ffd02b6f7d4" alt="Result label (Bitmap)"/> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>

```json
{
  "action": "poly2bitmap",
  "src": ["$data_1"],
  "dst": "$poly2bitmap_2",
  "settings": {
    "classes_mapping": {
      "chair": "chair_bitmap"
    }
  }
}
```
