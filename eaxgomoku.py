import sys
from gomoku import Gomoku
from utils import get_row_idx

INF = 1337
MAX_DEPTH = 2

class EaxGomoku(Gomoku):
    def __init__(self):
        # super(EaxGomoku).__init__()
        pass

    # def get_point(self, state, player):
    #     for l in range(15):
    #         data_line = state[:(l+1)*15]
    #         if data_line.find()

    def print_square(self, lst):
        sys.stdout.write('=' * 30)
        sys.stdout.write('\n')
        for l in range(15):
            for c in range(15):
                i = l * 15 + c
                sys.stdout.write(' %02d ' % lst[i])
            sys.stdout.write('\n')
        sys.stdout.write('=' * 30)
        sys.stdout.write('\n')

    def generate_ignore(self, state):
        ignore_set = set()

        for l in range(15):
            for c in range(15):
                i = l * 15 + c
                if state[i]:
                    continue
                
                i_up = (l - 1) * 15 + c if l > 0 else None
                i_down = (l + 1) * 15 + c if l < 15 - 1 else None
                i_left = l * 15 + c - 1 if c > 0 else None
                i_right = l * 15 + c + 1 if c < 15 - 1 else None
                i_upleft = (l - 1) * 15 + c - 1 if l > 0 and c > 0 else None
                i_upright = (l - 1) * 15 + c + 1 if l > 0 and c < 15 - 1 else None
                i_downleft = (l - 1) * 15 + c - 1 if l < 15 - 1 and c > 0 else None
                i_downright = (l - 1) * 15 + c + 1 if l < 15 - 1 and c < 15 - 1 else None

                to_check = [i_up, i_down, i_left, i_right, i_upleft, i_upright, i_downleft, i_downright]
                tmp_ignore = True
                for check in filter(lambda x: x is not None, to_check):
                    if state[check] :
                        tmp_ignore = False
                if tmp_ignore:
                    ignore_set.add(i)
        return  ignore_set

    def generate_dist_map(self, state):
        dist_map = [INF] * 225

        for l in range(15):
            for c in range(15):
                i = l * 15 + c
                if state[i]:
                    dist_map[i] = 0

        did_modification = True
        while did_modification:
            # print(dist_map)
            did_modification = False
            for l in range(15):
                for c in range(15):
                    i = l * 15 + c

                    i_up = (l - 1) * 15 + c if l > 0 else None
                    i_down = (l + 1) * 15 + c if l < 15 - 1 else None
                    i_left = l * 15 + c - 1 if c > 0 else None
                    i_right = l * 15 + c + 1 if c < 15 - 1 else None
                    i_upleft = (l - 1) * 15 + c - 1 if l > 0 and c > 0 else None
                    i_upright = (l - 1) * 15 + c + 1 if l > 0 and c < 15 - 1 else None
                    i_downleft = (l - 1) * 15 + c - 1 if l < 15 - 1 and c > 0 else None
                    i_downright = (l - 1) * 15 + c + 1 if l < 15 - 1 and c < 15 - 1 else None

                    to_check = [i_up, i_down, i_left, i_right, i_upleft, i_upright, i_downleft, i_downright]
                    min_around = INF
                    for check in filter(lambda x: x is not None, to_check):
                        if dist_map[check] < min_around:
                            min_around = dist_map[check]
                    if min_around < dist_map[i] - 1:
                        # print('Changing %r to %r' % (dist_map[i], min_around + 1))
                        dist_map[i] = min_around + 1
                        did_modification = True
                        

        return dist_map
        

    def get_winning_player(self, state):
        # TODO: diagonals
        w_l = self.get_winning_player_line(state)
        if w_l:
            return w_l
        return self.get_winning_player_col(state)
    
    def get_winning_player_col(self, state):
        for c in range(15):
            l = 0
            while l < 15:
                i = l * 15 + c
                if not state[i]:
                    l += 1
                    continue
                else:
                    checking_player = state[i]
                    from_idx = i
                    cnt = 0
                    while state[i] == checking_player:
                        cnt += 1
                        l += 1
                        i = l * 15 + c
                        if l == 15:
                            break
                    if cnt >= 5:
                        return (checking_player, get_row_idx(0, 1, from_idx, i - 1))

    def get_winning_player_line(self, state):
        for l in range(15):
            c = 0
            while c < 15:
                i = l * 15 + c
                if not state[i]:
                    c += 1
                    continue
                else:
                    checking_player = state[i]
                    from_idx = i
                    cnt = 0
                    while state[i] == checking_player:
                        cnt += 1
                        c += 1
                        i = l * 15 + c
                        if c == 15:
                            break
                    if cnt >= 5:
                        return (checking_player, get_row_idx(0, 1, from_idx, i - 1))

    def get_finishing_moves(self, state, player, moves=set([]), depth=0):
        w = e.get_winning_player(state)
        if w and w[0] == player:
            # print(state)
            return {frozenset(moves): [moves, depth, 1, w[1]]}
            
        if depth == MAX_DEPTH:
            return None
        winning_moves = {}
        # to_ignore = self.generate_ignore(state)
        dist_map = self.generate_dist_map(state)
        # self.print_square(dist_map)
        for i in range(15*15):
            # if i in to_ignore:
            #     continue
            # if depth == 0:
            #     print(i)
            if state[i]:
                continue
            if dist_map[i] > 2:
                continue
            newstate = state[:]
            newstate[i] = player
            ret = self.get_finishing_moves(newstate, player, moves | {i}, depth + 1)
            if not ret:
                ret = {}
            for k in ret:
                # if not winning_move:
                #     winning_move = ret
                # print(type(k))
                # print(type(ret))
                if frozenset(ret[k][0]) not in winning_moves:
                    winning_moves[frozenset(ret[k][0])] = ret[k]
                else:
                    winning_moves[frozenset(ret[k][0])][2] += 1
        
        return winning_moves
                


    def get_weight_moves(self, moves):
        # weight_map = [0] * 225
        ordered_moves = []
        weight_idx = {}
        min_depth = INF
        max_depth = -INF

        for move in moves.values():
            if move[1] < min_depth:
                min_depth = move[1]
            if move[1] > max_depth:
                max_depth = move[1]
            for idx in move[3]:
                if idx not in weight_idx:
                    weight_idx[idx] = 0
                weight_idx[idx] += 1

        for depth in range(min_depth, max_depth + 1):
            tmp_ordered = []
            for move in moves.values():
                if move[1] == depth:
                    tmp_ordered.append(move)
            tmp_ordered = sorted(tmp_ordered, key=lambda x:sum(weight_idx[y] for y in x[0]), reverse=True)
            for move in tmp_ordered:
              move[0] = sorted([x for x in move[0]], key=lambda x: weight_idx[x], reverse=True)
              ordered_moves.append(move)
        print(weight_idx)
        return ordered_moves
        # for l in range(15):
        #     for c in range(15):
        #         i = l * 15 + c
        #         if state[i] == player:
        #             weight_map[i] = 1
        # for m in moves:
            
        # self.print_square(weight_map)
                
    def play_turn(self, state, player):
        other_player = 1 if player == -1 else -1
        other_nm = self.get_finishing_moves(state, other_player)
        nm = self.get_finishing_moves(state, player)

        print('Other: %r' % (other_nm,))
        print('nm: %r' % (nm,))

        # self.get_winning_map_weight(player, state, nm)
        print(self.get_weight_moves(nm))
        return nm


if __name__ == '__main__':
    e = EaxGomoku()
    
    state = [0 for i in range(15*15)]

    state[0] = 1
    # state[2] = 1
    state[3] = 1

    state[9] = -1
    # state[10] = -1
    state[11] = -1

    # print(e.generate_dist_map(state))
    
    r = e.play_turn(state, -1)
    # print(r)
