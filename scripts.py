from datacenter import models
import random


def find_schoolkid(schoolkid):
    try:
        kid = models.Schoolkid.objects.get(full_name__contains=schoolkid)
        return kid
    except models.Schoolkid.DoesNotExist:
        print('Ученик с таким именем не найден...')
    except models.Schoolkid.MultipleObjectsReturned:
        print('Слишком много совпадений! Уточните ФИО ученика...')


def fix_marks(schoolkid):
    kid = find_schoolkid(schoolkid)
    if not kid:
        print('Из-за ошибки поиска ученика дальше программа выполниться не может...')
        return
    models.Mark.objects.filter(schoolkid=kid, points__lte=3).update(points=5)
    print('Все плохие оценки исправлены...')


def remove_chastisements(schoolkid):
    kid = find_schoolkid(schoolkid)
    if not kid:
        print('Из-за ошибки поиска ученика дальше программа выполниться не может...')
        return
    schoolkid_chastisements = models.Chastisement.objects.filter(schoolkid=kid)
    schoolkid_chastisements.delete()
    print('Все замечания ученика удалены...')


def create_commendation(schoolkid, subject):
    good_commendations = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!'
    ]
    commedation_text = random.choice(good_commendations)

    kid = find_schoolkid(schoolkid)
    if not kid:
        print('Из-за ошибки поиска ученика дальше программа выполниться не может...')
        return
    lessons = models.Lesson.objects.filter(year_of_study=kid.year_of_study, group_letter=kid.group_letter)
    subject_lessons = lessons.filter(subject__title=subject)
    random_lesson = random.choice(subject_lessons)
    lesson_date = random_lesson.date
    lesson_subject = random_lesson.subject
    lesson_teacher = random_lesson.teacher
    commendations = models.Commendation.objects.filter(teacher=lesson_teacher, subject=lesson_subject, schoolkid=kid)
    commendations.create(text=commedation_text, created=lesson_date, schoolkid=kid, subject=lesson_subject, teacher=lesson_teacher)
    print(f'Похвала ученику добавлена...')
