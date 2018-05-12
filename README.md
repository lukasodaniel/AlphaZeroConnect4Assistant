# Deep Reinforcement Learning

## Using concepts from AlphaZero on Connect4 for applications in enabling technologies

This project is a fork of [this repo](https://github.com/AppliedDataSciencePartners/DeepReinforcementLearning) which was written about in detail in [this article](https://medium.com/applied-data-science/how-to-build-your-own-alphazero-ai-using-python-and-keras-7f664945c188). Over the course of half a semester I modified this to be run UNC's Olympia server, trained several different networks, and created a small web app to hand test the progress of the different trained players. I then used the trained network to recommended moves, with the intention of increasing accessibility of the strategic game to all cognitive abilities. 

## Getting Started

It would be best to start by reading the original [article](https://medium.com/applied-data-science/how-to-build-your-own-alphazero-ai-using-python-and-keras-7f664945c188) and gaining some familiarity with the AlphaZero algorithm ([cheatsheet here](https://medium.com/applied-data-science/alphago-zero-explained-in-one-diagram-365f5abf67e0), from the creators of the artcile).

It would also be beneficial to familiarize oneself with how to use the different command line features of the different NVIDIA tools detailed in "Prerequisites" and how to control the NVIDIA hardware through the command line. 

### Prerequisites

Python and pip

This project uses [pipenv](https://github.com/pypa/pipenv). This should be enough to start working without a GPU. 

The Olympia and Classroom servers run tcsh by default, but I have had much more success using bash, especially with anything using pipenv.

#### With a GPU

For the code to run properly on a GPU you will need to install all of the [requirements for Tensorflow GPU](https://www.tensorflow.org/install/install_linux#nvidia_requirements_to_run_tensorflow_with_gpu_support) (under "NVIDIA requirements to run TensorFlow with GPU support"). 

The steps listed in that link are not the order in which those installations must be performed, nor do the versions listed on the Tensorflow website work with these particular versions of Python or Tensorflow. Listed below are the specific combination working with this Pipfile on Olympia. 

It is necessary to install the following in order:
	1. [Your appropriate NVIDIA driver](http://www.nvidia.com/Download/index.aspx?lang=en-us)
	2. [CUDA Toolkit 8.0](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)
		Append appropriate path to LD_LIBRARY_PATH enviornment variable 
			Note: This information is not about verison 8.0, you must follow these same instructions with the legacy version 8.0 available for download [here](https://developer.nvidia.com/cuda-toolkit-archive)
	3. [cuDNN SDK v5.1](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/)
		Ensure that you create the CUDA_HOME environment variable as described in the NVIDIA documentation
		Also ensure that the cuDNN you are getting is the for the proper version of the CUDA toolkit


You can ensure that you have properly installed the above by running the [verification steps of the cuDNN installation guide](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/#verify)
```
cp -r /path/to/cudnn_samples_v7/ $HOME # or whichever writable directory
cd $HOME/cudnn_samples_v7/mnistCUDNN
make clean && make
./mnistCUDNN
```

### Installing

#### With a GPU

By default the Pipfile is set to be run on an environment without a GPU.

If you plan to run this code using a GPU you must first modify the Pipfile by commenting out the "tensorflow" requirement on like 30 and deleting the leading '#' on line 29 resulting in the following: 
```
tensorflow-gpu = "==1.1.0" # uncomment for use on GPU
#tensorflow = "==1.1.0"		# comment out when using on system with GPU 
```

#### With and without a GPU

Install all of the Python dependencies by navigating to the root directory of this project and then entering.
```
pipenv install
```
As of May 8, 2018, this does not have any dependency issues, although there are deprecation warnings. Previously there was some sort of dependency cycle that could not be resolved, but installing using `--skip-lock` worked properly. 

Now we have a virtual environment with all of the necessary Python packages and if we use `pipenv shell` we can now execute anything within this virtual environment. 

If planning on using a GPU for training, the biggest thing to test at this point is if the GPU device is visible from Tensorflow, which can be done with by first starting the Virtual environment shell (`pipenv shell`), and then starting a python session (`$ python`) and running:
```
import tensorflow
from tensorflow.python.client import device_lib
device_lib.list_local_devices() # output should include multiple device descriptions one of which containing "GPU" under the name field
```

It is very possible that didn't work, there seem to be a few issues with versions of Tensorflow and newer NVIDIA drivers/tools. To reiterate, with these versions of Keras and Tensorflow on Olympia CUDA Toolkit 8.0 and cuDNN v5.1 ran properly. 

## Running the Jupyter Notebook

The basic idea of most of the functionality can be viewed in the run.ipynb notebook. 

### Running locally

Run by
```
pipenv shell
jupyter notebook
```

And navigate to `run.ipynb`.

### Tunnelling traffic to use the server

Run the jupyter notebook headless on the server with: 
```
jupyter notebook --no-browser --port=12345 # or any port
```

Then on your local machine establish an SSH tunnel with:
```
ssh -N -f -L localhost:8888:localhost:12345 remote_user@remote_host
```

Note: if attempting to tunnel to the Olympia machine, you must first tunnel through another server, so this results in two ssh tunnels. 


## Running for extended periods of time without a GUI

The nature of this particular task will require long runs (overnight to a couple of days), too long to keep an instance of running in a Jupyter notebook. This is the intended use of `main.py`. There are several ways you could choose to run this for an extended period, (GB suggested tmux), but my preferred way was using nohup. On the server (or locally) you can kick off this by using `nohup python main.py`. The output from this file will go to `nohup.out` 

This will run infinitely in the background until you kill it or it fails due to some system error. You can check the progress by checking `nohup.out`. 

I tended to either use 
`tail nohup.out` 

to view the most recent activity or 

`cat nohup.out | grep "BEST"`
which gives a summary of how many iterations of the player this particular run had gone through.

### Picking up from a previous run with `initialise.py`

TODO

## Using the Web App

The web app is very bare bones and is mostly to demo how to use the trained models in practice. To run the web app navigate to the project enter the following into the terminal:
```
pipenv shell
python server.py
```
The project will now be running 

## Further Project Navigation

### `run` and `run_archive` directories

### `config.py`

### `games`

## Extending this project

## Built With

* [Keras](https://keras.io/) - Deep learning library sitting atop a Tensorflow backend
* [Tensorflow](https://www.tensorflow.org/) - Specifically improved by using Tensorflow GPU
* [Bottle](https://bottlepy.org/docs/dev/) - Barebones web framework used to make a quick API and UI


## Authors

* [**David Foster**](https://medium.com/@dtfoster) - *Writer of the original article and code* - [Applied Data Science](https://github.com/AppliedDataSciencePartners)

* [**Lukas O'Daniel**](https://github.com/lukasodaniel) - *Extended the original code*

## Acknowledgments

* Thank you very much to [David Foster](https://medium.com/@dtfoster) of [Applied Data Science](https://github.com/AppliedDataSciencePartners).
