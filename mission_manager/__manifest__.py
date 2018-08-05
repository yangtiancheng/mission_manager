# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Mission Manager',
    'version' : '1.0',
    'summary': 'Send Invoices and Track Payments',
    'sequence': 10,
    'description': """
Core mechanisms for the accounting modules. To display the menuitems, install the module account_invoicing.
    """,
    'category': 'Mission',
    'depends' : ['base'],
    'data': [
        'views/mission_manager.xml',
        'datas/mission_datas.xml'
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
