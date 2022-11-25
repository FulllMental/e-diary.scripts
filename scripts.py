import random

from environs import Env

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation


def find_schoolkid(schoolkid):
    try:
        kid = Schoolkid.objects.get(full_name__contains=schoolkid)
        return kid
    except Schoolkid.DoesNotExist:
        print('Ученик с таким именем не найден...')
    except Schoolkid.MultipleObjectsReturned:
        print('Слишком много совпадений! Уточните ФИО ученика...')


def fix_marks(schoolkid):
    kid = find_schoolkid(schoolkid)
    if not kid:
        print('Из-за ошибки поиска ученика дальше программа выполниться не может...')
        return
    Mark.objects.filter(schoolkid=kid, points__lte=3).update(points=5)
    print('Все плохие оценки исправлены...')


def remove_chastisements(schoolkid):
    kid = find_schoolkid(schoolkid)
    if not kid:
        print('Из-за ошибки поиска ученика дальше программа выполниться не может...')
        return
    schoolkid_chastisements = Chastisement.objects.filter(schoolkid=kid)
    schoolkid_chastisements.delete()
    print('Все замечания ученика удалены...')


def create_commendation(schoolkid, subject):
    env = Env()
    env.read_env()
    good_commendations = env.list('COMMENDATIONS')
    commedation_text = random.choice(good_commendations)

    kid = find_schoolkid(schoolkid)
    if not kid:
        print('Из-за ошибки поиска ученика дальше программа выполниться не может...')
        return
    lessons = Lesson.objects.filter(year_of_study=kid.year_of_study, group_letter=kid.group_letter)
    if not lessons.count():
        print('Уроков по этому предмету у ученика не найдено, возможно их пока не было и стоит уточнить ФИО...')
        return
    subject_lessons = lessons.filter(subject__title=subject)
    if not subject_lessons.count():
        print('Либо нет такого предмета, либо предмет написан с ошибкой...')
        return
    random_lesson = random.choice(subject_lessons)
    lesson_date = random_lesson.date
    lesson_subject = random_lesson.subject
    lesson_teacher = random_lesson.teacher
    Commendation.odjects.create(text=commedation_text, created=lesson_date, schoolkid=kid, subject=lesson_subject, teacher=lesson_teacher)
    print('Похвала ученику добавлена...')
