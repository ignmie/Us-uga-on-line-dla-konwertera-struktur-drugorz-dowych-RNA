import xml.etree.cElementTree as et
from django.conf import settings

class ConvertDot:
    """Contains methods to convert from dot-brackets format"""

    def __init__(self, f):
        """
        Read dot-brackets data and store into internal dot-brackets object

        :param data: a list(title, sequence, dot-bracket) or a filename
        """
        if isinstance(f, list):
            name = str(f[0])
            name = name.replace('.dot', '').replace('>', '')
            title = str(f[0])
            seq = str(f[1])
            dots = str(f[2])
        else:
            temp = f.read().decode("UTF-8").splitlines()
            name = str(temp[0])
            name = name.replace('.dot', '').replace('>', '')
            title = temp[0]
            seq = temp[1]
            dots = temp[2]
        self.db = {'name': name, 'title': title, 'seq': seq, 'pairs': {}}

        opens = ('(', '[', '{', '<', 'A', 'B', 'C', 'D', 'E', 'F', 'G')
        closes = {')': '(', ']': '[', '}': '{', '>': '<', 'a': 'A', 'b': 'B',
                  'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G'}
        stack = {}
        for position, symbol in enumerate(dots, start=1):
            if symbol in opens:
                try:
                    stack[symbol].append(position)
                except:
                    stack[symbol] = [position]
            elif symbol in closes.keys():
                try:
                    self.db['pairs'][position] = stack[closes[symbol]].pop()
                    self.db['pairs'][self.db['pairs'][position]] = position
                except:
                    print("Incorrect input data")
            elif symbol != '.':
                print("Incorrect input data")

    def dot2ct(self, tofile=None):
        result = [str(i) + " " + str(self.db['seq'][i-1]) + " " + str(i-1) + " " + str(i+1) + " " + str(self.db['pairs'].get(i, 0)) + " " + str(i) for i in range(1, len(self.db['seq'])+1) ]
        path = self.db['name'] + '.ct'
        with open(str(settings.MEDIA_ROOT) + '\\'  + self.db['name'] + '.ct' , 'w+') as fw:
            fw.write(self.db['name']+ '.ct' + '\n' + '\n'.join(result))
            fw.close
        return(path)

    def dot2bpseq(self, tofile=None):
        result = [str(i) + " " + self.db['seq'][i-1] + " " + str(self.db['pairs'].get(i, 0)) for i in range(1, len(self.db['seq'])+1) ]
        path = self.db['name'] + '.bpseq'
        with open(str(settings.MEDIA_ROOT) + '\\'  + self.db['name'] + '.bpseq' , 'w+') as fw:
            fw.write(self.db['name'] + '.bpseq' + '\n' + '\n'.join(result))
            fw.close
        return (path)

    def dot2rnaml(self, tofile=None):      
        print(str(self.db['seq']))
        rnaml = et.Element("rnaml")
        molecule = et.SubElement(rnaml, "molecule")
        identity = et.SubElement(molecule, "identity")
        name = et.SubElement(identity, "name")
        name.text = self.db['title']
        sequence = et.SubElement(molecule, "sequence")
        sequence.set("length", str(len(self.db['seq'])))
        seq_data = et.SubElement(sequence, "seq-data")
        seq_data.text = self.db['seq']
        structure = et.SubElement(molecule, "structure")
        for i in range(1, len(self.db['seq']) + 1):
            if i < self.db['pairs'].get(i, 0):
                base_pair = et.SubElement(structure, "base-pair")
                basep5 = et.SubElement(base_pair, "base-id-p5")
                baseidp5 = et.SubElement(basep5, "base-id")
                position5 = et.SubElement(baseidp5, "position")
                position5.text = str(i)
                basep3 = et.SubElement(base_pair, "base-id-p3")
                baseidp3 = et.SubElement(basep3, "base-id")
                position3 = et.SubElement(baseidp3, "position")
                position3.text = str(self.db['pairs'].get(i, 0))
        path = self.db['name'] + '.xml'
        plik = open(str(settings.MEDIA_ROOT) + '\\'  + self.db['name'] + '.xml' , 'w+')
        plik.write(str(et.tostring((rnaml))))
        plik.close()
        return (path)
