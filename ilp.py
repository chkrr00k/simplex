LICENSE_MESSAGE="""
    #############################################################
    #                                                           #
    #   This program is relased in the GNU GPL v3.0 license     #
    #   you can modify/use this program as you wish. Please     #
    #   link the original distribution of this software. If     #
    #   you plan to redistribute your modified/copied copy      #
    #   you need to relased the in GNU GPL v3.0 licence too     #
    #   according to the overmentioned licence.                 #
    #                                                           #
    #   "PROUDLY" MADE BY chkrr00k (i'm not THAT proud tbh)     #
    #                                                           #
    #############################################################
    #                                                           #
    #                                                           #
    #                            YEE                            #
    #                                                           #
    #                                                           #
    #############################################################
    """

import copy

def out(l, t):
    print("[{}]: {}".format(l,str(t)))
def log(t):
    out("INFO", t)
def error(t):
    out("ERROR", t)
def warn(t):
    out("WARNING", t)
def sep():
    out("SEP", "#"*40)

def dump(m, dir="<", aux=-1):
    if aux > 0 and aux < len(m[0]):
        print(dir + "\t  " + (" "*6)*aux + ("|{:-^" + str(len(m[0])*6 - (6*aux) - 1) + "}|").format("auxiliary"))
    print(dir + "\t+" + "-"*6 + "+" + "-" * ((len(m[0])-1)*6) + "+")
    print(dir + "\t|" + "{:6.2f}|".format(m[0][0]) + "".join(["{:6.2f}".format(i) for i in m[0][1:]]) +"|")
    print(dir + "\t|" + "-"*6 + "+" + "-" * ((len(m[0])-1)*6) + "|")
    for mi in m[1:]:
        print(dir + "\t|" + "{:6.2f}|".format(mi[0]) + "".join(["{:6.2f}".format(i) for i in mi[1:]]) + "|")
    print(dir + "\t+" + "-"*6 + "+" + "-" * ((len(m[0])-1)*6) + "+")


def bland(m):
    return [ind for ind, x in enumerate(m[0][1:]) if x < 0][0] + 1

def pivot(m, j):
    col = [r[j] for r in m]
    minj = [(i, x) for i, x in enumerate(col[1:]) if x > 0]
    th = min(minj, key=lambda e: [r[0] for r in m[1:]][e[0]] / e[1])
    piv = th[1]
    i = th[0] + 1  
    log("Cycling on ({1},{2}) = {0}".format(piv , j, i))
    
    if piv != 1:
        log("Pivot wasn't 1")
        m[i] = [e / piv for e in m[i]]
    old = copy.deepcopy(m)
    for index, row in enumerate(old):
        if index != i:
            m[index] = [(e - m[i][jj]*row[j]) for jj, e in enumerate(m[index])]


    return m 

def simplex(m, aux=-1, res=False):
    opt = ill = False
    dump(m, ">", aux=aux)
    while not opt and not ill:
        mt = m if not res else [r[:aux] for r in m]
        if all([True if j >= 0 else False for j in mt[0][1:]]):
            opt = True
            log("Optimum found")
            dump(m, aux=aux)
        else:
            j = bland(m)
            log("Cycling on {} column".format(j))
            #m[j][1:]
            if all([True if i <= 0 else False for i in [r[j] for r in m[1:]]]):
                ill = True
                error("Unbounded problem")
            else:
                log("Pivoting")
                m = pivot(m, j)
                dump(m, aux=aux)   
    return m

def sol(m):
    pass


def isBase(c):
    c = copy.deepcopy(c[1:])
    c.sort(reverse=True)
    return c[0] == 1 and all([True if i == 0 else False for i in c[1:]])

def getBase(ms):
    m = [r[1:] for r in ms]
    cols = [[r[col] for r in m] for col in range(0, len(m[0]))]
    mcols = [[r[col] for r in ms] for col in range(0, len(ms[0]))]
    m2 = list(filter(isBase, cols))
    b = list()
    for i in m2:
        b.append((i[0], i.index(1.0), mcols.index(i)))
    result = dict()
    for el in b:
        if el[1] not in result:
            result[el[1]]= (el[0], el[2])

    return result

def sol(m):
    b = getBase(m)
    p = {b[e][1]: e for e in b.keys()}
    sl = [m[p[i]][0] if i in p else 0 for i in range(1, len(m[0]))]
    return sl
    
def twoPhases(m):
    imp = rid = False
    dump(m, ">")
    mod = False
    for i, e in enumerate(m[1:]):
        if e[0] < 0:
            log("Inverted b{}".format(i + 1))
            m[i + 1] = [-el for el in e]
            mod = True
    if mod:
        dump(m)
    old = copy.deepcopy(m)

    cb = getBase(m)
    
    auxl = len(m[0])
    na = ((len(m) - 1) - len(cb))
    m[0].extend([0]*na)

    opt = False
    if na != len(m) - 1:
        out("OPTIMIZATION", "Not all auxiliary will be generated")
        opt = True

    if na != 0:
        w = [i for i in range(1, len(m)) if i not in cb]
        print(w)
        for p in w:
            for r in range(1, len(m)):
                m[r].append(1 if p == r else 0)

        log("Added {} auxiliary variables as base".format(na))
        dump(m, aux=auxl)

    cost = copy.deepcopy(m[0])
    m[0] = [1 if c >= auxl else 0 for c in range(0, len(m[0]))]
    log("Replaced cost function")
    dump(m, aux=auxl)

    if opt:
        for i in range(auxl, len(m)):
            m[0] = [m[0][j] - m[i][j] for j in range(0, len(m[i]))]
    else:
        for i in range(1, len(m)):
            m[0] = [m[0][j] - m[i][j] for j in range(0, len(m[i]))]
    log("Auxiliary variables translated in base")
    dump(m, aux=auxl)

    log("Calling simplex")
    m = simplex(m, auxl)
    log("Simplex returned")

    if -sum(m[0]) > 0:
        imp = True
        error("Impossible, #2 violated")
    else:
        for r, c in getBase(m).items():
            if c[1] > auxl:
                if True:
