# How to run Assignment 2
To run assignment 2, the Rat26F syntax analyzer, run this in the directory with the assignment2.py Python script:

```bash
python assignment2.py [input file] [output file (optional)]
```

Input file: Path to a file containing Rat26F source code

Output file (optional): The path of the file where the results should be stored in. Defaults to 'output.txt' if omitted.

For example, to perform syntax analysis for source code in input.txt and store the results in output.txt, run:

```bash
python assignment2.py input.txt output.txt
```

If a syntax error is found, the error message will automatically be added to the end of the output file.
