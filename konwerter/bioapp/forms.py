from django import forms


class TestForm(forms.Form):
    plik = forms.FileField(required=False)
    seq =  forms.CharField(required=False, widget=forms.Textarea(attrs={'class' : 'myfieldclass'}))
    form_options = (
            (1, "dot-bracket"),
            (2, "CT"),
	    (3, "BPSEQ"),
	    (4, "RNAML"),
            )
    wiz_options = (
	(1,"klasyczna"),
	(2, "lukowa"),
	(3, "na okregu"),
	(4, "gorska"),
	)   
    formaty = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=form_options)
    wizualizacja = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=wiz_options)	