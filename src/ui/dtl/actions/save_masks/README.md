# Save Masks

`Save Masks` layer gives you an opportunity to get masked representations of data besides just images and annotations that you can get using `Save` layer. It includes machine and human masks representations.

In machine masks each of listed classes are colored in shades of gray that you specify. Note that black color `[0, 0, 0]` is automatically assigned to the `background` class. In human masks you would get stacked original images with the images having class colors above (see example).

As a result, an archive with Supervisely project structure will be created in `Team Files`.
It contains the following folders and `meta.json` file:

**ann** — contains json annotations for each image
**img** — contains raw images
**masks_human** — contains visual representation of generated mask
**masks_machine** — generated masks

### Settings

**masks_machine** — if `true` machine readable masks are generated.
**masks_human** — if `true` human readable masks are generated.
**gt_machine_color** - specifies colors of generated masks for each class exported.

- for class `kiwi` machine color is defined by `RGB=(100,100,100)`.
- for class `lemon` machine color is defined by `RGB=(200,200,200)`.

**gt_human_color** - specifies colors of generated masks for each class exported used in visual representation

- for class `kiwi` machine color is defined by `RGB=(255,0,0)`.
- for class `lemon` machine color is defined by `RGB=(27,0,255)`.

### Example

**masks_human** example.

![masks_human](https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/33aa3618-1032-4e37-8a74-f763e873670f)

**masks_machine** example.

![masks_machine](https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/ba9da74c-2b7a-4a1b-a4e9-5952a3a439e4)

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
