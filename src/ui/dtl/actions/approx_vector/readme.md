# Approx Vector

`Approx Vector` layer approximates vector figures: `lines` and `polygons`.
The operation decreases number of vertices with Douglas-Peucker algorithm.

### Settings:

- **classes** - Choose classes to apply transformation. Only classes with shape `line` or `polygon` are allowed.
- **epsilon** - Approximation accuracy, maximum distance between the original curve and its approximation.


### Example:

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Epsilon: 4</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/1e2c27b1-7cc3-4ce6-9b6c-e358b378fdb2" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/d8749d1f-0a2a-4359-985a-730d469814e0" alt="Epsilon: 4" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "approx_vector",
  "src": ["$data_3"],
  "dst": "$approx_vector_16",
  "settings": {
    "classes": ["camera", "cup"],
    "epsilon": 4
  }
}
</pre>
</details>
