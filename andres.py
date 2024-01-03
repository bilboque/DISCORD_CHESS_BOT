import berserk


# ps: regarde pas ma clé

# Créez une session avec le jeton API
session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session=session)

# Fonction pour défier l'IA
def challenge_ai():
    challenge_info = client.challenges.create_ai(level=5, clock_limit=300, clock_increment=3)
    print(f"Challenge created against AI. Game URL: {challenge_info}")
    print(f"Statut de la partie : {challenge_info['status']['name']}")



#fonction make_move :?
def make_move(self, game_id: str, move: str) -> None:
        """Make a move in a board game.

        :param game_id: ID of a game
        :param move: move to make
        """
        path = f"/api/board/game/{game_id}/move/{move}"
        self._r.post(path)


challenge_ai()


