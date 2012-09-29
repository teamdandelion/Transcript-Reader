#!/usr/bin/env ipython

groups2dept = {'Computer Science': {'CMSC'}, \
     'Philosophy': {'PHIL'}, \
     'Math & Statistics': {'MATH', 'STAT'},\
     'Economics & Business': {'ECON', 'BUSF'},\
     'Humanities': {'HUMA', 'SOSC', 'HIST', 'PSLC', 'SPAN', 'RLST'},\
     'Science': {'GEOS', 'BIOS'},\
     'Other': {}}

groupnames = list(groups2dept.iterkeys())



def invert_map2set(dictmap):
    newmap = {}
    for key, sett in dictmap.iteritems():
        for value in sett:
            newmap[value] = key
    return newmap

dept2group = invert_map2set(groups2dept)

class TranscriptReader:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.lines = f.readlines()
        self.classes = []
        self.quarter = ''
        self.year    = 0
        self.qytuples = []
        self.qy2gpa = {}
        self.group2gpa = {}

        map(self.read_transcript,self.lines) # will this do it in the right order?

        self.build_data()

        self.print_output()

    def read_transcript(self,line):
        line = line.split()
        if len(line) == 0:
            return
        if line[0] in ('Autumn', 'Winter', 'Spring'):
            self.qy = (line[0], int(line[1]))
            self.qytuples.append(self.qy)
        elif len(line[0]) == 4: # e.g. BIOS, CMSC

            # Course name may have spaces - so get the index of the list item corresponding to the 'Units' of the course
            for i in xrange(len(line)):
                if line[i] in ('100', '0'):
                    unit_idx = i

            if line[unit_idx] == '0':
                return  # Let's not bother with 0-unit classes,
                # i.e. writing seminars and the such

            dept = line[0]
            c_num = int(line[1])
            c_name = ' '.join(line[2:unit_idx])
            letter_grade = line[unit_idx+1]
            grade = letter2gpa(letter_grade)

            c_tuple = (self.qy, dept, c_num, c_name, grade)
            self.classes.append(c_tuple)

    def build_data(self):
        # Generate summary statistics, e.g. GPA by quarter, # classes by quarter, GPA by grouping, # classes by grouping
        self.qy2gpa = {}
        # maps from (Quarter, Year) -> [Avg GPA, # classes]
        # total rather than avg gpa until division at end of function
        self.group2gpa = {}
        # same but for (GroupingName) rather than (Quarter, Year)

        for (qy, dept, num, name, grade) in self.classes:
            try:
                self.qy2gpa[qy][0] += grade
                self.qy2gpa[qy][1] += 1
            except KeyError:
                self.qy2gpa[qy] = [grade, 1]

            try:
                group = dept2group[dept]
            except KeyError:
                group = 'Other'

            try:
                self.group2gpa[group][0] += grade
                self.group2gpa[group][1] += 1
            except KeyError:
                self.group2gpa[group] = [grade, 1]

        for grade_n in self.qy2gpa.itervalues():
            grade_n[0] /= grade_n[1]
        for grade_n in self.group2gpa.itervalues():
            grade_n[0] /= grade_n[1]

        global groupnames
        for (q,y) in self.qytuples:
            (gpa, n) = self.qy2gpa[(q,y)]
            print "{:20} {}: {:.2f} {}".format(q, y, gpa, n)
        
        def group2n(group):
            return self.group2gpa[group][1]

        groupnames = sorted(groupnames, key=group2n, reverse=True)

        for group in groupnames:
            (gpa, n) = self.group2gpa[group]
            print "{}: {:.2f} {}".format(group, gpa, n)



    def print_output(self,outFile=""):
        #output = "\nQuarter, Year, Dept, Num, Class, Grade\n"
        #for course in self.classes:
        #    output += '{},{},{},{},"{}",{:.1f}\n'.format(*course)

        #print output
        global groupnames
        for (q,y) in self.qytuples:
            (gpa, n) = self.qy2gpa[(q,y)]
            print "{} {}: {:.2f} {}".format(q, y, gpa, n)
        
        def group2n(group):
            return self.group2gpa[group][1]

        groupnames = sorted(groupnames, key=group2n, reverse=True)

        for group in groupnames:
            (gpa, n) = self.group2gpa[group]
            print "{}: {:.2f} {}".format(group, gpa, n)






def letter2gpa(textgrade):
    letter_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}

    if len(textgrade)==1:
        mod = 0
    elif textgrade[1] == '+':
        mod = 1
    elif textgrade[1] == '-':
        mod = -1

    letter = textgrade[0]

    grade = letter_map[letter] + mod * .3
    return grade




def main():
    tr = TranscriptReader('transcript.txt')




if __name__ == '__main__':
    main()
