<div align="center" markdown>

<img src="https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/73838fba-d57b-4405-9db5-80e3514f9983"/>

# Data Nodes
  
<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervisely.com/apps/supervisely-ecosystem/data-nodes)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/data-nodes)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/data-nodes.png)](https://supervisely.com)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/data-nodes.png)](https://supervisely.com)

</div>

## Overview

This application is a versatile tool designed for data transformation tasks (like filtering and augmentation). It allows you to create and manage Data transformation workflows by leveraging graphical nodes with settings.

<details open>
<summary><b>Available nodes</b></summary>

Input:

- [Images Project](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/data/README.md#images-project)

Pixel-level transformations:

- [Anonymize](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/anonymize/readme.md#anonymize)
- [Blur](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/blur/README.md#blur)
- [Contrast Brightness](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/contrast_brightness/README.md#contrast-and-brightness)
- [Noise](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/noise/README.md#noise)
- [Random Color](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/random_color/README.md#random_color)

Spatial-level transformations:

- [Crop](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/crop/README.md#crop)
- [Flip](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/flip/README.md#flip)
- [Instances Crop](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/instances_crop/README.md#instances-crop)
- [Multiply](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/multiply/README.md#multiply)
- [Resize](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/resize/README.md#resize)
- [Rotate](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/rotate/README.md#rotate)
- [Sliding Window](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/sliding_window/README.md#sliding-window)

Annotation-level transformations:

- [Approx Vector](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/approx_vector/README.md#approx-vector)
- [Background](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/background/README.md#background)
- [BBox](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/bbox/README.md#bounding-box)
- [Mask to Lines](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/bitmap2lines/README.md#mask-to-lines)
- [Bbox to Polygon](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/bbox2poly/README.md#bbox-to-polygon)
- [Bitwise Masks](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/bitwise_masks/README.md#bitwise-masks)
- [Change Classes Colors](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/color_class/README.md#change-classes-colors)
- [Drop By Class](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/drop_obj_by_class/README.md#drop-by-class)
- [Drop Lines By Length](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/drop_lines_by_length/README.md#drop-lines-by-length)
- [Drop Noise](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/drop_noise/README.md#drop-noise)
- [Duplicate Objects](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/duplicate_objects/README.md#duplicate-objects)
- [Mask to Polygon](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/find_contours/README.md#mask-to-polygon)
- [Line to Mask](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/line2bitmap/README.md#line-to-mask)
- [Merge Masks](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/merge_bitmaps/README.md#merge-masks)
- [ObjectsFilter](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/objects_filter/README.md#objects-filter)
- [Polygon to Mask](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/poly2bitmap/README.md#polygon-to-mask)
- [Rasterize](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/rasterize/README.md#rasterize)
- [Rename](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/rename/README.md#rename)
- [Skeletonize](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/skeletonize/README.md#skeletonize)
- [Split Masks](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/split_masks/README.md#split-masks)
- [Tag](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/tag/README.md#tag)

Filter and conditions:

- [Filter Image by Object](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/filter_image_by_object/readme.md#filter-image-by-object-action)
- [Filter Image by Tag](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/filter_image_by_tag/readme.md#filter-images-by-tag-action)
- [Filter Image without Object](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/filter_images_without_objects/README.md#filter-image-without-objects)
- [If](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/if_action/README.md#if-action)

Neural networks:

- [Apply NN](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/apply_nn/README.md#apply-nn)

Other:

- [Dataset](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/dataset/README.md#dataset)
- [Dummy](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/dummy/README.md#dummy)

Output:

- [Export Archive](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/save/README.md#export-archive)
- [Labeling Job](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/labeling_job/README.md#labeling-job)
- [Export Archive with Masks](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/save_masks/README.md#export-archive-with-masks)- 
- [Add to Existing Project](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/existing_project/README.md#add-to-existing-project)
- [Create New Project](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/supervisely/README.md#create-new-project)

</details>

#### Key features:

- **Transform Data:** Apply a wide variety of data transformation operations to images within a project. These transformations include rotation, cropping, blurring, resizing, and many more.

  ![transform-data](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/58d857fe-91af-413b-995b-20c674d72a9f)

- **Use Neural Networks:** Apply deployed models on your data to perform object detection, instance segmentation, and other tasks. You can use any of the neural network models available in the Supervisely Ecosystem, or train your own custom models.
  
  ![apply-nn](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/9f715cf2-9106-47d0-bda3-500d2508f3b8)

- **Enhance Data:** Improve the quality and usability of your image data by adjusting contrast, brightness, and noise levels.

- **Object-Level Manipulation:** Perform operations on individual objects or instances within images, such as cropping, duplicating, or changing their color classes.

  ![object-transforms](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/34294f35-b720-4941-9e19-5fce70be9c33)

- **Customize Workflows:** Create complex data transformation workflows by combining multiple transformation nodes to meet your specific requirements.

- **Node Documentation:** Detailed documentation is available for each transformation node, explaining how to use it effectively. These guides provide step-by-step instructions and examples for each node, making it easy for users to understand and leverage the full power of the application.

  ![node-docs](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/6d5d1c8a-9a72-4827-9869-714b98b2e418)

- **Save & Load Presets:** Save your customized transformation workflows as presets for future use. This feature allows you to store and reuse your preferred configurations quickly.

  ![load-preset](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/5cd9ebb7-0fd5-4901-a1d3-9ecee38b629f)

- **Output Flexibility:** Choose from multiple export options to save your transformed data in a format that best suits your needs.

  ![merge-projects](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/1baaedff-3d02-46bb-a307-d690036509d2)

## How To Run

You can run the application from the ecosystem, project or saved preset file.

<details open>
<summary><b>1. Run App from Ecosystem</b></summary>

![run-from-ecosystem-min](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/4dc28226-74d6-4603-a282-bdb94270d893)

</details>

<details open>
<summary><b>2. Run App from Project</b></summary>

![run-from-project-min](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/c92ecdc6-c038-4f86-880c-b974183dc6ab)

</details>

<!-- <details open>
<summary><b>3. Run App from Team Files</b></summary>

![run-from-teamfiles-min](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/ae996fcb-b9e0-4b1a-a514-bfab1097b40d)

</details> -->
