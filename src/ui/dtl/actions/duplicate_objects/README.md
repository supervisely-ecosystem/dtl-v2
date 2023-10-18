# Duplicate objects

`Duplicate Objects` layer simply clones figures of required classes. It can be useful to duplicate objects for comparing different labeling results.

### Settings:

- **classes_mapping** - Select classes to duplicate objects.

### Example. Duplicate `dog` class objects

Select `dog` class in settings and run the app. All `dog` class objects will be duplicated.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original image</strong></td>
<td style="text-align:center; width:50%"><strong>Duplicated objects</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/66d278f9-9c67-4ee4-b4a9-fc444816f67b" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/92ca606f-56b5-4717-a95b-c9034a85e6e3" alt="Duplicatred objects" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "duplicate_objects",
  "src": ["$data_1"],
  "dst": "$duplicate_objects_2",
  "settings": {
    "classes_mapping": {
      "blueberries": "__ignore__",
      "dog": "dog",
      "plants": "__ignore__",
      "raccoon": "__ignore__",
      "tree": "__ignore__",
      "__other__": "__ignore__"
    }
  }
}
</pre>
</details>
