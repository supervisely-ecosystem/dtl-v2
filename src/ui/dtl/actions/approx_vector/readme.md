# Approx Vector

`Approx Vector` layer approximates vector figure – reduce the number of vertices in vector figures and simplify them.
Supported shapes: `polyline` and `polygon`.
The operation decreases number of vertices with Douglas-Peucker algorithm.

### Settings:

- **classes** - Choose classes to apply transformation. Only classes with shape `line` or `polygon` are allowed.
- **epsilon** - Approximation accuracy, maximum distance between the original curve and its approximation.

### Example. Approximate vector figures

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Epsilon: 10</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/a1389f2c-8bbc-4182-a7e0-b39c676be777" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/6e6ded99-f9ac-4980-bb8e-bab08a025378" alt="Epsilon: 10" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "approx_vector",
  "src": ["$data_5"],
  "dst": "$approx_vector_6",
  "settings": {
    "classes": ["ballon"],
    "epsilon": 10
  }
}
</pre>
</details>
