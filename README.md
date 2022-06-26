# MobileNet in PyTorch

## Main contribution
User can convert pretrained models **from official TensorFlow implementation** and many other versions to this **pytorch implementation**

## Examples
Pretrained model: https://drive.google.com/file/d/1gFH0c6YregiiFctTFBIjr_7ffHZIUfxp/view?usp=sharing  
Converted from official TensorFlow  
Top 1 Accuracy: 64.21% | Top 5 Accuracy: 85.12%  
Precision: 0.6613 | Recall: 0.6421 | F1 score: 0.6411  


Pretrained model: https://drive.google.com/file/d/1DC_cmYVzupC8kteOnOjZSKnB2_uTHqKZ/view?usp=sharing  
Converted from wjc852456's pretrained model (sgd) https://pan.baidu.com/s/1nuRcK3Z  
Top 1 Accuracy: 67.03% | Top 5 Accuracy: 87.73%  
Precision: 0.6773 | Recall: 0.6703 | F1 score: 0.6659  

Pretrained model: https://drive.google.com/file/d/1CSSJi0brQZ0Le89XtYvrXXfpaFLyusSg/view?usp=sharing  
Converted from wjc852456's pretrained model (sgd-rmsprop) https://pan.baidu.com/s/1eRCxYKU  
Top 1 Accuracy: 67.95% | Top 5 Accuracy: 88.13%  
Precision: 0.6870 | Recall: 0.6795 | F1 score: 0.6762  

## Todo
1. implement conversion for different res, alpha, class and mobile_net_v2
2. allow separating pretrained model from its classifying layer (the last linear layer) to adapt to different number of class
3. clean up convert.py codes
4. complete this README.md file
5. support quick start in Google Colab
6. apply tqdm to display progress
 