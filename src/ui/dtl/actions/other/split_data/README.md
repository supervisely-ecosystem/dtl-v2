# Split Data

`Split Data` splits the input data into datasets based on condition.

If input project/dataset contains nested datasets data from them will be distributed across splits, and the final project will not include nested datasets.

### Settings

There are 4 ways of splitting the data:

- **percent**: data will be spread across datasets divided by the percentage of total images count.

- **number**: Each dataset will contain selected number of images. The last split will contain fewer images if the total number of images isn't evenly divisible by the selected number of images per split.

- **classes**: data will be split based on the presence of objects of annotation classes. Please note that when using this method the final project will likely include more images than the input project, as images are being duplicated into different datasets when there are more than one unique annotation class on it. Images with no annotations will be placed in the "unlabeled" dataset.

- **tags**: data will be split based on the presence of image and object tags on the image. Please note that when using this method the final project will likely include more images than the input project, as images are being duplicated into different datasets when there are more than one unique image/object tag on it. Images with no tags on them will be placed in the "unlabeled" dataset.

- **parts**: data will be split to equal parts (datasets) based on the number of parts specified. The last split will contain fewer images if the total number of images isn't evenly divisible by the number of parts.

### Example 1. Split Data by percentage

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original datasets</strong></td>
<td style="text-align:center; width:50%"><strong>Result: new datasets structure</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/user-attachments/assets/648e3b4e-a532-4b53-bec5-c51c89ea5474" alt="Original datasets"/> </td>
<td> <img src="https://github.com/user-attachments/assets/7085afee-a0ef-4ea1-bcec-bfb578d0265f" alt="Result datasets"/> </td>
</tr>
</table>

### Example 2. Split Data by classes

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original datasets</strong></td>
<td style="text-align:center; width:50%"><strong>Result: new datasets structure</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/user-attachments/assets/b373cc3b-f288-46d3-a40e-b1ea3173935b" alt="Original datasets"/> </td>
<td> <img src="https://github.com/user-attachments/assets/4b44ec7b-e25a-43db-bde1-eada8561548c" alt="Result datasets"/> </td>
</tr>
</table>

*in this instance, the amount of images more than doubled: the input project contained 953 images, and the output project contains 2213 images, because on average each image contained more than 2 unique annotation classes on it*

<details>
  <summary>JSON view</summary>
<pre>
  "action": "split_data",
  "src": {
    "source": [
      "$images_project_1"
    ]
  },
  "dst": "$split_data_2",
  "settings": {
    "split_method": "classes",
    "split_ratio": 50,
    "split_num": 50
  }
</pre>
</details>
