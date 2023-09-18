# Flip

Flip layer simply flips data (image + annotation) vertically or horizontally.

### Settings:
* Axis: 
  * Possible values: "vertical" or "horizontal"

Json config example:
```json
{
  "action": "flip",
  "src": ["$data1"],
  "dst": "$data2",
  "settings": {
    "axis": "vertical"
  }
}
```

## Example:

### Original Image
![Original image](https://raw.githubusercontent.com/supervisely/docs/master/assets/legacy/all_images/flip_001_orig.jpg)

### Axis: vertical
!["axis": "vertical"](https://raw.githubusercontent.com/supervisely/docs/master/assets/legacy/all_images/flip_002_vert.jpg)


### Axis: horizontal
!["axis": "horizontal"](https://raw.githubusercontent.com/supervisely/docs/master/assets/legacy/all_images/flip_003_hor.jpg)
