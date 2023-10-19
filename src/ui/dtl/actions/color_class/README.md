# Color Class

`Color Class` layer used for coloring classes as you wish.

### Settings:

- **classes\_color\_mapping** - Assign a new class color to each class. All specified classes will be colored. If you want to leave some classes unchanged select `default` option.

### Example. Change color of classes `horse` and `person`

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Color classes</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/8e03c98c-4c2c-4e30-8911-f17ada18b658" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/e1e24235-c7eb-40aa-bb03-af3cf859f0d5" alt="Color classes" /> </td>
</tr>
</table>

### Hex color

Hex color format present as string with 4 components: # + RED + GREEN + BLUE. Use online color converters to more accurately achieve the desired color.

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "color_class",
  "src": ["$data_5"],
  "dst": "$color_class_11",
  "settings": {
    "classes_color_mapping": {
      "horse": [126, 211, 33],
      "person": [208, 2, 27]
    }
  }
}
</pre>
</details>
