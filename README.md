# CSCAL
Class structure-aware adversarial loss for cross-domain human action recognition

## Requirements
Tested with:
* Ubuntu 18.04.2 LTS
* PyTorch 1.6.0
* Torchvision 0.7.0
* Python 3.7.3
* CUDA 10.2
* CuDNN 7.6.5

## Data Preparation
Download the Dataset from https://github.com/cmhungsteve/TA3N

## Usage
#### For testing
You can download the pre-trained model from https://pan.baidu.com/s/1I4d4Ijc4IYnKkTYLLYNIsA, code: yd8h, and run the script as below:

```
# one example
python CSCAL_test_models.py
```

#### For training the model from scratch
python CSCAL_train_adv.py
