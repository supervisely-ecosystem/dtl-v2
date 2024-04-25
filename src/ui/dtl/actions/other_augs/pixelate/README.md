# Pixelate

`Pixelate` layer adds mosaic pixelation to the images.

### Settings:

- **Severity** - Set value to specify the pixelation intensity. Goes from 1 to 5.

### Example. Pixelate the image

In this example, we pixelate the image with severity 5.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Pixelated: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/c589730f-4dfd-4640-b6d3-265d704d9c92" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/1a2f49c4-7f32-436f-a2fe-a55360dedec0" alt="Pixelated" width=95% /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "pixelate",
    "src": [
        "$images_project_1"
    ],
    "dst": "$pixelate_2",
    "settings": {
        "severity": 5
    }
}
</pre>
</details>
