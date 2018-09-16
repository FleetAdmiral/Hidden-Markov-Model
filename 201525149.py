import sys, os, math, re, random, copy
from collections import OrderedDict

if(sys.argv==""):
   print "Please enter a file name!"

fname=sys.argv[1]

tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag 9", "tag10"]

top_dict =dict()

no_iterations=10

def pi_norm(tags):
    pi=dict()
    sum=float(0)
    for tag in tags:
        pi[tag]=random.random()
        sum= sum+pi[tag]

    for tag in tags:
        pi[tag] = pi[tag]/sum
    return pi


def eta_gamma(matr_a, matr_b, fwd, backwd,tags, line):
    #Cleanse the data line first
    for i, word in enumerate(line):
        if word == '':
            del line[i]
    #INITIALISATION OF ETA dict.
    eta=dict()
    for i in range(1, len(line)+1):
        eta[i]=dict()
        for tag in tags:
            eta[i][tag] = dict()

    #Initialise the gamma values
    gamma = dict()
    for i in range(1, len(line)+1):
        gamma[i]=dict()

    #Algorithm
    for time in range(1, len(line)):
        denom=float(0)
        for ftag in tags:
            for stag in tags:
                denom = denom + (fwd[time][ftag]*matr_a[ftag][stag]*matr_b[stag][line[time]]*backwd[time+1][stag])


        for ftag in tags:
            gamma[time][ftag]=float(0)
            for stag in tags:
                eta[time][ftag][stag] = (fwd[time][ftag]*matr_a[ftag][stag]*matr_b[stag][line[time]]*backwd[time+1][stag])
                gamma[time][ftag] = gamma[time][ftag] + eta[time][ftag][stag]


    denom=float(0)
    for tag in tags:
        denom = denom + fwd[len(line)][tag]
    for tag in tags:
        gamma[len(line)][tag] = fwd[len(line)][tag]/denom

    return eta , gamma


def init_a(tags):
    a=dict()
    list_tag = tags
    for i in list_tag:
        for j in list_tag:
            if i not in a:
                a[i]=dict()
            a[i][j]=random.random()
        a[i]['f']=random.random()
    sum=float(0)
    matr_a = dict(copy.deepcopy(a))

    for ftag in tags:
        for stag in tags:
            sum= sum+matr_a[ftag][stag]
        sum=sum+ matr_a[ftag]['f']

    for ftag in tags:
        for stag in tags:
            matr_a[ftag][stag] = float(matr_a[ftag][stag])/sum
        matr_a[ftag]['f'] = float(matr_a[ftag]['f'])/sum


    b=dict()
    for tag in tags:
        b[tag]=dict()

    for tag in  tags:
        sum=float(0)
        for line in lines:
            for word in line:
                if word in b[tag]:
                    continue
                b[tag][word] = random.random()
                sum = sum+b[tag][word]
        for line in lines:
            for word in line:
                if word in b[tag]:
                    continue
                b[tag][word] = b[tag][word] /sum

    return matr_a, b

def tokenise(fname, a):
    f = open(fname, 'r')
    lines = list()
    regex = re.compile('[\W]+')

    for line in f:
        line = line.split(' ')

        if line[0].startswith("#"):
            continue

        for i, word in enumerate(line):
            line[i] = re.sub('[^a-zA-Z0-9]+', '', line[i])

            #Convert it into lowercase
            line[i] = line[i].lower()
            #If empty string is processed
            if line[i]=='':
                del line[i]
        #print line

        if not line:
            continue

        lines.append(line)

    return lines
a_=list()
lines = tokenise(fname, a_)

def a_norm(a, tags):
    sum=float(0)
    matr_a = copy.deepcopy(a)
    for ftag in tags:
        for stag in tags:
            sum = sum+matr_a[ftag][stag]
        sum= sum+matr_a[ftag]['f']

    for ftag in tags:
        for stag in tags:
            matr_a[ftag][stag] = float(matr_a[ftag][stag])/sum
        matr_a[ftag]['f'] = float(matr_a[ftag]['f'])/sum

    return matr_a

