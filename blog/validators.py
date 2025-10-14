from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def bad_keywords_validator(body: str) -> None:
    bad_keywords = ["murder", "kill", "die"]
    words = body.lower().split()
    for kw in bad_keywords:
        if kw in words:
            raise ValidationError(
                _("Your comment cannot include the word '%(kw)s'"),
                params={"kw": kw},
                code="bad keyword",
            )
