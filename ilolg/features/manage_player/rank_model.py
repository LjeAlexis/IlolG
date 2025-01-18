class RankModel:
    """
    Modèle pour gérer les rangs et divisions de League of Legends.
    """
    RANK_ORDER = {
        "UNRANKED": 0,
        "IRON": 1,
        "BRONZE": 2,
        "SILVER": 3,
        "GOLD": 4,
        "PLATINUM": 5,
        "DIAMOND": 6,
        "MASTER": 7,
        "GRANDMASTER": 8,
        "CHALLENGER": 9
    }

    DIVISION_ORDER = {
        "IV": 4,
        "III": 3,
        "II": 2,
        "I": 1
    }

    @staticmethod
    def get_rank_order(tier: str) -> int:
        """
        Retourne l'ordre d'un rang donné.

        Args:
            tier (str): Le rang (ex: "SILVER", "GOLD").

        Returns:
            int: Ordre du rang (plus grand = meilleur).
        """
        return RankModel.RANK_ORDER.get(tier.upper(), -1)

    @staticmethod
    def get_division_order(division: str) -> int:
        """
        Retourne l'ordre d'une division donnée.

        Args:
            division (str): La division (ex: "I", "III").

        Returns:
            int: Ordre de la division (plus petit = meilleur).
        """
        return RankModel.DIVISION_ORDER.get(division.upper(), float("inf"))
