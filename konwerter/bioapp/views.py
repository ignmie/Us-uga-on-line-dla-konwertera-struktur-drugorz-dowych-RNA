import re
from django.shortcuts import render
from django.conf import settings

from .forms import TestForm
from django.http import Http404
from .ct_convert import ct2bpseq, ct2rnaml, ct2dot
from .bpseq_convert import bpseq2ct, bpseq2rnaml, bpseq2dot
from .rnaml_convert import rnaml2ct, rnaml2bpseq, rnaml2dot
from .dot_convert import ConvertDot


title_form = "(>{1}.*(?:.dot|.ct|.bpseq))"
bracket_form = "[\.\<\[\{\(\)\>\]\}ABCDEFGabcdefg]+"
connect = "\s*\d+\s+[A-Z]\s+\d+\s+\d+\s+\d+\s+\d+"
base_pair = "\s*\d+\s+[A-Z]\s+\d+(?!\s)"

def index(request):
#####################################POST######################################
    if request.method == 'POST':
        try:
            form = TestForm(request.POST, request.FILES)
            try:
                if form.is_valid():
                    path_dot = ""
                    dot = ""
                    path_ct = ""
                    ct = ""
                    path_bpseq = ""
                    bpseq = ""
                    path_rnaml = ""
                    rnaml = ""
                    if(form.cleaned_data['formaty']):
                        formaty = form.cleaned_data['formaty']
                    else:
                        formaty = []
                    if bool(form.cleaned_data['plik']):
                        file_lines = request.FILES['plik'].read().decode("UTF-8").splitlines()
                    else:
                        file_lines = str(form.cleaned_data['seq']).splitlines()
                    name = str(file_lines[0])
                    if re.match("<rnaml>*", str(name)):
                        name = 'rnaml.xml'
                    else:
                        name = name.replace('>', '')
    #################################KONWERSJA Z RNAML#############################    
                    if re.match(".*.xml", name):
                        for i in range (0, len(formaty)):
                            if formaty[i]=="1":
                                path_dot =  rnaml2dot(str(file_lines[0]))
                                dot = open(str(settings.MEDIA_ROOT)  + "//" + path_dot, 'rb').read()
                            if formaty[i] == "2":
                                path_ct =  rnaml2ct(str(file_lines[0]))
                                ct = open(str(settings.MEDIA_ROOT)  + "//" + path_ct, 'rb').read()
                            if formaty[i] == "3":
                                path_bpseq =  rnaml2bpseq(str(file_lines[0]))
                                bpseq = open(str(settings.MEDIA_ROOT)  + "//" + path_bpseq, 'rb').read()
                         #wizual = wizualizacja(rodzaj,file_name)
                        return render(request, 'rnaml.html', {'dot': dot, 'path_dot': path_dot, 'ct': ct, 'path_ct': path_ct,'bpseq':bpseq,'path_bpseq': path_bpseq})
    #################################KONWERSJA Z DOT_BRACKET#######################                
                    elif re.findall(".*(dot)", str(file_lines)):
                        dot = ConvertDot(file_lines)
                        for i in range (0, len(formaty)): 
                            if formaty[i] =="2":
                                path_ct =  dot.dot2ct()
                                ct = open(str(settings.MEDIA_ROOT)  + "//" + path_ct, 'r').read()
                            if formaty[i] == "3":
                                path_bpseq =  dot.dot2bpseq()
                                bpseq = open(str(settings.MEDIA_ROOT)  + "//" + path_bpseq, 'r').read()
                            if formaty[i]=="4":
                                path_rnaml = ""
                                path_rnaml =  dot.dot2rnaml()
                                rnaml = open(str(settings.MEDIA_ROOT)  + "//" + path_rnaml, 'r').read()
                         #wizual = wizualizacja(rodzaj,file_name)
                        return render(request, 'dot.html', {'rnaml': rnaml, 'path_rnaml': path_rnaml, 'ct': ct, 'path_ct': path_ct,'bpseq':bpseq,'path_bpseq': path_bpseq})  
                    else:
                        file_name = file_lines[0]
                        if re.findall(title_form, str(file_lines)):
                            title = re.findall(title_form, str(file_lines))
                        else:
                            title = " "
    #################################KONWERSJA Z CT################################
                        if re.findall(connect, str(file_lines)): 
                            for i in range (0, len(formaty)):
                                if formaty[i]=="1":
                                    path_dot =  ct2dot(file_lines, title, file_name)
                                    dot = open(str(settings.MEDIA_ROOT)  + "//" + path_dot, 'r').read()
                                if formaty[i] == "3":
                                    path_bpseq =  ct2bpseq(file_lines, title, file_name)
                                    bpseq = open(str(settings.MEDIA_ROOT)  + "//" + path_bpseq, 'r').read()
                                if formaty[i] == "4":
                                    path_rnaml =  ct2rnaml(file_lines, title, file_name)
                                    rnaml = open(str(settings.MEDIA_ROOT)  + "//" + path_rnaml, 'r').read()
                             #wizual = wizualizacja(rodzaj,file_name)
                            return render(request, 'ct.html', {'dot': dot, 'path_dot': path_dot, 'rnaml': rnaml, 'path_rnaml': path_rnaml,'bpseq':bpseq,'path_bpseq': path_bpseq})
    #################################KONWERSJA Z BPSEQ#############################
                        elif re.findall(base_pair, str(file_lines)):
                            for i in range (0, len(formaty)):
                                if formaty[i]=="1":
                                    path_dot =  bpseq2dot(file_lines, title, file_name)
                                    dot = open(str(settings.MEDIA_ROOT)  + "//" + path_dot, 'rb').read()
                                if formaty[i] == "2":
                                    path_ct =  bpseq2ct(file_lines, title, file_name)
                                    ct = open(str(settings.MEDIA_ROOT)  + "//" + path_ct, 'rb').read()
                                if formaty[i] == "4":
                                    path_rnaml =  bpseq2rnaml(file_lines, title, file_name)
                                    rnaml = open(str(settings.MEDIA_ROOT)  + "//" + path_rnaml, 'rb').read()
                             #wizual = wizualizacja(rodzaj,file_name)
                            return render(request, 'bpseq.html', {'dot': dot, 'path_dot': path_dot, 'rnaml': rnaml, 'path_rnaml': path_rnaml,'ct':ct,'path_ct': path_ct})
                        else:
                            form = TestForm(initial={'formaty': [1,2,3,4],'wizualizacja': [1,2,3,4]})           
                            return render(request, 'nameerr.html', {'form': form})    
                else:
                    form = TestForm(initial={'formaty': [1,2,3,4],'wizualizacja': [1,2,3,4]})           
                    return render(request, 'nameerr.html', {'form': form})
            except:
                form = TestForm(initial={'formaty': [1,2,3,4],'wizualizacja': [1,2,3,4]})
                return render(request, 'nameerr.html', {'form': form})
################################NIEPOPRAWNY FORMAT#############################        
        except:
             form = TestForm(initial={'formaty': [1,2,3,4],'wizualizacja': [1,2,3,4]})           
             return render(request, 'nameerr.html', {'form': form})
######################################GET######################################    
    else:
        form = TestForm(initial={'formaty': [1,2,3,4],'wizualizacja': [1,2,3,4]})
        return render(request, 'name.html', {'form': form})
    
    
def wizualizacja(rodzaj,file_name):
    j=0
    sciezki = []
    for i in range (0, len(formaty)):
        if rodzaj[i]=="1":
            sciezki = []
            #sciezki[j++] = sciezka_obraz_klasyczna()
        #if rodzaj[i] == "2":
            #sciezki[j++] = sciezka_obraz_lukowa()
        #if rodzaj[i] == "4":
            #sciezki[j++] = sciezka_obraz_naokregu()
        #if rodzaj[i] == "4":
            #sciezki[j++] = sciezka_obraz_gorska()
    return sciezki    