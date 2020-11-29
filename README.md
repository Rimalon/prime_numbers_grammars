# Prime numbers generator
##Usage
#####For context free grammar generating use:
```
python cfg_generator.py
```
From "/turing_machine_generator" folder
#####To generate context free grammar with specific arguments use:
```
usage: cfg_generator.py [-h] [-tm TURING_MACHINE_PATH] [-g GRAMMAR_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -tm TURING_MACHINE_PATH, --turing_machine_path TURING_MACHINE_PATH
                        Path to turing machine file
  -g GRAMMAR_PATH, --grammar_path GRAMMAR_PATH
                        Output grammar path
```
#####For prime numbers generating use:
```
python prime_generator.py
```
From "/turing_machine_generator" folder
#####To start the prime number generator with specific arguments use:
```
usage: prime_generator.py [-h] [-g GRAMMAR_PATH] [-n N]

optional arguments:
  -h, --help            show this help message and exit
  -g GRAMMAR_PATH, --grammar_path GRAMMAR_PATH
                        Path to file with grammar
  -n N                  Prime numbers amount
```