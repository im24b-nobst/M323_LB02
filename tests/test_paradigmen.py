from datetime import date

import pytest

from trainingslog.models import Training
from trainingslog.paradigmen import km_pro_sportart, km_pro_sportart_oo, km_pro_sportart_prozedural

TRAININGS = (
    Training(date(2026, 10, 1), "Laufen", 10, 50),
    Training(date(2026, 10, 2), "Velo", 42.5, 90),
    Training(date(2026, 10, 3), "Laufen", 5.5, 30),
)
VARIANTEN = [km_pro_sportart, km_pro_sportart_prozedural, km_pro_sportart_oo]


@pytest.mark.parametrize("variante", VARIANTEN)
def test_alle_varianten_liefern_dasselbe(variante):
    assert variante(TRAININGS) == {"Laufen": 15.5, "Velo": 42.5}


@pytest.mark.parametrize("variante", VARIANTEN)
def test_leere_eingabe(variante):
    assert variante(()) == {}
