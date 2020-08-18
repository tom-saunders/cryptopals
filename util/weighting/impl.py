import util

@util.memoize
def _levenshtein_dist(left, right):
    if not left or not right:
        return max(len(left), len(right))
    elif left[-1] == right[-1]:
        return _levenshtein_dist(left[0:-1], right[0:-1])
    else:
        return 1 + min(_levenshtein_dist(left[0:-1], right),
                _levenshtein_dist(left, right[0:-1]),
                _levenshtein_dist(left[0:-1], right[0:-1]))

@util.memoize
def _damerau_levenshtein_dist(left, right):
    if not left or not right:
        return max(len(left), len(right))
    elif left[-1] == right[-1]:
        return _damerau_levenshtein_dist(
                left[0:-1],
                right[0:-1])
    else:
        min_dist = min(
                _damerau_levenshtein_dist(
                        left[0:-1],
                        right),
                _damerau_levenshtein_dist(
                        left,
                        right[0:-1]),
                _damerau_levenshtein_dist(
                        left[0:-1],
                        right[0:-1]))
        if len(left) > 1 and len(right) > 1:
            if left[-1] == right[-2]:
                transposed = right[:-2] + right[-1] + right[-2]
                transposed_dist = _damerau_levenshtein_dist(
                        left,
                        transposed)
                min_dist = min(min_dist, transposed_dist)
            if left[-2] == right[-1]:
                transposed = left[:-2] + left[-1] + left[-2]
                transposed_dist = _damerau_levenshtein_dist(
                        transposed,
                        right)
                min_dist = min(min_dist, transposed_dist)
        # we have done one addition operation in this block
        min_dist += 1
        return min_dist
