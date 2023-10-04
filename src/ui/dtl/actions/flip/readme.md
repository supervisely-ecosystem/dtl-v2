# Flip

`Flip` layer simply flips data (images + annotations) by vertical or horizontal axis.

### Settings:

- **axis** - Choose the axis along which the images with annotations will be flipped (`vertical` or `horizontal` axis).

### Examples:

### Original image

![flip-original](https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/15ef4c3c-3b52-4c61-84bd-329c9b7b5e1d)

#### Example 1. Flip image by `horizontal` axis

Select `horizontal` axis in layer settings.

![flip-horizontal](https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/0f415368-3ed3-4311-854c-1ba58e867dfa)

#### Example 2. Flip image by `vertical` axis

Select `vertical` axis in layer settings.

![flip-vertical](https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/8b079f03-c3b6-4926-8f24-21cff9837be5)

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
