# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp
from ..models import Role, User

class PostForm(FlaskForm):
    body = TextAreaField(u'记录下你的日志', validators=[Required()])
    submit =SubmitField(u'提交')


class EditProfileForm(FlaskForm):
    name = StringField(u'姓名',validators=[Length(0,64)])
    location = StringField(u'位置',validators=[Length(0,64)])
    about_me = TextAreaField(u'个性签名')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField(u'邮箱',validators=[Required(), Length(1,64),
                                           Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
        u'用户名必须是字母、数字、下划线、点号')])
    confirmed = BooleanField(u'账户已确认')
    role = SelectField(u'用户权限',coerce=int)       #attention selectfield
    name = StringField(u'真实姓名',validators=[Length(0,64)])
    location = StringField(u'位置',validators=[Length(0,64)])
    about_me = TextAreaField(u'个性签名')
    submit = SubmitField(u'提交')

    def __init__(self,user,*args,**kwargs):                #user为当前管理员操作的账户对象
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已存在')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已存在')    