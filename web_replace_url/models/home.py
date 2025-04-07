import json
import logging
import psycopg2
import threading
from odoo import tools
from odoo.addons.base.models.ir_http import _logger, FasterRule, IrHttp
import odoo
from odoo import http
from odoo.http import ROUTING_KEYS
from odoo.tools.misc import submap
import odoo.exceptions
import odoo.modules.registry
from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.service import security
from odoo.tools.translate import _
from odoo.modules.registry import Registry
from odoo import api, fields, models, _
from odoo.tools import transpile_javascript
from odoo.addons.base.models import ir_config_parameter
from odoo.addons.base.models.assetsbundle import JavascriptAsset
import werkzeug.utils
import werkzeug.routing
import werkzeug.exceptions
import werkzeug
import re
base_sorturl=['']

class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    def write(self, vals):
        data = super(IrConfigParameter, self).write(vals)
        if data and self.key == 'web.base.sorturl' :
            self.env['ir.http'].env.registry.clear_cache("routing")
            self.env['ir.attachment'].regenerate_assets_bundles()
        return   {'type': 'ir.actions.client', 'tag': 'soft_reload'}




@property
def content(self):
    content = super(JavascriptAsset, self).content
    if self.name == "/web/static/src/core/browser/router.js":
        content = re.sub(r'(?<!@)odoo', base_sorturl[0], content)
    if self.name == "/web/static/src/webclient/navbar/navbar.js":
        content = re.sub(r'(?<!@)odoo', base_sorturl[0], content)
    if self.is_transpiled:
        if not self._converted_content:
            self._converted_content = transpile_javascript(
                self.url, content)
        return self._converted_content
    return content

JavascriptAsset.content = content

def url_init(self, httprequest):
    if "odoo" in httprequest.path and "/web/static" not in  httprequest.path:
        httprequest.path = httprequest.path.replace(
            "odoo", base_sorturl[0])
    self.httprequest = httprequest
    self.future_response = http.FutureResponse()
    self.dispatcher = http._dispatchers['http'](self)
    self.geoip = http.GeoIP(httprequest.remote_addr)
    self.registry = None
    self.env = None

http.Request.__init__ = url_init

@tools.ormcache('key', cache='routing')
def routing_map(self, key=None):
    config_parameter = self.env['ir.config_parameter']
    base_sorturl[0] = config_parameter.sudo(
    ).get_param("web.base.sorturl", "")
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

IrHttp.routing_map = routing_map