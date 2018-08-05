# -*- coding: utf-8 -*-

from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _


class MissionManagerHead(models.Model):
    _name = 'mission.manager.head'
    _description = 'Mission Manager Head'

    name = fields.Char(string='Name', help='Name')
    active = fields.Boolean(string='Active', help='Active')
    number = fields.Integer(string='Number', help='Number')
    note = fields.Text(string='Note', help='Note')
    attachments = fields.Many2many(comodel_name='ir.attachment', string='Attachments', help='Attachments')
    b_person = fields.Many2one(comodel_name='hr.employee', string='B Person', help='B Person')
    t_person = fields.Many2one(comodel_name='hr.employee', string='T Person', help='T Person')
    state = fields.Selection(selection=[('draft','Draft'),('open','Open'),('doing','Doing'),('done','Done')
        , ('reactive', 'Re-active'), ('stop', 'Stop'), ('cancel', 'Cancel')])
    line_ids = fields.One2many('mission.progress','head_id', string = 'Progresses', help = 'Progresses')

    @api.multi
    def unlink(self):
        for rec in self:
            if self.env.uid == rec.create_uid:
                super(MissionManagerHead, rec).unlink()
            else:
                raise ValidationError("只有单据的创建人可以删除对应的单据。")

class MissionProgress(models.Model):
    _name = 'mission.progress'
    _order = 'line_number'

    head_id = fields.Many2one(comodel_name='mission.manager.head',string='Head ID', help='Head ID')
    name = fields.Char(string='Name', help='Name')
    line_number = fields.Integer(string='Line Number', help='Line Number')
    point_from_id = fields.Many2one(comodel_name='hr.employee', string='Point From', help='Point From')
    point_to_id = fields.Many2one(comodel_name='hr.employee', string='Point To', help='Point To')
    description = fields.Text(string='Description', help='Description')
    attachments = fields.Many2many(comodel_name='ir.attachment', string='Attachments', help='Attachments')



    @api.multi
    def unlink(self):
        for rec in self:
            if self.env.uid == rec.create_uid:
                super(MissionManagerHead, rec).unlink()
            else:
                raise ValidationError("只有单据的创建人可以删除对应的单据。")
