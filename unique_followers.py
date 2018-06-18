import json
followers = json.load(open("followers.txt"))

def unique_followers(dict,queries):
    unique = []
    for query in queries:
        for item in dict[query]:
            try:
                unique.index(item)
            except:
                unique.append(item)
    return unique

#NOT FINISHED
