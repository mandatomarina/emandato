from django.core.management.base import BaseCommand
from monitordeleis.models import Autor, Projeto
import requests
from lxml.etree import parse
import zipfile
import io

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _load_autores(self):
        print("Loading xml...")
        url = "http://www.al.sp.gov.br/repositorioDados/processo_legislativo/documento_autor.zip"
        autores = parse(self.download_extract_zip(url, "documento_autor.xml")).getroot()
        return autores

    def _create_autores(self):
        autores_xml = self._load_autores()
        autores = Autor.objects.all().values_list('idAutor', flat=True)
        projetos = Projeto.objects.all().values_list('idDocumento', flat=True)
        print("Loaded {} projects".format(len(autores_xml.xpath('//DocumentoAutor'))))
        for item in autores_xml.xpath('//DocumentoAutor'):
            nome = item.xpath('./NomeAutor')[0].text
            idDocumento = item.xpath('./IdDocumento')[0].text
            idAutor = item.xpath('./IdAutor')[0].text
            if idDocumento in projetos:
                p = Projeto.objects.filter(idDocumento=idDocumento)

                if idAutor not in autores:
                    a = Autor(nome=nome, idAutor=idAutor)
                    a.save() #trocar por commit
                if p:
                    a = Autor.objects.filter(idAutor=idAutor)[0]
                    p[0].autor.add(a)
                    #p[0].save()



    def download_extract_zip(self, url, arquivo):
        """
        Download a ZIP file and extract its contents in memory
        yields (filename, file-like object) pairs
        """
        response = requests.get(url)
        with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
            return thezip.open(arquivo)

    def handle(self, *args, **options):
        self._create_autores()
