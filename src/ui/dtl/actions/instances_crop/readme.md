# Instances Crop

Layer for cropping instances by specifying classes to crop and pixels or percentage to crop from each side.

### Settings:

- **classes** - Select classes of objects to crop. If name is not specified, then the class will not be modified.
- **pad** - Padding settings (pixels or percentage) for each side of the image (top, left, right, bottom).

### Example. Crop `car` class

Crop instances of class `car` with 50px padding from each side.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Cropped instance (50px padding from each side)</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/07b8e241-3733-4ef3-be21-506cc027c7b2" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/3693d57d-b127-4825-afba-7a4f7a389e5c" alt="Instances Crop" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "instances_crop",
  "src": ["$data_5"],
  "dst": "$instances_crop_6",
  "settings": {
    "classes": ["car"],
    "pad": {
      "sides": {
        "top": "50px",
        "left": "50px",
        "right": "50px",
        "bottom": "50px"
      }
    }
  }
}
</pre>
</details>
