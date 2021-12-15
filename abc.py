
# importing module
from vininfo import Vin
 
# Pass the VIN number into Vin methods
vin = Vin('JT3GN86R820256849')
 
# prints vehicle's country
print(vin.country)
 
# prints vehicle's manufacturer
print(vin.manufacturer)
 
# prints vehicle manufacturer's region
print(vin.region)

print(vin.years)
