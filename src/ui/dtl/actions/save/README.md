# Save

`Save` layer allows to export annotations and images. Annotations are stored in `.json` files. Images are stored in `.png` or `.jpg` files (due to format of source image). When exporting annotations, `meta.json` file containing all used classes for project is also exported.

Moreover, you can get visual representations of all annotated objects on top of your images by setting visualize to true.

As a result, an archive with Supervisely project structure will be created in `Team Files`.
It contains the following folders and `meta.json` file:

**ann** — contains json annotations for each image
**img** — contains raw images

### Settings

**visualize** — if `true` visual representations of all annotated objects are generated. `Bitmap` objects are drawn without modifications, `polygons` are filled with color associated with the class, for `rectangles` only borders are drawn.

### Example

If `visualize` attribute is set to `true` then for each images corresponding visualizations are generated.

![visualize-true](https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/7cf3ac03-e584-4327-9ba1-05d9d2cf1d68)

### JSON view

<details>
  <summary>JSON view</summary>
```json
{
  "action": "save",
  "src": ["$tag_16"],
  "dst": "New Project",
  "settings": {
    "visualize": true
  }
}
```
</details>
