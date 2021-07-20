from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import ( AbstractBaseUser, BaseUserManager )
from django.contrib.auth.models import ( PermissionsMixin, UserManager )
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class CustomUserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Smf jki8h０９；ｍｋuperuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    shop_number = models.PositiveSmallIntegerField( verbose_name='店舗ID', default=0, )

    email = models.EmailField( verbose_name='メールアドレス', max_length=255, unique=True, )

    first_name_representative = models.CharField( verbose_name='代表者「名」', max_length=30, blank=True, help_text='代表者の方の「名」' , )
    last_name_representative = models.CharField( verbose_name='代表者「姓」', max_length=30, blank=True, help_text='代表者の方の「姓」' , )
    first_name_representative_kana = models.CharField( verbose_name='代表者「メイ」', max_length=30, blank=True, help_text='代表者の方の「メイ」(フリガナ)' , )
    last_name_representative_kana = models.CharField( verbose_name='代表者「セイ」', max_length=30, blank=True, help_text='代表者の方の「セイ」(フリガナ)' , )

    first_name_manager = models.CharField( verbose_name='管理者「名」', max_length=30, blank=True, help_text='管理者の方の「名」' , )
    last_name_manager = models.CharField( verbose_name='管理者「姓」', max_length=30, blank=True, help_text='管理者の方の「姓」'  )
    first_name_manager_kana = models.CharField( verbose_name='管理者「メイ」', max_length=30, blank=True, help_text='管理者の方の「メイ」(フリガナ)' , )
    last_name_manager_kana = models.CharField( verbose_name='管理者「セイ」', max_length=30, blank=True, help_text='管理者の方の「セイ」(フリガナ)' , )

    tel = models.CharField( verbose_name='電話番号', max_length=15, blank=True, )

    remarks = models.TextField( verbose_name='備考', max_length=150, blank=True, )


    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('会員')
        verbose_name_plural = _('会員')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name_manager, self.last_name_manager)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
        return self.email



