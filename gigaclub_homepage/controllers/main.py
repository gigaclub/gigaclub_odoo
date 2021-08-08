from odoo import http
from odoo.http import request


class Main(http.Controller):
    @http.route("/", auth="public")
    def homepage(self):
        return request.render("gigaclub_homepage.homepage")

    @http.route(["/datenschutz"], auth="public", method=["GET"])
    def datenschutz(self):
        return request.render("gigaclub_homepage.datenschutz")

    @http.route(["/impressum"], auth="public", method=["GET"])
    def impressum(self):
        return request.render("gigaclub_homepage.impressum")
