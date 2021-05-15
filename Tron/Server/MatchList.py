from .Match import Match

class MatchList:

    def __init__(self):
        self.matches = {}
        self.amountOfMatches = 0

    def join(self, client, matchID):
        match = self.matches.get(key = matchID)

        if match is not None:
            match.join(client)
            
    def create(self, client):
        match = Match(self.amountOfMatches)
        match.join(client)
        match.start()
        self.matches[self.amountOfMatches] = match

        self.amountOfMatches += 1

    def shutdown(self):
        for id in self.matches:
            self.matches[id].stop()
            
        



