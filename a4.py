import sys

def is_atom(s):
    if not isinstance(s, str):
        return False
    if s == "":
        return False
    return is_letter(s[0]) and all(is_letter(c) or c.isdigit() for c in s[1:])

def is_letter(s):
    return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"

class KB:
    def __init__(self):
        self.clauses = {}
        self.atoms = {}
        self.inferred = {}

    def launch(self):
        while True:
            cmd = input("kb> ").split()
            try:
                if len(cmd) > 0:
                    if cmd[0] == "load":
                        if len(cmd) != 2:
                            print("Error: load command expects a file name")
                            continue
                        path = cmd[1]
                        _, clauses = self.load(path)
                        print("  {} definite clauses read in:".format(len(clauses)))
                        for clause in clauses:
                            print("    " + clause)
                              
                    elif cmd[0] == "tell":
                        if len(cmd) <= 1:
                            print("Error: tell command expects atoms")
                            continue
                        atoms = cmd[1:]
                        allValid = True
                        for atom in atoms:
                            if not is_atom(atom):
                                print("Error: \"{0}\" is not a valid atom".format(atom))
                                allValid = False
                                break
                        if allValid:
                            for atom in atoms:
                                if atom in self.atoms:
                                    print("Error: atom \"{0}\" already known to be true".format(atom))
                                else:
                                    self.tell(atom)
                                    print("   \"{0}\" added to KB".format(atom))
                    elif cmd[0] == "infer_all":
                        if len(cmd) != 1:
                            print("Error: infer_all expects no arguments")
                            continue
                        newly_inferred, already_inferred = self.infer_all()
                        print("   Newly inferred atoms:")
                        if newly_inferred == {}:
                            print("      <none>")
                        else:
                            print("      ", end='')
                            for atom in newly_inferred:
                                print(atom, end=' ')
                            print()
                        print("   Atoms already known to be true:")
                        if already_inferred == {}:
                            print("      <none>")
                        else:
                            print("      ", end='')
                            for atom in already_inferred:
                                print(atom, end=' ')
                print()
            except Exception as inst:
                print(inst)

    def load(self, path):
        """ Load clauses """
        file = open(path, 'r')
        clauses = [line.strip() for line in file.readlines()] # remove '\n' character
        new_clauses = {}
        for clause in clauses:
            head_atoms_split = clause.split('<--')
            if len(head_atoms_split) != 2:
                raise Exception("{0} is not a valid knowledge base".format(path))
            head = head_atoms_split[0].strip()
            nAmpersand = head_atoms_split[1].count(' & ')
            atoms = head_atoms_split[1].split(' & ')
            if nAmpersand + 1 != len(atoms):
                raise Exception("{0} is not a valid knowledge base".format(path))
            atoms = [atom.strip() for atom in atoms]
            for atom in atoms:
                if not is_atom(atom):
                    raise Exception("{0} is not a valid knowledge base".format(path))
            new_clauses[head] = atoms
        self.clauses = new_clauses
        return new_clauses, clauses
            
    def tell(self, atom):
        """ Tell an atom to be true """
        self.atoms[atom] = True
    

    def infer_all(self):
        """ Return newly inferred atoms  """
        already_inferred = dict(self.atoms)
        newly_inferred = {} # a set
        for _ in range(2): # need to loop through 2 times to handle the case when the a previous clause can't be inferred until the a later clause is inferred
            for head in self.clauses:
                if head not in self.atoms and head not in newly_inferred:
                    if all([atom in self.atoms for atom in self.clauses[head]]):
                        newly_inferred[head] = True
                        self.atoms[head] = True
        return newly_inferred, already_inferred
    
                    
                    
                    
            

if __name__ == '__main__':
    kb = KB()
    kb.launch()
