# Tag

`Tag` layer adds or removes tags from images.

Tags are used for several things, e.g. to split images by folders in save layers or to filter images by tag.

### Settings

**tag** — tag name.
**action** — action that will be performed with tag. Can be `add` or `remove`.

<details>
  <summary>JSON view</summary>

```json
{
  "action": "tag",
  "src": ["$data_1"],
  "dst": "$tag_2",
  "settings": {
    "tag": "car",
    "action": "add"
  }
}
```

</details>
