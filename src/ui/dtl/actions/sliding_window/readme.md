# Sliding Window

`Sliding Window` layer is used to crop part of image with its annotations by sliding of window from left to rigth, from top to bottom.

### Settings

- **Window**:
  - **window_width** (_int_ - window width in pixels)
  - **window_height** (_int_ - window height in pixels)
- **Min overlap**:
  - **x** (_int_ - minimum overlap in pixels along x axis)
  - **y** (_int_ - minimum overlap in pixels along y axis)

![sw_schema](https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/9e04540f-ee5f-4697-8a08-ea145ea2161c)

### Examples

#### Sliding window: window width: 512, window height: 512, min overlap: 32

Json config example:

```json
{
  "action": "sliding_window",
  "src": ["$data_1"],
  "dst": "$sliding_window_5",
  "settings": {
    "window": {
      "width": 512,
      "height": 512
    },
    "min_overlap": {
      "x": 32,
      "y": 32
    }
  }
}
```

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Sliding windows (512x512, overlap: 32)</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/88a1995f-3917-4985-88db-998052c28bc2" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/53466f82-5078-4e17-8aca-d9e0fa0d29a5" alt="Sliding window" /> </td>
</tr>
</table>
