# Thomas's functions for stuff

For anyone in the future reading this, I'm sorry I didn't have time to fully flesh out the examples or make clean markdown documentation. You'll have to rely on the incomplete examples and the docstrings. Unfortunately, the examples in the Summer 2024/Masking/***.ipynb files use functions that are slightly different from the polished ones in the python files here, so just be careful about that.

Some functions have examples provided in notebooks in the examples folder. If not, the files in the examples folder should give directions to notebooks in Summer 2024/Masking. However, those, as I mentioned, use slightly different functions, so just look at them for the general idea, but make sure you're following the ones in the python files here.

## Dependencies

These functions depend on the following python libraries:
* Numpy
* Pandas
* Matplotlib
* Scipy

I would recommend working in a conda environment, but you could use any python interpreter. For the examples files, make sure you're using something that can support Jupyter notebooks.

For a conda environment, run this in the command line:
```
conda install numpy pandas matplotlib scipy
```

For a python venv or local installation:
```
python3 -m pip install numpy pandas matplotlib scipy
```

## Plotting

Found in functions/plots.py; examples in examples/plotting_examples.ipynb

## Masking analysis

Found in functions/masking_analysis.py; examples in examples/masking_analysis_examples.ipynb

## Circadian model simulations

Ok I'm really sorry about the examples on this one. I just didn't have time to make fully polished examples for the examples folder. The documented functions are in functions/circadian_model.py. You can find the work I've done with the models in a few different notebooks from Summer 2024/Masking:
* poincare-oscillator.ipynb
* oscillator_entrainment_graph.ipynb
* locomotor_simulation.ipynb