# Save Masks

`Save Masks` layer gives you an opportunity to get masked representations of data besides just images and annotations that you can get using `Save` layer. It includes machine and human masks representations.

In machine masks each of listed classes are colored in shades of gray that you specify. Note that black color `[0, 0, 0]` is automatically assigned to the `background` class. In human masks you would get stacked original images with the images having class colors above (see example).

As a result, an archive with Supervisely project structure will be created in `Team Files`.
It contains the following folders and `meta.json` file:

**ann** — contains json annotations for each image

**img** — contains raw images

**masks\_human** — contains visual representation of generated mask

**masks\_machine** — generated masks

### Settings

**masks_machine** — if `true` machine readable masks are generated.

**masks_human** — if `true` human readable masks are generated.

**gt\_machine\_color** - specifies colors of generated masks for each class exported.

**gt\_human\_color** - specifies colors of generated masks for each class exported used in visual representation

### Example

<table>
<tr>
<td style="text-align:center; width:33%"><strong>Original image</strong></td>
<td style="text-align:center; width:34%"><strong>Human mask</strong></td>
<td style="text-align:center; width:33%"><strong>Machine mask</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/48913536/183e6cc6-1067-4d59-9458-00e86490af23" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/48913536/bc822c67-eb11-4ab8-8d03-e51b9625524f" alt="Human mask" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/48913536/cd442328-e22f-417d-8a57-d5a2f3750858" alt="Machine mask" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>

```json
{
  "action": "save_masks",
  "src": ["$data_1"],
  "dst": "My Project",
  "settings": {
    "masks_machine": true,
    "masks_human": true,
    "gt_machine_color": {
      "kiwi": [100, 100, 100],
      "lemon": [200, 200, 200]
    },
    "gt_human_color": {
      "kiwi": [255, 0, 0],
      "lemon": [27, 0, 255]
    }
  }
}
```

</details>
