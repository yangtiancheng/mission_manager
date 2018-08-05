# -*- coding: utf-8 -*-
import datetime
from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _


class MissionManagerHead(models.Model):
    _name = 'mission.manager.head'
    _description = 'Mission Manager Head'

    name = fields.Char(string='Name', help='Name')
    type = fields.Selection(selection=[('mission', 'Mission'), ('bug', 'BUG')], string='Type', help='Type')
    active = fields.Boolean(string='Active', help='Active', default=True)
    number = fields.Char(string='Number', help='Number')
    deadline_date = fields.Date(string='Deadline Date', help='Deadline Date')
    days = fields.Integer(compute="_get_last_days", string='Last Days', help='Last Days',store=True)
    rdc_number = fields.Char(string='RDC Number', help='RDC Number')
    note = fields.Text(string='Note', help='Note')
    attachments_ids = fields.Many2many(comodel_name='ir.attachment', string='Attachments', help='Attachments')
    current_point_id = fields.Many2one('res.users', string='Current Person', help='Current Person')
    # 优先级
    priority = fields.Selection(selection=[('low','Low'),('medium','Medium'),('high','High'),('max','Max')],string='Priority',help='Priority',default='Max')
    # 开始时间
    # 最初预计
    need_time = fields.Float(string='Need Time',help='Need Time',digits=(3,1),default=0.0)
    # 总消耗
    # 预计剩余


    state = fields.Selection(selection=[('draft', 'Draft'), ('open', 'Open'), ('doing', 'Doing'), ('done', 'Done')
        , ('reactive', 'Re-active'), ('stop', 'Stop'), ('cancel', 'Cancel'),('testing', 'Testing'),('tested', 'Tested'),('waiting', 'Waiting')],default='draft')
    line_ids = fields.One2many('mission.progress', 'head_id', string='Processes', help='Processes')


    @api.depends('deadline_date','state')
    @api.multi
    def _get_last_days(self):
        for rec in self:
            if rec.deadline_date:
                rec.days =  (datetime.datetime.strptime(rec.deadline_date, '%Y-%m-%d') - datetime.datetime.now()).days
            if rec.state == 'done':
                rec.days = 99999


    @api.model
    def create(self, vals):
        if 'number' not in vals or not vals['number']:
            if 'type' in vals and vals['type'] == 'mission':
                vals['number'] = self.env['ir.sequence'].next_by_code('seq_mission_number')
            elif 'type' in vals and vals['type'] == 'bug':
                vals['number'] = self.env['ir.sequence'].next_by_code('seq_bug_number')
            else:
                vals['number'] = ''
        return super(MissionManagerHead, self).create(vals)

    @api.multi
    def unlink(self):
        for rec in self:
            if self.env.uid == rec.create_uid.id:
                super(MissionManagerHead, rec).unlink()
            else:
                raise ValidationError("只有单据的创建人可以删除对应的单据。")
    @api.multi
    def copy(self, default=None):
        if not default:
            default = {}
        default.update(
            {
                'number':False,
                'rdc_number':False
            }
        )
        return super(MissionManagerHead, self).copy(default)

class MissionProgress(models.Model):
    _name = 'mission.progress'
    _order = 'line_number'

    head_id = fields.Many2one(comodel_name='mission.manager.head', string='Head ID', help='Head ID',ondelete='cascade')
    name = fields.Char(string='Name', help='Name')
    line_number = fields.Integer(string='Line Number', help='Line Number')
    point_from_id = fields.Many2one(comodel_name='res.users', string='Point From', help='Point From',default=lambda self: self.env.uid)
    point_to_id = fields.Many2one(comodel_name='res.users', string='Point To', help='Point To')
    description = fields.Text(string='Description', help='Description')
    used_time = fields.Float(string='Used Time', help='Used Time', digits=(3, 1), default=0.0)
    attachments_ids = fields.Many2many(comodel_name='ir.attachment', string='Attachments', help='Attachments')
    state = fields.Selection(selection=[('open', 'Open'), ('doing', 'Doing'), ('done', 'Done')
        , ('reactive', 'Re-active'), ('stop', 'Stop'), ('cancel', 'Cancel'),('testing', 'Testing'),('tested', 'Tested'),('waiting', 'Waiting'),('fixing', 'Fixing')])
    # 上线批次
    batch_number = fields.Char(string='Batch Number', help='Batch Number')


    @api.model
    def create(self, vals):
        if 'head_id' in vals:
            head_id = self.env['mission.manager.head'].browse(vals['head_id'])
            if 'state' in vals:
                head_id.state = vals['state']
            if 'point_to_id' in vals:
                head_id.current_point_id = vals['point_to_id']
        return super(MissionProgress, self).create(vals)

    @api.multi
    def write(self, vals):
        for rec in self:
            if rec.env.uid == rec.create_uid.id:
                if 'state' in vals:
                    rec.head_id.state = vals['state']
                if 'point_to_id' in vals:
                    rec.head_id.current_point_id = vals['point_to_id']
            else:
                raise ValidationError("不能删除他人的记录。")

        return super(MissionProgress, self).write(vals)
    @api.multi
    def unlink(self):
        for rec in self:
            if self.head_id.state == 'draft':
                super(MissionManagerHead, rec).unlink()
            else:
                raise ValidationError("不能删除正在执行的单据。")
