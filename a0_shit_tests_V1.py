logo = '''
   _____                          _    _       _
  / ____|                        | |  | |     (_)
 | (___   __ ___   ____   ___   _| |  | |_ __  _
  \\___ \\ / _` \\ \\ / /\\ \\ / / | | | |  | | '_ \\| |
  ____) | (_| |\\ V /  \\ V /| |_| | |__| | | | | |
 |_____/ \\__,_| \\_/    \\_/  \\__, |\\____/|_| |_|_|
                             __/ |
                            |___/
'''

disclaimer = u'''
\u0053\u0061\u0076\u0076\u0079\u0055\u006e\u0069\u0020\u0058\u0020\u4e00\u52fe\u0043\u0053\u5927\u8bfe\u5802\u5b66\u751f\u4f7f\u7528\u000d\u000a\u5206\u4eab\u5bb6\u7834\u4eba\u4ea1\u000d\u000a\u672a\u7ecf\u6388\u6743\u4f7f\u7528\u5bb6\u7834\u4eba\u4ea1\u000d\u000a\u003a\u0020\u0029
'''

instruction = u'''
\u0031\u002e\u0020\u6211\u7684\u0074\u0065\u0073\u0074\u0073\u6db5\u76d6\u4e86\u6700\u57fa\u672c\u7684\u9898\u76ee\u8981\u6c42\uff0c\u6bd4\u5b66\u6821\u8001\u5e08\u7ed9\u7684\u0074\u0065\u0073\u0074\u0073\u60c5\u51b5\u591a\u4e00\u4e9b\uff0c\u4f46\u662f\u5e76\u4e0d\u4ee3\u8868\u8fc7\u4e86\u6211\u7684\u0074\u0065\u0073\u0074\u0073\u4f60\u5c31\u53ef\u4ee5\u62ff\u5230\u6ee1\u5206\u000d\u000a\u0032\u002e\u0020\u8bf7\u4f60\u5b66\u6211\u7684\u0074\u0065\u0073\u0074\u0073\uff0c\u518d\u81ea\u5df1\u6dfb\u52a0\u66f4\u591a\u66f4\u590d\u6742\u7684\u60c5\u51b5\u000d\u000a\u0033\u002e\u0020\u4e0a\u8bfe\u6211\u4f1a\u6559\u4f60\u5982\u4f55\u5229\u7528\u8fd9\u4e2a\u6587\u4ef6\u6765\u0064\u0065\u0062\u0075\u0067
'''

from datetime import datetime
from gym import WorkoutClass, Instructor, Gym


def test_instructor_basic() -> None:
    """Test the public attributes of a new instructor."""
    instructor = Instructor(217, 'Eagle')
    instructor2 = Instructor(218, 'Shuai')
    assert instructor.get_id() == 217
    assert instructor.name == 'Eagle'
    assert instructor.get_num_certificates() == 0

    # test add certificate
    # NOTE: if certificate already exist, should return False and change nothing
    assert instructor.add_certificate("FUCK") == True
    assert instructor.get_num_certificates() == 1
    assert instructor.add_certificate("FUCK") == False
    assert instructor.get_num_certificates() == 1
    assert instructor.add_certificate("SHIT") == True
    assert instructor.get_num_certificates() == 2
    assert instructor.add_certificate("ASS") == True
    assert instructor.get_num_certificates() == 3
    assert instructor.add_certificate("FUCK") == False
    assert instructor.get_num_certificates() == 3

    assert instructor2.get_id() == 218
    assert instructor2.name == 'Shuai'
    assert instructor2.get_num_certificates() == 0


def test_instructor_can_teach() -> None:
    '''
    Test can teach of an instructor
    '''
    instructor = Instructor(217, 'Eagle')
    instructor.add_certificate('')
    w1 = WorkoutClass('Shit', [])
    assert instructor.can_teach(w1)

    w2 = WorkoutClass('Fuck', ['FUCK'])
    assert instructor.can_teach(w2) == False

    instructor.add_certificate('FUCK')
    assert instructor.can_teach(w2)
    assert instructor.can_teach(w1)

    w3 = WorkoutClass('Ass', ['SHIT', 'FUCK', 'ASS'])
    assert  instructor.can_teach(w3) == False
    instructor.add_certificate('ASS')
    assert  instructor.can_teach(w3) == False
    instructor.add_certificate('SHIT')
    assert  instructor.can_teach(w3)
    assert instructor.can_teach(w1)

