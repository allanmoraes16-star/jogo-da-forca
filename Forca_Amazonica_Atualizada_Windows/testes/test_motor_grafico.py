"""Testes sem pygame: autosave, recuperação, tentativas e pontuação."""
import json
import tempfile
from pathlib import Path
import unittest

from motor_grafico import (
    novo_estado,tentar_letra,proxima_rodada,
    salvar_jogo,carregar_jogo
)

class MotorGraficoTestes(unittest.TestCase):
    def test_nova_rodada(self):
        e=novo_estado()
        self.assertEqual(e['palavra'],'tambaqui')
        self.assertEqual(e['vidas'],6)
        self.assertFalse(e['finalizada'])

    def test_acerto_e_erro(self):
        e=novo_estado()
        self.assertEqual(tentar_letra(e,'t'),'acerto')
        self.assertEqual(tentar_letra(e,'x'),'erro')
        self.assertEqual(e['vidas'],5)

    def test_repeticao_nao_consume_vida(self):
        e=novo_estado()
        tentar_letra(e,'X')
        self.assertEqual(tentar_letra(e,' x '),'repetida')
        self.assertEqual(e['vidas'],5)

    def test_vitoria_pontos_40(self):
        e=novo_estado()
        for letra in 'tambqui':
            resultado=tentar_letra(e,letra)
        self.assertEqual(resultado,'vitoria')
        self.assertEqual(e['pontuacao'],40)
        self.assertEqual(e['vitorias'],1)
        self.assertTrue(e['finalizada'])

    def test_derrota(self):
        e=novo_estado()
        for letra in 'xyzfgh':
            resultado=tentar_letra(e,letra)
        self.assertEqual(resultado,'derrota')
        self.assertEqual(e['vidas'],0)
        self.assertEqual(e['pontuacao'],0)

    def test_proxima_sem_finalizar_lanca_erro(self):
        with self.assertRaises(ValueError):
            proxima_rodada(novo_estado())

    def test_continuacao_mantem_placar(self):
        e=novo_estado()
        for l in 'tambqui':tentar_letra(e,l)
        prox=proxima_rodada(e)
        self.assertEqual(prox['rodada'],2)
        self.assertEqual(prox['pontuacao'],40)
        self.assertEqual(prox['palavra'],'cupuacu')

    def test_salvar_recarregar_meio_rodada(self):
        with tempfile.TemporaryDirectory() as tmp:
            e=novo_estado()
            tentar_letra(e,'t');tentar_letra(e,'x')
            destino=Path(tmp)/'progresso.json'
            salvar_jogo(e,{'musica':False,'efeitos':True},destino)
            recuperado,config,msg=carregar_jogo(destino)
            self.assertEqual(recuperado,e)
            self.assertEqual(recuperado['acertadas'],['t'])
            self.assertEqual(recuperado['erradas'],['x'])
            self.assertFalse(config['musica'])
            self.assertIn('recuperado',msg.lower())

    def test_autosave_rodada_finalizada_nao_duplica_pontos(self):
        with tempfile.TemporaryDirectory() as tmp:
            e=novo_estado()
            for l in 'tambqui':tentar_letra(e,l)
            destino=Path(tmp)/'progresso.json'
            salvar_jogo(e,destino=destino)
            recuperado,_,_=carregar_jogo(destino)
            self.assertEqual(recuperado['pontuacao'],40)
            self.assertEqual(tentar_letra(recuperado,'t'),'finalizada')
            self.assertEqual(recuperado['pontuacao'],40)

    def test_save_corrompido_abre_novo_jogo(self):
        with tempfile.TemporaryDirectory() as tmp:
            destino=Path(tmp)/'progresso.json'
            destino.write_text('{quebrado!',encoding='utf8')
            estado,_,aviso=carregar_jogo(destino)
            self.assertEqual(estado['rodada'],1)
            self.assertIn('Não foi possível',aviso)

    def test_salvamento_impossivel_nao_substitui_valido(self):
        with tempfile.TemporaryDirectory() as tmp:
            destino=Path(tmp)/'progresso.json'
            e=novo_estado()
            salvar_jogo(e,destino=destino)
            conteudo=destino.read_bytes()
            e['acertadas']=['x'] # estado incompatível não deve gravar
            with self.assertRaises(ValueError):
                salvar_jogo(e,destino=destino)
            self.assertEqual(destino.read_bytes(),conteudo)


    def test_sequencia_aumenta_em_vitorias(self):
        e = novo_estado()
        for l in 'tambqui':
            tentar_letra(e, l)
        self.assertEqual(e['sequencia_atual'], 1)
        e = proxima_rodada(e)
        for l in 'cupa':
            tentar_letra(e, l)
        self.assertEqual(e['sequencia_atual'], 2)
        self.assertEqual(e['melhor_sequencia'], 2)

    def test_derrota_zera_sequencia(self):
        e = novo_estado(sequencia_atual=3, melhor_sequencia=3)
        for letra in 'xyzfgh':
            resultado = tentar_letra(e, letra)
        self.assertEqual(resultado, 'derrota')
        self.assertEqual(e['sequencia_atual'], 0)
        self.assertEqual(e['melhor_sequencia'], 3)

    def test_save_antigo_sem_sequencia_continua_compativel(self):
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp)/'progresso.json'
            conteudo = {
                'versao': 1,
                'estado': {
                    'rodada': 1, 'vitorias': 0, 'pontuacao': 0,
                    'palavra': 'tambaqui', 'dica': 'x',
                    'acertadas': ['t'], 'erradas': ['x'], 'vidas': 5,
                    'finalizada': False, 'mensagem': 'ok'
                },
                'config': {'musica': True, 'efeitos': False}
            }
            destino.write_text(json.dumps(conteudo), encoding='utf8')
            estado, config, _ = carregar_jogo(destino)
            self.assertEqual(estado['sequencia_atual'], 0)
            self.assertEqual(estado['melhor_sequencia'], 0)
            self.assertFalse(config['efeitos'])


    def test_vitoria_sem_mensagem_gif(self):
        e = novo_estado()
        for letra in 'tambqui':
            resultado = tentar_letra(e, letra)
        self.assertEqual(resultado, 'vitoria')
        self.assertIn('Nome revelado', e['mensagem'])
        self.assertNotIn('GIF', e['mensagem'])

if __name__=='__main__':
    unittest.main()
