def choose(n, k):
    if k > n or k < 0 or n < 0:
        return 0
    p = 1
    for i in range(min(k, n-k)):
        p *= (n-i)  / (i+1)
    return int(round(p))

def count_dist(a, v, z, r):
    p = 1
    for i in range(13):
        x = a[i]
        y = r[i] - a[i]
        p *= choose(v[i], x) * choose(z[i], y)
    return p

def get_odds(v=[3, 2, 1, 0, 0, 3, 3, 1, 3, 0, 7, 1, 2], r=[3,2,2,0,0,0,0,0,0,0,0,0,0], c=0):
    """
    v, r, and a are lists of length 13, whose positions correspond to ranks (ace is position 0, two is position 1, etc.)
    and values correspond to number of occurences
    v is known portion of cards. So, if v[0] == n, then there are n aces in known portion of cards
    r is revealed cards. So, if r[0] == n, then n aces have been revealed
    a is known cards that have been revealed. So, if a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], then all of the revealed cards have come
    from the unknown portion. 
    c is a rank, should be >=0 and <= 12. The program returns the odds of c being the rank of the next card revealed
    sum(v) should be 26. All values in v and r should be <= 24, and all values a[i] should be <= r[i]
    The program enumerates all possible values of a, and for each of these calculates the odds of c being the rank of the next card revealed
    weighted by the odds of the particular value of a occuring. The return value is the sum of all of these odds.
    """
    a = [0 for i in range(13)]
    m = [min(i,j) for i,j in zip(v, r)]
    i = 12
    t = 0
    z = [24-i for i in v]
    s_r = sum(r)
    t_left = 52 - s_r
    p = 0
    while i > -1:
        if a[i] > m[i]:
            a[i] = 0
            i -= 1
            if i == -1:
                break
            a[i] += 1
        else:
            if i == 12:
                x = count_dist(a, v, z, r)
                t += x

                k = v[c] - a[c]
                u = 24 - k

                s_a = sum(a)
                k_left = 26 - s_a # number of known cards left
                u_left = 26 - (s_r - s_a) # number of unknown cards left
                
                from_k = (k_left / t_left) * ((v[c] - a[c]) / k_left)
                from_u = (u_left / t_left) * ((z[c] - r[c] + a[c]) / (286-26+u_left))
                p += x * (from_u + from_k)

            if i < 12:
                i += 1
            else:
                a[i] += 1
    return p / t
