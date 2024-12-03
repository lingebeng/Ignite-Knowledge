from django import forms
from .models import User,ValidCode

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': '请传入用户名！',
        "max_length":'用户名长度在2~20之间！',
        "min_length": '用户名长度在2~20之间！'
    })
    email = forms.EmailField(error_messages={"required": '请传入邮箱！', 'invalid': '请传入一个正确的邮箱！'})
    valid_code = forms.CharField(max_length=4, min_length=4)
    password = forms.CharField(max_length=20, min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已经被注册！')
        return email

    def clean_valid_code(self):
        valid_code = self.cleaned_data.get('valid_code')
        email = self.cleaned_data.get('email')

        valid_model = ValidCode.objects.filter(email=email, valid_code=valid_code).first()
        if not valid_model:
            raise forms.ValidationError("验证码和邮箱不匹配！")
        valid_model.delete()
        return valid_code


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={"required": '请传入邮箱！', 'invalid': '请传入一个正确的邮箱！'})
    password = forms.CharField(max_length=20, min_length=6)
    remember_me = forms.IntegerField(required=False)