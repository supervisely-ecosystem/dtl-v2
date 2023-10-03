# Find Contours

Layer to extract contours from bitmaps and store results as polygons.

### Settings

- **Select classes** (class selection mode)

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