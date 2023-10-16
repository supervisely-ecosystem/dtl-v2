# Drop Lines by Length

`Drop Lines by Length` layer remove too long or to short lines.

Also this layer can drop lines with length in range.
Lines with more than two points also supported. For multi-lines total length is calculated as sum of sections.

### Settings

- **lines_class** - class name of target lines.
- **resolution_compensation** - used for images with different resolution (scales). If `false` - line length calcalute with pixels. If `true` - in relative units.
- **min_length** - minimal line length.
- **max_length** - maximal line length.
- **invert** - invert drop results. This mode can be used to remove lines with length in range.

### Example

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image (Lines)</strong></td>
<td style="text-align:center; width:50%"><strong>Result image</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/236714c1-a3c9-43bd-809e-7c54a9e9dcf0" alt="Original image (Lines)"/> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/f8648688-8710-4c81-8902-ff3cfc53feae" alt="Result image"/> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>

```json
{
  "action": "drop_lines_by_length",
  "src": ["$data_1"],
  "dst": "$drop_lines_by_length_2",
  "settings": {
    "lines_class": "squirrel_line",
    "resolution_compensation": true,
    "invert": true,
    "min_length": 1,
    "max_length": 5
  }
}
```

</details>
