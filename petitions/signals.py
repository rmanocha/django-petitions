from django.dispatch import Signal

petition_saved = Signal(providing_args = ["petition_form", "petition"])
