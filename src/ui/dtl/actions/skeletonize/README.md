# Skeletonize

Layer extracts skeletons from bitmap figures.

### Settings

- **Select classes** (only bitmap classes are allowed)
- **Skeletonization methods**:
  - **Skelitonization**
  - **Medial Axis**
  - **Thinning**

### Example

```json
{
    "action": "skeletonize",
    "src": [
        "$data_12"
    ],
    "dst": "$skeletonize_15",
    "settings": {
        "classes": [
            "Squirrel"
        ],
        "method": "skeletonization"
    }
}
```

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Skeletonized image</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/879c31b6-286e-4e00-90c6-c2ed16784e66" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/7dae7e72-2e71-4b08-a318-ab5a270a8fb7" alt="Skeletonized image" /> </td>
</tr>
</table>
