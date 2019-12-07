from kamus import Kamus
import fstem
from enum import Enum

kamus = Kamus()


class Stemmer(Enum):
    STANDARD_CS_STEMMER = 2
    ENHANCED_CS_STEMMER = 3


class Kata:
    rule: int = 0
    log_rules: int = 0

    def __init__(self, label, bentuk_dasar="", stemmer_choice=Stemmer.ENHANCED_CS_STEMMER):
        self.label = label
        self.bentuk_dasar = bentuk_dasar
        self.stemmer_choice = stemmer_choice

    def _check_dict_change(self, kata: str):
        if kamus.check(kata):
            self.bentuk_dasar = kata
            return True

        return False

    def stem(self):
        kata: str = self.label
        log_kata = kata
        log_kata_berawalan: str

        partikel = ""
        pp = ""
        ds = ""

        isprecedence = fstem.cekPrecedence(kata)

        if self._check_dict_change(kata): return

        if isprecedence:
            kata = self.reduksi_awalan(kata, ds, False)
            if self._check_dict_change(kata): return

        partikel = fstem.getPartikel(kata)
        pp = fstem.getPP(kata[:len(kata) - len(partikel)])
        ds = fstem.getDS(kata[:len(kata) - len(partikel)])

        kata = self.reduksi_akhiran(kata, partikel, pp, ds)
        log_kata_berawalan = self.reduksi_akhiran(self.label, partikel, pp, ds)

        if self._check_dict_change(kata): return

        if isprecedence:
            if prefix_sama:
                kata = self.recoding(log_rules)
            else:
                kata = self.recoding(rule, kata)

            if self._check_dict_change(kata): return
        else:
            kata = self.reduksi_awalan(kata, ds, True)
            if self._check_dict_change(kata): return

        if self.stemmer_choice == Stemmer.ENHANCED_CS_STEMMER:
            kata = self.loop_pengembalian_akhiran(log_kata_berawalan, partikel, pp, ds)
            if self._check_dict_change(kata): return

        try:
            index_strip = log_kata.index('-')
        except Exception as e:
            index_strip = -1

        if index_strip > 0 and index_strip != -1:
            kiri = Kata(log_kata[:index_strip])
            kanan = Kata(log_kata[index_strip + 1:])

            kiri.stem()
            kanan.stem()
            stem_kiri = kiri.get_bentuk_dasar(self.stemmer_choice)
            stem_kanan = kanan.get_bentuk_dasar(self.stemmer_choice)

            if (stem_kiri == stem_kanan) and stem_kiri != "":
                self.bentuk_dasar = stem_kiri

        if self._check_dict_change(kata):
            return
        else:
            self.bentuk_dasar = self.label = ''

    def get_bentuk_dasar(self):
        self.stem()

        return self.bentuk_dasar

    def loop_reduksi_awalan(self, kata: str, ds: str, isrecoded: bool):
        count = 1
        rule = 0
        log_rules = 0
        prefix_sama = False

        log_prefix = ""
        word = kata

        while count <= 3:
            if fstem.cekKombinasiTerlarang(word, ds):
                break

            rule = fstem.getRule(word, self.stemmer_choice)
            prefix = fstem.getPrefix(rule, word)

            if rule == 0:
                rule = log_rules

            if prefix == log_prefix:
                prefix_sama = True
                break
            else:
                word = fstem.getReduksi(rule, word)
                if kamus.check(word):
                    return word

            # logging previous iteratuon
            log_rules = rule
            log_prefix = prefix
            count += 1

        if (not kamus.check(word)) and isrecoded:
            if prefix_sama:
                word = self.recoding(log_rules, word)
            else:
                word = self.recoding(rule, word)

    def reduksi_awalan(self, kata: str, ds: str, isrecoded: bool):
        hasil = kata

        hasil = self.loop_reduksi_awalan(hasil, ds, isrecoded)

        return hasil

    def reduksi_akhiran(self, kata: str, partikel: str, pp: str, ds: str):
        if partikel != '':
            kata = kata[:len(kata) - len(partikel)]
            if kamus.check(kata):
                return kata

        if pp != '':
            kata = kata[:len(kata) - len(pp)]
            if kamus.check(kata):
                return kata

        if ds != '':
            kata = kata[:len(kata) - len(ds)]
            if kamus.check(kata):
                return kata

        return kata

    def loop_pengembalian_akhiran(self, kata: str, partikel: str, pp: str, ds: str):
        hasil = kata
        log = hasil

        if kamus.check(kata):
            return kata
        else:
            log = self.loop_reduksi_awalan(hasil, "", True)
            if kamus.check(log):
                return log

        while ds != "":
            if ds == "kan":
                hasil = hasil + "k"
                ds = "an"
            else:
                hasil = hasil + ds

            if kamus.check(hasil):
                return hasil
            else:
                log = self.loop_reduksi_awalan(hasil, ds, True)
                if kamus.check(log):
                    return log

        if pp != "":
            hasil = hasil + pp

            if kamus.check(hasil):
                return hasil
            else:
                log = self.loop_reduksi_awalan(hasil, "", True)
                if kamus.check(log):
                    return log

        if partikel != "":
            hasil = hasil + partikel

            if kamus.check(hasil):
                return hasil
            else:
                log = self.loop_reduksi_awalan(hasil, "", True)
                if kamus.check(log):
                    return log

        return hasil

    def recoding(self, rule: int, kata: str):
        recoding_chr: chr = ''
        result = kata

        if rule in [1, 6, 21]:
            recoding_chr = 'r'
        elif rule in [13, 26, 32]:
            recoding_chr = 'p'
        elif rule in [15, 28]:
            recoding_chr = 't'
        elif rule in [17, 30]:
            recoding_chr = 'k'
        elif rule in [18, 31]:
            recoding_chr = 'p'

        if recoding_chr != '':
            if rule in [13, 15, 26, 28]:
                result = recoding_chr + kata[1:]
            else:
                result = recoding_chr + kata
                if self.stemmer_choice == Stemmer.ENHANCED_CS_STEMMER and \
                        rule in [17, 30] and (not kamus.check(result)):
                    result = result[2:]

        return result
