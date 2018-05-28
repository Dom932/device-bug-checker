from bugs.cisco import CSCvg76186
from bugs.test_bug import TestBug


class BugClassMapper:
    """
    Class to map a bug to a bug class
    """

    @staticmethod
    def get_bug_class(bug_list=None):
        """
        Returns bug class based on bug_id. If no bug_id is specified all Bug Classes will be returned

        :param bug_list: bug ids to be checked. If not specified all bugs class will be return
        :type bug_list: list
        :return: bug class
        :raises KeyError: If bug_id is not contained in class mapper
        """
        bug_class_mapper = {

            "testbug": TestBug,
            "cscvg76186": CSCvg76186

        }

        return_classes = []

        if bug_list:

            # if bug_ids is not a list, convert it to list
            if not isinstance(bug_list, list):
                bug_list = [bug_list]

            for b in bug_list:
                try:
                    return_classes.append(bug_class_mapper[b.lower()])

                except KeyError as e:
                    raise e

            return return_classes

        else:
            return list(bug_class_mapper.values())
