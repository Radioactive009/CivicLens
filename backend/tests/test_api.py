import pytest
from rest_framework.test import APIClient
from django.core.management import call_command
from django.contrib.auth import get_user_model
from apps.constituencies.models import State, District, Constituency
from apps.elections.models import Election, PoliticalParty
from apps.demographics.models import DemographicIndicator
from apps.intelligence.models import NewsArticle

User = get_user_model()

@pytest.fixture(autouse=True)
def seed_test_database(db):
    """Seed the clean test database before running tests."""
    call_command('seed_demo_data')

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_user_login(api_client):
    response = api_client.post('/api/v1/auth/login/', {
        'username': 'admin',
        'password': 'Admin@12345'
    })
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_user_registration(api_client):
    response = api_client.post('/api/v1/auth/register/', {
        'username': 'newresearcher',
        'email': 'researcher@civiclens.org',
        'password': 'TestPassword@123',
        'password2': 'TestPassword@123',
        'role': 'RESEARCHER',
        'first_name': 'Test',
        'last_name': 'Researcher'
    })
    assert response.status_code == 201
    assert response.data['user']['username'] == 'newresearcher'

@pytest.mark.django_db
def test_constituencies_api(api_client):
    response = api_client.get('/api/v1/constituencies/')
    assert response.status_code == 200
    assert response.data['count'] >= 20

@pytest.mark.django_db
def test_dashboard_analytics_api(api_client):
    response = api_client.get('/api/v1/analytics/dashboard/')
    assert response.status_code == 200
    assert 'overview' in response.data
    assert response.data['overview']['total_constituencies'] >= 20
    assert len(response.data['turnout_trends']) > 0

@pytest.mark.django_db
def test_constituency_comparison_api(api_client):
    c1 = Constituency.objects.first()
    c2 = Constituency.objects.last()
    response = api_client.post('/api/v1/analytics/compare/', {
        'constituency_ids': [c1.id, c2.id]
    }, format='json')
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['name'] == c1.name

@pytest.mark.django_db
def test_demographics_api(api_client):
    response = api_client.get('/api/v1/demographics/')
    assert response.status_code == 200
    assert response.data['count'] > 0

@pytest.mark.django_db
def test_elections_turnout_api(api_client):
    response = api_client.get('/api/v1/elections/turnout/')
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) >= 2

@pytest.mark.django_db
def test_news_intelligence_api(api_client):
    response = api_client.get('/api/v1/intelligence/articles/')
    assert response.status_code == 200
    assert response.data['count'] > 0

@pytest.mark.django_db
def test_news_trends_api(api_client):
    response = api_client.get('/api/v1/intelligence/trends/')
    assert response.status_code == 200
    assert 'by_category' in response.data
    assert 'by_sentiment' in response.data
