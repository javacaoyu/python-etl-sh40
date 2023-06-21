


class Stu:
    pass

stu = None

def get_stu():
    global stu
    if not stu:
        stu = Stu()
        return stu
    return stu

