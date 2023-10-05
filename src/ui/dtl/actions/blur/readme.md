# Blur

`Blur` layer for blurring the image by applying a Gaussian or median filter.

### Settings:

**Blur type** - Choose between Gaussian and Median blur.

- **Gaussian**: set sigma min and max values.
- **Median**: set kernel size.

### Examples:

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Gaussian blur. Sigma: 4-6</strong></td>
<td style="text-align:center"><strong>Median blur, kernel size: 65</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/22476d1c-684b-4ce0-9675-ba5fc5b34370" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/19515c58-a215-407c-9c3e-66b423ac87e0" alt="Gaussian sigma: 4-6" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/ed4e54ac-4ddc-4e06-8564-b53aae2d33d2" alt="Median, kernel size: 65" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view for Gaussian blur</summary>
<pre>
{
  "action": "blur",
  "src": ["$data1"],
  "dst": "$data2",
  "settings": {
    "blur_type": "gaussian",
    "sigma": { "min": 4, "max": 6 }
  }
}
</pre>
</details>

<details>
  <summary>JSON view for Median blur</summary>
<pre>
{
  "action": "blur",
  "src": ["$data1"],
  "dst": "$data2",
  "settings": {
    "blur_type": "Median",
    "kernel_size": 65
  }
}
</pre>
</details>
