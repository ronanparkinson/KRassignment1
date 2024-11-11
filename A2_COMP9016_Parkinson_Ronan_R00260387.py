import logic
from logic import PropKB, KB, FolKB, Expr

kb = FolKB()

kb.tell(Expr('forall x (IsParent(x) ==> IsAncestor(x))')) 
kb.tell(Expr('forall x (AreSiblings(x, y) & ((IsChild(x, v) & IsChild(y, z)) | ((IsChild(x, z) & IsChild(y, v)) ==> AreCousins(v, z))'))

