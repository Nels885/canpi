from wtforms_sqlalchemy.orm import model_form

from .models import Fmux


FmuxForm = model_form(Fmux)