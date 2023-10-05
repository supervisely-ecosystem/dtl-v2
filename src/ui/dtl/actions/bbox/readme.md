# Bounding Box

`Bounding Box` layer converts annotations of specified classes to bounding boxes. Coordinates of bounding boxes are calculated like this:

```
minx = min(xcoords);
maxx = max(xcoords);
miny = min(ycoords);
maxy = max(ycoords);
```

### Settings:

- **classes_mapping** - Assign a new class name to each class. If name is not specified, then the class will not be modified.

❗ Selected classes will be replaced. If you want to keep them, use `Duplicate` layer first.


### Example:

<table>
<tr>
<td style="text-align:center"><strong>Original image: bitmap and polygon annotations</strong></td>
<td style="text-align:center"><strong>Output: bounding boxes</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/22476d1c-684b-4ce0-9675-ba5fc5b34370" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/897a9eae-0cf7-4010-83db-4a2fc80a38f9" alt="Bounding boxes" /> </td>
</tr>
</table>


### JSON view


<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "bbox",
  "src": ["$data_3"],
  "dst": "$bbox_17",
  "settings": {
    "classes_mapping": {
      "book": "book_bbox",
      "glasses": "glasses_bbox"
    }
  }
}
</pre>
</details>