def prepare_gym() -> Gym:
    g = Gym('SavvyUni')
    g.add_instructor(Instructor(1, 'Fuck1'))
    g.add_instructor(Instructor(2, 'Fuck2'))
    g.add_instructor(Instructor(3, 'Fuck3'))
    g.add_instructor(Instructor(4, 'Fuck4'))

    g.add_workout_class(WorkoutClass('Shit1', ['ShitA', 'ShitB']))
    g.add_workout_class(WorkoutClass('Shit2', ['ShitB', 'ShitC']))
    g.add_workout_class(WorkoutClass('Shit3', ['ShitC', 'ShitD']))

    g.add_room("Ass1", 2)
    g.add_room("Ass2", 20)
    g.add_room("Ass3", 40)
    return g


def test_gym_basic() -> None:
    """Test make sure all basic feature of gym works"""
    g = prepare_gym()

    assert g.add_instructor(Instructor(5, 'Fuck5'))
    assert g.add_instructor(Instructor(5, 'Fuck5')) == False
    assert g.add_instructor(Instructor(2, 'Fuck2')) == False

    assert g.add_workout_class(WorkoutClass('Shit4', []))
    assert g.add_workout_class(WorkoutClass('Shit1', [])) == False

    assert g.add_room('Ass1', 10) == False
    assert g.add_room('Ass4', 10)


def test_gym_schedule() -> None:
    '''
    Test schedule
    '''
    g = prepare_gym()

    # simple case
    t = datetime(2020, 1, 1)

    # should fail due to instructor1 does not have certificate
    assert g.schedule_workout_class(t, 'Ass1', 'Shit1', 1) == False

    # give that guy all the certificates
    g._instructors[1]._certificates = ['ShitA', 'ShitB', 'ShitC', 'ShitD']

    # now it should work
    assert g.schedule_workout_class(t, 'Ass1', 'Shit1', 1) == True

    # now one workout should be scheduled at time t
    assert t in g._schedule

    # now that time should have one workout scheduled
    assert 'Ass1' in g._schedule[t]
    assert len(g._schedule[t]) == 1
    assert g._schedule[t]['Ass1'][0]._id == 1
    assert g._schedule[t]['Ass1'][1]._name == 'Shit1'
    assert g._schedule[t]['Ass1'][2] == []

    # now we should not be able to schedule another workout at the same time with the same instructor
    assert g.schedule_workout_class(t, 'Ass1', 'Shit1', 1) == False
    assert g.schedule_workout_class(t, 'Ass2', 'Shit1', 1) == False

    # now we should not be able to schedule another workout at the same time with same location
    g._instructors[2]._certificates = ['ShitA', 'ShitB', 'ShitC', 'ShitD']
    assert g.schedule_workout_class(t, 'Ass1', 'Shit1', 2) == False

    # we should be able to add another workout at different time with same location with same instructor
    t2 = datetime(2020, 1, 2)
    assert g.schedule_workout_class(t2, 'Ass1', 'Shit1', 1)

    # we should be able to add another workout at same time with different location with different instructor
    assert g.schedule_workout_class(t, 'Ass2', 'Shit2', 2)

    # now we should have 3 workout scheduled in total
    assert 'Ass1' in g._schedule[t]
    assert 'Ass2' in g._schedule[t]
    assert 'Ass1' in g._schedule[t2]
    assert len(g._schedule) == 2
    assert len(g._schedule[t]) == 2
    assert len(g._schedule[t2]) == 1

    # Please add more tests yourself to test your code fully

