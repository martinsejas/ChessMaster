# ChessMaster

Computer Vision AI that detects positions on a Chess Board.

**The main notebook can be found in *notebooks/martin-chess-interpreter.ipynb***

Please refer to the Kaggle dataset: 
[Chess Positions](https://www.kaggle.com/datasets/koryakinp/chess-positions)

The original dataset is over 100k images, I only used a total of 4.2k

Final Accuracy was : 97%

## Steps to Run it

Make sure to clone this repository using: 
```bash
git clone https://github.com/martinsejas/ChessMaster.git
```


Once you have cloned it, go to the root of the repository and install the project requirements with:

```bash
pip install -r requirements.txt
```

Once you have done this, you simply have to run the *prediction_script.py* which will guide you to choose an image from your computer to predict.

The model is saved under *models/martin_chess.joblib*


