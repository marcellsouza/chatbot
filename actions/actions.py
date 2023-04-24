from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from api import api

class ActionBuscaPortal(Action):
    def __init__(self):
        self.servicos = api.Api()
    def name(self) -> Text:
        return "action_servico_busca"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                domain: DomainDict) -> List[Dict[Text, Any]]:
            """Normalize keywords and make request."""
            #ultima frase
            serv = tracker.get_slot('servico_pedido')

            #pesquisa na api
            res = self.servicos.search(serv)
            quantos = len(res)
            buttons = []
            if quantos:
                message = 'Encontrei alguns servicos que podem te interessar'
                if quantos > 4:
                     for i in range(0,5):
                        payload = "/servico_artigo{\"servico_entity\":\"" + res[i].link + "\"}"
                        buttons.append({"title": format(res[i].titulo), "payload": payload})
                else:
                     for service in res:
                        payload = "/servico_artigo{\"servico_entity\":\"" + service.link + "\"}"
                        buttons.append({"title": format(service.titulo), "payload": payload})
                dispatcher.utter_button_message(message, buttons)
            else:
                dispatcher.utter_message('Não encontrei nenhum serviço relacionado a isso. Pode tentar com outras palavras?')

class ActionGestaoInfo(Action):
    def __init__(self):
        self.meili = api.Meili('gestao')
    def name(self) -> Text:
        return "action_gestao_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                domain: DomainDict) -> List[Dict[Text, Any]]:
            """Normalize keywords and make request."""
            #ultima frase
            serv = tracker.get_slot('gestao_pedido')

            #pesquisa na api
            res = self.meili.search(serv,True)
            quantos = len(res)
            buttons = []
            if quantos:
                dispatcher.utter_message(f"{res['est_titulo']}")
                dispatcher.utter_message(f"[Clique aqui para ver informações sobre o orgão. Email,contato,endereço, gestão]({res['link']})")
            else:
                dispatcher.utter_message('Não encontrei o orgão ou secretaria.')

class ActionArtigoPortal(Action):
    def __init__(self):
        self.servicos = api.Api()
    def name(self) -> Text:
        return "action_servico_artigo"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                domain: DomainDict) -> List[Dict[Text, Any]]:
            serv = tracker.get_slot('servico_slug')
            print('serv');

            #pesquisa na api
            res = self.servicos.view(serv)
            if res:
                dispatcher.utter_message('Serviço: ' + res.titulo)
                if(not res.online):
                        dispatcher.utter_message('Esse serviço é presencial')
                else:
                        if(res.link):
                            resposta = f"Pode ser realizado pela internet [nessa página]({res.link})"
                            dispatcher.utter_message(resposta)
                        else:
                            dispatcher.utter_message('Pode ser realizado pela internet.')

                dispatcher.utter_message('O que é: ' + res.descricao)
                dispatcher.utter_message(f"[Clique para mais informações sobre esse serviço]({res.url})")
            else:
                dispatcher.utter_message('Não encontrei nenhum serviço relacionado a isso. Pode tentar com outras palavras?')

class ActionTutorialPortal(Action):
    def __init__(self):
        self.servicos = api.Api()
    def name(self) -> Text:
        return "action_servico_tutorial"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                domain: DomainDict) -> List[Dict[Text, Any]]:
            serv = tracker.get_slot('servico_slug')
            print('serv');

            #pesquisa na api
            res = self.servicos.view(serv)
            if res:
                buttons = []
                dispatcher.utter_message('Passo a passo: ' + res.titulo)
                if not res.online:
                        buttons.append({"title": 'Unidades disponíveis', "payload": '/servico_unidades'})
                if res.tutorial:
                    for step in res.tutorial:
                        dispatcher.utter_message(step.instrucoes)


                if(len(buttons)):
                    dispatcher.utter_button_message('Onde realizar', buttons)
            else:
                dispatcher.utter_message('Não encontrei nenhum serviço relacionado a isso. Pode tentar com outras palavras?')

