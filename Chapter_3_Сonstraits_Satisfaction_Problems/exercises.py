from typing import Dict, List

from Chapter_3_Сonstraits_Satisfaction_Problems.theory import WordSearchConstraint, GridLocation


# Number 1: Revise WordSearchConstraint so that overlapping letters are allowed

class WordSearchRevisedConstraint(WordSearchConstraint):
    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        all_locations = {}
        for word, locations in assignment.items():
            for index, location in enumerate(locations):
                if location in all_locations:
                    if all_locations[location] != word[index]:
                        return False
                else:
                    all_locations[location] = word[index]
        return True