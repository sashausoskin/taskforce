import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(500)
    
    def test_alustus(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_kateismaksu_edullinen_riittava(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(500), 500-240)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000+240)
    
    def test_kateismaksu_maukas_riittava(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 500-400)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000+400)
    
    def test_kateismaksu_lounasmaara_nousee(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat, 1)
    
    def test_kateismaksu_ei_riittava_maksu(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(1), 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(3), 3)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_korttimaksu_edullinen_riittava(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.kortti), True)
        self.assertEqual(self.kortti.saldo, 500-240)
    
    def test_korttimaksu_maukas_riittava(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.kortti), True)
        self.assertEqual(self.kortti.saldo, 500-400)
    
    def test_korttimaksu_tilastointi_edulliset(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_korttimaksu_tilastointi_maukkaat(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_korttimaksu_ei_rahaa_edullinen(self):
        self.kortti.saldo=10
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.kortti), False)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kortti.saldo, 10)
    
    def test_korttimaksu_ei_rahaa_maukas(self):
        self.kortti.saldo=300
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.kortti), False)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kortti.saldo, 300)
    
    def test_korttimaksu_kassa_ei_muutu(self):
        self.kortti.saldo=1000
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_kortin_lataus(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000+1000)
        self.assertEqual(self.kortti.saldo, 500+1000)

    def test_kortin_lataus_negatiivinen(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kortti.saldo, 500)