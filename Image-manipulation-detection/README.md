# Image manipulation detection

A library for benchmarking of image manipulation detection. This supports 3 classes of algorithms :

- Perceptual hashing methods (fast and simple methods designed for image forensics). The following algorithms are implemented in `hashing/imagehash.py` (taken and modified from [here](https://github.com/JohannesBuchner/imagehash)):
    - Average Hash
    - Perceptual hash
    - Difference hash
    - Wavelet hash
    - Crop resistant hash
    - Color hash
    - Histogram hash


- Features extractors and descriptors (designed for object/scene retievals). The following algorithms are supported in `hashing/featurehash.py` :
    - SIFT
    - ORB
    - FAST + LATCH
    - FAST + DAISY


- Neural networks (deep CNNs) whose features from last layers have been shown to provide high descriptors of the image (regardless of the specific task the network was designed for, e.g classification). The following architectures are supported (note that each network was pretrained on ImageNet either for classification or by contrastive self-supervised learning) in `hashing/neuralhash.py`:
    - inception v3 (classification)
    - EfficientNet B7 (classification)
    - ResNets with different depth and width multipliers (classification)
    - SimCLR ResNets (contrastive learning). Link to [paper](https://arxiv.org/abs/2002.05709) and [github](https://github.com/google-research/simclr).

The specific goal here is more to detect crude near duplicate image manipulations than to perform object or scene retrival.

# Pre-trained SimCLR models 

The pre-trained SimCLR models are not available in this repository due to their large size. To download them, please navigate to the path where you cloned the repo and run the following files from your terminal :

```
cd path_to_repo/hashing/SimCLRv1
python3 download.py 
```

This will download the files containing the models definitions to the current folder and convert them to Pytorch. The folder `tf_checkpoints` contains the Tensorflow definition of the models (directly downloaded from the [github of the authors](https://github.com/google-research/simclr)), and can be safely erased if you wish to save some disk space. 

The exact same procedure will download the models for SimCLRv2 : 

```
cd path_to_repo/hashing/SimCLRv2
python3 download.py 
```

By default, this will only download one model. To download the others, please have a look at the `--model` argument. If unsure what is accepted, please have a look at the help message :

> python3 download.py -h

# Usage

The basic usage for performing an experiment is 

> python3 main.py result_folder

Digest from the experiment will then be saved into `Results/result_folder`. Details are given below.

This library was created to benchmark all the different methods presented above. The easiest way for this is to choose a dataset, randomly split it in 2 parts (experimental and control groups), and sample a given number of images in both groups on which you can perform artificial attacks defined in `generator/generate_attacks.py`. The scripts `create_groups.py` and `create_attacks.py` perform those tasks, and save the images with correct name format for later matching.

Then given a database of images, an experimental group of images that are manipulations of some images in the database (all attacks on the images sampled from experimental group) and a control group containing images not present in the database (all attacks on the images sampled from control group), datasets can be declared in the following way (here with the BSDS500 dataset as an example) :

```
import hashing 
from helpers import utils

path_database = 'Datasets/BSDS500/Experimental/'
path_experimental = 'Datasets/BSDS500/Experimental_attacks/'
path_control = 'Datasets/BSDS500/Control_attacks/'

positive_dataset = hashing.create_dataset(path_experimental, existing_attacks=True)
negative_dataset = hashing.create_dataset(path_control, existing_attacks=True)
```

Additionally, if one wants to perform attacks at experiment time, without having to save them to disk (experiment will take more time but this will save storage space), it can be done as

```
path_dataset = 'Datasets/...'

dataset = hashing.create_dataset(path_dataset, fraction=0.3, existing_attacks=False):
```

where `fraction` is the fraction of the dataset on which attacks will be performed (give 1 for each image in the dataset).

Then declare the methods and algorithms you wish to use, along with thresholds for the matching logic, e.g :

```
algos = [
        hashing.ClassicalAlgorithm('Phash', hash_size=8),
        hashing.FeatureAlgorithm('ORB', n_features=30),
        hashing.NeuralAlgorithm('SimCLR v1 ResNet50 2x', device='cuda', distance='Jensen-Shannon')
        ]

thresholds = [
    np.linspace(0, 0.4, 20),
    np.linspace(0, 0.3, 20),
    np.linspace(0.3, 0.8, 20),
    ]
```

A list of all valid algorithms names can be found in `hashing/general_hash.py`, or equivalently by accessing the variable `ADMISSIBLE_ALGORITHMS` : 

```
import hashing
print(hashing.ADMISSIBLE_ALGORITHMS)
```

Valid arguments for an algorithm can be found looking at the docstrings for each of the three classes `hashing.ClassicalAlgorithm` (corresponding to perceptual hashing methods), `hashing.FeatureAlgorithm` (keypoint-related or *feature* extractors methods), and `hashing.NeuralAlgorithm` (obviously neural based methods).

Finally perform the benchmark and save the results :

```
save_folder = utils.parse_input()

digest = hashing.total_hashing(algos, thresholds, path_database, positive_dataset, negative_dataset, general_batch_size=64)
                               
utils.save_digest(digest, save_folder)
```

All this is contained in `main.py`. 

The final digest is composed of 6 files : `general.json` with general metrics for all the experiment, `attacks.json` containing the metrics for each types of attack, `images_pos.json` and `images_neg.json` containing number of correct/incorrect detection for each image in the database respectively, and `match_time.json` and `db_time.json` respectively containing the time (s) for the matching phase and the the database creation phase.

# Figure generation

To process and create figures from the digest, one can look into `process.py`. Figure generation is contained in `helpers/create_plot.py`. Note that by default this will require a LaTeX installation on the machine running the process. This can be disabled in `helpers/configs_plot.py`.

# Datasets

We used 3 datasets that can be found online, and for which we performed the splitting. They are the [BSDS500 dataset](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/resources.html), [ImageNet validation set (ILSVRC2012)](https://www.image-net.org/) and the [Kaggle memes dataset](https://www.kaggle.com/datasets/gmorinan/most-viewed-memes-templates-of-2018). For the kaggle memes dataset, one then need to run `data_retrieval/kaggle_splitter.py` to extract templates and annotate correctly the memes.

# Computational setup

For neural methods, use of a GPU is almost essential for computational efficiency. Other classes of methods do not rely on it, and their computations are performed exclusively on CPU.

# Results

(Excluded from anonymous submission)

The repository contains the folder `Results` containing digests from our own experiments. Each experiment contains a file `Experiment.yml` quickly summarizing the parameters for the experiment. You are free to look at it and perform the same benchmarks if you wish to verify results.

Additionally, people may use the data from the digest of our experiments and just recreate figures, using the experiment name along with `helpers/create_plot.py` functions. Examples are provided in `process.py`.