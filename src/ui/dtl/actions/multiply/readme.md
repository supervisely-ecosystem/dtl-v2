# Multiply

`Multiply` layer duplicates the image and annotations (multiplying by a given value).

### Settings:

- **multiply** - Set the value to multiply by. For example, if you set the value to 2, then the image and annotations will be duplicated twice.

## Example. Duplicate images with annotations

<table>
<tr>
<td style="text-align:center; width:33%"><strong>Original images</strong></td>
<td style="text-align:center; width:66%"><strong>Multiplied images</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/97c952d1-ecb8-4edb-9e22-b4b480f33a8e" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/7080258c-5bf8-46d1-947b-cfab4612479d" alt="Multiply" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
<pre>
{
  "action": "multiply",
  "src": ["$data_7"],
  "dst": "$multiply_9",
  "settings": {
    "multiply": 2
  }
}
</pre>
</details>
