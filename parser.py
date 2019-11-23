
# In[1]:


from collections import Counter

debug = False


# In[2]:


def mul_dict(dictionnary, n):
    return { k : v * n for k, v in dictionnary.items() }


# In[3]:


def detect_mol(strmol, index):
    
    if index > len(strmol):
        return (index, "")
    
    mol = strmol[index]
    if not mol.isupper():
        return (index, "")
    
    i = index + 1
    while i < len(strmol) and strmol[i].islower():
        mol += strmol[i]
        i += 1
        
    return (i, mol)


def detect_number(strmol, index):
    
    if index >= len(strmol):
        return (index, "")
    
    if not strmol[index].isdigit():
        return (index, "")
    
    i, c = detect_number(strmol, index+1)
    return (i, strmol[index] + c)


def detect_mol_and_count(strmol, index):
    i1, mol = detect_mol(strmol, index)
    if mol != "":
        i2, number = detect_number(strmol, i1)
        if number != "":
            return (i2, mol, int(number))
        else:
            return (i1, mol, 1)
    return (None, None, None)


# In[4]:



def parse_molecule(strmol):
    strlen = len(strmol)
    opening_brackets = ["(", "[", "{"]
    closing_brackets = [")", "]", "}"]
    
    def aux(index):
        if debug:
            print("Aux begin")
        
        # On initaliste le compteur de molécule 
        mol_dict = Counter({})
        i = index
        
        while True:
            
            if i >= strlen:
                if debug:
                    print("Finished")
                return (i, mol_dict)
            
            c = strmol[i]
            
            if c in opening_brackets:
                if debug:
                    print("Opening bracket detected at index "+str(i))
                i, mdict = aux(i+1) # On calcule récursivement le nombre de molécule dans la parenthèse
                i, n = detect_number(strmol, i) # On regarde par combien multiplier le compteur précédent
                if n != "":
                    mdict = mul_dict(mdict, int(n))
                mol_dict += mdict # On ajoute le compteur des molécules entre parenthèses au compteur actuel
                
            elif c in closing_brackets:
                if debug:
                    print("Closing bracket, aux returns " + str(i+1))
                return (i+1, mol_dict) # On s'arrete et on retourne le compteur
            else:
                newi, mol, count = detect_mol_and_count(strmol, i)
                if newi != None:
                    i = newi
                    if debug:
                        print("Found "+str(count) + " "+str(mol))
                    mol_dict[mol] += count
                else:
                    i += 1
                    
    return dict(aux(0)[1])
                
    


# In[5]:


print(parse_molecule("H2O"))
print(parse_molecule("Mg(OH)2"))
print(parse_molecule("K4[ON(SO3)2]2"))
print(parse_molecule("C33H36N4O6"))
print(parse_molecule("C(Fe7{H20}SF2[U2He5]2)"))

