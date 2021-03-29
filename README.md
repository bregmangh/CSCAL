# CSCAL
Class structure-aware adversarial loss for cross-domain human action recognition

## Requirements
Tested with:
* Ubuntu 18.04.2 LTS
* PyTorch 1.1.0
* Torchvision 0.3.0
* Python 3.7.3
* GeForce GTX 1080Ti
* CUDA 9.2.88
* CuDNN 7.14

## Data Preparation
Download the Dataset from https://github.com/cmhungsteve/TA3N

## Usage
#### For testing
* You can simply copy any script to the main folder (same location as all the `.py` files), and run the script as below:
```
# one example
python CSCAL_test_models.py
```

#### For training the model from scratch
python CSCAL_train_adv.py