class ActionBuscaDiario(Action):
    def __init__(self):
        self.meili = api.Meili('diarios')
    def name(self) -> Text:
        return "action_diario_busca"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                domain: DomainDict) -> List[Dict[Text, Any]]:

            #pegar o numero do diario
            serv = tracker.get_slot('diario_pedido')
            #pesquisa na api
            res = self.meili.search(serv,True)
            print(res)
            if res:
                dispatcher.utter_message('Encontrei o diario que você estava procurando')
                resposta = f"[#{res['numero']}: {res['publicacao']}]({res['arquivo']})"
                dispatcher.utter_message(resposta)
            else:
                dispatcher.utter_message('Não encontrei o diário especificado')

class ActionUltimosDiarios(Action):
    def __init__(self):
        self.meili = api.Meili('diarios')
    def name(self) -> Text:
        return "action_diarios_recentes"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                domain: DomainDict) -> List[Dict[Text, Any]]:
            #pesquisa na api
            res = self.meili.search('')
            quantos = len(res)
            if quantos:
                dispatcher.utter_message('Aqui estão as últimas edições do diário oficial')
                if quantos > 0:
                     for diario in res:
                         resposta = f"[#{diario['numero']}: {diario['publicacao']}]({diario['arquivo']})"
                         dispatcher.utter_message(resposta)
                dispatcher.utter_message('Você também pode me perguntar um sobre um diário especifico. Algo como "diario  de 25 de janeiro de 2023"')
            else:
                dispatcher.utter_message('Não encontrei os últimos diários. Isso pode ser um erro')

class ActionRelatorio(Action):
    def __init__(self):
        self.meili = api.Meili('transparencia')
    def name(self) -> Text:
        return "action_relatorio"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                domain: DomainDict) -> List[Dict[Text, Any]]:

            #pegar o numero do diario
            serv = tracker.get_slot('relatorio_pedido')
            #pesquisa na api
            res = self.meili.search(serv)
            quantos = len(res)
            if quantos:
                dispatcher.utter_message('Aqui estão os relatórios que encontrei')
                if quantos > 0:
                     for relatorio in res:
                         resposta = f"[#{relatorio['instituicao_name']}-{relatorio['tipo']} periodo: {relatorio['periodo']}]({relatorio['arquivo']})"
                         dispatcher.utter_message(resposta)
            else:
                dispatcher.utter_message('Não encontrei nenhum relatório com esses parâmetros')


class ActionSessao(Action):
    def __init__(self):
        self.meili = api.Meili('sessoes')
    def name(self) -> Text:
        return "action_sessao"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                domain: DomainDict) -> List[Dict[Text, Any]]:

            #pegar a informação da sessão
            serv = tracker.get_slot('sessao_pedida')
            res = self.meili.search(serv,hits=3)
            quantos = len(res)
            if quantos:
                dispatcher.utter_message('Aqui estão as sessões do TCE mais próximas que encontrei')
                if quantos > 0:
                     for sessao in res:
                         resposta = f"{sessao['descricao']} do dia {sessao['data_extenso']}"
                         dispatcher.utter_message(resposta)
                         arquivos = ""
                         if 'pauta' in sessao and 'ata' in sessao:
                            arquivos = f"[Pauta da sessão]({sessao['pauta']}) | [Ata da sessão]({sessao['ata']})"
                         elif 'pauta' in sessao:
                            arquivos = f"[Pauta da sessão]({sessao['pauta']})"
                         elif 'ata' in sessao:
                            arquivos = f"[Ata da sessão]({sessao['ata']})"
                         if(arquivos):
                             dispatcher.utter_message(arquivos)
                         else:
                             dispatcher.utter_message('Essa sessão não tem nenhum arquivo cadastrado')

            else:
                dispatcher.utter_message('Não encontrei nenhuma sessão com esses parâmetros')
