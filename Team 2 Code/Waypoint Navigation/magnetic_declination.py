from magnetic_field_calculator import MagneticFieldCalculator
from datetime import datetime

calculator = MagneticFieldCalculator()

result = calculator.calculate(
    latitude=41.8781,
    longitude=-87.6298,
    date=datetime.today().strftime('%Y-%m-%d')
)
field_value = result['field-value']
declination = field_value['declination']
print(declination)