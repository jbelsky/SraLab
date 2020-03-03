class Person:
    
    def __init__(self, _id):
        self.id = _id
        self.nominations = None
        self.top3 = None
        self.closest = None
        self.nom_list = None
        self.top3_list = None

    def add_nom_list(self, _row):
        self.nom_list = _row

    def check_nom_list_reciprocated(self, _person_dict):

        self.nom_list_recip = []

        for i, v in enumerate(self.nom_list):

            if v in _person_dict:
                friend = _person_dict[v]
                if not friend.nominations:
                    recip = 9
                elif v in friend.nominations:
                    recip = 1
                else:
                    recip = 0
            else:
                if v and v != 1:
                    recip = 9
                else:
                    recip = ""

            self.nom_list_recip.append(recip)

    def write_nom_row(self):

        out = []
        for i, nom in enumerate(self.nom_list):
            if not nom:
                nom = ""
            out.append(nom)
            out.append(self.nom_list_recip[i])

        return "\t".join([str(x) for x in out])

    def check_top3_list_reciprocated(self, _person_dict):

        self.top3_list_recip = []

        for i, v in enumerate(self.top3_list):

            if v in _person_dict:
                friend = _person_dict[v]
                if not friend.top3:
                    recip = 9
                elif v in friend.top3:
                    recip = 1
                else:
                    recip = 0
            else:
                if v and v != 1:
                    recip = 9
                else:
                    recip = ""
            self.top3_list_recip.append(recip)

    def write_top3_row(self):

        out = []
        for i, nom in enumerate(self.top3_list):
            if not nom:
                nom = ""
            out.append(nom)
            out.append(self.top3_list_recip[i])

        return "\t".join([str(x) for x in out])

    def check_closest_reciprocated(self, _person_dict):

        if self.closest in _person_dict:
            friend = _person_dict[self.closest]
            if not friend.closest:
                recip = 9
            elif self.closest == friend.closest:
                recip = 1
            else:
                recip = 0
        else:
            recip = 9

        self.closest_recip = recip

    def write_closest(self):
        closest = self.closest
        if not closest:
            closest = ""

        return str(closest) + "\t" + str(self.closest_recip)


    def add_top3_list(self, _row):
        self.top3_list = _row

    def add_nomination(self, arg_id):
        if not self.nominations:
            self.nominations = set()
        self.nominations.add(arg_id)

    def add_top3(self, arg_id):

        if not self.top3:
            self.top3 = []
        self.top3.append(arg_id)

    def add_closest(self, arg_id):

        self.closest = arg_id

    def check_if_nominated(self, arg_id):
        if arg_id in self.nominations:
            return True
        else:
            return False
    
    def set_top_three(self, arg_id_arr):
        if len(arg_id_arr) == 0:
            self.top3 = None
        else:
            self.top3 = set(arg_id_arr)
    
    def set_top(self, arg_id):
        self.top = arg_id

    def get_nominations(self):
        return self.nominations
    
    def get_top3(self):
        return self.top3
    
    def get_top(self):
        return self.top
    
    def is_id_in_nom(self, arg_id):
        if self.nominations and arg_id in self.nominations:
            return True
        else:
            return False

    def is_id_in_top3(self, arg_id):
        if self.top3 and arg_id in self.top3:
            return True
        else:
            return False
