from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class LegalRedactor:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def redact_contract(self, text: str):
        # 1. Analyze text for PII (Names, Phones, Emails, etc.)
        results = self.analyzer.analyze(text=text, entities=[], language='en')
        
        # 2. Redact/Anonymize the detected parts
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )
        return anonymized_result.text

# Example usage
if __name__ == "__main__":
    sample_legal_text = "This agreement is between Rajesh Kumar and Suresh Gupta regarding the property at Bandra, Mumbai."
    redactor = LegalRedactor()
    print(f"Original: {sample_legal_text}")
    print(f"Redacted: {redactor.redact_contract(sample_legal_text)}")