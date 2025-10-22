"""
Chatbot Cancer du Sein - Version SUPER SIMPLE
Pas de Streamlit, pas de dépendances externes
"""
import os
import json

class SimpleCancerChatbot:
    def __init__(self):
        self.knowledge = {
            "definition": {
                "question": "qu'est-ce que le cancer du sein",
                "answer": "Le cancer du sein est une tumeur maligne qui se développe à partir des cellules mammaires.",
                "keywords": ["cancer", "sein", "définition", "quoi"]
            },
            "risques": {
                "question": "facteurs de risque", 
                "answer": "Facteurs: âge, antécédents familiaux, mutations BRCA1/BRCA2.",
                "keywords": ["facteurs", "risque", "antécédents", "familiaux"]
            },
            "symptomes": {
                "question": "symptômes",
                "answer": "Symptômes: masse, changement de forme, écoulement mamelon.",
                "keywords": ["symptômes", "masse", "douleur", "écoulement"]
            }
        }
    
    def find_answer(self, question):
        question = question.lower()
        for key, data in self.knowledge.items():
            for keyword in data["keywords"]:
                if keyword in question:
                    return data["answer"]
        return "Je n'ai pas d'info sur ce sujet. Consultez un médecin."
    
    def start_chat(self):
        print("🤖 CHATBOT CANCER DU SEIN")
        print("Tapez 'quit' pour quitter\n")
        
        while True:
            question = input(" Votre question: ")
            if question.lower() == 'quit':
                break
            answer = self.find_answer(question)
            print(f" {answer}\n")

if __name__ == "__main__":
    bot = SimpleCancerChatbot()
    bot.start_chat()