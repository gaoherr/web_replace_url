import json
import logging
import psycopg2

import odoo.exceptions
import odoo.modules.registry
from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.service import security
from odoo.tools.translate import _
from odoo.addons.web.controllers.utils import is_user_internal

from odoo.addons.web.controllers.home import Home as WebHome
from odoo.addons.web.controllers import session
from odoo import api, fields, models, _

from odoo.addons.base.models import ir_config_parameter

base_sorturl=['']

class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    def write(self, vals):
        data = super(IrConfigParameter, self).write(vals)
        if data and self.key == 'web.base.sorturl' :
            self.env['ir.http'].env.registry.clear_cache("routing")
            self.env['ir.attachment'].regenerate_assets_bundles()
        return   {'type': 'ir.actions.client', 'tag': 'soft_reload'}
