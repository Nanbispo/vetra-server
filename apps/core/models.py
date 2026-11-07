import uuid
from django.db import models


class Marca(models.Model):
    codmar = models.AutoField(primary_key=True, db_column='codmar')
    nommarc = models.CharField(max_length=100, db_column='nommarc')

    class Meta:
        db_table = 'marca'

    def __str__(self):
        return self.nommarc


class Modelo(models.Model):
    codmod = models.AutoField(primary_key=True, db_column='codmod')
    codmar = models.ForeignKey(Marca, on_delete=models.CASCADE, db_column='codmar')
    nommod = models.CharField(max_length=150, db_column='nommod')
    segveh = models.CharField(max_length=20, db_column='segveh')

    class Meta:
        db_table = 'modelo'

    def __str__(self):
        return self.nommod


class TabelaFipeCache(models.Model):
    codcache = models.BigAutoField(primary_key=True, db_column='codcache')
    codfipe = models.CharField(max_length=20, db_column='codfipe')
    codmod = models.ForeignKey(Modelo, on_delete=models.CASCADE, db_column='codmod')
    anomod = models.IntegerField(db_column='anomod')
    tipcomb = models.CharField(max_length=30, db_column='tipcomb')
    valfipe = models.DecimalField(max_digits=12, decimal_places=2, db_column='valfipe')
    mesref = models.CharField(max_length=50, db_column='mesref')
    datatu = models.DateTimeField(auto_now=True, db_column='datatu')

    class Meta:
        db_table = 'tabela_fipe_cache'
        unique_together = ('codfipe', 'anomod')


class UfTaxa(models.Model):
    coduf = models.CharField(max_length=2, primary_key=True, db_column='coduf')
    aliqipva = models.DecimalField(max_digits=5, decimal_places=4, db_column='aliqipva')
    vallice = models.DecimalField(max_digits=8, decimal_places=2, db_column='vallice')

    class Meta:
        db_table = 'uf_taxa'

    def __str__(self):
        return self.coduf


class CatalogoManutencao(models.Model):
    codcat = models.AutoField(primary_key=True, db_column='codcat')
    segveh = models.CharField(max_length=20, db_column='segveh')
    nomitem = models.CharField(max_length=100, db_column='nomitem')
    valpadr = models.DecimalField(max_digits=10, decimal_places=2, db_column='valpadr')
    intkm = models.IntegerField(null=True, blank=True, db_column='intkm')

    class Meta:
        db_table = 'catalogo_manutencao'

    def __str__(self):
        return f"[{self.segveh}] {self.nomitem}"


class AvaliacaoVeiculo(models.Model):
    codaval = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='codaval')
    codfipe = models.CharField(max_length=20, db_column='codfipe')
    anomod = models.IntegerField(db_column='anomod')
    valanun = models.DecimalField(max_digits=12, decimal_places=2, db_column='valanun')
    kmatu = models.IntegerField(db_column='kmatu')
    coduf = models.ForeignKey(UfTaxa, on_delete=models.PROTECT, db_column='coduf')
    kmestano = models.IntegerField(default=15000, db_column='kmestano')
    valfipemom = models.DecimalField(max_digits=12, decimal_places=2, db_column='valfipemom')
    custoimed = models.DecimalField(max_digits=12, decimal_places=2, db_column='custoimed')
    tcoano1 = models.DecimalField(max_digits=12, decimal_places=2, db_column='tcoano1')
    datcria = models.DateTimeField(auto_now_add=True, db_column='datcria')

    class Meta:
        db_table = 'avaliacao_veiculo'


class ChecklistAvaliacao(models.Model):
    codcheck = models.BigAutoField(primary_key=True, db_column='codcheck')
    codaval = models.ForeignKey(AvaliacaoVeiculo, on_delete=models.CASCADE, related_name='checklist_items', db_column='codaval')
    codcat = models.ForeignKey(CatalogoManutencao, on_delete=models.PROTECT, db_column='codcat')
    indnec = models.BooleanField(default=False, db_column='indnec')
    valcust = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='valcust')

    class Meta:
        db_table = 'checklist_avaliacao'