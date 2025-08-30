from recommendation.recommendation_text import BURR_RECOMMENDATION_TEXT, LISP_RECOMMENDATION_TEXT, LISP_BURR_RECOMMENDATION_TEXT, HEALTHY_RECOMMENDATION_TEXT


def return_recommendation(diagnosis: str):
    if diagnosis == 'burr':
        return BURR_RECOMMENDATION_TEXT
    elif diagnosis == 'lisp':
        return LISP_RECOMMENDATION_TEXT
    elif diagnosis == 'lisp_burr':
        return LISP_BURR_RECOMMENDATION_TEXT
    elif diagnosis == 'healthy':
        return HEALTHY_RECOMMENDATION_TEXT
    else:
        return "Непредвиденный результат"