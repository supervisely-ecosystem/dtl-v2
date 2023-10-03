# Bbox to Polygon

`Bbox to Polygon` layer converts rectangles (`bounding boxes`) to polygons.

❗ Selected classes will be replaced. If you want to keep them, use `Duplicate` layer first.

### Settings

**classes_mapping** — Assign a new class name to each class. If name is not specified, then the class will not be modified.

<details>
  <summary>JSON config</summary>
```json
{
  "action": "bbox2poly",
  "src": ["$data_3"],
  "dst": "$bbox2poly_20",
  "settings": {
    "classes_mapping": {
      "watch_bbox": "watch_poly",
      "glasses_bbox": "glasses_poly"
    }
  }
}
```
</details>


### Example

<table>
<tr>
<td style="text-align:center"><strong>Original image: bounding boxes</strong></td>
<td style="text-align:center"><strong>Output: polygons</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/897a9eae-0cf7-4010-83db-4a2fc80a38f9" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/20004430-a2cd-4a06-a6f9-ec541dacb17a" alt="Polygons" /> </td>
</tr>
</table>
