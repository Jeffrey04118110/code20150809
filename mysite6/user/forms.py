from django import forms

class MyregFrom(forms.Form):
    # 在类中加表单验证
    # 限定username长度大于6，密码不能为空且前后一致
    username = forms.CharField(label='用户名',
                               initial='请填写用户名',
                               required=False)
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput,
                               required=False)
    password2 = forms.CharField(label='重复密码')

    def clean_username(self):
        """此方法限定username必须大于等于6个字符"""
        uname = self.cleaned_data['username']
        if len(uname) < 6:
            raise forms.ValidationError('用户名太短')
        return uname

    def clean_password(self):
        passwd = self.cleaned_data['password']
        if len(passwd) == 0:
            raise forms.ValidationError('密码不能为空')
        passwd2 = self.cleaned_data['password2']
        if passwd != passwd2:
            raise forms.ValidationError('前后密码不一致')
        return self.cleaned_data