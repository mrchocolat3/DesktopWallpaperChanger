import datetime

weekDay = datetime.datetime.now().strftime("%a")

dayType = {
    'Mon': {'type': 'hardDay', 'name': 'Hard day'},
    'Wed': {'type': 'demiHardDay', 'name': 'Demi Hard Day'},
    'Fri': {'type': 'normalDay', 'name': 'Normal Day'},
    'Sat': {'type': 'normalDay', 'name': 'Normal Day'},
    'Sun': {'type': 'funDay', 'name': 'Fun Day'},
    'Tue': {'type': 'funDay', 'name': 'Fun Day'},
    'Thu': {'type': 'funDay', 'name': 'Fun Day'}
}

Activities = {
    'funDay': {
        'st': '2h',
        'hw': '2h',
        'oa': '4h'
    },

    'hardDay': {
        'st': '5h',
        'hw': '4h',
        'oa': '0h'
    },

    'demiHardDay': {
        'st': '4h',
        'hw': '4h',
        'oa': '0h'
    },

    'normalDay': {
        'st': '5h',
        'hw': '5h',
        'oa': '0h'
    }
}

def get_weekDaySummary(weekDay):
    return dayType[weekDay]['name']

def get_weekDayType(weekDay):
    return dayType[weekDay]['type']

def get_weekDay():
    return weekDay

def get_Activity(weekDay):
    return Activities[get_weekDayType(weekDay)]
