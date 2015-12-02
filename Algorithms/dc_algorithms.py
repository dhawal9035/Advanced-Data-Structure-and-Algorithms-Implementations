# -*- coding: utf-8 -*-
from numpy import *  # analysis:ignore
import doctest
'#TODO: Add doctests, post them on the forum'

'STOCK_PRICES  = [100,113,110,85,105,102,86,63,81,101,94,106,101,79,94,90,97]'
STOCK_PRICE_CHANGES = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
'STOCK_PRICE_CHANGES = [-13, -3, -25, -20, -3, -16, -23, -18, -20, -7, -12, -5, -22, -15, -4, -7]'
'STOCK_PRICE_CHANGES = [1,2,3,4,5,6]'
l = len(STOCK_PRICE_CHANGES) - 1
m = l/2
'#Implement pseudocode from the book'


def find_maximum_subarray_brute(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum sub-array.
    Implement the brute force method from chapter 4
    time complexity = O(n^2)
    >>> find_maximum_subarray_brute([12, 3, 4, 5, 0, 5], 0, 5)
    (0, 5, 29)
    >>> find_maximum_subarray_brute([-8, -6, -5, -3, -9, -1, -4], 0, 6)
    (5, 5, -1)
    """
    max_sum = -inf
    for i in range(low, high+1):
        current_sum = 0
        for j in range(i, high+1):
            current_sum = current_sum + A[j]
            if max_sum < current_sum:
                max_sum = current_sum
                left_most = i
                right_most = j
    return left_most, right_most, max_sum

'Implement pseudocode from the book'


def find_maximum_crossing_subarray(A, low, mid, high):
    """
    Find the maximum sub-array that crosses mid
    Return a tuple (i,j) where A[i:j] is the maximum sub-array.
    """
    left_sum = -inf
    sum = 0
    left_most = -1
    for i in range(mid, low-1, -1):
        sum += A[i]
        if sum > left_sum:
            left_sum = sum
            left_most = i
    right_most = -1
    right_sum = -inf
    sum = 0
    for j in range(mid+1, high+1):
        sum = sum + A[j]
        if sum > right_sum:
            right_sum = sum
            right_most = j
    return left_most, right_most, left_sum+right_sum


def find_maximum_subarray_recursive(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Recursive method from chapter 4
    
    """
    if high == low:
        return low, high, A[low]
    else:
        mid = (low+high)/2

        left_low, left_high, left_sum = find_maximum_subarray_recursive(A, low, mid)
        right_low, right_high, right_sum = find_maximum_subarray_recursive(A, mid+1, high)
        cross_low, cross_high, cross_sum = find_maximum_crossing_subarray(STOCK_PRICE_CHANGES, low, mid, high)
        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_low, left_high, left_sum
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_low, right_high, right_sum
        else:
            return cross_low, cross_high, cross_sum


def find_maximum_subarray_iterative(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Do problem 4.1-5 from the book.
    >>> find_maximum_subarray_iterative([12, 3, 4, 5, 0, 5], 0, 5)
    (0, 5, 29)
    >>> find_maximum_subarray_iterative([-8, -6, -5, -3, -9, -1, -4], 0, 6)
    (5, 5, -1)
    """

    max_sum = -inf
    left = 0
    right = 0
    i = 0
    sum = 0

    for j in range(low, high+1):
        sum = sum + A[j]

        if sum > max_sum:
            max_sum = sum
            left = i
            right = j
        if sum <= 0:
            sum = 0
            i = j+1

    return left, right, max_sum


def square_matrix_multiply(A, B):
    """
    Return the product AB of matrix multiplication.
    >>> square_matrix_multiply(((1, 1), (1, 1)), ((1, 1), (1, 1)))
    array([[ 2.,  2.],
           [ 2.,  2.]])
    >>> square_matrix_multiply(((-1, -1), (-1, -1)), ((-1, 0), (0, 0)))
    array([[ 1.,  0.],
           [ 1.,  0.]])
    """
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.shape
    assert A.shape == A.T.shape
    C = zeros(shape=A.shape)
    r, c = A.shape
    for i in range(r):
        for j in range(r):
            C[i][j] = 0
            for k in range(r):
                C[i][j] = C[i][j]+A[i][k]*B[k][j]

    return C


def add(A, B):
    size = len(A)
    C = zeros((size, size))
    for i in range(size):
        for j in range(size):
            C[i][j] = A[i][j] + B[i][j]
    return C


def sub(A, B):
    size = len(A)
    C = zeros((size, size))
    for i in range(size):
        for j in range(size):
            C[i][j] = A[i][j]-B[i][j]
    return C


def square_matrix_multiply_strassens(A, B):
    """
    Return the product AB of matrix multiplication.
    Assume len(A) is a power of 2
    """
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.shape
    assert A.shape == A.T.shape
    assert (len(A) & (len(A) - 1)) == 0, "A is not a power of 2"
    s, t = A.shape
    if s == 1:
        return dot(A, B)
    else:
        n = s/2
        a11 = zeros((n, n))
        a12 = zeros((n, n))
        a21 = zeros((n, n))
        a22 = zeros((n, n))
        b11 = zeros((n, n))
        b12 = zeros((n, n))
        b21 = zeros((n, n))
        b22 = zeros((n, n))

        for i in range(n):
            for j in range(n):
                a11[i][j] = A[i][j]
                a12[i][j] = A[i][j+n]
                a21[i][j] = A[i+n][j]
                a22[i][j] = A[i+n][j+n]
                b11[i][j] = B[i][j]
                b12[i][j] = B[i][j+n]
                b21[i][j] = B[i+n][j]
                b22[i][j] = B[i+n][j+n]

        a_tmp = add(a11, a22)
        b_tmp = add(b11, b22)
        p1 = square_matrix_multiply_strassens(a_tmp, b_tmp)

        a_tmp = add(a21, a22)
        p2 = square_matrix_multiply_strassens(a_tmp, b11)

        b_tmp = sub(b12, b22)
        p3 = square_matrix_multiply_strassens(a11, b_tmp)

        b_tmp = sub(b21, b11)
        p4 = square_matrix_multiply_strassens(a22, b_tmp)

        a_tmp = add(a11, a12)
        p5 = square_matrix_multiply_strassens(a_tmp, b22)

        a_tmp = sub(a21, a11)
        b_tmp = add(b11, b12)
        p6 = square_matrix_multiply_strassens(a_tmp, b_tmp)

        a_tmp = subtract(a12, a22)
        b_tmp = add(b21, b22)
        p7 = square_matrix_multiply_strassens(a_tmp, b_tmp)

        c12 = add(p3, p5)
        c21 = add(p2, p4)

        a_tmp = add(p1, p4)
        b_tmp = add(a_tmp, p7)
        c11 = subtract(b_tmp, p5)

        a_tmp = add(p1, p3)
        b_tmp = add(a_tmp, p6)
        c22 = subtract(b_tmp, p2)

        C = zeros((s, s))
        for i in range(n):
            for j in range(n):
                C[i][j] = c11[i][j]
                C[i][j+n] = c12[i][j]
                C[i+n][j] = c21[i][j]
                C[i+n][j+n] = c22[i][j]
        return C


def test():
    doctest.testmod()
    print "Output of Brute Force is as below:"
    print find_maximum_subarray_brute(STOCK_PRICE_CHANGES, 0, l)
    print "Output of Iterative method is as below:"
    print find_maximum_subarray_iterative(STOCK_PRICE_CHANGES, 0, l)
    print "Output of Recursive Sub-array is as below:"
    print find_maximum_subarray_recursive(STOCK_PRICE_CHANGES, 0, l)
    print "Output of Square matrix Multiply is as below:"
    print square_matrix_multiply(((1, 2), (3, 4)), ((1, 2), (3, 4)))
    print "Output of Strassen's Square matrix Multiply is as below:"
    A = random.rand(2, 2)
    B = random.rand(2, 2)
    print "The matrices for multiplication are:"
    print "\n", A
    print "\n", B
    print "\n Output is:"
    print "\n", square_matrix_multiply_strassens(A, B)
    print "To compare"
    print dot(A, B)
if __name__ == '__main__':
    test()
