# Multiply

This action `multiplies` images by given value.

### Settings:

- **Multiply number** (_int_ - multiply value)

## Example:

#### Multiply

Json config example:

```json
{
  "action": "multiply",
  "src": ["$data_5"],
  "dst": "$multiply_12",
  "settings": {
    "multiply": 2
  }
}
```

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Multiply</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/22476d1c-684b-4ce0-9675-ba5fc5b34370" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/a1b22351-c8b9-406e-8bce-37af6e13c2fa" alt="Multiply" /> </td>
</tr>
</table>
