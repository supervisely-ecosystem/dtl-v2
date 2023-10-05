# Find Contours

`Find Contours` layer extracts contours from bitmaps and stores results as polygons.

### Settings

**classes_mapping** — Assign a new class name to each class. If name is not specified, then the class will not be modified.


### Example

<table>
<tr>
<td style="text-align:center"><strong>Original image (Bitmap)</strong></td>
<td style="text-align:center"><strong>Image with countors (Polygon)</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/ba578ac7-5110-46da-8dd9-eedbdcf11071" alt="Original image (Bitmap)" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/44beae2b-fb83-4e2a-bac6-93c7d650a5de" alt="Image with countors (Polygon)" /> </td>
</tr>
</table>

### JSON view


<details>
  <summary>JSON view</summary>
```json
{
    "action": "find_contours",
    "src": [
        "$data_12"
    ],
    "dst": "$find_contours_18",
    "settings": {
        "classes_mapping": {
            "cat": "cat_contours",
            "squirrel": "squirrel_contours"
        }
    }
}
```
</details>