def compute_eta(matr_a, matr_b, fwd, backwd, tags , line):

    for i, word in enumerate(line):
        if word == '':
            del line[i]

    eta=dict()
    for i in range(1, len(line)+1):
        eta[i]=dict()
        for tag in tags:
            eta[i][tag] = dict()

    for i  in range(1, len(line)):
        for ftag in tags:
            for stag in tags:
                #print "eta"

                eta[i][ftag][stag] = float(fwd[i][ftag] * backwd[i+1][stag] * matr_a[ftag][stag] * matr_b[stag][line[i]]) /fwd[len(line)+1]
                #print eta[i][ftag][stag]

    return eta

def init_b(tags, lines):

    b=dict()

    for tag in tags:
        b[tag]=dict()

    for tag in  tags:
        sum=float(0)

        for line in lines:
            for word in line:
                if word not in b[tag]:
                    break
                b[tag][word] = random.random()
                sum = sum+b[tag][word]

        for line in lines:
            for word in line:
                if word not in b[tag]:
                    break
                b[tag][word] = b[tag][word] /sum
    return b


def forward(matr_a, matr_b, pi, line, tags):
    fwd = dict()
    ''' 
    It is of the format fwd[timestamp][tag]
    
            print "b [i][word]" , b_matri[i][word], sum
    '''

    #line  = line[0]

    for i, word in enumerate(line):
        if word == '':
            del line[i]

    #First make the dict of dicts for len of lines
    for i in range(1,len(line)+1):
        fwd[i]=dict()

    c=dict()
    c[1] = float(0)
    for tag in tags:
        fwd[1][tag]=pi[tag]*matr_b[tag][line[0]]
        c[1] = c[1] + fwd[1][tag]
    #Scale the fwd[1]
    c[1] = 1./ c[1]

    for tag in tags:
        fwd[1][tag] = (c[1] * fwd[1][tag])


    #Now run the algorithm
    for i in range(2, len(line)+1):
        c[i] = float(0)
        j = i-1
        for tag_pres in tags:
            fwd[i][tag_pres]=float(0)
            for tag_prev in tags:
                fwd[i][tag_pres] =  fwd[i][tag_pres] +(fwd[j][tag_prev] * matr_a[tag_prev][tag_pres]  )
            fwd[i][tag_pres] = fwd[i][tag_pres]* matr_b[tag_pres][line[j]]
            #print i, tag_pres, "fwd", fwd[i][tag_pres]
            c[i] = c[i] + fwd[i][tag_pres]
        c[i] = 1./c[i]

        for tag in tags:
            fwd[i][tag] = (c[i] * fwd[i][tag])


    #Final layer computation
    x = len(line)+1
    fwd[x]=float(0)

    for tag in tags:
        #Everyone receives summation lol!

        fwd[x] = fwd[x] +(fwd[x-1][tag] * matr_a[tag]['f'])
        #print "fwd[x]" , fwd[x]
        #print "FWD[x]" ,  x, tag,fwd[x-1][tag], matr_a[tag]['f'], fwd[x]

    return fwd, c

