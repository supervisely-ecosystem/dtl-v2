# Instances Crop

`Instances Crop` layer crops objects of specified classes from image with configurable paddings (pixels or percentage from each side).

ℹ️ In case of multiple objects of the same class on the image, each object will be cropped separately. 
So from one image there can be produced multiple images, each with one target object. Other objects are removed from crop.

### Settings:

- **`classes`** - Select classes of objects to crop. It means that all objects of such classes will be cropped from image.
- **`pad`** - Padding settings (pixels or percentage) for each side of the image (`top`, `left`, `right`, `bottom`). It means how many will be padded from the sides of precise bounding box around object (may be defined in pixels or in percent of bounding box height).

Here is the graphical description of fields:

![instances-crop-01](https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/34a47747-a1f8-4a45-8967-087759179048)

Result of applying the layer from the example above:

![instances-crop-02](https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/01df02e3-7076-4961-bf81-7520d2929dba)

As we can see, "car" and "person" objects are cropped separetely. This layer from one input image produced three images with one target object. Other objects are dropped from the resulting images.


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
