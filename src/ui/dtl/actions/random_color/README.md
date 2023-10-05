# Random Color

`Random Color` layer changes image colors by randomly moving each of RGB components.
Pixels (in matrix of width 3) are right multiplied by a random matrix A using the following formula:

```python
A = np.eye(3) + np.random.randn(3, 3) * strength / 5
```

### Settings

- **strength** — color multiplier strength. min: 0, max: 1

### Example

<table>
<tr>
<td style="text-align:center"><strong>Original image</strong></td>
<td style="text-align:center"><strong>Random color image</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/f84cd464-d0f2-4823-bf96-23562ed58846" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/dtl-v2/assets/79905215/661b5d83-a91e-4ee6-a0e9-a1d5ed3b9c29" alt="Random color image" /> </td>
</tr>
</table>

### JSON view

<details>
  <summary>JSON view</summary>
```json
{
    "action": "random_color",
    "src": [
        "$data_12"
    ],
    "dst": "$random_color_21",
    "settings": {
        "strength": 0.65
    }
}
```
</details>
