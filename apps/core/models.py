import uuid
from django.db import models


class Marca(models.Model):
    codmar = models.IntegerField(primary_key=True, db_column='CODMAR')
    nommar = models.CharField(max_length=100, db_column='NOMMAR')

    class Meta:
        db_table = 'TABELA_MARCAS_VEICULOS'


class Modelo(models.Model):
    codmod = models.IntegerField(primary_key=True, db_column='CODMOD')
    codmar = models.ForeignKey(Marca, on_delete=models.CASCADE, db_column='CODMAR')
    nommod = models.CharField(max_length=150, db_column='NOMMOD')
    segveh = models.CharField(max_length=20, default='HATCH', db_column='SEGVEH')

    class Meta:
        db_table = 'TABELA_MODELOS_VEICULOS'


class FipeCache(models.Model):
    idcache = models.BigAutoField(primary_key=True, db_column='IDCACHE')
    codfipe = models.CharField(max_length=20, db_column='CODFIPE')
    codmod = models.ForeignKey(Modelo, on_delete=models.CASCADE, db_column='CODMOD')
    anomod = models.IntegerField(db_column='ANOMOD')
    tipcomb = models.CharField(max_length=30, db_column='TIPCOMB')
    valfipe = models.DecimalField(max_digits=12, decimal_places=2, db_column='VALFIPE')
    mesref = models.CharField(max_length=50, db_column='MESREF')
    datatu = models.DateTimeField(auto_now=True, db_column='DATATU')

    class Meta:
        db_table = 'TABELA_CACHE_FIPE'
        unique_together = ('codfipe', 'anomod')


class TaxaEstadual(models.Model):
    coduf = models.CharField(max_length=2, primary_key=True, db_column='CODUF')
    aliqipva = models.DecimalField(max_digits=5, decimal_places=4, db_column='ALIQIPVA')
    vallice = models.DecimalField(max_digits=8, decimal_places=2, db_column='VALLICE')

    class Meta:
        db_table = 'TABELA_TAXAS_ESTADUAIS'


class CatalogoManutencao(models.Model):
    idcat = models.AutoField(primary_key=True, db_column='IDCAT')
    segveh = models.CharField(max_length=20, db_column='SEGVEH')
    nomitem = models.CharField(max_length=100, db_column='NOMITEM')
    valpadr = models.DecimalField(max_digits=10, decimal_places=2, db_column='VALPADR')
    intkm = models.IntegerField(null=True, blank=True, db_column='INTKM')

    class Meta:
        db_table = 'TABELA_CATALOGO_MANUTENCAO'


class AvaliacaoVeiculo(models.Model):
    codaval = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='CODAVAL')
    codfipe = models.CharField(max_length=20, db_column='CODFIPE')
    anomod = models.IntegerField(db_column='ANOMOD')
    valanun = models.DecimalField(max_digits=12, decimal_places=2, db_column='VALANUN')
    kmatu = models.IntegerField(db_column='KMATU')
    coduf = models.ForeignKey(TaxaEstadual, on_delete=models.PROTECT, db_column='CODUF')
    kmestano = models.IntegerField(default=15000, db_column='KMESTANO')
    valfipemom = models.DecimalField(max_digits=12, decimal_places=2, db_column='VALFIPEMOM')
    custoimed = models.DecimalField(max_digits=12, decimal_places=2, db_column='CUSTOIMED')
    tcoano1 = models.DecimalField(max_digits=12, decimal_places=2, db_column='TCOANO1')
    datcria = models.DateTimeField(auto_now_add=True, db_column='DATCRIA')

    class Meta:
        db_table = 'TABELA_AVALIACOES_VEICULOS'


class ChecklistAvaliacao(models.Model):
    idcheck = models.BigAutoField(primary_key=True, db_column='IDCHECK')
    codaval = models.ForeignKey(AvaliacaoVeiculo, on_delete=models.CASCADE, related_name='items', db_column='CODAVAL')
    idcat = models.ForeignKey(CatalogoManutencao, on_delete=models.PROTECT, db_column='IDCAT')
    indnec = models.BooleanField(default=False, db_column='INDNEC')
    valcust = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='VALCUST')

    class Meta:
        db_table = 'TABELA_CHECKLIST_AVALIACAO'