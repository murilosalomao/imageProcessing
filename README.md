# Detecting Text in Signs

## Main Objective
Given a picture containing a sign with some text in it, output one or more crops of the regions where the text is located.

## Dataset
The dataset used belongs to the ICDAR3 (2017) Competition. There were selected 100 pictures with signs that contain text. Some examples can be found under the **imgs** folder

The entire dataset can be found [here](https://rrc.cvc.uab.es/?ch=8&com=downloads).

## Description

Duo to the lack of well-annotated datasets of diverse signs, and the short amount of time to annotate enough images to train a neural network, that approach has been discarded. Hence, the new goal is to achieve the main objective by using Image Processing techniques only.

The script will run as follows:
1. Read a coloured image as **grayscale**;
1. Smooth the image with **Gaussian Blur**, so the acquisition of real edges is improved;
2. **Binarize** the image with a given threshold, so it turns into black and white;
3. Run some **Edge Detection** algorithm;
4. Approximate the edges to polygons, and find the ones with the same shape of the sign (rectangular or hexagonal, for example);
5. At this moment, we will have a few polygons, which can be the sign. To choose the correct one, we will examine:
    1. The polygon area. If it's greater than a given threshold and smaller than the image area;
    2. Its content. If there's no content, it's not a valid plate.
7. Output the crop where the text is located.

Additionally, different parameters values were analyzed for each of the algorithms.

## Running it

Run

**python detect-text-plates.py**

Press Enter, and then write the image name

**imgs/img_883.jpg**

An output.jpg should appear in the folder
