# How to run Assignment 2
To run assignment 2, the Rat26F syntax analyzer, run this in the directory with the assignment2.py Python script:

```bash
python assignment2.py [input file] [output file (optional)] [OPTIONS (optional)]
```

Input file: A file containing Rat26F source code

Output file (optional): The path of the file where the results should be stored in

Optional options are:

`--save-syntax-error`: Write output to file even if a syntax error was detected. The syntax error message will be included at the end of the output file. **Recommended** if you don't have Python on your machine.

For example, to perform syntax analysis for source code in input.txt, store the results in output.txt, and save the syntax error if it occurs, run:

```bash
python assignment2.py input.txt output.txt --save-syntax-error
```

To *avoid* writing any files if a syntax error occurs, omit the `--save-syntax-error` option.
