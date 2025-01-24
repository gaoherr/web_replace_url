from . import util
from . import models
from . import controllers
from odoo.addons.base.models.assetsbundle import JavascriptAsset
from odoo.tools import transpile_javascript
import re
from odoo import http
import odoo
from .models.ir_http import base_sorturl
from odoo.modules.registry import Registry


def _uninstall_cleanup(env):
    env['ir.http'].env.registry.clear_cache("routing")
    env['ir.attachment'].regenerate_assets_bundles()

    @property
    def content(self):
        content = super(JavascriptAsset, self).content
        if self.is_transpiled:
            if not self._converted_content:
                self._converted_content = transpile_javascript(
                    self.url, content)
            return self._converted_content
        return content

    JavascriptAsset.content = content

    def url_init(self, httprequest):
        self.httprequest = httprequest
        self.future_response = http.FutureResponse()
        self.dispatcher = http._dispatchers['http'](self)
        self.geoip = http.GeoIP(httprequest.remote_addr)
        self.registry = None
        self.env = None

    http.Request.__init__ = url_init
