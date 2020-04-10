# Simplex
An implementation of the Danzig Simplex algorithm for linar programming
  
## Arguments  
`-h, --help`               Displays this help  
`-i, --interactive`        Reads from stdin the problem (default)  
`-f <name>, --file <name>` Reads from file  
`-j, --json`               The problem is written in json array style  
`-t, --textual`            The problem is written in as equations (default)  
`-s`                       Starts a selftest (useful for debug)  
`-l`                       Shows the license  
  
## Examples
To solve a problem in array form, the matrix must rapresent the tableau  
```bash
$ python3 ilp.py -j -i  
> [[0, -2, -1, 0, 0, 0], [2, 1, 0, 1, 0, 0], [3, 1, 1, 0, 1, 0], [5, 1, 2, 0, 0, 1]]
```
To solve a problem in equation form, it must already be in standard form  
```bash  
$ python3 ilp.py -t -i  
> -100a-300b
>a+ 2b+c= 80
>3a +b+d
```