##TODO fix this
                    error("FIXME {} is in base and it's auxiliary".format(str(c)))
                else:
                    rid = True
                    error("Redundant, #1 violated")
                    m.pop(i)
                    log("Deleted {} row".format(i))

        log("Cost restored")
        m[0] = cost
        dump(m, aux=auxl)

        b = getBase(m)
        for i in range(1, len(m)):
            m[0] = [m[0][j] - m[i][j]*b[i][0] for j in range(0, len(m[i]))]
        log("Original cost variables translated in base")
        dump(m, aux=auxl)

        log("Calling simplex")
        m = simplex(m, auxl, res=True)
        log("Simplex returned")        

        s = sol(m)[:auxl-1]
        log("Optimal solution found on ({})".format(",".join([str(i) for i in s])))

        return s
    warn("Returning None")
    return None

import re
import collections
def line(l):
    eq = re.split("=", l)
    if len(eq) > 1:
        k = eq[-1]
    else:
        k = 0
    vars = collections.OrderedDict()
    for el in [e for e in re.split("([+-]?\d*\w+)", eq[0]) if e.strip() != ""]:
        term = [e for e in re.split("([+-]?\d*)(\w+)", el) if e.strip() != ""]
        if term[0].strip() == "+" or term[0].strip() == "-":
            term[0] += "1"
        if len(term) == 1:
            term.append(term[0])
            term[0] = 1
        vars[term[1]] = float(term[0])
    return float(k), vars


def assemble(eqs):
    names = list()
    k = list()
    rest = list()
    for eq in eqs:
        k.append(eq[0])
        rest.append(eq[1])
        for value, name in enumerate(eq[1]):
            if name not in names:
                names.append(name)
    for eq in rest:
        for name in names:
            if name not in eq:
                eq[name] = 0
    res = list()
    for i, v in enumerate(k):
        tmp = list()
        tmp.append(v)
        for n in names:
            tmp.append(rest[i][n])
        res.append(tmp)
    return res

import sys
def getTextEquations(file=sys.stdin):
    textualEqs = list()
    for l in file:
        textualEqs.append(line(l.strip()))
    eqs = assemble(textualEqs)
    call(eqs)
    
def call(eqs):
    if len(eqs) == 0:
        error("You need to specify equations")
        return -1
    if len(eqs) == 1:
        error("Insert a correct amount of equations")
        return -1
    elif eqs[0][0] != 0:
        error("-z must be 0")
        warn("the first equation must be the function to minimize")
        return -2
    else:
        log("Calling two phases")
        return twoPhases(eqs)

def test():
    e = sol(simplex([[0, -2, -1, 0, 0, 0], [2, 1, 0, 1, 0, 0], [3, 1, 1, 0, 1, 0], [5, 1, 2, 0, 0, 1]]))

    a = twoPhases([[0, -1, -1, 0, 0, 0], [8, 1, 1, 1, 0, 0], [1, 1, -1, 0, -1, 0], [6, 1, 0, 0, 0, 1]])
    b = twoPhases([[0, 100, 125, 0, 0], [10, 2, 5, -1, 0], [3, 1, 1, 0, -1]])
    c = twoPhases([[0, -2, -3, 0, 0], [8, 0.1, 0.2, 1, 0], [9, 0.3, 0.1, 0, 1]])
    d = twoPhases([[0,200,300,0,0,0,0],[400,100,0,-1,0,0,0],[600,0,100,0,-1,0,0],[2000,100,200,0,0,-1,0],[1300,100,100,0,0,0,-1]])

    t = a == [4.5, 3.5, 0, 0, 1.5] and b == [1.6666666666666667, 1.3333333333333333, 0, 0] and c == [20.0, 29.999999999999996, 0, 0] and d == [6.0, 7.0, 200.0, 100.0, 0, 0] and e == [2, 1, 0, 0, 1]
    print("Self test: {}".format("OK" if t else "Not passed"))

HELP_MESSAGE = """Help:
Solves optimization problems
-h, --help               Displays this help
-i, --interactive        Reads from stdin the problem (default)
-f <name>, --file <name> Reads from file
-j, --json               The problem is written in json array style
-t, --textual            The problem is written in as equations (default)
-s                       Starts a selftest (useful for debug)
-l                       Shows the license
"""    
import getopt
try:
    opts, args = getopt.getopt(sys.argv[1:], "hif:ljts", ["help", "interactive", "file", "json", "textual"])
except getopt.GetoptError:
    print("Error in arguments\n")
    print(HELP_MESSAGE)
    sys.exit(1)
settings = {
    "file" : sys.stdin,
    "method": "j",
    "test": False
    }
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(HELP_MESSAGE)
        sys.exit(0)
    elif opt in ("-l"):
        print(LICENSE_MESSAGE)
        sys.exit(0)
    elif opt in ("-i", "--interactive"):
        pass
    elif opt in ("-f", "--file"):
        settings["file"] = open(args.strip(), "r")
    elif opt in ("-j", "--json"):
        settings["method"] = "j"
    elif opt in ("-t", "--textual"):
        settings["method"] = "t"
    elif opt in ("-s"):
        settings["test"] = True

if settings["test"]:
    test()
else:
    if settings["method"] == "t":
        getTextEquations(settings["file"])
    elif settings["method"] == "j":
        import json
        call(json.load(settings["file"]))
