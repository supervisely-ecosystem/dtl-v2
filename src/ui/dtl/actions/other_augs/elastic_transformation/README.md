# Elastic Transformation

`Elastic Transformation` layer applies elastic transformation augmentation to the images.

### Settings:

- **Severity** - Set value to specify the transformation intensity. Goes from 1 to 5.

### Example. Transform the image

In this example, we transform the image with severity 5.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Elastic Transformation: Severity 5</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/c589730f-4dfd-4640-b6d3-265d704d9c92" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/115161827/40677182-e110-4be4-b333-819e2b389806" alt="Elastic Transform" /> </td>
</tr>
</table>

<details>
  <summary>JSON view</summary>
<pre>
{
    "action": "elastictransform",
    "src": [
        "$images_project_1"
    ],
    "dst": "$elastictransform_2",
    "settings": {
        "severity": 5
    }
}
</pre>
</details>
