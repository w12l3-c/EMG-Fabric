# EMG-Fabric
Waterloo Biotron EMG Fabric SubTeam

The Python Script is going to be mounted on the Raspberry Pi which contains the functions of read and write files such that we can achieve real time collecting data + real time predicting with the ML model below. It will also be used to control motion on another 3D prosthetic arm (hopefully).

The model file contains the ML code for predicting the EMG signal recieved from our own designed EMG sesing sleeve.

<a target="_blank" href="https://colab.research.google.com/github/w12l3-c/EMG-Fabric/blob/main/EMG.ipynb">
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

---
Model Task:
- Process the signal into two categories: Grapse and Open

---
Preprocessing:

There are different datasets and each used different preprocessing method
For our own data:
- Signal Processing such as Bandpass and Lowpass
- Normalizing the Data

---
Model Summary(By Ranking):
- Using LightBGM to fit and train on the data of both dataset
  - LightBGM has the best result with 95% F1 score on multi-classification task of Rock Paper Scissors
  - LightBGM is overfitting our own data so we need more data and channels to get a better result
- Using a transfer learning method for Deep Neural Network Binary Classification
  - The base model is trained first with about 10K parameters on a richer database of EMG rock paper scissors from Kaggle
  - Retrain the model with about 1K parameter on our own collected data which can be found in this [repo](https://github.com/jacq-lee/emgFabric)
  - The Result of this DNN is about 95% accuracy on our own data and 85% on Rock Paper Scissors
- Using K-Means and Weighted K-Means
  - It is bad with Accuracy of 65% on Rock Paper Scissors and training time is doubling from DNN
  
---
Which model to use:

Depend on which model has better compatibility with the hardware such as Raspberry Pi and Arduino

---
Future ideas?:
- idk ¯\_(ツ)_/¯ ask the team leads



