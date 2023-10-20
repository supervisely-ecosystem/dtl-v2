# Rasterize

`Rasterize` layer converts all geometry figures to bitmaps and rasterizes objects on the image. (i.e. one pixel will belong to only one object)

### Settings

- **classes** — Select classes to rasterize. If no classes are selected, all objects will be preserved.

### Example

In this example original image contains two objects: **car** and **road**, and they are **overlapped** (car object is under the road object).
On the result image car and road objects are rasterized, and now they are not overlapped.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Road with rasterized Car object</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/ac369766-ffa3-4967-afc2-3bcc9b4bfcdc" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/15e6d16b-b942-45a9-b83e-3ace407e0d14" alt="Road with rasterized Car object" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "rasterize",
  "src": ["$data_7"],
  "dst": "$rasterize_6",
  "settings": {
    "classes_mapping": {
      "car": "car_rasterized",
      "road": "road_rasterized"
    }
  }
}
</pre>
</details>
