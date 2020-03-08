from friend import Friend

class Person:

    def __init__(self, _id):
        self.id = _id
        self.nominations = dict()

    def add_nominations(self, _row):

        # Iterate through the nominations section of the row
        for i in range(1, 11):

            # Get the value
            val = _row[i]

            # Skip if None or 1
            if not val or val == 1:
                continue

            # Initialize the friend
            nom = Friend(val)

            # Check whether friend is in top3
            if _row[i + 10] == 1:
                nom.set_top3()

            self.nominations[nom.get_id()] = nom

        # Get the closest idx
        closest_idx = _row[-1]

        # Get the top3 nominations
        top3_friends = self.get_top3()

        if closest_idx and top3_friends:
            friend_ids = list(top3_friends.keys())
            closest_friend = friend_ids[closest_idx - 1]
            top3_friends[closest_friend].set_closest()

    def get_id(self):
        return self.id

    def get_nominations(self):
        return self.nominations

    def get_top3(self):

        # Get the top3
        top3 = dict()

        for f_id, f_obj in self.nominations.items():

            if f_obj.is_top3():
                top3[f_id] = f_obj

        return top3

    # Get the closest friend
    def get_closest(self):

        for f_id, f_obj in self.nominations.items():

            if f_obj.is_closest():
                return f_id

    def check_reciprocal_friend(self, _nom):

        nom = _nom  # type: Person

        # Check if nomination data available
        if not nom.get_nominations():
            return 9
        elif self.id in nom.get_nominations():
            return 1
        else:
            return 0

    def check_reciprocal_top3(self, _nom):

        nom = _nom  # type: Person

        # Check if nomination data available
        if not nom.get_nominations():
            return 9
        elif self.id in nom.get_top3():
            return 1
        else:
            return 0

    def check_reciprocal_closest(self, _nom):

        nom = _nom  # type: Person

        # Check if nomination data available
        if not nom.get_closest():
            return 9
        elif self.id == nom.get_closest():
            return 1
        else:
            return 0
