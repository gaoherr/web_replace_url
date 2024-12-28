from odoo.http import ROUTING_KEYS
from odoo.tools.misc import submap
import werkzeug.utils
import werkzeug.routing
import werkzeug.exceptions
import werkzeug
from odoo.modules.registry import Registry
import threading

from odoo import models, tools
from odoo.addons.base.models.ir_http import _logger, FasterRule
import odoo
from odoo import http

from odoo import http

base_sorturl = ['']


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @tools.ormcache('key', cache='routing')
    def routing_map(self, key=None):
        config_parameter = self.env['ir.config_parameter']
        base_sorturl[0] = config_parameter.sudo().get_param("web.base.sorturl", "")
        _logger.info("Generating routing map for key %s", str(key))
        registry = Registry(threading.current_thread().dbname)
        installed = registry._init_modules.union(
            odoo.conf.server_wide_modules)
        mods = sorted(installed)
        routing_map = werkzeug.routing.Map(
            strict_slashes=False, converters=self._get_converters())
        for url, endpoint in self._generate_routing_rules(mods, converters=self._get_converters()):
            if 'odoo' in url:
                url = url.replace('odoo', base_sorturl[0])
            routing = submap(endpoint.routing, ROUTING_KEYS)
            if routing['methods'] is not None and 'OPTIONS' not in routing['methods']:
                routing['methods'] = routing['methods'] + ['OPTIONS']
            rule = FasterRule(url, endpoint=endpoint, **routing)
            rule.merge_slashes = False
            routing_map.add(rule)
        return routing_map
