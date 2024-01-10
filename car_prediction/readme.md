# This is my Car Prediction elaboration

## Overview

The used car analysis involved applying different regression models to different car brands to evaluate their predictive performances. The models were evaluated using two key metrics, the coefficient of determination (r2_score) and the mean squared error (MSE). Here are the key results for each model type:
1. Linear regression:
   * r2_score: 0.7251
   * MSE: 5182.27
   * The linear regression model shows a mediocre performance with room for improvement as the r2_score is not high and the MSE is relatively high.
  
2. Random Forest Regressor:
   * Example for Mercedes:
     * r2_score: 0.9578
     * MSE: 2333.89
   * The Random Forest models deliver very good results overall for different car brands with high r2_scores and low MSE values. They outperform other models in terms of predictive performance.

3. Decision Tree Regressor:
   * Example for Mercedes:
     * r2_score: 0.9539
     * MSE: 2438.82
   * The decision tree models achieve good results, but slightly worse compared to the random forest models.

4. Support Vector Regressor:
   * Example for Mercedes:
     * r2_score: -0.4870
     * MSE: 13849.90
   * The Support Vector Regression models show overall poor performance with negative r2_scores and high MSE values. They may not fit the available data well.

5. KNN regressor:
   * Example for Mercedes:
     * r2_score: 0.3576
     * MSE: 9103.02
   * The KNN models show mixed results with some good r2_scores, but also some negative values and relatively high MSE values.


**Conclusion:**
The Random Forest models are shown to be the overall best choice for predicting used car prices, as they have both high r2_scores and low MSE values for different car brands. The Decision Tree models are acceptable, while the Linear Regression, Support Vector Regression and KNN models show lower performance. It is emphasized that further optimization of the hyperparameters and careful data cleaning could lead to improved results.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [License](#license)

## Getting Started

You can see the results at [this repository](https://github.com/kfitkau/my-projects/blob/main/car_prediction/ML_Ausarbeitung.ipynb), but if you want to try out the Jupyter Notebook yourself, you should follow these instructions:

### Prerequisites

- Python 3.10 or later
- Jupyter Notebook

### Installation

1. Clone the repository to your local machine:

 ```bash
   git clone https://github.com/kfitkau/my-projects.git
 ```

2. Navigate to car_prediciton
```bash
  cd car_prediction
```

3. Create a virtual environment with python
```bash
  python -m venv venv
```

4. activate the virtual environment
```bash
  .\venv\Scripts\activate
```

5. Install the required Python packages
```bash
  pip install -r requirements.txt
```

6. Open the jupyter notebook
```bash
  jupyter lab ML_Ausarbeitung.ipynb
 ```

7. Open the Car Prediction at http://localhost:8888/lab/tree/ML_Ausarbeitung.ipynb and run the cells.
The data for the elaboration comes from the Kaggle platform. This step can be skipped to the Chapter 3 if the data has already been downloaded.
If the csv files have been lost, please refer to chapter 2 in the ML_Engineering.ipynb

## License
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
MIT License

Copyright (c) [2023] [Kevin Fitkau]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED,
