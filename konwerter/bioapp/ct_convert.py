from .dot_structure import dot_structure
import xml.etree.cElementTree as ET
import re
from django.conf import settings

def ct2dot(cts, input_title, file_name):
    try:
        if re.match(">.*.ct", input_title[0]):
            title = input_title[0]
            title = title.replace('.ct', '')
        else:
            title = "seq_name"
        A = []
        B = []
        seq = ''
    
        idx = 0
        while idx < len(cts):
            line = cts[idx].split()
            if len(line) >= 6 and line[0] == line[5]:
                if line[5] == '1':  # first line
                    A = [int(line[0])]
                    B = [int(line[4])]
                    seq += line[1]
                else:
                    A.append(int(line[0]))
                    B.append(int(line[4]))
                    seq += str(line[1])
            idx += 1
        if len(A) > 0:
            s = dot_structure(A, B) 
        path = title.replace('>','') + '.dot'
        with open(str(settings.MEDIA_ROOT) + '\\' + path , 'w') as d:
            d.write(title + '.dot' + '\n' + seq + '\n' + ''.join(s))
            d.close
        print("Conversion from (ct) to (dot) completed successfully!")
        return (path)
    except:
        return ("Invalid input format")

def ct2rnaml(cts, input_title, file_name):
    try:
        if re.match(">.*.ct", input_title[0]):
            title = input_title[0]
            title = title.replace('.ct', '').replace('>', '')
        else:
            title = "seq_name"
    
        A = []
        B = []
        seq = ''
    
        idx = 0
        while idx < len(cts):
            line = cts[idx].split()
            if len(line) >= 6 and line[0] == line[5]:
                if line[5] == '1':  # first line
                    A = [int(line[0])]
                    B = [int(line[4])]
                    seq += line[1]
                else:
                    A.append(int(line[0]))
                    B.append(int(line[4]))
                    seq += str(line[1])
            idx += 1
    
        rnaml = ET.Element("rnaml")
        molecule = ET.SubElement(rnaml, "molecule")
        identity = ET.SubElement(molecule, "identity")
        name = ET.SubElement(identity, "name")
        name.text = str(title)
        sequence = ET.SubElement(molecule, "sequence")
        sequence.set("length", str(len(seq)))
        seq_data = ET.SubElement(sequence, "seq-data")
        seq_data.text = seq
        structure = ET.SubElement(molecule, "structure")
    
        for a, b in zip(A, B):
            if b > a:
                base_pair = ET.SubElement(structure, "base-pair")
    
                basep5 = ET.SubElement(base_pair, "base-id-p5")
                baseidp5 = ET.SubElement(basep5, "base-id")
                position5 = ET.SubElement(baseidp5, "position")
                position5.text = str(a)
    
                basep3 = ET.SubElement(base_pair, "base-id-p3")
                baseidp3 = ET.SubElement(basep3, "base-id")
                position3 = ET.SubElement(baseidp3, "position")
                position3.text = str(b)
    
        #tree = ET.fromstring(rnaml)
        #tree.write(file_name + ".xml")
        path = title + '.xml'
        plik = open(str(settings.MEDIA_ROOT) + '\\' + title + '.xml' , 'wb')
        plik.write(ET.tostring(rnaml))
        plik.close()
        print("Conversion from (ct) to (rnaml) completed successfully!")
        return (path)
    except:
        print("Invalid input format")


def ct2bpseq(cts, input_title, file_name):
    try:
        if re.match(">.*.ct", input_title[0]):
            title = input_title[0]
            title = title.replace('.ct', '.bpseq')
        else:
            title = ">seq_name.bpseq"
    
        idx = 0
        string = []
        while idx < len(cts):
            line = cts[idx].split()
            if len(line) >= 6 and line[0] == line[5]:
                string.append(str(line[0]) + ' ' + str(line[1]) + ' ' + str(line[4]))
            idx += 1
        # print('\n'.join(string))
    
        path = title.replace('>','') + '.bpseq'
        with  open(str(settings.MEDIA_ROOT) + '\\' + path , 'w') as d:
            d.write(title + '\n' + '\n'.join(string))
            d.close
        print("Conversion from (ct) to (rnaml) completed successfully!")
        return (path)
    except:
        print("Invalid input format")