import decimal
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField
from wtforms.validators import DataRequired
from wtforms import DecimalField


class BetterDecimalField(DecimalField):
    """
    Very similar to WTForms DecimalField, except with the option of rounding
    the data always.
    """

    def __init__(self, label=None, validators=None, places=2, rounding=None,
                 round_always=False, **kwargs):
        super(BetterDecimalField, self).__init__(
            label=label, validators=validators, places=places, rounding=
            rounding, **kwargs)
        self.round_always = round_always

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = decimal.Decimal(valuelist[0])
                if self.round_always and hasattr(self.data, 'quantize'):
                    exp = decimal.Decimal('.1') ** self.places
                    if self.rounding is None:
                        quantized = self.data.quantize(exp)
                    else:
                        quantized = self.data.quantize(
                            exp, rounding=self.rounding)
                    self.data = quantized
            except (decimal.InvalidOperation, ValueError):
                self.data = None
                raise ValueError(self.gettext('Não é um valor decimal válido'))


class BillingForm(FlaskForm):
    cliente = SelectField("cliente", coerce=int, render_kw={'readonly': True}, choices=[])
    mes = SelectField("mes", validators=[DataRequired()],
                      choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
                               ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')])
    ano = DateField("dataEntrada", validators=[DataRequired(message="ano!")], format='%Y',render_kw={"placeholder": 'AAAA'})

    valor = BetterDecimalField(round_always=True,  render_kw={"placeholder": '0.00'})