class Shop(models.Model):
    shop_name = models.CharField( verbose_name='店名', default='SHOP', max_length=20, )
    shop_name_kana = models.CharField( verbose_name='テンメイ', default='ショップ', max_length=30, )

    manager_name = models.CharField( verbose_name='管理者', default='CHIEF', max_length=15, )
    manager_account = models.ForeignKey('User', verbose_name='管理者アカウント', to_field='email', related_name='ManagerAccount', on_delete='models.DO_NOTHING', null=True, )

    #連絡用
    email = models.EmailField( verbose_name='お客様用メールアドレス', max_length=255, blank = True, null = True )
    tel_shop = models.CharField( verbose_name='電話番号', max_length=15, blank=True, )
    website = models.CharField( verbose_name='サイトURL', default='http://www.', max_length=100, )

    #アクセス情報
    zip_code = models.CharField(
        verbose_name='郵便番号',max_length=8,blank=True,
    )

    address1 = models.CharField(
        verbose_name='都道府県',max_length=40,blank=True,
    )
    
    address2 = models.CharField(
        verbose_name='市区町村',max_length=40,blank=True,
    )
    
    address3 = models.CharField(
        verbose_name='丁目',max_length=40,blank=True,
    )
    address4 = models.CharField(
        verbose_name='番地以降',max_length=40,blank=True,
    )
    
    address5 = models.CharField(
        verbose_name='建物名・部屋番号等',max_length=40,blank=True,
    )

    station1 = models.CharField( verbose_name='付近の駅・バス停１', max_length=15, blank=True, )
    station1_time = models.PositiveSmallIntegerField( verbose_name='駅・バス停１からの所要時間', default=0, )

    station2 = models.CharField( verbose_name='付近の駅・バス停２', max_length=15, blank=True, )
    station2_time = models.PositiveSmallIntegerField( verbose_name='駅・バス停２からの所要時間', default=0, )

    station3 = models.CharField( verbose_name='付近の駅・バス停３', max_length=15, blank=True, )
    station3_time = models.PositiveSmallIntegerField( verbose_name='駅・バス停３からの所要時間', default=0, )

    #サービス内容
    price_basic = models.PositiveSmallIntegerField( verbose_name='基本料金', default=0, )

    support_list = ( (0,''), (1,'可'), (2,'応相談'), )

    wheelchair = models.IntegerField( verbose_name='車イス対応',choices=support_list, default=0, )
    visually = models.IntegerField( verbose_name='視覚障碍対応',choices=support_list, default=0, )
    hearing = models.IntegerField( verbose_name='聴覚障碍対応',choices=support_list, default=0, ) 



    #営業時間
    is_holiday_sunday = models.BooleanField( verbose_name='日曜日', default='False', )
    is_holiday_monday = models.BooleanField( verbose_name='月曜日', default='False')
    is_holiday_tuesday = models.BooleanField( verbose_name='火曜日', default='False')
    is_holiday_wednesday = models.BooleanField( verbose_name='水曜日', default='False')
    is_holiday_thursday = models.BooleanField( verbose_name='木曜日', default='False')
    is_holiday_friday = models.BooleanField( verbose_name='金曜日', default='False')
    is_holiday_saturday = models.BooleanField( verbose_name='土曜日', default='False')

    time_list = ( (00,'00:00'),  (1,'00:30'), (2,'01:00'),  (3,'01:30'), (4,'02:00'),  (5,'02:30'), (6,'03:00'),  (7,'03:30'), (8,'04:00'),  (9,'04:30'), (10,'05:00'), (11,'05:30'),
                  (12,'06:00'), (13,'06:30'),(14,'07:00'), (15,'07:30'),(16,'08:00'), (17,'08:30'),(18,'09:00'), (19,'09:30'),(20,'10:00'), (21,'10:30'), (22,'11:00'), (23,'11:30'),
                  (24,'12:00'), (25,'12:30'),(26,'13:00'), (27,'13:30'),(28,'14:00'), (29,'14:30'),(30,'15:00'), (31,'15:30'),(32,'16:00'), (33,'16:30'), (34,'17:00'), (35,'17:30'),
                  (36,'18:00'), (37,'18:30'),(38,'19:00'), (39,'19:30'),(40,'20:00'), (41,'20:30'),(42,'21:00'), (43,'21:30'),(44,'22:00'), (45,'22:30'), (46,'23:00'), (47,'23:30'), (48,'24:00'), )

    time_open_sunday1 = models.IntegerField( verbose_name='【日曜日】開店時刻１',choices=time_list, default=0, help_text='sunday', )
    time_close_sunday1 = models.IntegerField( verbose_name='【日曜日】閉店時刻１',choices=time_list, default=0, help_text='sunday', )
    time_open_sunday2 = models.IntegerField( verbose_name='【日曜日】開店時刻２',choices=time_list, default=0, help_text='sunday', )
    time_close_sunday2 = models.IntegerField( verbose_name='【日曜日】閉店時刻２',choices=time_list, default=0, help_text='sunday', )

    time_open_monday1 = models.IntegerField( verbose_name='【月曜日】開店時刻１',choices=time_list, default=0, help_text='monday', )
    time_close_monday1 = models.IntegerField( verbose_name='【月曜日】閉店時刻１',choices=time_list, default=0, help_text='monday', )
    time_open_monday2 = models.IntegerField( verbose_name='【月曜日】開店時刻２',choices=time_list, default=0, help_text='monday', )
    time_close_monday2 = models.IntegerField( verbose_name='【月曜日】閉店時刻２',choices=time_list, default=0, help_text='monday', )

    time_open_tuesday1 = models.IntegerField( verbose_name='【火曜日】開店時刻１',choices=time_list, default=0, help_text='tuesday', )
    time_close_tuesday1 = models.IntegerField( verbose_name='【火曜日】閉店時刻１',choices=time_list, default=0, help_text='tuesday', )
    time_open_tuesday2 = models.IntegerField( verbose_name='【火曜日】開店時刻２',choices=time_list, default=0, help_text='tuesday', )
    time_close_tuesday2 = models.IntegerField( verbose_name='【火曜日】閉店時刻２',choices=time_list, default=0, help_text='tuesday', )

    time_open_wednesday1 = models.IntegerField( verbose_name='【水曜日】開店時刻１',choices=time_list, default=0, help_text='wednesday', )
    time_close_wednesday1 = models.IntegerField( verbose_name='【水曜日】閉店時刻１',choices=time_list, default=0, help_text='wednesday', )
    time_open_wednesday2 = models.IntegerField( verbose_name='【水曜日】開店時刻２',choices=time_list, default=0, help_text='wednesday', )
    time_close_wednesday2 = models.IntegerField( verbose_name='【水曜日】閉店時刻２',choices=time_list, default=0, help_text='wednesday', )

    time_open_thursday1 = models.IntegerField( verbose_name='【木曜日】開店時刻１',choices=time_list, default=0, help_text='thursday', )
    time_close_thursday1 = models.IntegerField( verbose_name='【木曜日】閉店時刻１',choices=time_list, default=0, help_text='thursday', )
    time_open_thursday2 = models.IntegerField( verbose_name='【木曜日】開店時刻２',choices=time_list, default=0, help_text='thursday', )
    time_close_thursday2 = models.IntegerField( verbose_name='【木曜日】閉店時刻２',choices=time_list, default=0, help_text='thursday', )

    time_open_friday1 = models.IntegerField( verbose_name='【金曜日】開店時刻１',choices=time_list, default=0, help_text='friday', )
    time_close_friday1 = models.IntegerField( verbose_name='【金曜日】閉店時刻１',choices=time_list, default=0, help_text='friday', )
    time_open_friday2 = models.IntegerField( verbose_name='【金曜日】開店時刻２',choices=time_list, default=0, help_text='friday', )
    time_close_friday2 = models.IntegerField( verbose_name='【金曜日】閉店時刻２',choices=time_list, default=0, help_text='friday', )

    time_open_saturday1 = models.IntegerField( verbose_name='【土曜日】開店時刻１',choices=time_list, default=0, help_text='saturday', )
    time_close_saturday1 = models.IntegerField( verbose_name='【土曜日】閉店時刻１',choices=time_list, default=0, help_text='saturday', )
    time_open_saturday2 = models.IntegerField( verbose_name='【土曜日】開店時刻２',choices=time_list, default=0, help_text='saturday', )
    time_close_saturday2 = models.IntegerField( verbose_name='【土曜日】閉店時刻２',choices=time_list, default=0, help_text='saturday', )


    #評価用
    point = models.IntegerField( verbose_name='店舗ID', default=0, )

    remarks_shop = models.TextField( verbose_name='備考', max_length=150, blank=True, )

    created_at = models.DateTimeField( auto_now_add=True, )
    updated_at = models.DateTimeField( auto_now=True, )

    class Meta:
        verbose_name = _('店舗情報')
        verbose_name_plural = _('店舗情報')

    def __str__(self):
        return self.shop_name