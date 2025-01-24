

from odoo.addons.base.models.assetsbundle import JavascriptAsset
from odoo.tools import transpile_javascript
import re
from odoo import http
import odoo
from .models.ir_http import base_sorturl
from odoo.modules.registry import Registry

# def get_baseurl():
#     config = odoo.tools.config
#     dbname = config['db_name']
#     with Registry(dbname).cursor() as cursor:
#         cursor.execute(
#             "SELECT value FROM ir_config_parameter WHERE key = %s", ("web.base.sorturl",))
#         result = cursor.fetchall()[0][0]
#         return result


@property
def content(self):
    content = super(JavascriptAsset, self).content
    if self.name == "/web/static/src/core/browser/router.js":
        content = re.sub(r'(?<!@)odoo', base_sorturl[0], content)
    if self.name == "/web/static/src/webclient/navbar/navbar.js":
        content = re.sub(r'(?<!@)odoo', base_sorturl[0], content)
    if self.is_transpiled:
        if not self._converted_content:
            self._converted_content = transpile_javascript(self.url, content)
        return self._converted_content
    return content


JavascriptAsset.content = content


def url_init(self, httprequest):
    if "odoo" in httprequest.path:
        httprequest.path = httprequest.path.replace("odoo", base_sorturl[0])
    self.httprequest = httprequest
    self.future_response = http.FutureResponse()
    self.dispatcher = http._dispatchers['http'](self)
    self.geoip = http.GeoIP(httprequest.remote_addr)
    self.registry = None
    self.env = None


http.Request.__init__ = url_init
