import os
from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from analytics import ajustar_riesgo

APP = Path(__file__).resolve().parents[1] / "app.py"


class RiskTests(unittest.TestCase):
    def test_risk_never_negative(self):
        self.assertEqual(ajustar_riesgo(0.01, 15, 50, 20), 0)

    def test_risk_never_over_100(self):
        self.assertEqual(ajustar_riesgo(0.99, 60, 1, 1), 100)

    def test_adjustments(self):
        self.assertEqual(ajustar_riesgo(0.5, 30, 20, 4), 55)


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {"OPENAI_API_KEY": ""})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.app = AppTest.from_file(str(APP))
        self.app.secrets["OPENAI_API_KEY"] = ""
        self.app.run(timeout=30)
        self.assertFalse(self.app.exception)

    def navigate(self, page):
        self.app.sidebar.radio[0].set_value(page).run(timeout=30)
        self.assertFalse(self.app.exception)

    def test_all_pages(self):
        for page in self.app.sidebar.radio[0].options:
            with self.subTest(page=page):
                self.navigate(page)

    def test_cart_profiles_quantities_and_extreme_inputs(self):
        self.navigate("Carrito Inteligente")
        self.app.number_input(key="sofa").set_value(2)
        self.app.number_input(key="mesa").set_value(3)
        self.app.run()
        self.assertIn("Subtotal: $1,400", [x.value for x in self.app.subheader])
        for profile in self.app.selectbox[0].options:
            for minutes, views, visits in [(0, 50, 20), (60, 1, 1)]:
                with self.subTest(profile=profile, minutes=minutes):
                    self.app.selectbox[0].set_value(profile)
                    self.app.slider[0].set_value(minutes)
                    self.app.slider[1].set_value(views)
                    self.app.slider[2].set_value(visits)
                    self.app.button[0].click().run(timeout=30)
                    self.assertFalse(self.app.exception)
                    risk = float(self.app.metric[0].value.rstrip("%"))
                    self.assertGreaterEqual(risk, 0)
                    self.assertLessEqual(risk, 100)

    def test_chat_without_key(self):
        self.navigate("Asistente Virtual")
        self.app.chat_input[0].set_value("¿Qué mesa recomiendas?").run()
        self.assertFalse(self.app.exception)
        self.assertIn("No se detectó OPENAI_API_KEY.", [x.value for x in self.app.warning])

    def test_assembly_products(self):
        self.navigate("Armado Inteligente")
        for product in self.app.selectbox[0].options:
            self.app.selectbox[0].set_value(product).run()
            self.assertFalse(self.app.exception)

    def test_model_missing_is_handled(self):
        from streamlit import cache_resource
        cache_resource.clear()
        with patch("joblib.load", side_effect=FileNotFoundError):
            self.navigate("Carrito Inteligente")
            self.assertTrue(self.app.error)
        cache_resource.clear()

    def test_chat_api_error_is_handled(self):
        self.app.secrets["OPENAI_API_KEY"] = "test-placeholder"
        with patch("openai.OpenAI") as client:
            client.return_value.chat.completions.create.side_effect = RuntimeError("private diagnostic")
            self.navigate("Asistente Virtual")
            self.app.chat_input[0].set_value("Hola").run()
            self.assertFalse(self.app.exception)
            self.assertTrue(self.app.error)
            self.assertNotIn("private diagnostic", self.app.error[0].value)


if __name__ == "__main__":
    unittest.main()
