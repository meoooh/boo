from rest_framework import serializers

from wl import models

class OwlUserSerializer(serializers.HyperlinkedModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = models.OwlUser
        fields = ('url', 'id', 'deviceId', 'userId', 'sex',
                  'birthday', 'password', 'password2')
        read_only_fields = ('userId', 'deviceId',)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(OwlUserSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    @property
    def data(self):
        _data = super(OwlUserSerializer, self).data

        if isinstance(_data, dict):
            if 'password' in _data:
                del _data['password']
        elif isinstance(_data, list):
            for i in _data:
                if 'password' in i:
                    del i['password']

        return _data

    def restore_object(self, attrs, instance=None):
        user = super(OwlUserSerializer, self).restore_object(attrs, instance)
        if instance is None:
            user.set_password(attrs['password'])
        return user

    def to_native(self, obj):
        if 'password2' in self.fields:
            del self.fields['password2']
        return super(OwlUserSerializer, self).to_native(obj)

    def validate_sex(self, attrs, source):
        if attrs['sex'] not in (0, 1):
            raise serializers.ValidationError(
                _("You must choice '1' or '0'. '1' means male and '0' means" +
                    " female. Your input: '%(value)s'"),
                code='invalid',
                params={'value': attrs['sex']}
            )
        return attrs

    def validate_password2(self, attrs, source):
        # http://goo.gl/U7FGWZ
        if attrs['password'] == attrs.pop('password2'):
            return attrs
        raise serializers.ValidationError(
            _("The two password fields didn't match."),
            code='password_mismatch',
        )