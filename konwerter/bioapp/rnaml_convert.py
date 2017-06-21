from xml.dom.minidom import parse, parseString
from .dot_structure import dot_structure
from django.conf import settings


def rnaml2dot(cts):
    #try:
    if isinstance(cts, str):
        dom = parseString(cts)
    else:
        dom = parse(cts)
    seq_data = dom.getElementsByTagName('seq-data')
    name = dom.getElementsByTagName('name')
    main_name = name[0].firstChild.nodeValue
    seq = seq_data[0].firstChild.nodeValue.replace(' ', '').replace('\n', '')
    base_pair = dom.getElementsByTagName('base-pair')
    A = []
    B = []

    i = 0
    for x in base_pair:
        position = base_pair[i].getElementsByTagName('position')
        A.append(position[0].firstChild.nodeValue)
        B.append(position[1].firstChild.nodeValue)
        i += 1

    X = [0] * len(seq)
    for n, i in zip(A, B):
        X[int(n) - 1] = int(i)


    Y = []
    for i in range(1, len(seq) + 1):
        Y.append(i)

    d = dot_structure(Y, X)

    path = 'plik.dot'
    with open(str(settings.MEDIA_ROOT) + '\plik.dot' , 'w') as f:
        f.write('>' + str(main_name) + '.dot' + '\n' + str(seq) + '\n' + ''.join(d))
        f.close
    print("Conversion from (rnaml) to (dot) completed successfully!")
    return (path)
    #except:
        #return ("Invalid input format")


def rnaml2bpseq(cts):
    try:
        if isinstance(cts, str):
            dom = parseString(cts)
        else:
            dom = parse(cts) 
        seq_data = dom.getElementsByTagName('seq-data')
        name = dom.getElementsByTagName('name')
        main_name = name[0].firstChild.nodeValue
        seq = seq_data[0].firstChild.nodeValue.replace(' ', '').replace('\n', '')
        base_pair = dom.getElementsByTagName('base-pair')
        A = []
        B = []
    
    
        i = 0
        for x in base_pair:
            position = base_pair[i].getElementsByTagName('position')
            A.append(position[0].firstChild.nodeValue)
            B.append(position[1].firstChild.nodeValue)
            i += 1
    
    
        X = [0] * len(seq)
        for n, i in zip(A, B):
            X[int(n) - 1] = int(i)
        # jezeli 2 i 10 to para to tez zapisze to jako 10 i 2
        for n, i in zip(B, A):
            X[int(n) - 1] = int(i)
    
    
        Y = []
        for i in range(1, len(seq) + 1):
            Y.append(i)
    
        output = []
    
        for i in range(len(seq)):
            output.append("%s%s%s%s%s" % (Y[i], ' ', seq[i], ' ', X[i]))
        
        path = 'plik.bpseq'
        with open(str(settings.MEDIA_ROOT) + '\plik.bpseq' , 'w') as f:
            f.write('>' + main_name + '.bpseq' + '\n' + '\n'.join(output))
            f.close
        print("Conversion from (rnaml) to (bpseq) completed successfully!")
        return (path)
    except:
        return ("Invalid input format")


def rnaml2ct(cts):
    try:
        if isinstance(cts, str):
            dom = parseString(cts)
        else:
            dom = parse(cts)
        seq_data = dom.getElementsByTagName('seq-data')
        name = dom.getElementsByTagName('name')
        main_name = name[0].firstChild.nodeValue
        seq = seq_data[0].firstChild.nodeValue.replace(' ', '').replace('\n', '')
        base_pair = dom.getElementsByTagName('base-pair')
        A = []
        B = []
    
    
        i = 0
        for x in base_pair:
            position = base_pair[i].getElementsByTagName('position')
            A.append(position[0].firstChild.nodeValue)
            B.append(position[1].firstChild.nodeValue)
            i += 1
    
    
        X = [0] * len(seq)
        for n, i in zip(A, B):
            X[int(n) - 1] = int(i)
    
        for n, i in zip(B, A):
            X[int(n) - 1] = int(i)
    
    
        Y = []
        for i in range(1, len(seq) + 1):
            Y.append(i)
    
        output = []
    
        for i in range(len(seq)):
            output.append("%s%s%s%s%s%s%s%s%s%s%s" % (Y[i], ' ', seq[i], ' ', i, ' ', i + 2, ' ', X[i], ' ', Y[i]))
        
        path = 'plik.ct'
        with open(str(settings.MEDIA_ROOT) + '\plik.ct' , 'w') as f:
            f.write('>' + main_name + '.ct' + '\n' + '\n'.join(output))
            f.close
        print("Conversion from (rnaml) to (ct) completed successfully!")
        return (path)
    except:
        return ("Invalid input format")