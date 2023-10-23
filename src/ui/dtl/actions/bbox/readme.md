# Bounding Box

`Bounding Box` layer converts annotations of classes with shapes of other types into classes with bounding boxes.

Coordinates of bounding boxes are calculated like this:

```
min_x = min(x_coords);
max_x = max(x_coords);
min_y = min(y_coords);
max_y = max(y_coords);
```

### Settings:

- **classes** - Select classes to convert to bounding boxes. If no classes are selected, all classes will be ignored.

❗ Selected classes will be replaced. If you want to keep them, use `Duplicate` layer first.

### Example. Convert annotations to bounding boxes

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image: bitmap and polygon annotations</strong></td>
<td style="text-align:center; width:50%"><strong>Output: bounding boxes</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/175304fb-563c-4a62-b300-e972de93d82e" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/d936292b-ca1d-4ba7-8dce-51b01edcf069" alt="Bounding boxes" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "bbox",
  "src": ["$data_5"],
  "dst": "$bbox_7",
  "settings": {
    "classes_mapping": {
      "ballon": "__default__"
    }
  }
}
</pre>
</details>
