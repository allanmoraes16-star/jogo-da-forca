"""Testes automáticos do Projeto 08 (somente biblioteca padrão de Python)."""
import contextlib
import io
import unittest
from unittest.mock import patch

from projeto08_forca import (
    ANIMAIS, FRUTAS, PEIXES, PALAVRAS, MAX_ERROS,
    categoria_da_palavra, escolher_palavra, montar_exibicao,
    venceu, ler_letra, jogar_rodada, principal,
)


class TestarCatalogo(unittest.TestCase):
    def test_01_estrutura_e_quantidade(self):
        self.assertIsInstance(PALAVRAS, tuple)
        self.assertEqual(len(PALAVRAS), 96)
        self.assertEqual([len(PEIXES), len(FRUTAS), len(ANIMAIS)], [32, 32, 32])
        self.assertEqual(MAX_ERROS, 6)
        self.assertTrue(all(isinstance(par, tuple) and len(par) == 2 for par in PALAVRAS))

    def test_02_sem_repeticoes_e_respostas_validas(self):
        palavras = [palavra for palavra, _ in PALAVRAS]
        self.assertEqual(len(palavras), len(set(palavras)))
        self.assertTrue(all(p.isascii() and p.isalpha() and p.islower() for p in palavras))
        self.assertTrue(all(dica.strip() for _, dica in PALAVRAS))

    def test_03_intercalacao_das_categorias(self):
        self.assertEqual([categoria_da_palavra(PALAVRAS[i][0]) for i in range(6)], [
            'PEIXES', 'FRUTAS E SEMENTES', 'OUTROS ANIMAIS',
            'PEIXES', 'FRUTAS E SEMENTES', 'OUTROS ANIMAIS'])

    def test_04_primeiras_palavras_categorias(self):
        self.assertEqual(escolher_palavra(1)[0], 'tambaqui')
        self.assertEqual(escolher_palavra(2)[0], 'cupuacu')
        self.assertEqual(escolher_palavra(3)[0], 'onca')

    def test_05_ciclo_com_96_rodadas(self):
        self.assertEqual(escolher_palavra(97), escolher_palavra(1))
        self.assertEqual(escolher_palavra(98), escolher_palavra(2))
        self.assertEqual(escolher_palavra(96), PALAVRAS[-1])

    def test_06_rodada_invalida(self):
        with self.assertRaises(ValueError):
            escolher_palavra(0)

    def test_07_categoria_desconhecida(self):
        with self.assertRaises(ValueError):
            categoria_da_palavra('dinossauro')


class TestarRegras(unittest.TestCase):
    def test_08_montar_exibicao(self):
        self.assertEqual(montar_exibicao('tambaqui', ['t', 'a']), 't a _ _ a _ _ _')

    def test_09_venceu(self):
        self.assertFalse(venceu('tambaqui', ['t', 'a', 'm']))
        self.assertTrue(venceu('tambaqui', list('tambaqui')))

    def test_10_validacao_de_entrada(self):
        with patch('builtins.input', side_effect=['12', 'ab', 'á', 't', ' A ']), \
             contextlib.redirect_stdout(io.StringIO()) as saida:
            self.assertEqual(ler_letra(['t']), 'a')
        self.assertIn('Você já tentou', saida.getvalue())
        self.assertEqual(saida.getvalue().count('Digite apenas UMA letra'), 3)

    def test_11_vitoria_40_pontos(self):
        with patch('builtins.input', side_effect=list('tambqui')), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(jogar_rodada(1), (True, 40))

    def test_12_derrota_seis_erros(self):
        with patch('builtins.input', side_effect=list('xyzvwk')), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(jogar_rodada(1), (False, 0))

    def test_13_repeticao_nao_custa_vida(self):
        with patch('builtins.input', side_effect=['x', 'x'] + list('tambqui')), \
             contextlib.redirect_stdout(io.StringIO()) as saida:
            self.assertEqual(jogar_rodada(1), (True, 35))
        self.assertIn('Você já tentou essa letra', saida.getvalue())

    def test_14_placar_uma_rodada(self):
        with patch('builtins.input', side_effect=list('tambqui') + ['talvez', 'n']), \
             contextlib.redirect_stdout(io.StringIO()) as saida:
            principal()
        self.assertIn('Rodadas: 1', saida.getvalue())
        self.assertIn('Vitórias: 1', saida.getvalue())
        self.assertIn('Pontuação total: 40', saida.getvalue())
        self.assertIn("Responda apenas 's' ou 'n'", saida.getvalue())

    def test_15_placar_dois_tipos_de_rodadas(self):
        # rodada 1 = tambaqui; rodada 2 = cupuacu
        with patch('builtins.input', side_effect=list('tambqui') + ['s'] + list('xyzvwl') + ['n']), \
             contextlib.redirect_stdout(io.StringIO()) as saida:
            principal()
        self.assertIn('Rodadas: 2', saida.getvalue())
        self.assertIn('Vitórias: 1', saida.getvalue())
        self.assertIn('Pontuação total: 40', saida.getvalue())


if __name__ == '__main__':
    unittest.main()
