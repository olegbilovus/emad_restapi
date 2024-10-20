from app.models.images import RestrictionFilter


def check_restriction_filter(text: str) -> RestrictionFilter:
    sex = "sex" in text
    violence = "violence" in text
    return RestrictionFilter(sex=sex, violence=violence)
