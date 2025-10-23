"""
Transforme prompt en données structurées
"""
import re
from typing import Dict, Any

class PromptParser:
    def __init__(self):
        self.medical_terms = {
            'age': [r'(\d+)\s*ans', r'âge\s*(\d+)', r'j.ai\s*(\d+)\s*ans'],
            'family_history': [
                r'mère.*cancer', r'père.*cancer', r'famil.*cancer',
                r'antécédent.*cancer', r'maman.*cancer', r'parent.*cancer'
            ],
            'symptoms': [
                r'masse', r'boule', r'grosseur', r'durcissement',
                r'douleur.*sein', r'écoulement', r'rougeur', r'peau.*orange'
            ],
            'imaging': [
                r'mammographie', r'échographie', r'irm', r'scanner',
                r'radio', r'image', r'cliché', r'examen.*imagerie'
            ]
        }
    
    def parse_prompt(self, natural_prompt: str) -> Dict[str, Any]:
        
        prompt_lower = natural_prompt.lower()
        
        
        patient_info = self._extract_patient_info(prompt_lower)
        has_image = self._detect_image_mention(prompt_lower)
        clean_question = self._extract_main_question(prompt_lower)
        
        return {
            'question': clean_question,
            'patient_info': patient_info,
            'has_image': has_image
        }
    
    def _extract_patient_info(self, prompt: str) -> Dict[str, Any]:
        
        info = {}
        
        # age
        for pattern in self.medical_terms['age']:
            match = re.search(pattern, prompt)
            if match:
                info['age'] = int(match.group(1))
                break
        
        # Antecedents 
        for pattern in self.medical_terms['family_history']:
            if re.search(pattern, prompt):
                info['family_history'] = True
                break
        
        # symptoms
        symptoms = []
        for symptom_pattern in self.medical_terms['symptoms']:
            if re.search(symptom_pattern, prompt):
                symptoms.append(symptom_pattern)
        
        if symptoms:
            info['symptoms'] = symptoms
        
        return info if info else None
    
    def _detect_image_mention(self, prompt: str) -> bool:
        
        for pattern in self.medical_terms['imaging']:
            if re.search(pattern, prompt):
                return True
        return False
    
    def _extract_main_question(self, prompt: str) -> str:
       
     
        question = prompt
        
        # Supprime les mentions d'âge
        question = re.sub(r'\d+\s*ans', '', question)
        question = re.sub(r'âge\s*\d+', '', question)
        
        # Supprime les mentions familiales
        question = re.sub(r'mère.*cancer', '', question)
        question = re.sub(r'famil.*cancer', '', question)
        
        # Nettoie la question
        question = re.sub(r'\s+', ' ', question).strip()
        
        # Si la question est vide, retourne une version simplifiée
        if not question or len(question) < 10:
            return "Évaluation risque cancer sein"
        
        return question