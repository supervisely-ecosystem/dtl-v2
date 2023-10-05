# Bitmap to Lines

`Bitmap to Lines` layer converts thinned (skeletonized) bitmaps to lines.

It is extremely useful if you have some raster objects representing lines or edges, maybe forming some tree or net structure, and want to work with vector objects.

Each input bitmap should be already thinned (use `Skeletonize` layer to do it), and for single input mask a number of lines will be produced.

Resulting lines may have very many vertices, so consider applying `Approx Vector` layer to results of this layer.
Internally the layer builds a graph of 8-connected pixels, determines minimum spanning tree(s), then extracts diameters from connected components of the tree.

### Settings

**classes_mapping** — Assign a new class name to each class. If name is not specified, then the class will not be modified.
**min_points_cnt** — min number of vertices for each output line. Other lines will be dropped.


### Example

<table>
<tr>
<td style="text-align:center"><strong>Original image (Bitmap)</strong></td>
<td style="text-align:center"><strong>Skeletonized</strong></td>
<td style="text-align:center"><strong>Bitmap to Lines</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/ba91b0c2-8c55-4264-8d85-d5735e4fd972" alt="Original image (Bitmap)"/> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/e8ce60c5-cf94-47d5-94b7-9d442c6591f7" alt="Skeletonized"/> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/899ec8c2-b9ee-4f50-b276-bdf68d0d3237" alt="Bitmap to Lines"/> </td>
</tr>
</table>


### JSON view


<details>
  <summary>JSON view</summary>

```json
{
    "action": "bitmap2lines",
    "src": [
        "$data_1"
    ],
    "dst": "$bitmap2lines_7",
    "settings": {
        "classes_mapping": {
            "cat": "cat_line",
            "horse": "horse_line",
            "sheep": "sheep_line"
        },
        "min_points_cnt": 2
    }
}
```
</details>