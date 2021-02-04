from rest_framework import serializers

from .models import PersonIIN


class PersonIINSerializer(serializers.ModelSerializer):
    iin = serializers.CharField(min_length=12, max_length=12)
    age = serializers.SerializerMethodField()

    class Meta:
        model = PersonIIN
        fields = ['iin', 'age']

    def get_age(self, person):
        res = PersonIIN.check_object(person)
        if isinstance(res, str):
            return res
        return res.years
