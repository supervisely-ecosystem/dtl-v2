# Rotate

`Rotate` layer rotates images and its annotations.

#### Settings:

- **rotate_angles** - Set the range of angles (`min_degrees` and `max_degrees`) to rotate the image.
- **black_regions** - Set the `mode` to handle black regions (possible values: `keep`, `crop`, `preserve_size`).

Each image will be rotated by a random angle (around the image center, CCW) with uniform distribution from `min_degrees` to `max_degrees`. You can:

- keep original image data (`mode: keep`), then new regions will be filled with black color;
- crop rotated result to exclude black regions (`mode: crop`);
- crop rotated result to preserve original image size and scale of objects (`mode: preserve_size`);

### Examples:

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Rotated Image (min_degrees: -45, max_degrees: 45, mode: keep)</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/22476d1c-684b-4ce0-9675-ba5fc5b34370" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/e71bfda8-1f5c-4fd6-8fd0-671c95a3c676" alt="Rotated Image. Mode: keep" /> </td>
</tr>
</tr>
<tr>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align:center"><strong>Rotated Image (min_degrees: -45, max_degrees: 45, mode: crop)</strong></td>
<td style="text-align:center"><strong>Rotated Image (min_degrees: -45, max_degrees: 45, mode: preserve_size)</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/c954859a-eef1-4f7a-8035-6d313a7d14b1" alt="Rotated Image. Mode: crop" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/957f43f8-db5a-4644-9e4b-6d6a7a6e27f4" alt="Rotated Image. Mode: preserve_size" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "rotate",
  "src": [],
  "dst": "$rotate_5",
  "settings": {
    "rotate_angles": {
      "min_degrees": -45,
      "max_degrees": 45
    },
    "black_regions": {
      "mode": "keep"
    }
  }
}
</pre>
</details>
