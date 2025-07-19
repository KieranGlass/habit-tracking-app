from models.completion import Completion

"""
    Tests for the Completion Model
    
    Tests written for all methods within the Completion Model
    
    Tests use a specific test database as these tests are only interested in
    testing the functionality of the methods.
"""

def test_get_all_completions(test_db):
    
    completions = Completion.get_all_completions(test_db)
    
    assert len(completions) == 28
    
def test_get_completions_by_habit(test_db):
    
    completion_one = Completion.get_completions_by_habit(test_db, 1)
    completion_four = Completion.get_completions_by_habit(test_db, 4)
    completion_six = Completion.get_completions_by_habit(test_db, 6)
    completion_thirteen = Completion.get_completions_by_habit(test_db, 13)
    
    assert len(completion_one) == 6
    assert len(completion_four) == 1
    assert len(completion_six) == 3
    assert len(completion_thirteen) == 2
    
    assert completion_one[0][1] == "02/05/2025"
    assert completion_one[2][1] == "06/07/2025"
    assert completion_one[5][1] == "09/07/2025"
    
def test_save_to_db(test_db):
    
    new_completion = Completion(29, 10, "01/06/2025")
    new_completion.save_to_db(test_db)
    
    completions = Completion.get_all_completions(test_db)
    
    assert len(completions) == 29
    
    check_completion = Completion.get_completions_by_habit(test_db, 10)
    
    assert len(check_completion) == 1
    assert check_completion[0][1] == "01/06/2025"