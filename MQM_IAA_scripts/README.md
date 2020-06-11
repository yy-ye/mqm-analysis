**Instructions on how to use the scripts to extract annotations and calculate Inter-Annotator Agreement**
-----

1. For starters you need the annotated .csv file exported from translate5 (e.g. "test_set_annotator1.csv")  

2. Add the path to the main directory (mqm_analysis) to the script main.py (line 20) and run "python main.py".

*Step 1. The script prepare_MQM_output.py essentially just gives it additional tags to make it a proper .xml file.

*Step 2. Then it parses the output of that script - i.e. the new .xml file - with the script parse_MQM_system.py (use the output from step 2. as standard input).

*Step 3. Finally, it feeds the parsed output to the script extract_MQM_stats.py, and you know how many tokens you have, and how many tokens have which error on them. Line 42 states Obmission, Missing and Punctuation. Add or remove these categories based on your tagset. Line 59 specifies punctuation, to avoid double counting, considering that punctuation could be annotated to one missing or incorrect punctuation at a time. Also, change index at line 75 to the way you want to save the file.
(**Note that this script  includes but comments out a Croatian tokeniser which is not included in this repo. If you require tokenisation for Croatian, we suggest the [ReLDI](https://github.com/clarinsi/reldi-tokeniser) tokeniser. In case you are using a different language, consider using an appropriate tokeniser, just in case.**). 

*Step 4. For IAA (Inter Annotator Agreement), after parsing everything following the above steps, the extract_MQM_sent_IAA_stats.py is called, which requires as input two *.parsed files (output from step 3.) - define their names within the script main.py(line 56, 58). (Also note that MQM error categories have been hard-coded here, so make sure to double check that all the MQM error categories you're using are actually in the script extract_MQM_sent_IAA_stats.py (e.g. lines 71-74, and then everything from 115-134)).

*Step 5. extract_error_per_sentence creates a histogram of error distribution per sentences. The error amounts per sentence have been hard-coded  as the Dataframe in the script extract_error_per_sentence.py (line 45-46) - change this according to labels, counts, labels2 and counts2.

*Step 6. Extract amounts of tokens with errors per system from both annotators concatenated for the test set.