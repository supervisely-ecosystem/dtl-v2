# BBox to Polygon

`BBox to Polygon` layer converts rectangles (`bounding boxes`) to polygons.

### Settings

- **classes_mapping** — Select classes to convert to polygons. If no classes are selected, all classes will be ignored.

❗ Selected classes will be replaced. If you want to keep them, use `Duplicate` layer first.

### Example. Convert bounding boxes to polygons

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image: bounding boxes</strong></td>
<td style="text-align:center; width:50%"><strong>Output: polygons</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/d58ae002-f23f-499e-b136-192c7719c500" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/a8b53945-a908-4070-a7ed-9c1902f46c27" alt="Polygons" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON vieww</summary>
<pre>
{
  "action": "bbox2poly",
  "src": ["$data_5"],
  "dst": "$bbox2poly_7",
  "settings": {
    "classes_mapping": {
        "peas": "__default__"
    }
  }
}
</pre>
</details>
