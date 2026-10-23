from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Application

User = get_user_model()


class BaseCase(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password="pass12345!")
        self.bob = User.objects.create_user("bob", password="pass12345!")
        self.app = Application.objects.create(owner=self.alice, company="Acme", role="Django Intern")


class WebTests(BaseCase):
    def test_list_requires_login(self):
        resp = self.client.get(reverse("tracker:list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/", resp.url)

    def test_user_sees_only_own_applications(self):
        Application.objects.create(owner=self.bob, company="Secret Co", role="Spy")
        self.client.login(username="alice", password="pass12345!")
        resp = self.client.get(reverse("tracker:list"))
        self.assertContains(resp, "Acme")
        self.assertNotContains(resp, "Secret Co")

    def test_cannot_edit_someone_elses_application(self):
        self.client.login(username="bob", password="pass12345!")
        resp = self.client.get(reverse("tracker:edit", args=[self.app.pk]))
        self.assertEqual(resp.status_code, 404)

    def test_create_sets_owner(self):
        self.client.login(username="alice", password="pass12345!")
        self.client.post(reverse("tracker:new"), {
            "company": "Globex", "role": "Full Stack Intern", "status": "applied",
            "applied_on": "2026-10-23", "job_url": "", "notes": "",
        })
        self.assertTrue(Application.objects.filter(company="Globex", owner=self.alice).exists())

    def test_filter_by_status(self):
        Application.objects.create(owner=self.alice, company="Initech", role="Dev", status="offer")
        self.client.login(username="alice", password="pass12345!")
        resp = self.client.get(reverse("tracker:list"), {"status": "offer"})
        self.assertContains(resp, "Initech")
        self.assertNotContains(resp, "Acme")


class ApiTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.api = APIClient()

    def test_api_requires_auth(self):
        self.assertEqual(self.api.get("/api/applications/").status_code, 403)

    def test_api_lists_only_own(self):
        Application.objects.create(owner=self.bob, company="Hidden", role="X")
        self.api.force_authenticate(self.alice)
        data = self.api.get("/api/applications/").json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["company"], "Acme")

    def test_api_create_and_isolation(self):
        self.api.force_authenticate(self.alice)
        resp = self.api.post("/api/applications/", {"company": "Hooli", "role": "Intern"}, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["owner"], "alice")
        self.api.force_authenticate(self.bob)
        pk = resp.json()["id"]
        self.assertEqual(self.api.get(f"/api/applications/{pk}/").status_code, 404)
