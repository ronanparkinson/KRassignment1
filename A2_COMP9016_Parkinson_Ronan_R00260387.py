from logic import PropKB, KB, FolKB, Expr, fol_fc_ask, fol_bc_ask, fol_bc_or, expr, unify_mm
import random

def questionOne():
    kb = FolKB()
    #rules
    kb.tell(expr('(Parent(x,y) & HasblueEyes(x)) ==> InheritsBlueEyes(y)'))
    kb.tell(expr("Parent(x, y) ==> Ancestor(x, y)"))
    kb.tell(expr("(Parent(x, y) & Ancestor(z, x)) ==> Ancestor(z, y)"))
    kb.tell(expr("(Parent(pa, cx) & Parent(pb, cy) & Sibling(pa, pb) & NotEqual(cx != cy)) ==> Cousin(cx, cy)"))

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
            for checkInherit in gotBlueEyes:
                print(gotBlueEyes)
            ##could remove the rule from the kb here if prevent it from happening afterwards unnecessarily

    ##Inference
    inheritsBE()

    haveBlueEyes = fol_fc_ask(kb, expr('HasblueEyes(Frank)')) #[{}] is the correct result as it means no subs were needed
    print('\nDoes Frank have blue eyes?', list(haveBlueEyes))
    #print("\nForward Chaining Query: hasblueEyes(Frank)")

    infer_rash_alice = fol_bc_ask(kb, expr('HasblueEyes(Frank)'))
    for rash in infer_rash_alice:
        print(rash)

    def print_clauses(kb, message="Clauses in the Knowledge Base:", bool_print=True):
        if bool_print:
          #  print("\n" + message)
            for clause in kb.clauses:
                print(clause)
        print("Total Clauses: ", len(kb.clauses))
    print_clauses(kb)

questionOne()