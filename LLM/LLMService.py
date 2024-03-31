# services/llm/base_service.py

class LLMService:
    """
    Classe de base pour les services de modèles de langage à grande échelle (LLM).
    Elle définit une interface commune pour interroger les différents services LLM.
    """

    def query(self, prompt, api_key):
        """
        Méthode pour envoyer une requête à un service LLM spécifique.
        Cette méthode doit être implémentée par toutes les sous-classes.

        :param prompt: Le texte (prompt) à envoyer au modèle LLM.
        :param api_key: La clé API pour accéder au service LLM.
        :return: La réponse du modèle LLM.
        """
        raise NotImplementedError("La méthode query doit être implémentée par les sous-classes.")