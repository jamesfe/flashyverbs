from bs4 import BeautifulSoup
import re
import json


with open('scraping/verbtranslations.json', 'r') as infile:
    vtrans = json.load(infile)


def get_datafile(verb):
    data = ''
    fname = 'scraping/data/{}'.format(verb)
    with open(fname, 'r') as infile:
        data = infile.read()

    soup = BeautifulSoup(data, 'html.parser')
    return soup


def get_raw_tense_data(verb, tense):
    tense_lookup = {
        'présent': 'pane-13',
        'passé simple': 'pane-7'
    }
    soup = get_datafile(verb)
    present = soup.find_all("div", class_=tense_lookup[tense])[0]
    pstring = str(present)
    pstring = pstring.replace("\n", "")
    return pstring


def verb_to_csv(french_verb, tense):
    pstring = get_raw_tense_data(french_verb, tense)
    pane_guts = re.findall(".*h2>(.*)</br>.*", pstring)
    if type(pane_guts) is list and len(pane_guts) > 0:
        pane_guts = pane_guts[0]
    else:
        print('issue parsing {}'.format(french_verb))
        return None
    verblist = [_.strip() for _ in pane_guts.split("<br>")][0:6]

    ret_val = {
        french_verb: {
            'tenses': {
                tense: {}
            },
            'translation': vtrans[french_verb]
        }
    }

    french_subj = ['je', 'tu', 'il,elle,on', 'nous', 'vous', 'ils,elles']

    for i, subj in enumerate(french_subj):
        ret_val[french_verb]['tenses'][tense][subj] = verblist[i]
    return ret_val
