#!/usr/bin/python
"""
An unusually easy leetcode hard. The problem is to find the length of the
longest valid string of parentheses. As soon as you see (or for many, 
remember) the relationship between stacks and valid parens you essentially
solved the problem. 
"""
import sys
with open(sys.argv[1]) as f:
    test_parens = [line for line in f]

def longest_paren(parens):
    paren_stack = []
    valid_subs = [1]
    curr_sum = 0
    for char in parens:
        if char == "(":
            paren_stack.append("(")
        if char == ")":
            if paren_stack:
                paren_stack.pop()
                curr_sum += 2
            else:
                valid_subs.append(curr_sum)
                curr_sum = 0
    valid_subs.append(curr_sum)
    return max(valid_subs)  

for paren in test_parens:
    print(longest_paren(paren))
