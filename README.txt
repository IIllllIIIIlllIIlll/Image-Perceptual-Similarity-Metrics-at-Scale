# README

## Code repositories

To facilitate the understanding and code re-use, the supporting code has been split into two. 

1. "Image Manupulation Detection" evaluates the performance of different metrics and their robustness to perturbations, parameters  and metrics sweeps and results trasnferability from synthetic dataset to real-world memes
2. "Feature Search At Scale" focuses on task relative to unsupervised image clustering. That latter part contains large sections of code corresponding to experiments that were not included into paper, but to validate in principle some of our statements - eg. regarding SimCLR v2 fine-tuning.

## Memes-Clean dataset

The memes-clean dataset was created by removing the following non-perceptual templates from the 2018 most popular Reddit memes dataset. We believe that this analysis would require methods to parse the text specifically, that is indicative of the template (eg "you-vs-the-guy") or a more extensive understanding of context by  joint text/image models. Neither of them being within the scope of this paper, we proceeded to remove non-perceptual templates.

Specific templates removed are:

- 'zuckerberg',
- 'harold',
- 'netflix-adaptation',
- 'shrek',
- 'so-glad',
- 'who-would-win',
- 'you-vs-the-guy',
- 'skyrim-100',


## 4chan Dataset. 

Due to the content, the dataset should be asked directly from the authors of the ICWSM 2021 Memes, Radicalisation, and the Promotion of Violence on Chan Sites paper. 

After the data is donwloaded and fully decompressed, `Feature-search-at-scale/data_retrieval/chan_prefilter.py`, once modified to set local root directory and executed, will extract and check for integrity images from the 4chan /pol/ and /k/ boards in the dataset.

To process it, the function `get_features` in `Feature-search-at-scale/clustering/tools.py` will need to be hard patched, as indicated in the #TODO marker in the file. 

DBSCAN sweep was then performed with the following stops: 
 - min_cluster=3, min_intercluster_distance=5.250
 - min_cluster=4, min_intercluster_disatnce=3.500
 - min_cluster=7, min_intercluster_disatnce=4.000