# ein beispiel zur erstellung von labels mit der soap-API von dhl
# WICHTIG! die zeep lib installieren:  https://docs.python-zeep.org/en/master/

import datetime
import os
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, Transport, xsd, helpers

user = your_user_name
password = your_portal_password

# WICHTIG! in der wsdl datei muss die zeile:
# <soap:address location="https://cig.dhl.de/services/production/soap"/>
# für die sandbox angepasst werden:
#  <soap:address location="https://cig.dhl.de/services/sandbox/soap"/>

wsdl = 'test-geschaeftskundenversand-api-3.2.0.wsdl'

session = Session()
session.auth = HTTPBasicAuth(user, password)
session.get(url='https://cig.dhl.de/services/sandbox/soap')

header = xsd.Element(
    '{http://test.python-zeep.org}Authentification',
    xsd.ComplexType([
        xsd.Element(
            '{http://test.python-zeep.org}user',
            xsd.String()),
        xsd.Element(
            '{http://test.python-zeep.org}signature',
            xsd.String()),
    ])
)

header_value = header(user='2222222222_01', signature='pass')
client = Client(wsdl, transport=Transport(session=session))

labelData = {
    'Version': {
        'majorRelease': '3',
        'minorRelease': '2',
    },
    'ShipmentOrder': {
        'sequenceNumber': '123ab43cSSD',
        'Shipment': {
            'ShipmentDetails': {
                'product': 'V66WPI',
                'accountNumber': '22222222226601',
                'customerReference': '123ab43cSSD',
                'shipmentDate': datetime.date.today().strftime('%Y-%m-%d'),
                'ShipmentItem': {
                    'weightInKG': 0.75,
                    'lengthInCM': 20,
                    'widthInCM': 15,
                    'heightInCM': 10,
                },
                'Notification': 'mail@mail.com',
                'Service': {
                    'Premium': {'active': '1'},  # Premium - mit tracking = 1 sonst 0
                }
            },
            'Shipper': {
                'Name': {
                    'name1': 'max mustermann',
                    'name2': 'mustermann`s küche '
                },
                'Address': {
                    'streetName': 'Irgendwostr.',
                    'streetNumber': '40',
                    'zip': '12345',
                    'city': 'Frankfurt',
                    'Origin': {
                        'countryISOCode': 'DE'
                    }
                },
            },
            'Receiver': {
                'name1': 'Sofia Musterfrau',
                'Address': {
                    'streetName': '5th Av.',
                    'streetNumber': '1',
                    'zip': '54321',
                    'city': 'New York',
                    'province': 'New York',
                    'Origin': {
                        'country': 'UNITED STATES',
                        'countryISOCode': 'US'
                    }
                },
            },
            'ExportDocument': {
                'invoiceNumber': 'rchng.1234',
                'exportType': 'OTHER',
                'exportTypeDescription': 'Permanent',
                'placeOfCommital': 'Deutschland',
                'additionalFee': '11',
                'ExportDocPosition': [
                    {
                        'description': 'Whatever',
                        'countryCodeOrigin': 'DE',
                        'customsTariffNumber': '12345678',
                        'amount': 3,
                        'netWeightInKG': 0.05,
                        'customsValue': 11,
                    },
                    {
                        'description': 'WasAuchImmer',
                        'countryCodeOrigin': 'DE',
                        'customsTariffNumber': '12345678',
                        'amount': 1,
                        'netWeightInKG': 0.05,
                        'customsValue': 12.23,
                    },
                ]
            }
        }
    }
}

result = client.service.createShipmentOrder(_soapheaders=[header_value], **labelData)
input_dict = helpers.serialize_object(result)

os.system('clear')
print(result)

# für mich nur wichtige daten:
o = input_dict.get('CreationState')[0]
print(o.get('shipmentNumber'))  # tracking id
print(o.get('LabelData').get('labelUrl'))  # label download url
