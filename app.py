from flask import Flask, jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from pydantic import BaseModel, Field

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='API Rest PY')
spec.register(server)


class Jogador(BaseModel):
    id: int = Field(default=None, ge=1)
    nome: str
    time: str


class Jogadores(BaseModel):
    jogadores: list[Jogador]
    count: int


player1 = Jogador(id=1, nome='Neymar', time='PSG')
player2 = Jogador(id=2, nome='William', time='Fulham')
player3 = Jogador(id=3, nome='Lucas', time='Tottenham')
player4 = Jogador(id=4, nome='Richarlison', time='Tottenham')

players = [player1, player2, player3, player4]


@server.get('/jogadores')
@spec.validate(resp=Response(HTTP_200=Jogadores))
def list_players():
    """Lista todos os jogadores"""
    return jsonify(Jogadores(jogadores=players, count=(len(players))).dict())


@server.post('/jogadores')
@spec.validate(body=Request(Jogador), resp=(Response(HTTP_200=Jogador)))
def add_player():
    """Adiciona um novo jogador"""
    body = request.context.body.dict()
    return body


@server.put('/jogadores/<int:id>')
@spec.validate(body=Request(Jogador), resp=(Response(HTTP_200=Jogador)))
def update_player(id: int):
    """Edita um jogador"""
    for player in players:
        if player.id == id:
            body = request.context.body.dict()
            player.nome = body['nome']
            player.time = body['time']
            return player.dict()


if __name__ == '__main__':
    server.run()
