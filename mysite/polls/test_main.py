from freezegun import freeze_time

from .models import PersonIIN


def test_create(db, client):
    response = client.post('/iin/', {'iin': '051110600124'})
    assert response.status_code == 201
    data = response.json()
    assert 'age' in data
    assert 'iin' in data
    assert data['age'] == 15


def test_ensure_this_field_has_no_more_than_12_characters(db, client):
    response = client.post('/iin/', {'iin': '1231423123123123'})
    assert response.status_code == 400
    data = response.json()
    assert data['iin'][0] == 'Ensure this field has no more than 12 characters.'


def test_ensure_this_field_has_at_least_12_characters(db, client):
    response = client.post('/iin/', {'iin': '12314'})
    assert response.status_code == 400
    data = response.json()
    assert data['iin'][0] == 'Ensure this field has at least 12 characters.'


@freeze_time('2014-10-05')
def test_age_22(db, client):
    response = client.post('/iin/', {'iin': '911110300124'})
    data = response.json()
    assert 'age' in data
    assert data['age'] == 22


@freeze_time('1999-11-11')
def test_age_8(db, client):
    PersonIIN.objects.create(iin='911110300124')
    response = client.get('http://127.0.0.1:8000/iin/')
    data = response.json()
    assert 'age' in data[0]
    assert data[0]['age'] == 8


@freeze_time('1999-11-11')
def test_you_cannot_be_less_than_0(db, client):
    PersonIIN.objects.create(iin='011110600124')
    response = client.get('http://127.0.0.1:8000/iin/')
    data = response.json()
    assert 'age' in data[0]
    assert data[0]['age'] == 'You cannot be less than 0'


def test_IIN_should_not_consist_of_letters(db, client):
    PersonIIN.objects.create(iin='dwandwajda')
    PersonIIN.objects.create(iin='dwandwadajda')
    PersonIIN.objects.create(iin='dwandwadwajda')
    response = client.get('http://127.0.0.1:8000/iin/')
    data = response.json()
    for i in range(len(data)):
        assert 'age' in data[i]
        assert data[i]['age'] == 'IIN should not consist of letters'


def test_day_is_out_of_range_for_month(db, client):
    PersonIIN.objects.create(iin='010230600124')
    response = client.get('http://127.0.0.1:8000/iin/')
    data = response.json()
    assert 'age' in data[0]
    assert data[0]['age'] == 'day is out of range for month'
