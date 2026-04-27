
from django.db import models
from django.conf import settings
from apps.vias.models import Via

class Ocorrencia(models.Model):
    class Tipo(models.TextChoices):
        ACIDENTE        = 'ACIDENTE',        'Acidente'
        CONGESTIONAMENTO= 'CONGESTIONAMENTO', 'Congestionamento'
        BURACO          = 'BURACO',          'Buraco na via'
        SEMAFORO        = 'SEMAFORO',        'Semáforo com defeito'
        ALAGAMENTO      = 'ALAGAMENTO',      'Alagamento'
        OBRA            = 'OBRA',            'Obra / interdição'

#o ciclo de status de uma ocorrência(aberta->em atendimento->fechada)
    class Status(models.TextChoices):
        ABERTA         = 'ABERTA',         'Aberta'
        EM_ATENDIMENTO = 'EM_ATENDIMENTO', 'Em atendimento'
        ENCERRADA      = 'ENCERRADA',      'Encerrada'

#define o tipo de ocorrência e o usuário dá detalhes da situação
    tipo      = models.CharField(
        max_length=20, 
        choices=Tipo.choices)
    verbose_name='Tipo de ocorrência',
    descricao = models.TextField()
    status    = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.ABERTA
    )

    #detalha em qual via está a ocorrência
    via = models.ForeignKey(
        Via, 
        on_delete=models.SET_NULL,
        null=True,
        verbose_name = 'Via/Rua'
    )
    
    #Detalhes do usuário que fez a ocorrência
    usuario   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
        verbose_name = 'Registrada por'
    )
#informa a localização da via com ocorrências
    latitude  = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

#imagem e data/hora da via com ocorrência
    foto      = models.ImageField(upload_to='ocorrencias/', blank=True, verbose_name= 'Foto da ocorrência')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
    #nome amigável no admin
        verbose_name = 'Ocorrência'
        verbose_name_plural = 'Ocorrências'
    # Ordena as ocorrências da mais recente para a mais antiga
        ordering = ['-criado_em']
    #representação textual de quando se 'imprime' uma ocorrência
    def __str__(self):
        return f'{self.get_tipo_display()} - {self.get_status_display()}'