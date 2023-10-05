# Bitwise Masks

`Bitwise Masks` layer make bitwise operations between bitmap annotations.

### Settings

- **type** — Choose between `and`, `or` and`nor` operations.
- **class_mask** — Class name of the mask. First element of bitwise operation. It unchangeble class.
- **classes_to_correct** — List of class names to correct.

### Example

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>type `nor`</strong></td>
<td style="text-align:center"><strong>type `or`</strong></td>
<td style="text-align:center"><strong>type `and`</strong></td>
</tr>
<tr>
<td> <img src="" alt="Original image" /> </td>
<td> <img src="" alt="type `nor`" /> </td>
<td> <img src="" alt="type `or`" /> </td>
<td> <img src="" alt="type `and`" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "bitwise_masks",
  "src": ["$data_1"],
  "dst": "$bitwise_masks_2",
  "settings": {
    "type": "nor",
    "class_mask": "plants",
    "classes_to_correct": ["book"]
  }
}
</pre>
</details>
