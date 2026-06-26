import calendar
from datetime import date


def calcular_meta(

    valor_vendido,

    meta,

    ultima_data

):

    percentual = (

        (valor_vendido / meta) * 100

        if meta > 0

        else 0

    )

    restante = max(

        meta - valor_vendido,

        0

    )

    ultimo_dia = calendar.monthrange(

        ultima_data.year,

        ultima_data.month

    )[1]

    dias_restantes = (

        date(

            ultima_data.year,

            ultima_data.month,

            ultimo_dia

        )

        - ultima_data

    ).days

    media_necessaria = (

        restante / dias_restantes

        if dias_restantes > 0

        else restante

    )

    if percentual >= 150:

        bonus = 3

        proximo = "Meta máxima"

        falta_bonus = 0

    elif percentual >= 125:

        bonus = 2

        proximo = "150%"

        falta_bonus = max(

            meta * 1.5 - valor_vendido,

            0

        )

    elif percentual >= 100:

        bonus = 1

        proximo = "125%"

        falta_bonus = max(

            meta * 1.25 - valor_vendido,

            0

        )

    else:

        bonus = 0

        proximo = "100%"

        falta_bonus = max(

            meta - valor_vendido,

            0

        )

    valor_bonus = (

        valor_vendido

        * (bonus / 100)

    )

    return {

        "percentual": percentual,

        "restante": restante,

        "dias_restantes": dias_restantes,

        "media_necessaria": media_necessaria,

        "bonus": bonus,

        "valor_bonus": valor_bonus,

        "proximo": proximo,

        "falta_bonus": falta_bonus

    }