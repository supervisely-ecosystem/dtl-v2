# Noise

Noise layer (`noise`) adds noise of Gaussian distribution to the images.

### Settings:

- **Mean**:
  - _int_. Possible values: number
- **Spread**:
  - _int_. Possible values: number

### Example:

#### Noise: Mean: 13, Spread: 65

Json config example:

```json
{
  "action": "noise",
  "src": ["$data_5"],
  "dst": "$noise_10",
  "settings": {
    "mean": 13,
    "std": 65
  }
}
```

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Noise: Mean: 13, Spread: 65</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/22476d1c-684b-4ce0-9675-ba5fc5b34370" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/6005c07c-8f5f-41da-8e69-c415c6191f58" alt="Noise: Mean" /> </td>
</tr>
</table>
