# Python Example Script

This is a simple example of a Python script that can be run from the command line. First, create a virtual environment and install the necessary dependencies

```bash
conda create -n canonical python=3.10
conda activate canonical
pip install -r requirements.txt
```

Next, create a `.env` file in the root of the project with the following contents:

```bash
cp .env.example .env
```

Then, replace the `CANONICAL_API_KEY` and the `OPENAI_API_KEY` values in the `.env` file with their actual values.

Then, run the script:

```bash
python example.py
```
