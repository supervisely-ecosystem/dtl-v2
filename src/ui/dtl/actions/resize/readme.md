# Resize

Resize the image to the specified width and height. If aspect ratio is enabled, the image will be resized to fit within the specified width and height boundaries.

#### Settings:

- **width** - Set the width of the resized image.
- **height** - Set the height of the resized image.
- **aspect_ratio** - Specify whether to keep the aspect ratio of the image.

### Example. Resize image

In this example we will resize image to 1200x1200 pixels without keeping aspect ratio.

<img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/e4c90d16-85c6-4e84-9139-259e87835b4c" alt="Resized Image" />

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "resize",
  "src": ["$data_1"],
  "dst": "$resize_2",
  "settings": {
    "width": 1200,
    "height": 1200,
    "aspect_ratio": {
      "keep": false
    }
  }
}
</pre>
</details>
