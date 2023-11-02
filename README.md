<div align="center" markdown>

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

<details>
<summary>Click to expand the list of available nodes</summary>

Input:

- [Images Project](/src/ui/dtl/actions/data/README.md#images-project)

Pixel-level transformations:

- [Blur](/src/ui/dtl/actions/blur/README.md#blur)
- [Contrast Brightness](/src/ui/dtl/actions/contrast_brightness/README.md#contrast-and-brightness)
- [Noise](/src/ui/dtl/actions/noise/README.md#noise)

Spatial-level transformations:

- [Crop](/src/ui/dtl/actions/crop/README.md#crop)
- [Flip](/src/ui/dtl/actions/flip/README.md#flip)
- [Instances Crop](/src/ui/dtl/actions/instances_crop/README.md#instances-crop)
- [Multiply](/src/ui/dtl/actions/multiply/README.md#multiply)
- [Resize](/src/ui/dtl/actions/resize/README.md#resize)
- [Rotate](/src/ui/dtl/actions/rotate/README.md#rotate)
- [Sliding Window](/src/ui/dtl/actions/sliding_window/README.md#sliding-window)

Annotation-level transformations:

- [Approx Vector](/src/ui/dtl/actions/approx_vector/README.md#approx-vector)
- [Background](/src/ui/dtl/actions/background/README.md#background)
- [BBox](/src/ui/dtl/actions/bbox/README.md#bounding-box)
- [Mask to Lines](/src/ui/dtl/actions/bitmap2lines/README.md#mask-to-lines)
- [Bbox to Polygon](/src/ui/dtl/actions/bbox2poly/README.md#bbox-to-polygon)
- [Bitwise Masks](/src/ui/dtl/actions/bitwise_masks/README.md#bitwise-masks)
- [Change Classes Colors](/src/ui/dtl/actions/color_class/README.md#change-classes-colors)
- [Drop By Class](/src/ui/dtl/actions/drop_obj_by_class/README.md#drop-by-class)
- [Drop Lines By Length](/src/ui/dtl/actions/drop_lines_by_length/README.md#drop-lines-by-length)
- [Drop Noise](/src/ui/dtl/actions/drop_noise/README.md#drop-noise)
- [Duplicate Objects](/src/ui/dtl/actions/duplicate_objects/README.md#duplicate-objects)
- [Mask to Polygon](/src/ui/dtl/actions/find_contours/README.md#mask-to-polygon)
- [Line to Mask](/src/ui/dtl/actions/line2bitmap/README.md#line-to-mask)
- [Merge Masks](/src/ui/dtl/actions/merge_bitmaps/README.md#merge-masks)
- [ObjectsFilter](/src/ui/dtl/actions/objects_filter/README.md#objects-filter)
- [Polygon to Mask](/src/ui/dtl/actions/poly2bitmap/README.md#polygon-to-mask)
- [Random Colors](/src/ui/dtl/actions/random_color/README.md#random_color)
- [Rasterize](/src/ui/dtl/actions/rasterize/README.md#rasterize)
- [Rename](/src/ui/dtl/actions/rename/README.md#rename)
- [Skeletonize](/src/ui/dtl/actions/skeletonize/README.md#skeletonize)
- [Split Masks](/src/ui/dtl/actions/split_masks/README.md#split-masks)
- [Tag](/src/ui/dtl/actions/tag/README.md#tag)

Other:

- [Dataset](/src/ui/dtl/actions/dataset/README.md#dataset)
- [Dummy](/src/ui/dtl/actions/dummy/README.md#dummy)
- [If](/src/ui/dtl/actions/if_action/README.md#if-action)

Output:

- [Export Archive](/src/ui/dtl/actions/save/README.md#export-archive)
- [Export Archive with Masks](/src/ui/dtl/actions/save_masks/README.md#export-archive-with-masks)
- [New Project](/src/ui/dtl/actions/supervisely/README.md#new-project)

</details>

#### Key features:

- **Transform Data:** Apply a wide variety of data transformation operations to images within a project. These transformations include rotation, cropping, blurring, resizing, and many more.

  ![transform-data](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/6b1fb925-1961-44cc-be6c-2777294f7f06)

- **Enhance Data:** Improve the quality and usability of your image data by adjusting contrast, brightness, and noise levels.

- **Object-Level Manipulation:** Perform operations on individual objects or instances within images, such as cropping, duplicating, or changing their color classes.

  ![object-transforms](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/b16b6767-403b-49f4-be9e-6aa0dcbb0c2d)

- **Customize Workflows:** Create complex data transformation workflows by combining multiple transformation nodes to meet your specific requirements.

- **Node Documentation:** Detailed documentation is available for each transformation node, explaining how to use it effectively. These guides provide step-by-step instructions and examples for each node, making it easy for users to understand and leverage the full power of the application.

  ![node-docs](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/91c82b09-4ea4-444a-9819-f2dbf5d28f2b)

- **Save & Load Presets:** Save your customized transformation workflows as presets for future use. This feature allows you to store and reuse your preferred configurations quickly.

  ![load-preset-min](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/c3a262fb-41c8-4116-8efd-beaadcd8f62b)

- **Output Flexibility:** Choose from multiple export options to save your transformed data in a format that best suits your needs.

  ![merge-projects](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/17fd2b98-66ed-496c-a2b5-f8a43b0d3910)

## How To Run

**Step 1:** Run the application from the ecosystem, project, dataset or preset file.

**Step 2:** Wait until the app is started and open the app.

Once the app is started, new task appear in workspace tasks. Wait for the message `Application is started` and then press `Open App` button.

![run-app](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/c3fee897-9aac-4f1b-be8b-893df3839202)
