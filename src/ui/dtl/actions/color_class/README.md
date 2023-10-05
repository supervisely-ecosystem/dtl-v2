# Color Class

`Color Class` layer used for coloring classes as you wish. Add this class at the end of graph, before data saving.

### Settings:

- **classes_color_mapping** - Assign a new class color to each class. By default, all classes will be colored with the same color as the original class.

### Examples:

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Color 3 classes</strong></td>
</tr>
<tr>
<td> <img src="" alt="Original image" /> </td>
<td> <img src="" alt="Color classes" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view for `Sides` crop type</summary>
<pre>
{
  "action": "color_class",
  "src": ["$data_1"],
  "dst": "$color_class_2",
  "settings": {
    "classes_color_mapping": {
      "book": [144, 144, 204],
      "camera": [0, 170, 0],
      "cell phone": [255, 128, 128],
    }
  }
}
</pre>
</details>
