import unittest
from src.agent import respond, retrieve, tokenize


class TestAgent(unittest.TestCase):
    def test_order_tracking(self):
        result = respond("How can I track my order?")
        self.assertEqual(result["status"], "answered")
        self.assertEqual(result["source"], "FAQ-001")

    def test_invoice(self):
        result = respond("I need an invoice")
        self.assertEqual(result["source"], "FAQ-002")

    def test_medical_escalation(self):
        result = respond("Can I change my dosage?")
        self.assertEqual(result["status"], "escalate")
        self.assertIsNone(result["source"])

    def test_side_effect_escalation(self):
        self.assertEqual(respond("I had a side effect")["status"], "escalate")

    def test_unknown_escalation(self):
        self.assertEqual(respond("Tell me about quantum gravity")["status"], "escalate")

    def test_empty(self):
        self.assertEqual(respond(" ")["status"], "clarify")


if __name__ == "__main__":
    unittest.main()