def baum_welch(matr_a, matr_b, pi, tags, lines):

    for k , line in enumerate(lines):

        if line=='':
            continue
        print ""
        print "Iteration number: " , k
        print "The line in this iteration is: "
        temp_s = ""
        for ki in line:
            temp_s = temp_s+" "+ki
        print temp_s
        temp_line = line
        for i, word in enumerate(line):
            if word == '':
                del line[i]
        iterations = 0
        while(iterations < no_iterations ):
            #E-STEP
            fwd, c = forward(matr_a, matr_b, pi, line, tags)
            backwd = backward(matr_a, matr_b, pi, line, tags, c)
            gamma = compute_gamma(fwd, backwd, tags, line)
            eta = compute_eta(matr_a, matr_b, fwd, backwd, tags , line)

            #M-STEP
            old_matr_a = copy.deepcopy(matr_a)
            old_matr_b = copy.deepcopy(matr_b)

            for ftag in tags:
                for stag in tags:
                    num=float(0)
                    den=float(0)
                    for time in range(1, len(line)):
                        num =  num +eta[time][ftag][stag]
                        den = den+gamma[time][ftag]
                        for temp_tag in tags:
                            den  = den+eta[time][ftag][temp_tag]

                    #print "den is", den
                    matr_a[ftag][stag] = num/(den)


            for tag in tags:
                for word in line:
                    num=float(0)
                    den=float(0)
                    for time in range(1, len(line)+1):
                        if line[time-1]==word:
                            num = num+gamma[time][tag]
                        den = den+gamma[time][tag]
                    matr_b[tag][word]  = num/den

            iterations=iterations+1
        matr_a = a_norm(matr_a, tags)
        matr_b = normalise_b_internal(matr_b, tags, temp_line)

    return matr_a, matr_b


def backward(matr_a, matr_b, pi, line, tags, c ):
    backwd = dict()
    for i, word in enumerate(line):
        if word == '':
            del line[i]
    for i in range(1,len(line)+1):
        backwd[i]=dict()

    #Now initialise the T timestamp probs
    for tag in tags:
        backwd[len(line)][tag]=c[len(line)]
    #Now run the algorithm
    for i in range(len(line)-1, 0, -1):
        j = i+1
        for tag_pres in tags:
            backwd[i][tag_pres]=float(0)
            for tag_future in tags:
                backwd[i][tag_pres] =backwd[i][tag_pres]+ (backwd[j][tag_future] * matr_a[tag_pres][tag_future] * matr_b[tag_future][line[i]] )

            backwd[i][tag_pres] = (c[i] * backwd[i][tag_pres] )

    #Final layer computation, well this actually does not matter!
    x = 0
    backwd[x]=float(0)


    for tag in tags:
        #Everyone receives summation lol!
        backwd[x] = backwd[x] + (backwd[x+1][tag] * pi[tag])

    return backwd


def normalise_b_internal(b, tags, sentence):
    #print line
    for tag in tags:
        sum=float(0)
        for word in sentence:
            sum = sum +b[tag][word]
        for word in sentence:
            b[tag][word] = b[tag][word] / sum
    return b


def compute_gamma(fwd, backwd, tags, line):
    #Cleanse the data line first
    for i, word in enumerate(line):
        if word == '':
            del line[i]

    #Initialise the gamma values
    gamma = dict()
    for i in range(1, len(line)+1):
        gamma[i]=dict()

    #Algorithm computation
    for i in range(1, len(line)+1):
        for tag in tags:
            #print "fwd", fwd[i][tag] , backwd[i][tag] , fwd[len(line)+1]
            gamma[i][tag] = (fwd[i][tag] * backwd[i][tag]) / fwd[len(line)+1]

    return gamma

print "Number of iterations in each iteration of Baum Welch: "
print no_iterations
matr_a, matr_b = init_a(tags)
pi = pi_norm(tags)
matr_a, matr_b = baum_welch(matr_a, matr_b, pi, tags, lines)
for tag in matr_b:
    col = matr_b[tag]
    top = sorted(col, key=col.get, reverse=True)
    top=top[:100]
    top_dict[tag] = top

for tag_no in tags:
    print top_dict[tag_no]

m = open('temp_file.txt', 'w+')
m.write("A Matrix\n")
for ftag in tags:
    for stag in tags:
        m.write(ftag+ "->"+stag+" "+str(matr_a[ftag][stag])+'\n')
    m.write("B Matrix\n")
    for line in lines:
        for word in line:
            for tag in  tags:
                m.write(tag+ "->"+word+" "+str(matr_b[tag][word])+'\n')





