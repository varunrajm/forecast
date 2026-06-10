import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


class ForecastApiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.sample_path = Path(__file__).resolve().parents[1] / "sample_data" / "retail_sales_sample.csv"

    def test_health(self) -> None:
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_forecast_with_linear_regression(self) -> None:
        with self.sample_path.open("rb") as file:
            response = self.client.post(
                "/api/forecast",
                files={"file": ("retail_sales_sample.csv", file, "text/csv")},
                data={"horizon": "30", "model": "linear_regression"},
            )

        payload = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["model"], "linear_regression")
        self.assertEqual(payload["horizon"], 30)
        self.assertIn("metrics", payload)
        self.assertGreater(len(payload["forecast_chart"]), 0)
        self.assertGreater(len(payload["insights"]), 0)

    def test_rejects_invalid_horizon(self) -> None:
        with self.sample_path.open("rb") as file:
            response = self.client.post(
                "/api/forecast",
                files={"file": ("retail_sales_sample.csv", file, "text/csv")},
                data={"horizon": "14", "model": "linear_regression"},
            )

        self.assertEqual(response.status_code, 422)
        self.assertIn("Horizon must be one of", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
