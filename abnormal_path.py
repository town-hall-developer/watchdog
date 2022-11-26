# 같은 path 별로 묶어서 시간대별로 비교.

# 정상
# alb   nginx
# 7     8
# 7     8
# 8     8
# 8     9


# alb   nginx
# 7     8
# 7
# 7     8
# 8     8
# 8     9

# alb   nginx
# 7     8
# 7     8
# 8
# 8     9

# alb   nginx
# 7     8
#       8
# 8     8
# 8     9


# 첫 번째 것의 abnormal 을 찾음
def find_abnormal(alb, nginx):
    abnormal = []

    n_idx = 0
    a_idx = 0

    while n_idx < len(nginx) and a_idx < len(alb):

        if (nginx[n_idx] - 1 == alb[a_idx] or nginx[n_idx] == alb[a_idx]):
            n_idx += 1
            a_idx += 1

            if (len(nginx) == n_idx):
                while (len(alb) > a_idx):
                    abnormal.append(alb[a_idx])
                    a_idx += 1
                break

    return abnormal


print(find_abnormal([7, 8, 8], [8, 8, 9]))
