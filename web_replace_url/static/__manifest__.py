# Copyright 2018 Simone Orsi - Camptocamp SA
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
{
    "name": "Url odoo18 Replace",
    'version': '1.0.3',
    "author": "1311793927@qq.com",
    'support': '1311793927qq.com',
    "summary": "URL Replace  link",
    "description":"Odoo18 Replace odoo in hyperlink",
    "category": "Extra Tools",
    "license": "LGPL-3",
	'images': ['static/description/main_banner.png'],
    "depends": ["web",'base'],
    "application": False,
    "installable": True,
    "data": [
          'data/data.xml',
          'views/ir_config_parameter_views.xml'
      ],
    "assets": {
        "web.assets_backend": [
            "web_replace_url/static/src/**/*",
        ],
    },
    "installable": True,
    'uninstall_hook': '_uninstall_cleanup',
    'post_init_hook': '_setup_module',
}
