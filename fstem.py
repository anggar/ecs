from collections import namedtuple
from typing import List
from enum import Enum

Confix = namedtuple("Confix", ['ps', 'ds', 'partikel'], defaults=("", "", ""))


class Stemmer(Enum):
    STANDARD_CS_STEMMER = 2
    ENHANCED_CS_STEMMER = 3


def _contain(fx, kata: str, part_list: List[str]) -> str:
    for part in part_list:
        if fx(kata, part):
            return part

    return ""


def _endswith_contain(kata: str, part_list: List[str]) -> str:
    return _contain(str.endswith, kata, part_list)


def _startswith_contain(kata: str, part_list: List[str]) -> str:
    return _contain(str.startswith, kata, part_list)


def _confix_contain_from_kata(kata: str, ds: str, confixes: List[Confix]) -> bool:
    for part in confixes:
        if kata.startswith(part.ps) and part.ds == ds:
            return True

    return False


def _confix_contain_from_suffix(ps: str, ds: str, partikel: str, confixes: List[Confix]) -> bool:
    for part in confixes:
        if ps == part.ps and ds == part.ds and partikel == part.partikel:
            return True

    return False


def getPartikel(kata: str):
    return _endswith_contain(kata, ["kah", "lah", "tah", "pun"])


# Possesive Pronoun
def getPP(kata: str):
    return _endswith_contain(kata, ["nya", "ku", "mu"])


def getDS(kata: str):
    return _endswith_contain(kata, ["i", "kan", "an"])


def cekKombinasiTerlarang(kata: str, ds: str):
    kombinasi_terlarang: List[Confix] = [Confix("be", "i"), Confix("di", "an"),
                                         Confix("ke", "i"), Confix("ke", "kan"), Confix("me", "an"),
                                         Confix("se", "i"), Confix("se", "kan"), Confix("te", "an")]

    return _confix_contain_from_kata(kata, ds, kombinasi_terlarang)


def isvocal(kar: chr):
    if kar in ['a', 'i', 'u', 'e', 'o']:
        return True

    return False


def isnotvocal(kar: chr):
    return not isvocal(kar)


def cekPrecedence(kata: str):
    s: str = kata
    partikel = ""
    ds = ""
    pp = ""

    partikel = getPartikel(kata)
    pp = getPP(kata[:len(partikel)])
    ds = getDS(kata[:(len(partikel) + len(pp))])

    # Tipe awalan
    awalan = _startswith_contain(s, ["di", "ke", "se", "be", "ter",
                                     "te", "me", "pe"])

    precedences = [Confix("be", partikel="lah"), Confix("be", "an"),
                   Confix("me", "i"), Confix("di", "i"),
                   Confix("pe", "i"), Confix("ter", "i")]

    return _confix_contain_from_suffix(awalan, ds, partikel, precedences)


def getRule(kata: str, stemmer_choice: Stemmer):
    rule: int = 0

    try:
        if kata.startswith("di"):
            rule = -3
        elif kata.startswith("ke"):
            rule = -2
        elif kata.startswith("se"):
            rule = -1
        elif kata.startswith("be"):
            rule = getRuleBE(kata)
        elif kata.startswith("te"):
            rule = getRuleTE(kata)
        elif kata.startswith("me"):
            rule = getRuleME(kata, stemmer_choice)
        elif kata.startswith("pe"):
            rule = getRulePE(kata, stemmer_choice)
    except Exception as e:
        raise
    finally:
        return rule


def getRuleBE(kata: str):
    # R01: berV... ber-V | be-rV
    if kata.startswith("ber") and isvocal(kata[3]):
        return 1
    # R02: berCAP... ber-CAP where C != r and P != r
    elif kata.startswith("ber") and \
            isnotvocal(kata[3]) and kata[3] != 'r' and \
            kata[5:7] != 'er':
        return 2
    # R03: berCAerV... ber-CAerV where C != r
    elif kata.startswith("ber") and \
            isnotvocal(kata[3]) and kata[3] != r and \
            kata[5:7] == 'er' and isvocal(kata[7]):
        return 3
    # R04: belajar... bel-ajar
    elif kata == "belajar":
        return 4
    # R05: beC1erC2... be-C1erC2 where C1 not in {r, l}
    elif kata.startswith("be") and \
            isnotvocal(kata[2]) and kata[2] not in ['r', 'l'] and \
            kata[3:5] == 'er' and isnotvocal(kata[5]):
        return 5

    return 0


def getRuleTE(kata: str):
    if kata.startswith("ter") and isvocal(kata[3]):
        return 6
    elif kata.startswith("ter") and \
            isnotvocal(kata[3]) and kata[3] != 'r' and \
            kata[4:6] == 'er' and isvocal(kata[6]):
        return 7
    elif kata.startswith("ter") and \
            isnotvocal(kata[3]) and kata[4:6] == 'er':
        return 8
    elif kata.startswith("te") and \
            isnotvocal(kata[2]) and kata[2] != 'r' and \
            kata[3:5] == 'er' and isvocal(kata[5]):
        return 9
    elif kata.startswith("ter") and \
            isvocal(kata[3]) and kata[3] != 'r' and \
            kata[4:6] == 'er' and isvocal(kata[6]):
        return 10
    return 0


