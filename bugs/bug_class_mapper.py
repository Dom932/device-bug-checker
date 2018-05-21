from bugs.cisco import CSCvg76186
from bugs.test_bug import TestBug


class BugClassMapper:
    """
    Class to map a bug to a bug class
    """

    @staticmethod
    def get_bug_class(bug_id):
        """
        Static method to map get a bug class file

        :param bug_id: bug id to be checked
        :type bug_id: str

        :return: bug class

        :raises KeyError: If bug_id is not contained in class mapper
        """

        bug_class_mapper = {

            "TestBug": TestBug,
            "CSCvg76186": CSCvg76186

        }

        try:
            # get list of bugs
            return bug_class_mapper[bug_id]

        except KeyError:
            return None

