from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("""<html>
                                <head>
                                    <meta charset="UTF-8">
                                    <title>KonverterRNA</title>
                                    <link rel="stylesheet" href="css/style.css">
        
                                </head>
                                <body>
                                    <div class="wrapp">
                                        <div class="header">
                                            <h1>KonverterRNA</h1>
                                            <form action="test.py" method="POST" ENCTYPE="multipart/form-data">
                                                <input type="file" name="plik"/>
                                                <br/>
                                                <textarea name="poletekstowe" cols="200" rows="30" >Prosze podać strukture</textarea>
                                                <div>
                                                    <form action="...">
                                                        <select name="format">
                                                            <option>dot-bracket</option>
                                                            <option>CT</option>
                                                            <option>BPSEQ</option>
                                                            <option>RNAML</option>
                                                            (...)
                                                        </select>
                                                    </form>
                                                    <form action="...">
                                                        <select name="typ_wizualizacji">
                                                            <option>klasyczna</option>
                                                            <option>łukowa</option>
                                                            <option>na okręgu</option>
                                                            <option>górska</option>
                                                            (...)
                                                        </select>
                                                    </form>
                                                <input type="submit" value="Wyślij plik"/>
                                                </div> 
                                            </form>               
                                        </div>
                                    </div>
                                </body>
                            </html>""")
