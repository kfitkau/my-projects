# This is my GermEval21 elaboration

## Overview
Germeval is a shared task and evaluation campaign for natural language processing (NLP) and computational linguistics tasks related to the German language. Germeval21, short for 'German Evaluation Campaign of Natural Language Processing and Computational Linguistics Systems,' is a pivotal event in the world of natural language processing and computational linguistics. Germeval 2021 Shared Task on the Identification of Toxic, Engaging, and Fact-Claiming Comments. This is my Approach to the Task with finetuning the library models for sequence classification

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [License](#license)

## Getting Started

You can see the results at [this repository](https://github.com/kfitkau/my-projects/tree/main/germeval21/germeval21.pdf), but if you want to try out the Jupyter Notebook yourself, you should follow these instructions:

### Prerequisites

- Python 3.10 or later
- Jupyter Notebook

### Installation

1. Clone the repository to your local machine:

 ```bash
   git clone https://github.com/kfitkau/my-projects.git
 ```

2. Navigate to germeval21
```bash
  cd germeval21
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
  jupyter lab germeval21.ipynb
 ```

## Usage
Open the GermEval21 at http://localhost:8888/lab/tree/germeval21.ipynb and run the cells.
This is my Approach to the Task with finetuning the library models for sequence classification on the models: "german-nlp-group/electra-base-german-uncased"
In cell 7 you can exchange the model name with any other model that is aligned for text classification.
To do this, you can select other models at [https://huggingface.co/models](https://huggingface.co/models) using the "Text Classification" filter.
Click on a model and copy model name to clipboard (example: "ml6team/distilbert-base-german-cased-toxic-comments") and put it in cell 7 at model_name.
Example: model_name = 'german-nlp-group/electra-base-german-uncased' -> model_name = 'ml6team/distilbert-base-german-cased-toxic-comments'

## License
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
MIT License

Copyright (c) [2021] [Kevin Fitkau]

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
