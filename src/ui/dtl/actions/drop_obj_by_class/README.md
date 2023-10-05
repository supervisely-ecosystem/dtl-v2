# Drop by Class

`Drop by Class` layer simply removes annotations of specified classes.

> ℹ️ You can also use data layer and map unnecessary classes to \_\_ignore\_\_

### Settings

- **classes** — Select classes. All objects of selected classes will be removed.

### Example

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Remove objects of selected classes</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/d2fb3d97-d299-4720-bf7a-14232a840f6a" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/7ca78a5c-b5c8-4ec2-a319-23e20fe53437" alt="Drop by Class" /> </td>
</tr>
</table>

### JSON view


<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "drop_obj_by_class",
  "src": ["$data_1"],
  "dst": "$drop_obj_by_class_4",
  "settings": {
    "classes": ["cell phone", "computer", "notebook"]
  }
}
</pre>
</details>
