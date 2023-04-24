from bs4 import BeautifulSoup
class Cleanable:
    def clean(self,attr):
        return BeautifulSoup(attr,features="html.parser").get_text()

class Unit:
    def __init__(self, dados):
        self.agendamento = dados['agendamento']
        self.atendimento = dados['atendimento']
        self.nome = dados['unidade']['nome']
        self.endereco = dados['unidade']['endereco']
        self.complemento = dados['unidade']['complemento']
        self.bairro = dados['unidade']['bairro']
        self.mapa = dados['unidade']['source']

class Step(Cleanable):
    def __init__(self,journey_step):
        self.titulo = self.clean(journey_step['titulo'])
        self.instrucoes = self.clean(journey_step['conteudo'])
        self.ordem = str(journey_step['ordem'])

class Article(Cleanable):
    def __init__(self, article_data):
        self.base = 'https://servicos.portal.ap.gov.br/servicos/'
        self.titulo = article_data['titulo']
        self.descricao = self.clean(article_data['descricao'])
        self.publico = self.clean(article_data['publico'])
        self.requisitos = self.clean(article_data['requisitos'])
        self.tempo = str(article_data['tempo'])
        self.custo = article_data['custo']
        self.online = article_data['online']
        self.has_link = article_data['acesso_externo']
        self.link =  article_data['url_externo'] if self.has_link else ''
        self.url = self.base + article_data['slug']
        self.medida_tempo = article_data['tipo_tempo']


class Service(Cleanable):
    def __init__(self,service):

        self.titulo = service['titulo']
        self.descricao = self.clean(service['descricao'])
        self.orgao = service['setor']['orgao']['sigla'] or service['setor']['sigla']
        self.link = service['slug']
        self.online = service['online']

