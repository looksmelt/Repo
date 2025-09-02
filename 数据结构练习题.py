from statistics import mean
def drop_first_last(grades):
    first ,*middle, last = grades
    return mean(middle)