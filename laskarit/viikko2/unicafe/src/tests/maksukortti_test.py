import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(10)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
    
    def test_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 10)
    
    def test_lataaminen_toimii(self):
        self.maksukortti.lataa_rahaa(10)
        self.assertEqual(self.maksukortti.saldo, 20)
    
    def test_vahennys_tarpeeksi_rahaa(self):
        self.maksukortti.ota_rahaa(5)
        self.assertEqual(self.maksukortti.saldo, 5)
    
    def test_vahennys_ei_tarpeeksi_rahaa(self):
        self.maksukortti.ota_rahaa(20)
        self.assertEqual(self.maksukortti.saldo, 10)

    def test_vahennys_palautusarvot(self):
        self.assertEqual(self.maksukortti.ota_rahaa(5), True)
        self.assertEqual(self.maksukortti.ota_rahaa(20), False)
    
    def test_oikea_tulostus(self):
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")