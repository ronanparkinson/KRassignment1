from logic import PropKB, KB, FolKB, Expr, fol_fc_ask, fol_bc_ask, fol_bc_or, expr, unify_mm
import random

def questionOne():
    kb = FolKB()
    #rules
    kb.tell(expr('(Parent(x,y) & HasblueEyes(x)) ==> InheritsBlueEyes(y)'))
    kb.tell(expr("Parent(x, y) ==> Ancestor(x, y)"))
    kb.tell(expr("(Parent(x, y) & Ancestor(z, x)) ==> Ancestor(z, y)"))
    kb.tell(expr("(Parent(pa, cx) & Parent(pb, cy) & Sibling(pa, pb) & NotEqual(cx, cy)) ==> Cousin(cx, cy)"))

    #facts
    kb.tell(expr("Parent(Alice, Carol)"))
    kb.tell(expr("Parent(Bob, Carol)"))
    kb.tell(expr("Parent(Alice, Dave)"))
    kb.tell(expr("Parent(Bob, Dave)"))
    kb.tell(expr("Spouse(Eve, Dave)"))
    kb.tell(expr('Parent(Carol, Frank)'))   
    kb.tell(expr('HasblueEyes(Carol)'))

    def inheritsBE():
        doesInherit = random.random() < 0.5
        if doesInherit:
            kb.tell(expr('InheritsBlueEyes(y) ==> HasblueEyes(y)'))
            gotBlueEyes = fol_fc_ask(kb, expr('HasblueEyes(Frank)'))
            gotBlueEyesBC = fol_bc_ask(kb, expr('HasblueEyes(Frank)'))
            print("fc", list(gotBlueEyes))
            for checkInheritBC in gotBlueEyesBC:
                print("bc", checkInheritBC)
            ##could remove the rule from the kb here to prevent it from happening afterwards unnecessarily

    ##Inference
    inheritsBE()

    haveBlueEyes = fol_fc_ask(kb, expr('HasblueEyes(Frank)')) #[{}] is the correct result as it means no subs were needed
    print('\nDoes Frank have blue eyes?', list(haveBlueEyes))
    #print("\nForward Chaining Query: hasblueEyes(Frank)")

    gotBlueEyes = fol_bc_ask(kb, expr('HasblueEyes(Frank)'))
    for Beyes in gotBlueEyes:
        print(Beyes)

    def print_clauses(kb, message="Clauses in the Knowledge Base:", bool_print=True):
        if bool_print:
          #  print("\n" + message)
            for clause in kb.clauses:
                print(clause)
        print("Total Clauses: ", len(kb.clauses))
    print_clauses(kb)

    # ancestorWithBE = fol_bc_ask(kb, expr('HasblueEyes(x)'))
    # for AncWithBeyes in ancestorWithBE:
    #     print("Franks ancestors with blue eyes:", AncWithBeyes)

    ancestorWithBE = fol_bc_ask(kb, expr('Ancestor(x, Frank)'))
    for Ancestor in ancestorWithBE:
       # print("One of Franks ancestors:", Ancestor)
        checkIfAncestorHasBE = fol_bc_ask(kb, expr('HasblueEyes(x)'))
        for AncWithBEs in checkIfAncestorHasBE:
            #print("Franks ancestors with Blue Eyes", AncWithBEs)
            if Ancestor == AncWithBEs:
                print("One of Franks ancestors with blue eyes is:", Ancestor)

    areCousins = fol_fc_ask(kb, expr("Cousin(Carol, Eve)"))
    print(("Are Carol and eve cousins?", list(areCousins)))

    # areCousinsBC = fol_bc_ask(kb, expr("Cousin(Carol, Eve)"))
    # for check in areCousinsBC:
    #     print(("Are Carol and eve cousins in BC?", check))

questionOne()

from probability import BayesNet, enumeration_ask


def questionTwo():
    env_tech_impact = BayesNet([
        ('TechInnovation', '', 0.8),  # Prior probability
        ('Urbanisation', '', 0.4),  # Prior probability
        ('JobMarket', 'TechInnovation', {
            (True,): 0.85,
            (False,): 0.3
        }),
        ('CleanEnergyAdoption', 'TechInnovation Urbanisation', {
            (True, True): 0.75,
            (True, False): 0.5,
            (False, True): 0.3,
            (False, False): 0.1
        }),
        ('CarbonEmissions', 'Urbanisation CleanEnergyAdoption', {
            (True, True): 0.4,
            (True, False): 0.55,
            (False, True): 0.7,
            (False, False): 0.95
        }),
        ('EcologicalFootprint', 'CarbonEmissions', {
            (True,): 0.6,
            (False,): 0.45
        }),
    ])

    # Query the network
    print("P(JobMarket | TechInnovation):")
    print(enumeration_ask('JobMarket', {'TechInnovation': True}, env_tech_impact).show_approx())

    print("\nP(CarbonEmissions | Urbanisation=True, CleanEnergyAdoption=False):")
    print(enumeration_ask('CarbonEmissions', {'Urbanisation': True, 'CleanEnergyAdoption': False},
                          env_tech_impact).show_approx())

    print("\nP(EcologicalFootprint | CarbonEmissions=True):")
    print(enumeration_ask('EcologicalFootprint', {'CarbonEmissions': True}, env_tech_impact).show_approx())

questionTwo()

































