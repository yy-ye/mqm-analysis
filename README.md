# MQM error analysis code and annotation result

by [Filip Klubička](https://github.com/GreenParachute/mqm-eng-cro) and Yuying Ye


## Contents

- **csv** annotated .csv file exported from translate5.
- **MQM_IAA_scripts** Python scripts to conduct the statistical analysis on MQM. output. The script **main.py** runs all the analysis.
- **202004232204** output of the analysis on two NMT systems.
-**extra_sys** additional annotation of the third NMT system, the code adjusted for analysing this single output and the result.

## How to use the scripts to extract annotations and calculate Inter-Annotator Agreement


Firstly, you need the annotated .csv file exported from **translate5** (e.g. `test_set_annotator1.csv`)  

Then add the path to the main directory (mqm_analysis) to the script main.py (line 20) and run 

```
python main.py
```

## Functions of scripts

##### Step 1. 
`prepare_MQM_output.py` essentially just gives it additional tags to make it a proper .xml file.

* Step 2. `parse_MQM_system.py` parses the output of step 1, i.e. the new .xml file. (`parse_MQM_system.p` use the output from step 2. as standard input.)

* Step 3. `extract_MQM_stats.py` processes the parsed output from step 2 and shows how many tokens you have, and how many tokens have which error on them. 

Line 42 states Obmission, Missing and Punctuation. Add or remove these categories based on your tagset. Line 59 specifies punctuation, to avoid double counting, considering that punctuation could be annotated to one missing or incorrect punctuation at a time. Also, change index at line 75 to the way you want to save the file.
(**Note that this script  includes but comments out a Croatian tokeniser which is not included in this repo. If you require tokenisation for Croatian, we suggest the [ReLDI](https://github.com/clarinsi/reldi-tokeniser) tokeniser. In case you are using a different language, consider using an appropriate tokeniser, just in case.**). 

* Step 4. For IAA (Inter Annotator Agreement), after parsing everything following the above steps, the `extract_MQM_sent_IAA_stats.py` is called, which requires as input two \*.parsed files (output from step 3.) - define their names within the script main.py(line 56, 58). (Also note that MQM error categories have been hard-coded here, so make sure to double check that all the MQM error categories you're using are actually in the script extract_MQM_sent_IAA_stats.py (e.g. lines 71-74, and then everything from 115-134)).

* Step 5. `extract_error_per_sentence.py` creates a histogram of error distribution per sentences. The error amounts per sentence have been hard-coded  as the Dataframe in the script extract_error_per_sentence.py (line 45-46) - change this according to labels, counts, labels2 and counts2.

* Step 6. Extract amounts of tokens with errors per system from both annotators concatenated for the test set.

Citation/References
-----
If you use the MQM error analysis code or annotation result, we'd appreciate if you cite the [paper](https://arxiv.org/abs/2006.08297) about it!

```
@article{10.1007/s10590-018-9214-x,
	author = {Klubi\u{a}?Ka, Filip and Toral, Antonio and S\'{a}nchez-Cartagena, V\'{\i}ctor M.},
	title = {Quantitative Fine-Grained Human Evaluation of Machine Translation Systems: A Case Study on English to Croatian},
	year = {2018},
	issue_date = {September 2018},
	publisher = {Kluwer Academic Publishers},
	address = {USA},
	volume = {32},
	number = {3},
	issn = {0922-6567},
	url = {https://doi.org/10.1007/s10590-018-9214-x},
	doi = {10.1007/s10590-018-9214-x},
	journal = {Machine Translation},
	month = sep,
	pages = {195–215}
}
```

```
@inproceedings{ye-toral-2020-fine,
    title = "Fine-grained Human Evaluation of Transformer and Recurrent Approaches to Neural Machine Translation for {E}nglish-to-{C}hinese",
    author = "Ye, Yuying  and
      Toral, Antonio",
    booktitle = "Proceedings of the 22nd Annual Conference of the European Association for Machine Translation",
    month = nov,
    year = "2020",
    address = "Lisboa, Portugal",
    publisher = "European Association for Machine Translation",
    url = "https://www.aclweb.org/anthology/2020.eamt-1.14",
    pages = "125--134"
}
``` 
