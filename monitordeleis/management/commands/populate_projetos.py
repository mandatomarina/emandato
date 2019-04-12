from django.core.management.base import BaseCommand
from monitordeleis.models import Projeto
import requests
from lxml.etree import parse
import zipfile
import io
import datetime

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_projetos_xml(self):
        print("Loading xml...")
        url = "http://www.al.sp.gov.br/repositorioDados/processo_legislativo/proposituras.zip"
        projetos = parse(self.download_extract_zip(url, "proposituras.xml")).getroot()
        return projetos

    def _create_projetos(self):
        projetos = self._load_projetos_xml()
        base = Projeto.objects.all().values_list('idDocumento', flat=True)

        for item in projetos.xpath('//propositura'):
            ano_legislativo = item.xpath('./AnoLegislativo')[0].text
            numero_legislativo = item.xpath('./NroLegislativo')[0].text
            ementa = item.xpath('./Ementa')[0].text
            idDocumento = item.xpath('./IdDocumento')[0].text
            natureza_id = item.xpath('./IdNatureza')[0].text
            count = 0
            if ano_legislativo in ['2019'] and natureza_id in ['1', '2', '3', '4'] and idDocumento not in base: #configurar para coisas uteis
                data = self.date_convert(item.xpath('./DtPublicacao')[0].text)
                dt_publicacao = self.date_convert(item.xpath('./DtEntradaSistema')[0].text)
                p = Projeto(ementa=ementa, idDocumento=idDocumento, numero_legislativo=numero_legislativo,
                            ano_legislativo=ano_legislativo, data=data, dt_publicacao=dt_publicacao,
                            natureza_id=natureza_id)
                count += 1
                p.save() #trocar por commit
        print("{} projetos carregados".format(count))

    def download_extract_zip(self, url, arquivo):
        """
        Download a ZIP file and extract its contents in memory
        yields (filename, file-like object) pairs
        """
        response = requests.get(url)
        with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
            return thezip.open(arquivo)

    def date_convert(self, date):
        return datetime.datetime.strptime(date.split("T")[0], "%Y-%m-%d")

    def handle(self, *args, **options):
        self._create_projetos()
