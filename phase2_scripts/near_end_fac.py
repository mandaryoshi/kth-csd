


"""
    1. receive an ip
    2. run script a to receive an ixp id
    3. run script c to get a facility set for the ixp id  = [facIXP]
    4. find the previous hop of that ixp ip using script e results
    5. use script d to get the AS of the previous hop
    6. fetch the facilities for that as using the as to fac results = [facPREV] 
    7. check the common facilities between these two  - [facIXP] and [facPREV] = [facRES]

    8. if more than one facility remains, use script f to get the neighbours of the previous hop
    9. check the as of these neighbours using script d
    10. fetch the facilities of these as = [fac3] - [facX]
    11. check the common facilities [facRES] and [fac3 - facX]
"""