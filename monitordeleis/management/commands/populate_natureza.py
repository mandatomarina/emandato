from django.core.management.base import BaseCommand
from monitordeleis.models import Natureza
import requests
from lxml.etree import fromstring

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_naturezas(self):
        print("Loading xml...")
        url = "https://www.al.sp.gov.br/repositorioDados/processo_legislativo/naturezasSpl.xml"
        xml = requests.get(url).content
        naturezas = fromstring(xml)
        return naturezas

    def _create_naturezas(self):
        naturezas = self._load_naturezas()
        for item in naturezas.xpath('/natureza//natureza'):
            nome = item.xpath('./nmNatureza')[0].text
            idNatureza = item.xpath('./idNatureza')[0].text
            if item.xpath('./sgNatureza'):
                sigla = item.xpath('./sgNatureza')[0].text
            else:
                sigla = ''
            tipo = item.xpath('./tpNatureza')[0].text
            n = Natureza(nome=nome, idNatureza=idNatureza, sigla=sigla, tipo=tipo)
            n.save()


    def handle(self, *args, **options):
        self._create_naturezas()
