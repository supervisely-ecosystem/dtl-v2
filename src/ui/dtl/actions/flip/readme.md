# Flip

`Flip` layer simply flips data (images + annotations) vertically or horizontally.

### Settings:

- **axis** - Choose between `horizontal` and `vertical` axis to flip images and annotations.

### Examples:

### Original image

![flip-original](https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/4a70f4e7-b17b-4812-93df-481f90af18a6)

#### Example 1. Flip image by `horizontal` axis

Select `horizontal` axis in layer settings.

![flip-horizontal](https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/25ac0b70-b6b9-4a4d-b8d3-7ee1fabcdc9d)

#### Example 2. Flip image by `vertical` axis

Select `vertical` axis in layer settings.

![flip-vertical](https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/fd71f345-8e40-4f58-94f9-0bd787448c65)

### JSON config example

<details>
  <summary>JSON config</summary>
<pre>
{
  "action": "flip",
  "src": ["$data1"],
  "dst": "$data2",
  "settings": {
    "axis": "vertical"
  }
}
</pre>
</details>
