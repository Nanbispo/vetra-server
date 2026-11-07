import requests
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

# Import your cache and model classes (adjust the import path if necessary)
from app.core.models import FipeCache, Modelo, Marca

FIPE_API_BASE_URL = "https://parallelum.com.br/fipe/api/v1/carros"


class FipeService:
    """
        Busca o preço FIPE no cache local (TABELA_CACHE_FIPE)[cite: 1].
        Caso não exista ou esteja defasado (>30 dias), consome a API pública e atualiza o banco[cite: 1].
    """

    @staticmethod
    def get_or_fetch_price(codfipe: str, anomod: int, codmod_id: int = None) -> dict:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        cache_entry = FipeCache.objects.filter(
            codfipe=codfipe, 
            anomod=anomod,
            datatu__gte=thirty_days_ago
        ).first()

        if cache_entry:
            return {
                'valfipe': cache_entry.valfipe,
                'mesref': cache_entry.mesref,
                'tipcomb': cache_entry.tipcomb,
                'cached': True
            }

        # Consulta externa se o cache expirou ou não existe
        url = f"{FIPE_API_BASE_URL}/veiculos/{codfipe}/{anomod}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            # Sanitização do preço ("R$ 45.000,00" -> Decimal 45000.00)
            raw_price = data.get("Valor", "0").replace("R$", "").replace(".", "").replace(",", ".").strip()
            valfipe = Decimal(raw_price)
            mesref = data.get("MesReferencia", "")
            tipcomb = data.get("Combustivel", "Flex")

            if codmod_id:
                modelo_obj = Modelo.objects.get(pk=codmod_id)
                FipeCache.objects.update_or_create(
                    codfipe=codfipe,
                    anomod=anomod,
                    defaults={
                        'codmod': modelo_obj,
                        'valfipe': valfipe,
                        'mesref': mesref,
                        'tipcomb': tipcomb
                    }
                )

            return {
                'valfipe': valfipe,
                'mesref': mesref,
                'tipcomb': tipcomb,
                'cached': False
            }
        except Exception:
            # Em caso de falha externa, recupera a versão de cache mais recente disponível
            fallback = FipeCache.objects.filter(codfipe=codfipe, anomod=anomod).first()
            if fallback:
                return {
                    'valfipe': fallback.valfipe,
                    'mesref': fallback.mesref,
                    'tipcomb': fallback.tipcomb,
                    'cached': True
                }
            raise ValueError("Não foi possível obter a cotação FIPE para o veículo informado.")
