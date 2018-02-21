# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class MisReportInstance(models.Model):
    _inherit = 'mis.report.instance'

    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account', string='Analytic Account')
    operating_unit_ids = fields.Many2many('operating.unit', string='Operating Unit')

    @api.multi
    def preview(self):
        self.ensure_one()
        res = super(MisReportInstance, self).preview()
        res['context'] = {
            'account_analytic_id': self.account_analytic_id.id,
        }
        return res


class MisReportInstancePeriod(models.Model):
    _inherit = 'mis.report.instance.period'

    @api.multi
    def _get_additional_move_line_filter(self):
        self.ensure_one()
        res = super(MisReportInstancePeriod, self).\
            _get_additional_move_line_filter()
        val = self.env.context.get('account_analytic_id')
        if val:
            res.append(('analytic_account_id', 'child_of', val))
        return res

    @api.multi
    def _get_additional_query_filter(self, query):
        self.ensure_one()
        res = super(MisReportInstancePeriod, self).\
            _get_additional_move_line_filter()
        # TODO filter on analytic account if query.model_id has
        #      a field of type account.analytic.account
        return res