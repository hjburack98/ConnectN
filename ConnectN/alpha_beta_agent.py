import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        if brd.w >= 10 and brd.h >= 10:
            self.max_depth = 2
        elif brd.w > 6 or brd.h > 6:
            self.max_depth = 5
        else:
            self.maxDepth = 6

        alpha = -math.inf
        beta = math.inf

        successors = self.get_successors(brd)

        bestMove = None

        for succ in successors:
            util = self.get_min_value(succ[0], alpha, beta, 1)
            if util >= alpha:
                alpha = util
                bestMove = succ

        return bestMove[1]




    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ

    def getNumber(self, brd, x, y, dx, dy):
        ownCount = 0
        opponentCount = 0

        for i in range(brd.n):
            if y+i*dy >= brd.h or x+i*dx >= brd.w:
                break

            j = brd.board[y + i*dy][x + i*dx]
            if j == self.player:
                ownCount = ownCount + 1
            elif j > 0:
                opponentCount = opponentCount + 1

        if ownCount == brd.n:
            return math.inf

        if opponentCount == brd.n:
            return -math.inf

        if opponentCount == brd.n-1:
            return math.pow(-100000, ownCount)

        elif opponentCount == brd.n-2:
            return math.pow(-10000, ownCount)

        if ownCount == brd.n-1:
            return math.pow(100000, ownCount)

        if ownCount == brd.n-2:
            return math.pow(10000, ownCount)

        if ownCount == brd.n-3:
            return math.pow(1000, ownCount)

        if(brd.n > 4):
            if opponentCount == brd.n-4:
                return math.pow(-100, ownCount)
            if ownCount == brd.n-4:
                return math.pow(100, ownCount)


        return math.pow(10, ownCount)


    def heuristic(self, brd):
        total = 0

        for x in range(brd.w - brd.n + 1):
            for y in range(brd.h):
                util = self.getNumber(brd, x, y, 1, 0)
                if util == math.inf:
                    return math.inf

                if util == -math.inf:
                    return -math.inf

                total = total + util

        for x in range(brd.w):
            for y in range(brd.h):
                util = self.getNumber(brd, x, y, 0, 1)
                if util == math.inf:
                    return math.inf

                if util == -math.inf:
                    return -math.inf

                total = total + util

        for x in range(brd.w - brd.n + 1):
            for y in range(brd.h - brd.n + 1):
                util = self.getNumber(brd, x, y, 1, 1)
                if util == math.inf:
                    return math.inf

                if util == -math.inf:
                    return -math.inf

                total = total + util

        for x in range(brd.w - brd.n):
            for y in range(brd.h - brd.n + 1):
                util = self.getNumber(brd, x, y, 1, -1)
                if util == math.inf:
                    return math.inf

                if util == -math.inf:
                    return -math.inf

                total = total + util

        return total

    def isEnd(self, brd):
        return not self.get_successors(brd)

    def getEndUtil(self, brd):
        outcome = brd.get_outcome()
        if outcome == 0:
            return 0

        if outcome == 1:
            return math.inf

        if outcome == 2:
            return -math.inf

    def get_max_value(self, brd, alpha, beta, depth):

        if self.isEnd(brd):
            util = self.getEndUtil(brd)
            return util

        elif depth >= self.max_depth:
            util = self.heuristic(brd)
            return util

        util = -math.inf

        for succ in self.get_successors(brd):
            util = max(util, self.get_min_value(succ[0], alpha, beta, depth + 1))

            if util >= beta:
                return util

            alpha = max(alpha, util)

        return util

    def get_min_value(self, brd, alpha, beta, depth):
        if self.isEnd(brd):
            util = self.getEndUtil(brd)
            return util

        elif depth >= self.max_depth:
            util = self.heuristic(brd)
            return util

        util = math.inf

        for succ in self.get_successors(brd):
            util = min(util, self.get_max_value(succ[0], alpha, beta, depth + 1))

            if util <= alpha:
                return util

            beta = min(beta, util)

        return util

THE_AGENT = AlphaBetaAgent("BurackHarrison", 4)




