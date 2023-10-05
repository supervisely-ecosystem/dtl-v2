# If Action

`if` layer is used to split input data to several flows with a specified criterion.

### Settings

Let's consider all possible use cases.

<details>
  <summary>Use case: split with probability</summary>

In this case input data (image + annotation) will go to the "left" branch (`$if_10__true`) with probability 95% and to the "right" branch (`$if_10__false`) with probability 5%.

It can be used in several scenarios. Split data to train and val subsets.
First scenario is when we are going to split data into train and validation sets by adding corresponding tag to each image.

```json
{
  "action": "if",
  "src": ["$data_1"],
  "dst": ["$if_10__true", "$if_10__false"],
  "settings": {
    "condition": {
      "probability": 0.95
    }
  }
}
```

</details>

<details>
  <summary>Use case: split data by objects count</summary>

This case allows us to split data by objects count (`min_objects_count` value).

In the example below, images with equal or more that three objects will be passed to `$if_10__true` branch, other images — to the `$if_10__false` branch.

```json
{
  "action": "if",
  "src": ["$data_1"],
  "dst": ["$if_10__true", "$if_10__false"],
  "settings": {
    "condition": {
      "min_objects_count": 3
    }
  }
}
```

</details>

<details>
  <summary>Use case: split by image height or width</summary>

For example, we are going to filter images by minimum image height (200 pixels)

```json
{
  "action": "if",
  "src": ["$data_1"],
  "dst": ["$if_10__true", "$if_10__false"],
  "settings": {
    "condition": {
      "min_height": 200
    }
  }
}
```

The same can be applied to minimum width:

```json
{
  "action": "if",
  "src": ["$data_1"],
  "dst": ["$if_10__true", "$if_10__false"],
  "settings": {
    "condition": {
      "min_width": 200
    }
  }
}
```

This case is useful when we are going to skip some small images after applying `Crop` layer.

</details>

<details>
  <summary>Use case: split by tags</summary>

This example passes images with tag "party" or "dinner" to the `$if_10__true` branch, other images are passed to `$if_10__false` branch.

```json
{
  "action": "if",
  "src": ["$data_1"],
  "dst": ["$if_10__true", "$if_10__false"],
  "settings": {
    "condition": {
      "tags": ["party", "dinner"]
    }
  }
}
```

</details>

<details>
  <summary>Use case: split by class presence</summary>

In this example images which contain any object of some required class (person or dog) are passed to the `$if_10__true` branch.

```json
{
  "action": "if",
  "src": ["$data_1"],
  "dst": ["$if_10__true", "$if_10__false"],
  "settings": {
    "condition": {
      "include_classes": ["person", "dog"]
    }
  }
}
```

</details>

<details>
  <summary>Use case: split by images names in range, and step</summary>

Names is ordered alphabetical (a, b ,c ...).

```json
{
  "action": "if",
  "src": ["$data_1"],
  "dst": ["$if_10__true", "$if_10__false"],
  "settings": {
    "condition": {
      "name_in_range": ["a0100", "a0105"],
      "frame_step": 2
    }
  }
}
```

Should pass images with names ["00100", "00102", "00104"] into first branch (`$if_10__true`) and else into (`$if_10__false`) branch.

</details>
