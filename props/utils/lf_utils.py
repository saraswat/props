"""
  Collection of routines to simplify logic forms, primarily by removing default
  structure, moving to a variable free (de Bruijn) representation, etc.
"""
import copy
from pprint import pprint
def simplify_single_dict(lf, feat):
    "Replace {feat:v} by v everywhere in lf."
    if isinstance(lf, dict):
        if len(lf)==1 and feat in lf:
            return simplify_single_dict(lf[feat], feat)
        return dict([(k, simplify_single_dict(lf[k],feat)) for k in lf.keys()])
    if isinstance(lf, list):
        return [simplify_single_dict(v,feat) for v in lf]
    return lf
def update_fields(lf, f1, f2):
    "Replace f1:text by f1:text1 where text1 is value of f2 field, if on stripping it is the same as text."
    if isinstance(lf, dict):
        if f1 in lf and f2 in lf and lf[f1]==lf[f2].strip():
            lf[f1]=lf[f2]
            del lf[f2]
        return dict([(k, update_fields(lf[k], f1, f2)) for k in lf.keys()])
    if isinstance(lf, list):
        return [update_fields(v,f1,f2) for v in lf]
    return lf

def remove_empty_dict(lf):
    """
    Remove f:{} for any attribute f, anywhere in lf. Repeat until quiescence.

    Transitively, apply all rules that get enabled by removing an empty dic, such as
    simplify_single_dict.

    """
    while True:
        lf2 = remove_empty_dict__(lf)
        lf3 = simplify_single_dict(lf2, 'word')
        if lf3 == lf:
            return lf
        lf = lf3
        
def remove_empty_dict__(lf):
    if isinstance(lf, dict):
        return dict([(k, remove_empty_dict__(lf[k]))
                     for k in lf.keys()
                     if lf[k] != {}])
    if isinstance(lf, list):
        return [remove_empty_dict__(v) for v in lf]
    return lf

# No need to remove empty lists as values?

def simplify_single_list(lf):
    "Replace f:[{...}] with f:{...}."
    if isinstance(lf, dict):
        return dict([(k, simplify_single_list(lf[k])) for k in lf.keys()])
    if isinstance(lf, list):
        if len(lf)==1 and isinstance(lf[0], dict):
            return simplify_single_list(lf[0])
        return [simplify_single_list(e) for e in lf]
    return lf

#def remove_feats(lf, feats):
#    "Remove all occurrences of feat:v in lf, for feat in feats."
#    if isinstance(lf, dict):
#        return dict([(k, remove_feats(lf[k],feats))
#                     for k in lf.keys()
#                     if not k in feats])
#    if isinstance(lf, list):
#        return [remove_feats(v,feats) for v in lf]
#    return lf

def remove_paths(lf, paths):
    "Remove all occurrences of path, for path in paths."
    for path in paths:
        lf = remove_path(lf, path)
    return lf

def remove_path(lf, path):
    "Remove all instances of path, a list of attributes or indices, in lf."
    lf = remove_path__(lf, path, path)
    lf = remove_empty_dict(lf)
    return lf

def remove_path__(lf, path, origpath, started=False):
    "A path is a sequence of keys."
    assert len(path) > 0, "Path must be non-empty"
    assert len(origpath) > 0, "OrigPath must be non-empty"
    if isinstance(lf, dict):
        return dict([(k, remove_path__(lf[k], path[1:], origpath, True)
                      if started and k == path[0]
                      else remove_path__(lf[k], origpath[1:], origpath, True)
                      if k == origpath[0] 
                      else remove_path__(lf[k], origpath, origpath))
                     for k in lf.keys()
                     if not((started and k == path[0] and len(path) == 1)
                            or ((not started) and k==origpath[0] and len(origpath)==1))])
    if isinstance(lf, list):
        return [remove_path__(lf[k], path[1:], origpath, True)
                if started and k == path[0]
                else remove_path__(lf[k], origpath[1:], origpath, True)
                if k == origpath[0] 
                else remove_path__(lf[k], origpath, origpath)
                for k, v in enumerate(lf)
                if not((started and k == path[0] and len(path) == 1)
                       or ((not started) and k==origpath[0] and len(origpath)==1))]
    return lf    

def get_target_addresses(lf, addresses=[], prefix=[]):
    """
     Return (address, path to address) pairs. There may be multiple
     such entries for the same address, but they will each have the
     same path, that is ok.
    """
    if isinstance(lf, dict):
        for k in lf.keys():
            subtree = lf[k]
            p = copy.copy(prefix)
            p.append(k)
            if isinstance(subtree, dict) and 'xtarget' in subtree:
                addresses.append((subtree['xtarget'], p))
            addresses = get_target_addresses(subtree, addresses, p)
        return addresses
    if isinstance(lf, list):
        for k,subtree in enumerate(lf):
            p = copy.copy(prefix)
            p.append(k)
            if isinstance(subtree, dict) and 'xtarget' in subtree:
                addresses.append((subtree['xtarget'], p))
            addresses = get_target_addresses(subtree, addresses, p)
    return addresses

def replace_refs_with_addresses(lf, addresses):
    if isinstance(lf, dict):
        return dict([(k, addresses[lf[k]] if k=='xref' 
                      else replace_refs_with_addresses(lf[k],addresses))
                      for k in lf.keys()])
    if isinstance(lf, list):
        return [replace_refs_with_addresses(e, addresses) for e in lf]
    return lf


def to_de_bruijn(lf):
    """
     Convert lf to a variant of the de Bruijn notation, basically replacing 
     'xref': id with the path from the root to 'xtarget':id.
     An advantage of this notation is that it does not need variable names.
     (A disadvantage is that changign the structure of the formula can change
      its meaning in unexpected ways.)
     Assumption: For any given id for which there is an 'xref':id subterm,
     there is a unique subterm of lf which is a dictionary with an 'xtarget'
     key with value id.
    """
    lf=simplify_single_list(lf)
    targets = get_target_addresses(lf)
    targets = dict(targets)
    lf = replace_refs_with_addresses(lf, targets)
    lf = remove_path(lf, ['xtarget'])
    lf = simplify_single_dict(lf, 'word')
    return lf


def lf_clean(lf):
    "Clean up the logical form, removing clutter."
    lf=remove_paths(lf, [['index'],
                         ['node'],
                         ['propositions'], 
                         ['feats','definite'],
                         ['feats','implicit'],
                         ['feats','passive'],
                         ['feats','tense'],
                         ['feats','pos']])
    lf=update_fields(lf, 'word', 'text')
    lf=simplify_single_dict(lf, 'word')
    lf=remove_empty_dict(lf)
    return lf