def getRuleME(kata: str, stemmer_choice: Stemmer):
    if stemmer_choice.value == 2:
        if kata.startswith("men") and \
                kata[3] in ['c', 'd', 'j', 'z']:
            return 14
        elif kata.startswith("memp") and kata[4] != 'e' and \
                isvokal(kata[4]):
            return 19
    elif stemmer_choice.value == 3:
        if kata.startswith("men") and \
                kata[3] in ['c', 'd', 'j', 'z', 's']:
            return 14
        elif kata.startswith("memp") and kata[4] != 'e':
            return 19

    if kata.startswith("me") and isvocal(kata[3]) and \
            kata[2] in ['l', 'r', 'w', 'y']:
        return 10
    elif kata.startswith("mem") and kata[3] in ['b', 'f', 'v']:
        return 11
    elif kata.startswith("mempe"):
        return 11
    elif kata.startswith("mem") and \
            ((kata[3] == 'r' and isvocal(kata[4])) or \
             isvocal(kata[3])):
        return 13
    elif kata.startswith("men") and isvocal(kata[3]):
        return 15
    elif kata.startswith("meng") and \
            kata[4] in ['g', 'h', 'k', 'q']:
        return 16
    elif kata.startswith("meng") and isvocal(kata[4]):
        return 17
    elif kata.startswith("meny") and isvocal(kata[4]):
        return 18
    return 0


def getRulePE(kata: str, stemmer_choice: Stemmer):
    if stemmer_choice == Stemmer.STANDARD_CS_STEMMER:
        if kata.startswith("peng") and kata[4] in ['g', 'h', 'q']:
            return 29
    elif stemmer_choice == Stemmer.ENHANCED_CS_STEMMER:
        if kata.startswith("peng") and isnotvocal(kata[4]):
            return 29

    if kata.startswith("pe") and kata[2] in ['w', 'y'] and \
            isvocal(kata[3]):
        return 20
    elif kata.startswith("per") and isvocal(kata[3]):
        return 21
    elif kata.startswith("per") and isnotvocal(kata[3]) and \
            kata[3] != 'r' and kata[5:7] != 'er':
        return 23
    elif kata.startswith("per") and isnotvocal(kata[3]) and \
            kata[3] != 'r' and kata[5:7] != 'er' and isvocal(kata[7]):
        return 24
    elif kata.startswith("pem") and kata[3] in ['b', 'f', 'v']:
        return 25
    elif kata.startswith("pem") and \
            ((kata[3] == 'r' and isvocal(kata[4])) or \
             isvocal(kata[3])):
        return 26
    elif kata.startswith("pen") and kata[3] in ['c', 'd', 'j', 'z']:
        return 27
    elif kata.startswith("pen") and isvocal(kata[3]):
        return 28
    elif kata.startswith("peng") and isvocal(kata[4]):
        return 30
    elif kata.startswith("peny") and isvocal(kata[4]):
        return 31
    elif kata.startswith("pel") and isvocal(kata[3]):
        return 32
    elif kata.startswith("pe") and isnotvocal(kata[2]) and \
            kata[2] not in ['l', 'r', 'm', 'n', 'w', 'y'] and \
            kata[3:5] == 'er' and isvocal(kata[5]):
        return 33
    elif kata.startswith("pe") and isnotvocal(kata[2]) and \
            kata[2] not in ['l', 'r', 'm', 'n', 'w', 'y'] and \
            kata[3:5] != 'er':
        return 34
    elif kata.startswith("pe") and isnotvocal(kata[2]) and \
            kata[2] not in ['l', 'r', 'm', 'n', 'w', 'y'] and \
            kata[3:5] == 'er' and isnotvocal(kata[5]):
        return 36
    return 0


def getPrefix(rule: int, kata: str):
    prefix = ""

    switcher = {
        -3: kata[0:2],
        -2: kata[0:2],
        -1: kata[0:2],

        1: "ber",
        2: "ber",
        3: "ber",

        4: "bel",
        5: "be",

        6: "ter",
        7: "ter",
        8: "ter",
        35: "ter",

        9: "te",
        10: "me",

        11: "mem",
        12: "mem",
        19: "mem",

        # inspect later
        13: kata[0:2],
        15: kata[0:2],
        26: kata[0:2],
        28: kata[0:2],

        14: "men",
        16: "meng",
        17: "meng",
        18: "meny",

        20: "pe",
        34: "pe",
        36: "pe",

        21: "per",
        23: "per",
        24: "per",
        33: "per",

        25: "pem",
        27: "pen",
        29: "peng",
        30: "peng",
        31: "peny",
        32: "pel" if kata.startswith("pelajar") else "pe",

        0 : "",
    }

    return switcher.get(rule, 0)


def getReduksi(rule: int, kata: str):
    prefix = ""

    if rule in [
        -3, -2, -1,
        5, 9, 10,
        13, 15, 26, 28,
        20, 34, 36
    ]:
        return kata[2:]
    elif rule in [
        1, 2, 3,
        6, 7, 8, 35,
        11, 12, 19,
        14,
        21, 23, 24,
        25, 27
    ]:
        return kata[3:]
    elif rule in [
        16, 17,
        29, 30
    ]:
        return kata[4:]
    elif rule in [
        18, 31
    ]:
        return "s" + kata[4:]
    elif rule == 4:
        return "ajar"
    elif rule == 32:
        return "ajar" if kata.startswith("pelajar") else kata[2:]
