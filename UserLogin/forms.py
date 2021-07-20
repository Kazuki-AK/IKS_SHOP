from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ( AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm )
from .models import Shop

User = get_user_model()

class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class UserUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = User
        fields = ('email',
                  'last_name_representative', 'first_name_representative', 'last_name_representative_kana', 'first_name_representative_kana',
                  'last_name_manager', 'first_name_manager', 'last_name_manager_kana', 'first_name_manager_kana',
                  'tel', 'remarks',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ShopUpdateForm(forms.ModelForm):
    """ショップ情報更新フォーム"""

    class Meta:
        model = Shop
        fields = ( 'shop_name', 'manager_name', 'email','tel_shop', 'website',
                   'zip_code', 'address1', 'address2', 'address3', 'address4', 'address5',
                   'station1', 'station1_time', 'station2', 'station2_time', 'station3', 'station3_time',
                   'price_basic', 'wheelchair', 'visually', 'hearing', 
                   'remarks_shop', )

        widgets = {
            'zip_code':
            forms.TextInput(
                #attrsでp-postal-codeを指定
                attrs={'class': 'p-postal-code','placeholder': '記入例：8900053',},
            ),
            'address1': forms.TextInput(
                #attrsでp-region/p-region-idを指定
                #attrs={'class': 'p-region','placeholder': '記入例：鹿児島県'},
                attrs={'class': 'p-region-id','placeholder': '記入例：鹿児島県'},
            ),
            'address2': forms.TextInput(
                #attrsでp-locality p-street-address p-extended-addressを指定
                attrs={'class': 'p-locality', 'placeholder': '記入例：鹿児島市'}, 
            ),
            'address3': forms.TextInput(
                #attrsでp-locality p-street-address p-extended-addressを指定
                attrs={'class': 'p-street-address', 'placeholder': '記入例：中央町１０丁目'}, 
            ),
            'address4': forms.TextInput(
                #attrsでp-locality p-street-address p-extended-addressを指定
                attrs={'class': 'p-extended-address', 'placeholder': '記入例：３３－４'}, 
            ),
            'address5': forms.TextInput(
                attrs={'class': '','placeholder': '記入例：トリマビル'},
            ),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['zip_code'].widget.attrs['class'] = 'form-control p-postal-code'
        self.fields['address1'].widget.attrs['class'] = 'form-control p-region'
        self.fields['address2'].widget.attrs['class'] = 'form-control p-locality'
        self.fields['address3'].widget.attrs['class'] = 'form-control p-street-address'
        self.fields['address4'].widget.attrs['class'] = 'form-control p-extended-address'


class TimeUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = Shop
        fields = ('is_holiday_sunday', 'is_holiday_monday', 'is_holiday_tuesday', 'is_holiday_wednesday', 'is_holiday_thursday', 'is_holiday_friday', 'is_holiday_saturday',
                  'time_open_sunday1', 'time_close_sunday1', 'time_open_sunday2', 'time_close_sunday2',
                  'time_open_monday1', 'time_close_monday1', 'time_open_monday2', 'time_close_monday2',
                  'time_open_tuesday1', 'time_close_tuesday1', 'time_open_tuesday2', 'time_close_tuesday2',
                  'time_open_wednesday1', 'time_close_wednesday1', 'time_open_wednesday2', 'time_close_wednesday2',
                  'time_open_thursday1', 'time_close_thursday1', 'time_open_thursday2', 'time_close_thursday2',
                  'time_open_friday1', 'time_close_friday1', 'time_open_friday2', 'time_close_friday2',
                  'time_open_saturday1', 'time_close_saturday1', 'time_open_saturday2', 'time_close_saturday2', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            self.fields['time_open_sunday1'].widget.attrs['class'] = 'form-control sunday'
            self.fields['time_close_sunday1'].widget.attrs['class'] = 'form-control sunday'
            self.fields['time_open_sunday2'].widget.attrs['class'] = 'form-control sunday'
            self.fields['time_close_sunday2'].widget.attrs['class'] = 'form-control sunday'
            
            self.fields['time_open_monday1'].widget.attrs['class'] = 'form-control monday'
            self.fields['time_close_monday1'].widget.attrs['class'] = 'form-control monday'
            self.fields['time_open_monday2'].widget.attrs['class'] = 'form-control monday'
            self.fields['time_close_monday2'].widget.attrs['class'] = 'form-control monday'
            
            self.fields['time_open_tuesday1'].widget.attrs['class'] = 'form-control tuesday'
            self.fields['time_close_tuesday1'].widget.attrs['class'] = 'form-control tuesday'
            self.fields['time_open_tuesday2'].widget.attrs['class'] = 'form-control tuesday'
            self.fields['time_close_tuesday2'].widget.attrs['class'] = 'form-control tuesday'
            
            self.fields['time_open_wednesday1'].widget.attrs['class'] = 'form-control wednesday'
            self.fields['time_close_wednesday1'].widget.attrs['class'] = 'form-control wednesday'
            self.fields['time_open_wednesday2'].widget.attrs['class'] = 'form-control wednesday'
            self.fields['time_close_wednesday2'].widget.attrs['class'] = 'form-control wednesday'

            self.fields['time_open_thursday1'].widget.attrs['class'] = 'form-control thursday'
            self.fields['time_close_thursday1'].widget.attrs['class'] = 'form-control thursday'
            self.fields['time_open_thursday2'].widget.attrs['class'] = 'form-control thursday'
            self.fields['time_close_thursday2'].widget.attrs['class'] = 'form-control thursday'

            self.fields['time_open_friday1'].widget.attrs['class'] = 'form-control friday'
            self.fields['time_close_friday1'].widget.attrs['class'] = 'form-control friday'
            self.fields['time_open_friday2'].widget.attrs['class'] = 'form-control friday'
            self.fields['time_close_friday2'].widget.attrs['class'] = 'form-control friday'

            self.fields['time_open_saturday1'].widget.attrs['class'] = 'form-control saturday'
            self.fields['time_close_saturday1'].widget.attrs['class'] = 'form-control saturday'
            self.fields['time_open_saturday2'].widget.attrs['class'] = 'form-control saturday'
            self.fields['time_close_saturday2'].widget.attrs['class'] = 'form-control saturday'


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class EmailChangeForm(forms.ModelForm):
    """メールアドレス変更フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email