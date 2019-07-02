import json

from sqlalchemy import func

from flashserver.database import test_session_factory
from flashserver.models import Language, VerbGroup, VerbData, PracticeQuestion, TenseGroup, Subject
from flashserver.models import User, PracticeList, VerbToList


session = test_session_factory()
language_cache = {}


def insert_basic_groups():
    items = ['simple', 'fundamental']
    for item in items:
        if session.query(VerbGroup).filter(VerbGroup.group_name == item).count() == 0:
            maxgroup = session.query(func.max(VerbGroup.ordering)).first()[0]
            if maxgroup is None:
                maxgroup = 0

            session.add(VerbGroup(group_name=item, ordering=maxgroup + 1))
            session.commit()


def insert_french_subjects():
    subjects = ['je', 'tu', 'vous', 'il,elle,on', 'nous', 'ils,elles']
    french_id = check_insert_lang('fr')
    for item in subjects:
        if session.query(Subject).filter(Subject.subject_name == item, Subject.language == french_id).count() == 0:
            new_subj = Subject(subject_name=item, language=french_id)
            session.add(new_subj)
    session.commit()


def insert_tense_ids():
    print('Adding new tenses.')
    tenses = [
        'présent',
        'imparfait',
        'passé simple',
        'futur simple',
        'passé composé',
        'plus-que-parfait',
        'passé antérieur',
        'futur antérieur',
        'subjonctif présent',
        'subjonctif imparfait',
        'subjonctif passé',
        'subjonctif plus-que-parfait',
        'conditionnel présent',
        'conditionnel passé',
        'impératif présent',
        'impératif passé']

    for index, item in enumerate(tenses):
        if session.query(TenseGroup).filter(TenseGroup.tense_name == item).count() == 0:
            new_tense = TenseGroup(tense_name=item, ordering=index)
            session.add(new_tense)
    session.commit()


def check_insert_verb(verb, group_id):
    lang_id = check_insert_lang(verb.get('lang'))
    existing_verb = session.query(VerbData.id).filter(
        VerbData.name == verb.get('name'),
        VerbData.language == lang_id).first()
    if existing_verb is None:
        new_verb = VerbData(group_id=group_id, name=verb.get('name'), language=lang_id)
        session.add(new_verb)
        session.commit()
        return new_verb.id
    else:
        return existing_verb.id


def get_tense_id(tense):
    res = session.query(TenseGroup.id).filter(TenseGroup.tense_name == tense).first()
    if res is not None:
        return res.id
    else:
        print('Error getting tense for {}'.format(tense))
    return None


def get_subject_id(subject):
    res = session.query(Subject.id).filter(Subject.subject_name == subject).first()
    if res is not None:
        return res.id
    else:
        print('Error getting subject for {}'.format(subject))
    return None


def check_insert_lang(lang):
    if lang in language_cache:
        return language_cache.get(lang)

    lang_id = session.query(Language.id).filter(Language.language == lang).first()

    if lang_id is None:
        new_lang = Language(language=lang)
        session.add(new_lang)
        session.commit()
        language_cache[lang] = new_lang.id
        return new_lang.id
    else:
        language_cache[lang] = lang_id
        return lang_id


def check_insert_group(group_name):
    group_id = session.query(VerbGroup.id).filter(VerbGroup.group_name == group_name).first()
    if group_id is None:
        print('No group_id for {}'.format(group_name))
        return None
    else:
        return group_id


def insert(item):
    existing_question = session.query(PracticeQuestion.id).filter(
        PracticeQuestion.question_text == item['question'],
        PracticeQuestion.answer_text == item['answer']).count()
    if existing_question > 0:
        print('Not entering {} -> {} since it already exists.'.format(item['question'], item['answer']))
        return None
    group_id = check_insert_group(item['group_name'])
    verb_id = check_insert_verb(item['verb'], group_id)
    tense_id = get_tense_id(item['tense'])
    qlang_id = check_insert_lang(item['qlang'])
    alang_id = check_insert_lang(item['alang'])
    subject_id = get_subject_id(item['subject'])
    question_data = {
        'verb_id': verb_id,
        'tense_id': tense_id,
        'question_text': item['question'],
        'answer_text': item['answer'],
        'qlang': qlang_id,
        'alang': alang_id,
        'subject_id': subject_id
    }
    new_q = PracticeQuestion(**question_data)
    session.add(new_q)
    print('Added new question {} -> {}'.format(item['question'], item['answer']))
    session.commit()


def empty_tables():
    print('emptying tables')
    delete_order = [
        PracticeQuestion,
        Subject,
        TenseGroup,
        VerbData,
        VerbGroup]

    for item in delete_order:
        session.query(item).delete()


def simple_practice_list():
    """Users are linked to a practice list which consists of some groups of verbs + their tenses"""
    print('adding practice user, list, practicelist')
    basic_user = session.query(User).filter(User.username == "tester").first()
    if basic_user is None:
        basic_user = User(password_hash='555', username='tester')
        session.add(basic_user)
    first_plist = session.query(PracticeList).filter(
        PracticeList.list_name == "testing list",
        PracticeList.user_id == basic_user.id).first()
    if first_plist is None:
        first_plist = PracticeList(list_name="testing list", user_id=basic_user.id)
        session.add(first_plist)
    available_tenses = session.query(TenseGroup.id).all()
    group_id = check_insert_group('fundamental')
    for tense_id in available_tenses:
        session.add(VerbToList(practice_list_id=first_plist.id, group_id=group_id, tense_id=tense_id))
    session.commit()


def load_data():
    data = []
    with open('./flashserver/data_loader/questions.json', 'r') as infile:
        data = json.load(infile)

    if len(data) == 0:
        print('No Data to load')
    return data


empty_tables()

insert_basic_groups()
insert_french_subjects()
insert_tense_ids()
for item in load_data():
    insert(item)

simple_practice_list()
