from boardgamegeek import BGGClient
bgg = BGGClient()
game = bgg.game(game_id=13)
print(game.name)
