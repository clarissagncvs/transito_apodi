from django import forms
from .models import Ocorrencia


class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ['tipo', 'via', 'descricao', 'semaforo', 'horario_incidente']

        widgets = {
            'tipo': forms.Select(attrs={'class': 'input'}),
            'via': forms.Select(attrs={'class': 'input'}),
            'descricao': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Insira aqui sua descrição',
                'rows': 3
            }),
            'semaforo': forms.Select(attrs={'class': 'input'}),
            'horario_incidente': forms.TimeInput(attrs={'class': 'input', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deixa o campo semáforo opcional no formulário
        self.fields['semaforo'].required = False
        self.fields['tipo'].label = "Tipo de ocorrência"
        self.fields['via'].label = "Endereço (Via)"
        self.fields['descricao'].label = "Descrição"