def test_register():
    g = prepare_gym()
    t = datetime(2020, 1, 1)
    t2 = datetime(2020, 1, 2)
    g._instructors[1]._certificates = ['ShitA', 'ShitB', 'ShitC', 'ShitD']
    g._instructors[2]._certificates = ['ShitA', 'ShitB', 'ShitC', 'ShitD']
    g.schedule_workout_class(t, 'Ass1', 'Shit1', 1)
    g.schedule_workout_class(t2, 'Ass1', 'Shit1', 1)
    g.schedule_workout_class(t, 'Ass2', 'Shit2', 2)

    # Ass1 has capacity of 2, currently empty room
    assert g.register(t, "Name1", "Shit1")
    assert g._schedule[t]['Ass1'][2] == ['Name1']
    # Cannot register the same guy again
    assert g.register(t, "Name1", "Shit1") == False
    assert g._schedule[t]['Ass1'][2] == ['Name1']
    # But can register this guy at diff time though
    assert g.register(t2, "Name1", "Shit1")
    assert g._schedule[t]['Ass1'][2] == ['Name1']
    assert g._schedule[t2]['Ass1'][2] == ['Name1']

    # register another guy
    assert g.register(t, "Name2", "Shit1")
    assert len(g._schedule[t]['Ass1'][2]) == 2

    # now you can't register for this time and this room anymore
    assert g.register(t, "Name3", "Shit1") == False

    # Add more yourself

def test_offerings_at():
    g = prepare_gym()
    t = datetime(2020, 1, 1)
    t2 = datetime(2020, 1, 2)
    g._instructors[1]._certificates = ['ShitA', 'ShitB', 'ShitC', 'ShitD']
    g._instructors[2]._certificates = ['ShitA', 'ShitB', 'ShitC', 'ShitD']
    g.schedule_workout_class(t, 'Ass1', 'Shit1', 1)
    g.schedule_workout_class(t2, 'Ass1', 'Shit1', 1)
    g.schedule_workout_class(t, 'Ass2', 'Shit2', 2)

    r1 = g.offerings_at(t)
    r2 = g.offerings_at(t2)

    # two scheduled at t, 1 scheduled at t2
    assert ('Fuck1', 'Shit1', 'Ass1') in r1
    assert ('Fuck2', 'Shit2', 'Ass2') in r1
    assert r2 == [('Fuck1', 'Shit1', 'Ass1')]

    # Add more yourself

def test_instructor_hours():
    g = prepare_gym()
    t = datetime(2020, 1, 1)
    t2 = datetime(2020, 1, 2)
    g._instructors[1]._certificates = ['ShitA', 'ShitB', 'ShitC', 'ShitD']
    g._instructors[2]._certificates = ['ShitA', 'ShitB', 'ShitC', 'ShitD']
    g.schedule_workout_class(t, 'Ass1', 'Shit1', 1)
    g.schedule_workout_class(t2, 'Ass1', 'Shit1', 1)
    g.schedule_workout_class(t, 'Ass2', 'Shit2', 2)

    r = g.instructor_hours(datetime(2019, 12, 31), datetime(2020, 12, 31))
    assert r == {1: 2, 2: 1, 3: 0, 4: 0}
    r = g.instructor_hours(datetime(2020, 1, 1), datetime(2020, 1, 1))
    assert r == {1: 1, 2: 1, 3: 0, 4: 0}

    # Add more yourself

def test_payroll():
    g = prepare_gym()
    t = datetime(2020, 1, 1)
    t2 = datetime(2020, 1, 2)
    g._instructors[1]._certificates = ['ShitA', 'ShitB', 'ShitC', 'ShitD']
    g._instructors[2]._certificates = ['ShitA', 'ShitB', 'ShitC', 'ShitD']
    g.schedule_workout_class(t, 'Ass1', 'Shit1', 1)
    g.schedule_workout_class(t2, 'Ass1', 'Shit1', 1)
    g.schedule_workout_class(t, 'Ass2', 'Shit2', 2)

    r = g.payroll(datetime(2019, 12, 31), datetime(2020, 12, 31), 10)
    assert r == [(1, 'Fuck1', 2, 32.0), (2, 'Fuck2', 1, 16.0), (3, 'Fuck3', 0, 0.0), (4, 'Fuck4', 0, 0.0)]
    r = g.payroll(datetime(2020, 1, 1), datetime(2020, 1, 1), 10)
    assert r == [(1, 'Fuck1', 1, 16.0), (2, 'Fuck2', 1, 16.0), (3, 'Fuck3', 0, 0.0), (4, 'Fuck4', 0, 0.0)]

    # Add more yourself

if __name__ == '__main__':
    print(logo)
    print(disclaimer)
    print(instruction)
    import pytest
    pytest.main(['a0_shit_tests_V1.py'])
